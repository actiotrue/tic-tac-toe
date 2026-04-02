package auth

import (
	"errors"
	"log"

	"github.com/golang-jwt/jwt/v5"
)

type Claims struct {
	UserId string `json:"sub"`
	jwt.RegisteredClaims
}

func ParseToken(tokenString string, secretKey string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (any, error) {
		return []byte(secretKey), nil
	})
	if err != nil {
		log.Println(err)
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !token.Valid || !ok {
		return nil, errors.New("invalid token")
	}

	return claims, nil
}
