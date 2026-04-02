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

	gameStoreClient *integration.GameStoreClient
	gameRepository  *storage.GameRepository
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

		gameStoreClient: gameStoreClient,
		gameRepository:  storage.NewGameRepository(redisClient),
	}
}

func (h *Hub) FromDAO(dao dto.GameDAO) *matchmaking.Game {
	game := &matchmaking.Game{
		Id:              dao.Id,
		PlayerIds:       append([]string(nil), dao.PlayerIds...),
		SideByUserId:    dao.PlayerSide,
		ClientsByUserId: make(map[string]*client.Client),
		Board:           dao.Board,
		Turn:            dao.Turn,
		Status:          dao.Status,
		Winner:          dao.Winner,
		StartTime:       dao.StartTime,
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
	game.Status = "finished"
	winner := game.OpponentOf(game.Turn)
	game.Winner = winner
	game.BroadcastState()
	game.BroadcastGameOver(winner, nil)
	h.finishGame(game)
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
			game.SendStartInfo(message.Client)
			game.BroadcastState()
			return
		}
		h.addToWaitingQueue(message.Client)
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

		ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
		if err := h.gameRepository.SaveGameState(ctx, game.ToDAO()); err != nil {
			log.Println("Error saving game state: ", err)
		}
		cancel()

		if game.Status == "finished" {
			h.finishGame(game)
		}
	case "leaveQueue":
		h.removeFromWaitingQueue(message.Client)
		log.Printf("User %s left from waiting queue", message.Client.UserId)
	default:
		log.Println("Unknown message type: ", base.Type)
	}

}

func (h *Hub) finishGame(game *matchmaking.Game) {
	log.Println("Game finished: ", game.Id)
	go func() {
		err := h.gameStoreClient.SaveGame(*game)
		if err != nil {
			log.Println("Error saving game state: ", err)
		}
	}()
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	h.gameRepository.DeleteGame(ctx, &dto.GameDAO{Id: game.Id, PlayerIds: game.PlayerIds})
	cancel()

	for _, pid := range game.PlayerIds {
		delete(h.GameByUserId, pid)
	}
	delete(h.GamesById, game.Id)
}

func (h *Hub) tryRestore(client *client.Client) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
	gameId, err := h.gameRepository.GetGameByUserId(ctx, client.UserId)
	cancel()
	if err != nil || gameId == "" {
		return
	}

	game := h.GamesById[gameId]
	if game == nil {
		ctx, cancel := context.WithTimeout(context.Background(), time.Second*2)
		gameDao, err := h.gameRepository.GetGameById(ctx, gameId)
		cancel()
		if err != nil {
			return
		}
		game = h.FromDAO(*gameDao)
		h.GamesById[gameId] = game
		for _, pid := range game.PlayerIds {
			h.GameByUserId[pid] = game
		}
	}

	game.UpdatePlayerClient(client)
	game.SendStartInfo(client)
	game.BroadcastState()
}

func (h *Hub) Run() {
	ticker := time.NewTicker(time.Second * 1)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			h.checkGameTimeouts()
		case client := <-h.Register:
			// Replace any previous client for same userId.
			if old := h.ClientsByUserId[client.UserId]; old != nil && old != client {
				// Best-effort: close old connection; its pumps will exit.
				_ = old.Conn.Close()
				// Don't close old.Send here (could race with sender); it will be GC'd when pumps exit.
			}
			h.ClientsByUserId[client.UserId] = client
			h.tryRestore(client)
		case client := <-h.Unregister:
			// Only unregister if this exact client is the active one for that userId.
			if h.ClientsByUserId[client.UserId] == client {
				delete(h.ClientsByUserId, client.UserId)
			}
			h.removeFromWaitingQueue(client)
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

func (h *Hub) addToWaitingQueue(client *client.Client) {
	if h.GameByUserId[client.UserId] != nil {
		return
	}
	for _, c := range h.WaitingQueue {
		if c.UserId == client.UserId {
			return
		}
	}
	h.WaitingQueue = append(h.WaitingQueue, client)

	msg := dto.SearchingOpponent{
		Type: "searchingOpponent",
	}
	bytes, err := json.Marshal(msg)
	if err != nil {
		log.Println("Error marshalling message: ", err)
		return
	}
	client.Send <- bytes
	log.Println(len(h.WaitingQueue))
	if len(h.WaitingQueue) >= 2 {
		player1, player2 := h.WaitingQueue[0], h.WaitingQueue[1]
		if player1.UserId == player2.UserId {
			h.WaitingQueue = h.WaitingQueue[1:]
			return
		}
		h.WaitingQueue = h.WaitingQueue[2:]

		game := matchmaking.NewGame(player1, player2)
		log.Println("Game created: ", game.Id)
		h.GamesById[game.Id] = game
		for _, pid := range game.PlayerIds {
			h.GameByUserId[pid] = game
		}

		ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
		if err := h.gameRepository.SaveGameState(ctx, game.ToDAO()); err != nil {
			log.Println("Error saving initial game state: ", err)
		}
		cancel()

		game.Start()
		game.BroadcastState()
	}
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
