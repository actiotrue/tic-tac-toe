package ws

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/Jud1k/tic-tac-toe/internal/hub"

	"github.com/gorilla/websocket"
)

type Server struct {
	Config   config.Config
	Hub      *hub.Hub
	upgrader websocket.Upgrader
}

func NewServer(config config.Config, hub *hub.Hub) *Server {
	return &Server{
		Config: config,
		Hub:    hub,
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			CheckOrigin: func(r *http.Request) bool {
				origin := r.Header.Get("Origin")
				if len(config.CorsOrigins) == 0 {
					return false
				}
				for _, allowed := range config.ParseCors() {
					if allowed == "*" || allowed == origin {
						return true
					}
				}
				return false
			},
		},
	}
}

func (s *Server) HandleWs(w http.ResponseWriter, r *http.Request) {
	ticket := extractTicket(r)
	if ticket == "" {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()
	userId, err := s.Hub.TicketRepository.GetUserIdByTicket(ctx, ticket)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	wsConn, err := s.upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error: ", err)
		return
	}

	client := &client.Client{
		UserId:   userId,
		Conn:     wsConn,
		Send:     make(chan []byte),
		Incoming: s.Hub.Incoming,
		Done:     s.Hub.Unregister,
	}
	s.Hub.Register <- client

	go client.WritePump()
	go client.ReadPump()
}

func extractTicket(r *http.Request) string {
	return r.URL.Query().Get("ticket")
}
