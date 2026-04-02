package dto

import "time"

type JoinQueueRequest struct {
	Type string `json:"type"`
}

type MakeMoveRequest struct {
	Type    string `json:"type"`
	Payload struct {
		Index int `json:"index"`
	} `json:"payload"`
}

type SearchingOpponent struct {
	Type string `json:"type"`
}

type GameStarted struct {
	Type    string             `json:"type"`
	Payload GameStartedPayload `json:"payload"`
}

type GameStartedPayload struct {
	GameID     string `json:"gameId"`
	YourSide   string `json:"yourSide"`
	OpponentId string `json:"opponentId"`
	Turn       string `json:"turn"`
}

type GameState struct {
	Type    string           `json:"type"`
	Payload GameStatePayload `json:"payload"`
}

type GameStatePayload struct {
	Turn        string   `json:"turn"`
	Board       []string `json:"board"`
	YourSide    string   `json:"yourSide"`
	SecondsLeft int      `json:"secondsLeft"`
}

type GameOver struct {
	Type    string          `json:"type"`
	Payload GameOverPayload `json:"payload"`
}

type GameOverPayload struct {
	Winner      string `json:"winner"`
	WinningLine []int  `json:"winningLine"`
}

type GameResult string

const (
	GameResultX    GameResult = "x_won"
	GameResultO    GameResult = "o_won"
	GameResultDraw GameResult = "draw"
)

type Player struct {
	GameId   string `json:"gameId"`
	PlayerId string `json:"playerId"`
	Side     string `json:"side"`
	Type     string `json:"type"`
}

type GameResultRequest struct {
	Id       string     `json:"id"`
	Result   GameResult `json:"result"`
	Duration int        `json:"duration"`
	Players  []Player   `json:"players"`
}

type GameDAO struct {
	Id         string            `json:"gameId"`
	PlayerIds  []string          `json:"playerIds"`
	PlayerSide map[string]string `json:"playerSide"`
	Board      [9]string         `json:"board"`
	Turn       string            `json:"turn"`
	Status     string            `json:"status"`
	Winner     string            `json:"winner"`
	StartTime  time.Time         `json:"startTime"`
}
