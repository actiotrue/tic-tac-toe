package ws

import (
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

func generateTicket() string {
	return uuid.NewString()
}

func TestExtractToken(t *testing.T) {
	req := &http.Request{
		URL: &url.URL{
			RawQuery: "ticket=query-token",
		},
	}

	token := extractTicket(req)

	if token != "query-token" {
		t.Errorf("expected 'query-token', got '%s'", token)
	}
}

func TestExtractToken_Empty(t *testing.T) {
	req := httptest.NewRequest("GET", "/", nil)

	token := extractTicket(req)

	if token != "" {
		t.Errorf("expected empty token, got '%s'", token)
	}
}

func TestHandleWs_Upgrade(t *testing.T) {
	server := &Server{}

	ticket := generateTicket()

	s := httptest.NewServer(http.HandlerFunc(server.HandleWs))
	defer s.Close()

	url := "ws" + s.URL[4:] + "?ticket=" + ticket

	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		t.Fatalf("failed to connect: %v", err)
	}
	defer conn.Close()
}
