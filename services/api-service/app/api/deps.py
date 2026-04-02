from pathlib import Path
import jwt
import asyncpg
from typing import Annotated, Any, AsyncGenerator
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer

from redis import Redis

from app.core.database import database
from app.core.settings import settings
from app.schemas.user import UserRead, UserReadWithoutPassword
from app.services.game import GameService
from app.services.player import PlayerService
from app.core.redis import redis_client
from app.services.user import UserService

REDIS_SCRIPTS_DIR = Path(__file__).parent / "redis_scripts"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/access-token")


async def get_db() -> AsyncGenerator[asyncpg.Connection, Any]:
    async with database.pool.acquire() as conn:
        yield conn


DbConnectionDep = Annotated[asyncpg.Connection, Depends(get_db)]


def get_redis_client() -> Redis:
    return redis_client


RedisClientDep = Annotated[Redis, Depends(get_redis_client)]


async def get_user_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> UserService:
    return UserService(db_conn, redis_client)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_player_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> PlayerService:
    return PlayerService(db_conn, redis_client)


PlayerServiceDep = Annotated[PlayerService, Depends(get_player_service)]


async def get_game_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> GameService:
    return GameService(db_conn, redis_client)


GameServiceDep = Annotated[GameService, Depends(get_game_service)]


async def get_current_user(
    user_service: UserServiceDep, token: str = Depends(oauth2_scheme)
) -> UserRead:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


CurrentUserDep = Annotated[UserReadWithoutPassword, Depends(get_current_user)]


def verify_internal_service_key(
    key: str = Header(alias="X-Internal-Service-Key"),
) -> str:
    if key != settings.INTERNAL_SERVICE_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal service key",
        )
    return True


InternalServiceKeyDep = Annotated[bool, Depends(verify_internal_service_key)]
