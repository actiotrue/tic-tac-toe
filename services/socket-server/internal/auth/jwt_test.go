package auth

import (
	"testing"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

func generateToken(secret string, userID string) (string, error) {
	claims := Claims{
		UserId: userID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour)),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret))
}

func TestParseToken_Valid(t *testing.T) {
	secret := "test-secret"

	tokenString, err := generateToken(secret, "123")
	if err != nil {
		t.Fatal(err)
	}

	claims, err := ParseToken(tokenString, secret)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if claims.UserId != "123" {
		t.Errorf("expected userId 123, got %s", claims.UserId)
	}
}

func TestParseToken_InvalidSignature(t *testing.T) {
	tokenString, _ := generateToken("secret1", "123")

	_, err := ParseToken(tokenString, "wrong-secret")
	if err == nil {
		t.Fatal("expected error, got nil")
	}
}

func TestParseToken_InvalidToken(t *testing.T) {
	_, err := ParseToken("invalid.token.here", "secret")

	if err == nil {
		t.Fatal("expected error, got nil")
	}
}
