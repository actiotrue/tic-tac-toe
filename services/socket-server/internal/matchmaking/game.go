package matchmaking

import (
	"encoding/json"
	"log"
	"slices"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/google/uuid"
)

var lines = [][]int{
	{0, 1, 2},
	{3, 4, 5},
	{6, 7, 8},
	{0, 3, 6},
	{1, 4, 7},
	{2, 5, 8},
	{0, 4, 8},
	{2, 4, 6},
}

type Game struct {
	Id              string                    `json:"gameId"`
	PlayerIds       []string                  `json:"playerIds"`
	SideByUserId    map[string]string         `json:"playerSide"`
	ClientsByUserId map[string]*client.Client `json:"-"`
	Board           [9]string
	Turn            string
	Status          string
	Winner          string
	StartTime       time.Time
	TurnEndTime     time.Time `json:"turnEndTime"`
}

func NewGame(player1, player2 *client.Client) *Game {
	p1 := player1.UserId
	p2 := player2.UserId
	return &Game{
		Id:        uuid.New().String(),
		PlayerIds: []string{p1, p2},
		SideByUserId: map[string]string{
			p1: "X",
			p2: "O",
		},
		ClientsByUserId: map[string]*client.Client{
			p1: player1,
			p2: player2,
		},
		Board:       [9]string{"", "", "", "", "", "", "", "", ""},
		Status:      "playing",
		Turn:        "X",
		StartTime:   time.Now(),
		TurnEndTime: time.Now().Add(10 * time.Second),
	}
}

func (g *Game) ToDAO() dto.GameDAO {
	return dto.GameDAO{
		Id:         g.Id,
		PlayerIds:  append([]string(nil), g.PlayerIds...),
		PlayerSide: g.SideByUserId,
		Board:      g.Board,
		Turn:       g.Turn,
		Status:     g.Status,
		Winner:     g.Winner,
		StartTime:  g.StartTime,
	}
}

func (g *Game) updateTurnTimer() {
	g.TurnEndTime = time.Now().Add(10 * time.Second)
}

func (g *Game) send(client *client.Client, data interface{}) {
	if client == nil {
		return
	}
	bytes, err := json.Marshal(data)
	if err != nil {
		log.Println(err)
		return
	}
	defer func() {
		if r := recover(); r != nil {
			log.Printf("Recovered from panic while sending to client %s: %v", client.UserId, r)
		}
	}()
	client.Send <- bytes
}

func (g *Game) attachClient(c *client.Client) {
	if c == nil {
		return
	}
	if !slices.Contains(g.PlayerIds, c.UserId) {
		return
	}
	if g.ClientsByUserId == nil {
		g.ClientsByUserId = make(map[string]*client.Client)
	}
	g.ClientsByUserId[c.UserId] = c
}

func (g *Game) detachUser(userId string) {
	if g.ClientsByUserId == nil {
		return
	}
	g.ClientsByUserId[userId] = nil
}

func (g *Game) Detach(userId string) {
	g.detachUser(userId)
}

func (g *Game) BroadcastState() {
	for _, userId := range g.PlayerIds {
		player := g.ClientsByUserId[userId]
		if player == nil {
			continue
		}
		msg := dto.GameState{
			Type: "gameState",
			Payload: dto.GameStatePayload{
				Board:       g.Board[:],
				Turn:        g.Turn,
				YourSide:    g.SideByUserId[userId],
				SecondsLeft: int(time.Until(g.TurnEndTime).Seconds()),
			},
		}
		g.send(player, msg)
	}
}

func (g *Game) BroadcastGameOver(winner string, winningLine []int) {
	msg := dto.GameOver{
		Type: "gameOver",
		Payload: dto.GameOverPayload{
			Winner:      winner,
			WinningLine: winningLine,
		},
	}
	for _, userId := range g.PlayerIds {
		g.send(g.ClientsByUserId[userId], msg)
	}
}

func (g *Game) Start() {
	playerX := g.ClientsByUserId[g.PlayerIds[0]]
	playerY := g.ClientsByUserId[g.PlayerIds[1]]

	msgX := dto.GameStarted{
		Type: "gameStarted",
		Payload: dto.GameStartedPayload{
			GameID:     g.Id,
			YourSide:   "X",
			OpponentId: g.PlayerIds[1],
			Turn:       g.Turn,
		},
	}

	msgO := dto.GameStarted{
		Type: "gameStarted",
		Payload: dto.GameStartedPayload{
			GameID:     g.Id,
			YourSide:   "O",
			OpponentId: g.PlayerIds[0],
			Turn:       g.Turn,
		},
	}

	g.send(playerX, msgX)
	g.send(playerY, msgO)
}

func (g *Game) SendStartInfo(to *client.Client) {
	if to == nil {
		return
	}
	if !slices.Contains(g.PlayerIds, to.UserId) {
		return
	}
	opponentId := ""
	for _, id := range g.PlayerIds {
		if id != to.UserId {
			opponentId = id
			break
		}
	}
	msg := dto.GameStarted{
		Type: "gameStarted",
		Payload: dto.GameStartedPayload{
			GameID:     g.Id,
			YourSide:   g.SideByUserId[to.UserId],
			OpponentId: opponentId,
			Turn:       g.Turn,
		},
	}
	g.send(to, msg)
}

func (g *Game) HandleMove(userId string, index int) {
	if g.Status != "playing" || g.Board[index] != "" || index < 0 || index > 8 {
		return
	}

	symbol := g.SideByUserId[userId]
	if g.Turn != symbol {
		return
	}

	g.Board[index] = symbol
	isWin, winner, winningLine := g.checkWinner()
	if isWin {
		g.Status = "finished"
		g.Winner = winner
		g.BroadcastState()
		g.BroadcastGameOver(winner, winningLine)
		return
	}

	isDraw := true
	for _, v := range g.Board {
		if v == "" {
			isDraw = false
			break
		}
	}
	if isDraw {
		g.Status = "finished"
		g.Winner = winner
		g.BroadcastState()
		g.BroadcastGameOver("draw", nil)
		return
	}

	if g.Turn == "X" {
		g.Turn = "O"
	} else {
		g.Turn = "X"
	}
	g.updateTurnTimer()
	g.BroadcastState()
}

func (g *Game) OpponentOf(symbol string) string {
	if symbol == "X" {
		return "O"
	}
	return "X"
}

func (g *Game) checkWinner() (bool, string, []int) {
	for _, line := range lines {
		var a, b, c int
		a = line[0]
		b = line[1]
		c = line[2]
		s := g.Board[a]
		if s != "" && s == g.Board[b] && s == g.Board[c] {
			return true, s, line
		}
	}
	return false, "", nil
}

func (g *Game) UpdatePlayerClient(newClient *client.Client) {
	g.attachClient(newClient)
}
