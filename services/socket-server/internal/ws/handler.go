package ws

import (
	"log"
	"net/http"
	"strings"

	"github.com/Jud1k/tic-tac-toe/internal/auth"
	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/Jud1k/tic-tac-toe/internal/hub"

	"github.com/gorilla/websocket"
)

type Server struct {
	Config config.Config
	Hub    *hub.Hub
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func (s *Server) HandleWs(w http.ResponseWriter, r *http.Request) {
	token := extractToken(r)
	if token == "" {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	claims, err := auth.ParseToken(token, s.Config.SecretKey)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	log.Println("User connected with id: ", claims.UserId)

	wsConn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error: ", err)
		return
	}

	client := &client.Client{
		UserId:   claims.UserId,
		Conn:     wsConn,
		Send:     make(chan []byte),
		Incoming: s.Hub.Incoming,
		Done:     s.Hub.Unregister,
	}
	s.Hub.Register <- client

	go client.WritePump()
	go client.ReadPump()
}

func extractToken(r *http.Request) string {
	authHeader := r.Header.Get("Authorization")
	if after, ok := strings.CutPrefix(authHeader, "Bearer "); ok {
		return after
	}
	return r.URL.Query().Get("token")
}
