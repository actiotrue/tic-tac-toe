package integration

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/Jud1k/tic-tac-toe/internal/matchmaking"
)

type GameStoreClient struct {
	BaseUrl    string
	HttpClient *http.Client
	ApiKey     string
}

func NewGameStoreClient(baseUrl string, apiKey string) *GameStoreClient {
	return &GameStoreClient{
		BaseUrl:    baseUrl,
		HttpClient: &http.Client{Timeout: 10 * time.Second},
		ApiKey:     apiKey,
	}
}

func (c *GameStoreClient) SaveGame(game matchmaking.Game) error {
	if len(game.Players) < 2 {
		return fmt.Errorf("not enough players to save game")
	}

	var gameResult dto.GameResult
	switch game.Winner {
	case "X":
		gameResult = dto.GameResultX
	case "O":
		gameResult = dto.GameResultO
	case "draw":
		gameResult = dto.GameResultDraw
	default:
		return fmt.Errorf("unknown winner status: %s", game.Winner)
	}

	finishedGame := dto.GameResultRequest{
		Id:       game.Id,
		Result:   gameResult,
		Duration: int(game.EndGameTime.Sub(game.StartGameTime).Seconds()),
		Players: []dto.Player{
			{
				GameId:   game.Id,
				PlayerId: game.Players[0].Id,
				Side:     game.Players[0].Side,
				Type:     "human",
			},
			{
				GameId:   game.Id,
				PlayerId: game.Players[1].Id,
				Side:     game.Players[1].Side,
				Type:     "human",
			},
		},
	}

	payload, err := json.Marshal(finishedGame)
	if err != nil {
		log.Println(err)
		return err
	}

	req, err := http.NewRequest("POST", c.BaseUrl+"/api/v1/games/service", bytes.NewBuffer(payload))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Internal-Service-Key", c.ApiKey)
	resp, err := c.HttpClient.Do(req)
	if err != nil {
		log.Println(err)
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 201 {
		return fmt.Errorf("error saving game: %s", resp.Status)
	}
	return nil
}

func (c *GameStoreClient) GetPlayers(userIds []string) ([]*dto.PlayerInfo, error) {
	body, err := json.Marshal(userIds)
	if err != nil {
		return nil, fmt.Errorf("marshal ids: %w", err)
	}

	req, err := http.NewRequest("POST", c.BaseUrl+"/api/v1/players/batch/service", bytes.NewBuffer(body))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Internal-Service-Key", c.ApiKey)
	resp, err := c.HttpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("error getting player: %s", resp.Status)
	}

	var player []*dto.PlayerInfo
	err = json.NewDecoder(resp.Body).Decode(&player)
	if err != nil {
		return nil, err
	}
	return player, nil
}
