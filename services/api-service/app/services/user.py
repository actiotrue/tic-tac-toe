import uuid

from asyncpg import Connection
from redis import Redis

from app.core.security import settings, get_password_hash, verify_password
from app.dao.uow import UnitOfWork
from app.models import User
from app.schemas.player import PlayerCreate
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, connection: Connection, redis_client: Redis):
        self.uow = UnitOfWork(connection, redis_client)

    async def create_user(self, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        user_id = uuid.uuid7()
        async with self.uow as uow:
            user = await uow.users.create(user_id, user_in.username, hashed_password)
            image_url = settings.CLOUDINARY_BASE_IMAGE_PUBLIC_ID
            new_player = PlayerCreate(
                user_id=user_id, username=user_in.username, image_url=image_url
            )
            await uow.players.create(new_player)
            await uow.leaderboard.create(user_id)
            return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.uow as uow:
            return await uow.users.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.uow as uow:
            return await uow.users.get_by_username(username)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.get_user_by_username(username)
        if not user:
            verify_password(password, settings.DUMMY_HASH)
            return None
        verifed, updated_password_hash = verify_password(password, user.hashed_password)
        if not verifed:
            return None
        if updated_password_hash:
            async with self.uow as uow:
                await uow.users.update_hashed_password(user.id, updated_password_hash)
        return user

    async def update_user_password(self, user_id: int, password: str) -> User:
        hashed_password = get_password_hash(password)
        async with self.uow as uow:
            return await uow.users.update_hashed_password(user_id, hashed_password)
