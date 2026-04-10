from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated
from pydantic import AnyUrl, BeforeValidator, computed_field


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


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
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DUMMY_HASH: str = "$argon2id$v=19$m=65536,t=3,p=4$J0mNsoKtRj8pkAWaZIKtRA$EBLZ9qeI4KX2+4euhyYVfWmKpQXTGv/6PTY0mv/XaDQ"

    CLOUDINARY_BASE_IMAGE_PUBLIC_ID: str

    INTERNAL_SERVICE_KEY: str

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]

    model_config = SettingsConfigDict(
        env_ignore_empty=True, extra="allow", env_file="../.env"
    )


settings = Settings()
