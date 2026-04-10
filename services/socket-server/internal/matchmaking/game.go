package matchmaking

import (
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

type PlayerMatchData struct {
	Client *client.Client
	Info   *dto.PlayerInfo
}

type Player struct {
	Id       string
	Side     string // "X" или "O"
	Client   *client.Client
	Username string
	ImageUrl string
}

type Game struct {
	Id            string
	Players       [2]*Player
	Board         [9]string
	Turn          string
	Status        string
	Winner        string
	StartGameTime time.Time
	EndGameTime   time.Time
	TurnEndTime   time.Time
	RematchState  map[string]bool
}

func NewGame(players []PlayerMatchData) *Game {
	player1, player2 := players[0], players[1]
	rematchState := make(map[string]bool)
	for _, player := range players {
		rematchState[player.Client.UserId] = false
	}
	return &Game{
		Id: uuid.New().String(),
		Players: [2]*Player{
			{
				Id:       player1.Client.UserId,
				Side:     "X",
				Client:   player1.Client,
				Username: player1.Info.Username,
				ImageUrl: player1.Info.ImageUrl,
			},
			{
				Id:       player2.Client.UserId,
				Side:     "O",
				Client:   player2.Client,
				Username: player2.Info.Username,
				ImageUrl: player2.Info.ImageUrl,
			},
		},
		Board:         [9]string{"", "", "", "", "", "", "", "", ""},
		Status:        "playing",
		Turn:          "X",
		StartGameTime: time.Now(),
		TurnEndTime:   time.Now().Add(30 * time.Second),
		RematchState:  rematchState,
	}
}

func (g *Game) ToDAO() dto.GameDAO {
	players := make([]dto.GameDaoPlayer, 0)
	for _, p := range g.Players {
		players = append(players, dto.GameDaoPlayer{
			Id:       p.Id,
			Side:     p.Side,
			Username: p.Username,
			ImageUrl: p.ImageUrl,
		})
	}
	return dto.GameDAO{
		Id:          g.Id,
		Players:     players,
		Board:       g.Board,
		Turn:        g.Turn,
		Status:      g.Status,
		Winner:      g.Winner,
		StartTime:   g.StartGameTime,
		TurnEndTime: g.TurnEndTime,
	}
}

func (g *Game) GetPlayerByUserID(userID string) *Player {
	for _, p := range g.Players {
		if p.Id == userID {
			return p
		}
	}
	return nil
}

func (g *Game) GetPlayerBySide(side string) *Player {
	for _, p := range g.Players {
		if p.Side == side {
			return p
		}
	}
	return nil
}

func (g *Game) getSideByUserId(userId string) string {
	for _, player := range g.Players {
		if player.Id == userId {
			return player.Side
		}
	}
	return ""
}

func (g *Game) updateTurnTimer() {
	g.TurnEndTime = time.Now().Add(30 * time.Second)
}

func (g *Game) attachClient(c *client.Client) {
	if c == nil {
		return
	}
	for _, player := range g.Players {
		if player.Id == c.UserId {
			player.Client = c
		}
	}
}

func (g *Game) detachUser(userId string) {
	for _, player := range g.Players {
		if player.Id == userId {
			player.Client = nil
		}
	}
}

func (g *Game) Detach(userId string) {
	g.detachUser(userId)
}

func (g *Game) GetPlayersInfo() []dto.PlayerInfo {
	players := make([]dto.PlayerInfo, len(g.Players))
	for i, p := range g.Players {
		players[i] = dto.PlayerInfo{
			UserId:   p.Id,
			Username: p.Username,
			Side:     p.Side,
			ImageUrl: p.ImageUrl,
		}
	}
	return players
}

func (g *Game) BroadcastState() {
	players := g.GetPlayersInfo()
	for _, player := range g.Players {
		secondsLeft := max(int(time.Until(g.TurnEndTime).Seconds()), 0)
		side := g.getSideByUserId(player.Id)
		msg := dto.GameState{
			Type: "gameState",
			Payload: dto.GameStatePayload{
				Board:       g.Board[:],
				Turn:        g.Turn,
				YourSide:    side,
				SecondsLeft: secondsLeft,
				Players:     players,
			},
		}
		player.Client.SendJSON(msg)
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
	for _, player := range g.Players {
		player.Client.SendJSON(msg)
	}
}

func (g *Game) HandleMove(userId string, index int) {
	if g.Status != "playing" || g.Board[index] != "" || index < 0 || index > 8 {
		return
	}

	symbol := g.getSideByUserId(userId)
	if g.Turn != symbol {
		return
	}

	g.Board[index] = symbol
	isWin, winner, winningLine := g.checkWinner()
	if isWin {
		g.EndGameTime = time.Now()
		g.ApplyFinish(winner, winningLine)
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
		g.EndGameTime = time.Now()
		g.ApplyFinish("draw", nil)
		return
	}
	g.Turn = g.OpponentOf(g.Turn)

	g.updateTurnTimer()
}

func (g *Game) ApplyFinish(winner string, line []int) {
	g.Status = "finished"
	g.Winner = winner
	g.BroadcastState()
	g.BroadcastGameOver(winner, line)
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

func (g *Game) CheckReadyRematch() bool {
	allTrue := true
	for _, v := range g.RematchState {
		if !v {
			allTrue = false
			break
		}
	}
	return allTrue
}

func (g *Game) BroadcastRematchState() {
	msg := dto.GameRematchState{
		Type: "rematchState",
		Payload: dto.GameRematchStatePayload{
			Ready: g.RematchState,
		},
	}

	for _, player := range g.Players {
		player.Client.SendJSON(msg)
	}
}

func (g *Game) getOpponentByUserId(userId string) *Player {
	for _, player := range g.Players {
		if player.Id != userId {
			return player
		}
	}
	return nil
}

func (g *Game) BroadcastGameClosed(reason string, userId string) {
	msg := dto.GameClosed{
		Type: "gameClosed",
		Payload: dto.GameClosedPayload{
			Reason: reason,
		},
	}

	to := g.getOpponentByUserId(userId)
	if to != nil {
		to.Client.SendJSON(msg)
	}
}
