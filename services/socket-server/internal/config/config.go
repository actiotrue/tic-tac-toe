package config

type Config struct {
	SecretKey          string `env:"SECRET_KEY"`
	InternalServiceKey string `env:"INTERNAL_SERVICE_KEY"`
	FastApiUrl         string `env:"FASTAPI_URL"`
	RedisAddr          string `env:"REDIS_ADDR"`
}
