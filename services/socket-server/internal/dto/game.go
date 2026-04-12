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

type GameState struct {
	Type    string           `json:"type"`
	Payload GameStatePayload `json:"payload"`
}

type GameStatePayload struct {
	Turn        string       `json:"turn"`
	Board       []string     `json:"board"`
	YourSide    string       `json:"yourSide"`
	SecondsLeft int          `json:"secondsLeft"`
	Players     []PlayerInfo `json:"players"`
}

type OngoingGame struct {
	GameId    string       `json:"gameId"`
	Players   []PlayerInfo `json:"players"`
	Turn      string       `json:"turn"`
	StartedAt time.Time    `json:"startedAt"`
}

type OngoingGamesSnapshot struct {
	Games []OngoingGame `json:"games"`
}

type OngoingGameCreated struct {
	Game OngoingGame `json:"game"`
}

type OngoingGameFinished struct {
	GameId string `json:"gameId"`
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

type PlayerInfo struct {
	UserId   string `json:"userId"`
	Username string `json:"username"`
	Side     string `json:"side"`
	ImageUrl string `json:"imageUrl"`
}

type GameResultRequest struct {
	Id       string     `json:"id"`
	Result   GameResult `json:"result"`
	Duration int        `json:"duration"`
	Players  []Player   `json:"players"`
}

type GameRematchRequest struct {
	Type string `json:"type"`
}

type GameRematchState struct {
	Type    string                  `json:"type"`
	Payload GameRematchStatePayload `json:"payload"`
}

type GameRematchStatePayload struct {
	Ready map[string]bool `json:"ready"`
}

type GameClosed struct {
	Type    string            `json:"type"`
	Payload GameClosedPayload `json:"payload"`
}

type GameClosedPayload struct {
	Reason string `json:"reason"`
}

type GameDaoPlayer struct {
	Id       string `json:"userId"`
	Side     string `json:"side"`
	Username string `json:"username"`
	ImageUrl string `json:"imageUrl"`
}

type GameDAO struct {
	Id          string          `json:"gameId"`
	Players     []GameDaoPlayer `json:"players"`
	Board       [9]string       `json:"board"`
	Turn        string          `json:"turn"`
	Status      string          `json:"status"`
	Winner      string          `json:"winner"`
	StartTime   time.Time       `json:"startTime"`
	TurnEndTime time.Time       `json:"turnEndTime"`
}
