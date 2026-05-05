package ws

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/Jud1k/tic-tac-toe/internal/hub"

	"github.com/gorilla/websocket"
)

type Server struct {
	Config   config.Config
	Hub      *hub.Hub
	upgrader websocket.Upgrader
}

func NewServer(config config.Config, hub *hub.Hub) *Server {
	server := &Server{Config: config, Hub: hub}
	server.upgrader = websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
		CheckOrigin: func(r *http.Request) bool {
			origin := r.Header.Get("Origin")
			if origin == "" {
				return true
			}
			return server.isOriginAllowed(origin)
		},
	}
	return server
}

func (s *Server) HandleWs(w http.ResponseWriter, r *http.Request) {
	userId, ok := s.authenticateTicket(w, r)
	if !ok {
		return
	}

	wsConn, err := s.upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error: ", err)
		return
	}

	wsClient := &client.Client{
		UserId:   userId,
		Role:     client.RolePlayer,
		Conn:     wsConn,
		Send:     make(chan []byte, 32),
		Incoming: s.Hub.Incoming,
		Done:     s.Hub.Unregister,
	}
	s.Hub.Register <- wsClient

	go wsClient.WritePump()
	go wsClient.ReadPump()
}

func (s *Server) HandleSpectatorWs(w http.ResponseWriter, r *http.Request) {
	userId, ok := s.authenticateTicket(w, r)
	if !ok {
		return
	}

	gameId := extractGameId(r)
	if gameId == "" {
		http.Error(w, "gameId is required", http.StatusBadRequest)
		return
	}

	snapshotCh := make(chan []dto.OngoingGame, 1)
	s.Hub.OngoingSnapshotRequest <- snapshotCh
	snapshot := <-snapshotCh

	isAvailable := false
	for _, game := range snapshot {
		if game.GameId == gameId {
			isAvailable = true
			break
		}
	}
	if !isAvailable {
		http.Error(w, "Game is not available", http.StatusNotFound)
		return
	}

	wsConn, err := s.upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error: ", err)
		return
	}

	spectator := &client.Client{
		UserId:       userId,
		Role:         client.RoleSpectator,
		TargetGameId: gameId,
		Conn:         wsConn,
		Send:         make(chan []byte, 32),
		Done:         s.Hub.Unregister,
	}
	s.Hub.Register <- spectator

	go spectator.WritePump()
	go spectator.ReadPump()
}

func (s *Server) HandleOngoingGamesSSE(w http.ResponseWriter, r *http.Request) {
	if !s.setCorsHeaders(w, r) {
		http.Error(w, "Origin not allowed", http.StatusForbidden)
		return
	}
	
	_, ok := s.authenticateTicket(w, r)
	if !ok {
		return
	}

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("X-Accel-Buffering", "no")

	subscriber := &hub.OngoingGamesSubscriber{Events: make(chan hub.OngoingEvent, 32)}
	s.Hub.RegisterOngoing <- subscriber
	defer func() {
		s.Hub.UnregisterOngoing <- subscriber
	}()

	snapshotCh := make(chan []dto.OngoingGame, 1)
	s.Hub.OngoingSnapshotRequest <- snapshotCh
	snapshot := <-snapshotCh

	payload, err := json.Marshal(dto.OngoingGamesSnapshot{Games: snapshot})
	if err != nil {
		http.Error(w, "Failed to create snapshot", http.StatusInternalServerError)
		return
	}
	if err := writeSSEEvent(w, flusher, "activeGames", payload); err != nil {
		return
	}

	ticker := time.NewTicker(20 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-r.Context().Done():
			return
		case event, ok := <-subscriber.Events:
			if !ok {
				return
			}
			if err := writeSSEEvent(w, flusher, event.Name, event.Data); err != nil {
				return
			}
		case <-ticker.C:
			if _, err := fmt.Fprint(w, ": keepalive\n\n"); err != nil {
				return
			}
			flusher.Flush()
		}
	}
}

func (s *Server) authenticateTicket(w http.ResponseWriter, r *http.Request) (string, bool) {
	ticket := extractTicket(r)
	if ticket == "" {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return "", false
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	userId, err := s.Hub.TicketRepository.GetUserIdByTicket(ctx, ticket)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return "", false
	}
	return userId, true
}

func (s *Server) setCorsHeaders(w http.ResponseWriter, r *http.Request) bool {
	origin := r.Header.Get("Origin")
	if origin == "" {
		return true
	}
	if !s.isOriginAllowed(origin) {
		return false
	}

	w.Header().Set("Access-Control-Allow-Origin", origin)
	w.Header().Set("Vary", "Origin")
	return true
}

func (s *Server) isOriginAllowed(origin string) bool {
	if len(s.Config.CorsOrigins) == 0 {
		return false
	}
	for _, allowed := range s.Config.ParseCors() {
		if allowed == "*" || allowed == origin {
			return true
		}
	}
	return false
}

func writeSSEEvent(w http.ResponseWriter, flusher http.Flusher, eventName string, data []byte) error {
	if _, err := fmt.Fprintf(w, "event: %s\n", eventName); err != nil {
		return err
	}
	if _, err := fmt.Fprintf(w, "data: %s\n\n", data); err != nil {
		return err
	}
	flusher.Flush()
	return nil
}

func extractTicket(r *http.Request) string {
	return r.URL.Query().Get("ticket")
}

func extractGameId(r *http.Request) string {
	return r.URL.Query().Get("gameId")
}
