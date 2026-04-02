from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "tic-tac-toe"
    DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = "6379"
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DUMMY_HASH: str = "$argon2id$v=19$m=65536,t=3,p=4$J0mNsoKtRj8pkAWaZIKtRA$EBLZ9qeI4KX2+4euhyYVfWmKpQXTGv/6PTY0mv/XaDQ"

    CLOUDINARY_BASE_IMAGE_PUBLIC_ID: str

    INTERNAL_SERVICE_KEY: str

    model_config = SettingsConfigDict(
        env_ignore_empty=True, extra="allow", env_file="../.env"
    )


settings = Settings()
