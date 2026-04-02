import subprocess
from typing import AsyncGenerator, Any, Generator
import uuid
import asyncpg
from httpx import ASGITransport, AsyncClient
import pytest
from redis.asyncio import Redis

from app.models import Player, User, Game


TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"
TEST_REDIS_URL = "redis://localhost:6379"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[Any, Any, Any]:
    subprocess.run(["dbmate", "--url", TEST_DATABASE_URL, "up"], check=True)
    yield


@pytest.fixture
async def db() -> AsyncGenerator[asyncpg.Connection, Any]:
    from app.core.database import Database

    database = Database(TEST_DATABASE_URL)
    await database.connect()
    async with database.pool.acquire() as conn:
        yield conn
    await database.close()


@pytest.fixture
async def redis_client() -> AsyncGenerator[Redis, Any]:
    from redis.asyncio import ConnectionPool

    pool = ConnectionPool.from_url(
        TEST_REDIS_URL, decode_responses=True, max_connections=10
    )
    redis = Redis(connection_pool=pool)
    await redis.ping()  # type: ignore
    yield redis
    await redis.aclose(close_connection_pool=True)


@pytest.fixture
async def client(
    db: asyncpg.Connection, redis_client: Redis
) -> AsyncGenerator[AsyncClient, Any]:
    from app.main import app
    from app.api.deps import get_db, get_redis_client

    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_redis_client] = lambda: redis_client
    try:
        async with AsyncClient(
            transport=ASGITransport(app), base_url="http://test"
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def clean_test_db(db: asyncpg.Connection) -> None:
    async with db.transaction():
        tables = await db.fetch("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name != 'schema_migrations'
        """)
        if tables:
            names = ", ".join([f'"{t["table_name"]}"' for t in tables])
            await db.execute(f"TRUNCATE {names} RESTART IDENTITY CASCADE;")


@pytest.fixture(scope="function")
async def auth_header(client: AsyncClient) -> dict[str, str]:
    username = "test_username"
    password = "test"

    response = await client.post(
        "/api/v1/signup", json={"username": username, "password": password}
    )
    assert response.status_code == 201

    response = await client.post(
        "/api/v1/login/access-token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    assert response.status_code == 200

    access_token = response.json()["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
async def test_user(db: asyncpg.Connection) -> User:
    user_id = uuid.uuid7()
    username = "test_username"
    hashed_password = "hashed_password"
    async with db.transaction():
        row = await db.fetchrow(
            "INSERT INTO users (id, username, hashed_password) VALUES ($1, $2, $3) RETURNING *",
            user_id,
            username,
            hashed_password,
        )
        user = User.from_row(row)
    return user


@pytest.fixture(scope="function")
async def test_player(db: asyncpg.Connection, test_user: User) -> User:
    username = "test_username"
    image_url = "https://example.com/image.png"
    async with db.transaction():
        row = await db.fetchrow(
            "INSERT INTO players (user_id, username, image_url) VALUES ($1, $2, $3) RETURNING *",
            str(test_user.id),
            username,
            image_url,
        )
        player = Player.from_row(row)
    return player


@pytest.fixture(scope="function")
async def test_game(db: asyncpg.Connection, test_player: Player) -> Game:
    id = uuid.uuid7()
    result = "x_won"
    duration = 2
    async with db.transaction():
        row = await db.fetchrow(
            "INSERT INTO games (id,result,duration) VALUES ($1,$2,$3) RETURNING *",
            str(id),
            result,
            duration,
        )
        query_game_players = """
        INSERT INTO game_players (game_id, player_id, side, type) VALUES ($1,$2,$3,$4),($5,$6,$7,$8)
        """
        game = Game.from_row(row)

        await db.fetchrow(
            query_game_players,
            str(game.id),
            str(test_player.user_id),
            "X",
            "human",
            str(game.id),
            str(test_player.user_id),
            "O",
            "human",
        )
    return game
