package ws

import (
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"
)

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

func TestExtractGameId(t *testing.T) {
	req := &http.Request{
		URL: &url.URL{
			RawQuery: "gameId=game-123",
		},
	}

	gameId := extractGameId(req)
	if gameId != "game-123" {
		t.Errorf("expected game id game-123, got %s", gameId)
	}
}

func TestHandleWs_UnauthorizedWithoutTicket(t *testing.T) {
	server := &Server{}

	req := httptest.NewRequest(http.MethodGet, "/api/v1/ws/game", nil)
	rr := httptest.NewRecorder()
	server.HandleWs(rr, req)

	if rr.Code != http.StatusUnauthorized {
		t.Fatalf("expected status %d, got %d", http.StatusUnauthorized, rr.Code)
	}
}
