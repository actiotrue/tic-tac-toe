import json

import asyncpg

from app.core.settings import settings


class Database:
    def __init__(self, db_url):
        self.db_url = db_url

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(self.db_url, init=self.__setup_connection)

    async def __setup_connection(self, conn: asyncpg.Connection) -> None:
        await conn.set_type_codec(
            "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )
        await conn.set_type_codec(
            "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )

    async def close(self) -> None:
        await self.pool.close()


database = Database(settings.DATABASE_URL)
