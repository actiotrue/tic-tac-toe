package ws

import (
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"

	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
)

func generateToken(secret string, userId string) (string, error) {
	claims := jwt.MapClaims{
		"sub": userId,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString([]byte(secret))
	if err != nil {
		return "", err
	}

	return tokenString, nil
}

func TestExtractToken_FromHeader(t *testing.T) {
	req := &http.Request{
		Header: http.Header{
			"Authorization": []string{"Bearer test-token"},
		},
	}

	token := extractToken(req)

	if token != "test-token" {
		t.Errorf("expected 'test-token', got '%s'", token)
	}
}

func TestExtractToken_FromQuery(t *testing.T) {
	req := &http.Request{
		URL: &url.URL{
			RawQuery: "token=query-token",
		},
	}

	token := extractToken(req)

	if token != "query-token" {
		t.Errorf("expected 'query-token', got '%s'", token)
	}
}

func TestExtractToken_Empty(t *testing.T) {
	req := httptest.NewRequest("GET", "/", nil)

	token := extractToken(req)

	if token != "" {
		t.Errorf("expected empty token, got '%s'", token)
	}
}

func TestHandleWs_Upgrade(t *testing.T) {
	server := &Server{
		Config: config.Config{
			SecretKey: "test-secret",
		},
	}

	token, err := generateToken("test-secret", "123")
	if err != nil {
		t.Fatalf("failed to generate token: %v", err)
	}
	s := httptest.NewServer(http.HandlerFunc(server.HandleWs))
	defer s.Close()

	url := "ws" + s.URL[4:] + "?token=" + token

	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		t.Fatalf("failed to connect: %v", err)
	}
	defer conn.Close()
}
