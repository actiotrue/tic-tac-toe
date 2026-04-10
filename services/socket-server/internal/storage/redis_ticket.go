package storage

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

type TicketKeys struct {
	ticket string
}

type TicketRepository struct {
	redis *redis.Client
	keys  TicketKeys
}

func NewTicketRepository(redisClient *redis.Client) *TicketRepository {
	return &TicketRepository{redis: redisClient, keys: TicketKeys{ticket: "ws_ticket:%s"}}
}

func (r *TicketRepository) GetUserIdByTicket(ctx context.Context, ticket string) (string, error) {
	user_id, err := r.redis.Get(ctx, fmt.Sprintf(r.keys.ticket, ticket)).Result()
	if err != nil {
		return "", err
	}

	r.redis.Del(ctx, fmt.Sprintf(r.keys.ticket, ticket))

	return user_id, nil
}
