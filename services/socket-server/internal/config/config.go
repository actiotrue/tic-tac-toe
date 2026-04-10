package config

import "strings"

type Config struct {
	SecretKey          string `env:"SECRET_KEY"`
	InternalServiceKey string `env:"INTERNAL_SERVICE_KEY"`
	FastApiUrl         string `env:"FASTAPI_URL"`
	RedisAddr          string `env:"REDIS_ADDR"`
	CorsOrigins        string `env:"BACKEND_CORS_ORIGINS"`
}

func (c *Config) ParseCors() []string {
	return strings.Split(c.CorsOrigins, ",")
}
