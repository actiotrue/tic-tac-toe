package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/redis/go-redis/v9"
)

type GameKeys struct {
	game string
	user string
}

type GameRepository struct {
	redis *redis.Client
	keys  GameKeys
}

func NewGameRepository(redisClient *redis.Client) *GameRepository {
	return &GameRepository{redis: redisClient, keys: GameKeys{game: "game:%s", user: "user:%s:active_game"}}
}

func (r *GameRepository) SaveGameState(ctx context.Context, game dto.GameDAO) error {
	data, err := json.Marshal(game)
	if err != nil {
		return err
	}

	pipe := r.redis.Pipeline()
	pipe.Set(ctx, fmt.Sprintf(r.keys.game, game.Id), data, time.Hour)

	for _, player := range game.Players {
		pipe.Set(ctx, fmt.Sprintf(r.keys.user, player.Id), game.Id, time.Hour)
	}

	_, err = pipe.Exec(ctx)
	return err
}

func (r *GameRepository) GetGameByUserId(ctx context.Context, userID string) (string, error) {
	return r.redis.Get(ctx, fmt.Sprintf(r.keys.user, userID)).Result()
}

func (r *GameRepository) GetGameById(ctx context.Context, gameId string) (*dto.GameDAO, error) {
	data, err := r.redis.Get(ctx, fmt.Sprintf(r.keys.game, gameId)).Result()
	if err != nil {
		return nil, err
	}
	var game dto.GameDAO
	err = json.Unmarshal([]byte(data), &game)
	if err != nil {
		return nil, err
	}
	return &game, nil
}

func (r *GameRepository) DeleteGame(ctx context.Context, game dto.GameDAO) error {
	pipe := r.redis.Pipeline()
	pipe.Del(ctx, fmt.Sprintf(r.keys.game, game.Id))
	for _, player := range game.Players {
		pipe.Del(ctx, fmt.Sprintf(r.keys.user, player.Id))
	}
	_, err := pipe.Exec(ctx)
	return err
}
