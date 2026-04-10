package hub

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/Jud1k/tic-tac-toe/internal/integration"
	"github.com/Jud1k/tic-tac-toe/internal/matchmaking"
	"github.com/Jud1k/tic-tac-toe/internal/storage"
	"github.com/redis/go-redis/v9"
)

type Hub struct {
	ClientsByUserId map[string]*client.Client
	Register        chan *client.Client
	Unregister      chan *client.Client
	Incoming        chan client.Message
	WaitingQueue    []*client.Client
	GameByUserId    map[string]*matchmaking.Game
	GamesById       map[string]*matchmaking.Game

	TicketRepository *storage.TicketRepository
	gameStoreClient  *integration.GameStoreClient
	gameRepository   *storage.GameRepository
}

func NewHub(gameStoreClient *integration.GameStoreClient, redisClient *redis.Client) *Hub {
	return &Hub{
		ClientsByUserId: make(map[string]*client.Client),
		Register:        make(chan *client.Client),
		Unregister:      make(chan *client.Client),
		Incoming:        make(chan client.Message),
		WaitingQueue:    []*client.Client{},
		GameByUserId:    make(map[string]*matchmaking.Game),
		GamesById:       make(map[string]*matchmaking.Game),

		gameStoreClient:  gameStoreClient,
		gameRepository:   storage.NewGameRepository(redisClient),
		TicketRepository: storage.NewTicketRepository(redisClient),
	}
}

func (h *Hub) FromDAO(dao dto.GameDAO) *matchmaking.Game {
	var players [2]*matchmaking.Player

	for i := 0; i < len(dao.Players) && i < 2; i++ {
		p := dao.Players[i]
		players[i] = &matchmaking.Player{
			Id:       p.Id,
			Side:     p.Side,
			Username: p.Username,
			ImageUrl: p.ImageUrl,
			Client:   h.ClientsByUserId[p.Id],
		}
	}
	game := &matchmaking.Game{
		Id:            dao.Id,
		Players:       players,
		Board:         dao.Board,
		Turn:          dao.Turn,
		Status:        dao.Status,
		Winner:        dao.Winner,
		StartGameTime: dao.StartTime,
		TurnEndTime:   dao.TurnEndTime,
	}
	return game
}

func (h *Hub) checkGameTimeouts() {
	now := time.Now()
	for _, game := range h.GamesById {
		if game.Status == "playing" && now.After(game.TurnEndTime) {
			h.handleTimeout(game)
			log.Println("Game timed out: ", game.Id)
		}
	}
}

func (h *Hub) handleTimeout(game *matchmaking.Game) {
	winner := game.OpponentOf(game.Turn)
	game.ApplyFinish(winner, nil)
}

func (h *Hub) handleMessage(message client.Message) {
	var base struct {
		Type string `json:"type"`
	}
	err := json.Unmarshal(message.Data, &base)
	if err != nil {
		log.Println("Error unmarshalling message: ", err)
		return
	}
	switch base.Type {
	case "joinQueue":
		uid := message.Client.UserId
		if game := h.GameByUserId[uid]; game != nil {
			game.UpdatePlayerClient(message.Client)
			game.BroadcastState()
			return
		}
		err := h.tryRestore(message.Client)
		if err != nil {
			h.addToWaitingQueue(message.Client)
			return
		}
	case "makeMove":
		uid := message.Client.UserId
		game := h.GameByUserId[uid]
		if game == nil {
			log.Println("No game found for client")
			return
		}

		var request dto.MakeMoveRequest
		if err := json.Unmarshal(message.Data, &request); err != nil {
			log.Println("Error unmarshalling message: ", err)
			return
		}
		game.HandleMove(uid, request.Payload.Index)
		gameDao := game.ToDAO()

		//TODO: Need to save game state in background, but without races when last turn
		ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
		defer cancel()
		if err := h.gameRepository.SaveGameState(ctx, gameDao); err != nil {
			log.Println("Error saving game state: ", err)
		}
		log.Println("Game status:", game.Status)
		game.BroadcastState()
	case "leaveQueue":
		h.removeFromWaitingQueue(message.Client)
		log.Printf("User %s left from waiting queue", message.Client.UserId)
	case "rematchRequest":
		game := h.GameByUserId[message.Client.UserId]
		if game == nil {
			log.Println("No game found for client")
			return
		}
		h.handleRematchRequest(game, message.Client)
	case "newGame":
		game := h.GameByUserId[message.Client.UserId]
		if game != nil {
			h.finishGame(game)
		}
		h.addToWaitingQueue(message.Client)
	default:
		log.Println("Unknown message type: ", base.Type)
	}
}

func (h *Hub) handleRematchRequest(game *matchmaking.Game, client *client.Client) {
	if game.Status != "finished" || game.RematchState[client.UserId] {
		return
	}
	game.RematchState[client.UserId] = true
	game.BroadcastRematchState()

	ready := game.CheckReadyRematch()
	if ready {
		h.finishGame(game)
		client1 := game.Players[0].Client
		client2 := game.Players[1].Client
		h.startNewGame(client1, client2)
	}
}

func (h *Hub) finishGame(game *matchmaking.Game) {
	log.Println("Game finished: ", game.Id)

	copyGame := *game

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()

	gameDao := copyGame.ToDAO()
	log.Printf("Deleting game %s from Redis", game.Id)
	if err := h.gameRepository.DeleteGame(ctx, gameDao); err != nil {
		log.Printf("Error deleting game from Redis: %v", err)
	}

	go func() {
		err := h.gameStoreClient.SaveGame(copyGame)
		if err != nil {
			log.Println("Error saving game state: ", err)
		}
	}()
	h.deleteGameFromHub(game)
}

func (h *Hub) deleteGameFromHub(game *matchmaking.Game) {
	for _, player := range game.Players {
		delete(h.GameByUserId, player.Id)
	}
	delete(h.GamesById, game.Id)
}

func (h *Hub) tryRestore(client *client.Client) error {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	gameId, err := h.gameRepository.GetGameByUserId(ctx, client.UserId)
	cancel()
	if err != nil || gameId == "" {
		return err
	}

	game := h.GamesById[gameId]
	if game == nil {
		ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
		defer cancel()
		gameDao, err := h.gameRepository.GetGameById(ctx, gameId)
		if err != nil {
			return err
		}
		game = h.FromDAO(*gameDao)
		h.GamesById[gameId] = game
		for _, player := range game.Players {
			h.GameByUserId[player.Id] = game
		}
	}

	game.UpdatePlayerClient(client)
	game.BroadcastState()
	return nil
}

func (h *Hub) Run() {
	ticker := time.NewTicker(time.Second * 1)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			h.checkGameTimeouts()
		case client := <-h.Register:
			if old := h.ClientsByUserId[client.UserId]; old != nil && old != client {
				if old.Conn != client.Conn {
					log.Printf("Replacing existing connection for user %s", client.UserId)
					h.removeFromWaitingQueue(old)
					if game := h.GameByUserId[old.UserId]; game != nil {
						game.Detach(old.UserId)
					}
					old.Conn.Close()
				}
			}
			h.ClientsByUserId[client.UserId] = client
		case client := <-h.Unregister:
			if current, ok := h.ClientsByUserId[client.UserId]; ok && current == client {
				delete(h.ClientsByUserId, client.UserId)
			}
			h.removeFromWaitingQueue(client)
			if game := h.GameByUserId[client.UserId]; game != nil && game.Status == "finished" {
				game.RematchState[client.UserId] = false
				game.BroadcastGameClosed("playerLeft", client.UserId)
				h.finishGame(game)
			}
			if game := h.GameByUserId[client.UserId]; game != nil {
				game.Detach(client.UserId)
			}
			close(client.Send)
		case msg := <-h.Incoming:
			log.Println(string(msg.Data))
			h.handleMessage(msg)
		}
	}
}

func (h *Hub) prepareMatchData(clients ...*client.Client) []matchmaking.PlayerMatchData {
	ids := make([]string, len(clients))
	for i, c := range clients {
		ids[i] = c.UserId
	}
	playersInfo, err := h.gameStoreClient.GetPlayers(ids)
	if err != nil {
		log.Printf("Error fetching player info: %v", err)
		return nil
	}

	infoMap := make(map[string]*dto.PlayerInfo)
	for _, info := range playersInfo {
		infoMap[info.UserId] = info
	}

	data := make([]matchmaking.PlayerMatchData, len(clients))
	for i, c := range clients {
		data[i] = matchmaking.PlayerMatchData{
			Client: c,
			Info:   infoMap[c.UserId],
		}
	}
	return data
}

func (h *Hub) startSearchingOpponent(client *client.Client) {
	msg := dto.SearchingOpponent{
		Type: "searchingOpponent",
	}
	client.SendJSON(msg)
}

func (h *Hub) addToWaitingQueue(client *client.Client) {
	if client.Conn == nil {
		return
	}
	if h.GameByUserId[client.UserId] != nil {
		return
	}
	for _, c := range h.WaitingQueue {
		if c.UserId == client.UserId {
			return
		}
	}
	h.WaitingQueue = append(h.WaitingQueue, client)
	log.Println(len(h.WaitingQueue))

	h.startSearchingOpponent(client)

	if len(h.WaitingQueue) >= 2 {
		client1, client2 := h.WaitingQueue[0], h.WaitingQueue[1]
		if client1.UserId == client2.UserId {
			h.WaitingQueue = h.WaitingQueue[1:]
			return
		}
		h.WaitingQueue = h.WaitingQueue[2:]
		h.startNewGame(client1, client2)
	}
}

func (h *Hub) startNewGame(client1, client2 *client.Client) {
	players := h.prepareMatchData(client1, client2)
	game := matchmaking.NewGame(players)
	log.Println("Game created: ", game.Id)

	h.GamesById[game.Id] = game
	for _, player := range game.Players {
		h.GameByUserId[player.Id] = game
	}

	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
		defer cancel()
		if err := h.gameRepository.SaveGameState(ctx, game.ToDAO()); err != nil {
			log.Println("Error saving initial game state: ", err)
		}
	}()

	game.BroadcastState()
}

func (h *Hub) removeFromWaitingQueue(client *client.Client) {
	for i, waitingClient := range h.WaitingQueue {
		if waitingClient == client {
			h.WaitingQueue = append(h.WaitingQueue[:i], h.WaitingQueue[i+1:]...)
			log.Printf("User %s left from waiting queue", client.UserId)
			return
		}
	}
}
