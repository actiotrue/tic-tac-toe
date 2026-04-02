import uuid

from loguru import logger

from app.dao.postgres.base import SqlDaoBase
from app.exceptions import EntityNotFound
from app.models import User


class UserDao(SqlDaoBase):
    """UserDao for crud operations on users"""

    async def create(
        self, user_id: uuid.UUID, username: str, hashed_password: str
    ) -> User:
        query = """INSERT INTO users (id, username, hashed_password) VALUES ($1, $2, $3) RETURNING *"""
        row = await self.db.fetchrow(query, user_id, username, hashed_password)
        user = User.from_row(row)
        logger.info(f"Created user ID: {user.id} Username: {user.username}")
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        query = """SELECT * FROM users WHERE id = $1"""
        row = await self.db.fetchrow(query, user_id)
        if row is None:
            return None
        user = User.from_row(row)
        logger.info(f"Found user ID: {user.id} Username: {user.username}")
        return user

    async def get_by_username(self, username: str) -> User | None:
        query = """SELECT * FROM users WHERE username = $1"""
        row = await self.db.fetchrow(query, username)
        if row is None:
            return None
        user = User.from_row(row)
        logger.info(f"Found user ID: {user.id} Username: {user.username}")
        return user

    async def update_username(self, user_id: uuid.UUID, username: str) -> User:
        query = """UPDATE users SET username = $1 WHERE id = $2 RETURNING *"""
        row = await self.db.fetchrow(query, username, user_id)
        if row is None:
            raise EntityNotFound("User", user_id)
        user = User.from_row(row)
        return user

    async def update_hashed_password(
        self, user_id: uuid.UUID, hashed_password: str
    ) -> User:
        row = await self.db.fetchrow(
            "UPDATE users SET hashed_password = $1 WHERE id = $2 RETURNING *",
            hashed_password,
            user_id,
        )
        if row is None:
            raise EntityNotFound("User", user_id)
        user = User.from_row(row)
        return user
