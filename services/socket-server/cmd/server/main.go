package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/caarlos0/env/v11"
	"github.com/redis/go-redis/v9"

	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/Jud1k/tic-tac-toe/internal/hub"
	"github.com/Jud1k/tic-tac-toe/internal/integration"
	"github.com/Jud1k/tic-tac-toe/internal/ws"
)

func main() {
	var config config.Config
	if err := env.Parse(&config); err != nil {
		log.Fatal("Parsing error: ", err)
	}
	gameStoreClient := integration.NewGameStoreClient(config.FastApiUrl, config.InternalServiceKey)

	rdb := redis.NewClient(&redis.Options{
		Addr:     config.RedisAddr,
		Password: "",
		DB:       0,
	})
	defer rdb.Close()
	ctx := context.Background()
	err := rdb.Ping(ctx).Err()
	if err != nil {
		log.Fatal(err)
	}

	hub := hub.NewHub(gameStoreClient, rdb)
	go hub.Run()

	server := ws.NewServer(config, hub)
	http.HandleFunc("/api/v1/ws/game", server.HandleWs)
	fmt.Println("Listening on port 8080")

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
