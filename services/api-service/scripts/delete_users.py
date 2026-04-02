import asyncio
import os

from asyncpg import create_pool
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")


async def delete_users():
    try:
        async with create_pool(dsn=POSTGRES_URL, command_timeout=60) as pool:
            async with pool.acquire() as con:
                users_records = await con.fetch("""
                SELECT id FROM users;
                """)
                if not users_records:
                    print("No records found")
                    return
                ids = [record["id"] for record in users_records]
                await con.execute(
                    """
                DELETE FROM users WHERE id = ANY($1);
                """,
                    ids,
                )
                print("Users deleted successfully")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(delete_users())
