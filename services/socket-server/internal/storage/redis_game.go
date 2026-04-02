package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/redis/go-redis/v9"
)

type Keys struct {
	game string
	user string
}

type GameRepository struct {
	redis *redis.Client
	keys  Keys
}

func NewGameRepository(redisClient *redis.Client) *GameRepository {
	return &GameRepository{redis: redisClient, keys: Keys{game: "game:%s", user: "user:%s:active_game"}}
}

func (r *GameRepository) SaveGameState(ctx context.Context, game dto.GameDAO) error {
	data, err := json.Marshal(game)
	if err != nil {
		return err
	}

	pipe := r.redis.Pipeline()
	pipe.Set(ctx, fmt.Sprintf(r.keys.game, game.Id), data, time.Hour)

	for _, playerId := range game.PlayerIds {
		pipe.Set(ctx, fmt.Sprintf(r.keys.user, playerId), game.Id, time.Hour)
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

func (r *GameRepository) DeleteGame(ctx context.Context, game *dto.GameDAO) {
	pipe := r.redis.Pipeline()
	pipe.Del(ctx, fmt.Sprintf(r.keys.game, game.Id))
	for _, playerId := range game.PlayerIds {
		pipe.Del(ctx, fmt.Sprintf(r.keys.user, playerId))
	}
	pipe.Exec(ctx)
}
