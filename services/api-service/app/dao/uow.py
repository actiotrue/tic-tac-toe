from typing import Self

from asyncpg import Connection
from redis import Redis

from app.dao.redis.leaderboard import LeaderboardDao
from app.dao.postgres.game import GameDao
from app.dao.postgres.player import PlayerDao
from app.dao.postgres.user import UserDao


class UnitOfWork:
    def __init__(self, sql_connection: Connection, redis_client: Redis):
        self.sql_conn = sql_connection
        self.users = UserDao(self.sql_conn)
        self.players = PlayerDao(self.sql_conn)
        self.games = GameDao(self.sql_conn)

        self.redis = redis_client
        self.leaderboard = LeaderboardDao(self.redis)

    async def __aenter__(self) -> Self:
        self._transaction = self.sql_conn.transaction()
        await self._transaction.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        self._transaction = None

    async def commit(self) -> None:
        await self._transaction.commit()

    async def rollback(self) -> None:
        await self._transaction.rollback()
