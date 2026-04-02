import uuid

from asyncpg import Connection
import pytest
from redis import Redis
from app.services.user import UserService
from app.schemas.user import UserCreate
from app.exceptions import EntityNotFound


@pytest.fixture(scope="function")
def user_service(db: Connection, redis_client: Redis) -> UserService:
    return UserService(db, redis_client)


@pytest.mark.asyncio
async def test_get_user_by_id(user_service: UserService):
    user_id = uuid.uuid7()
    user = await user_service.get_user_by_id(user_id)

    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_username(user_service: UserService):
    user_username = "John"
    user = await user_service.get_user_by_username(user_username)

    assert user is None


@pytest.mark.asyncio
async def test_create_user(user_service: UserService):
    user = await user_service.create_user(
        UserCreate(username="John", password="password")
    )

    assert user.username == "John"
    assert user.hashed_password is not None
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_get_create_user(user_service: UserService):
    created_user = await user_service.create_user(
        UserCreate(username="John", password="password")
    )
    user = await user_service.get_user_by_id(created_user.id)

    assert user.username == "John"
    assert user.hashed_password is not None
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_update_user_password(user_service: UserService):
    created_user = await user_service.create_user(
        UserCreate(username="John", password="password")
    )
    updated_user = await user_service.update_user_password(
        created_user.id, "new_password"
    )

    assert updated_user.username == created_user.username
    assert updated_user.id == created_user.id
    assert updated_user.created_at == created_user.created_at
    assert updated_user.updated_at is not None
    assert updated_user.hashed_password is not None


@pytest.mark.asyncio
async def test_update_user_password_error(user_service: UserService):
    user_id = uuid.uuid7()

    with pytest.raises(EntityNotFound):
        await user_service.update_user_password(user_id, "new_password")


@pytest.mark.asyncio
async def test_authenticate_user(user_service: UserService):
    user = await user_service.create_user(
        UserCreate(username="John", password="password")
    )
    authenticated_user = await user_service.authenticate_user("John", "password")

    assert authenticated_user.username == user.username
    assert authenticated_user.hashed_password == user.hashed_password
    assert authenticated_user.id == user.id
    assert authenticated_user.created_at == user.created_at
    assert authenticated_user.updated_at == user.updated_at


@pytest.mark.asyncio
async def test_authenticate_user_error(user_service: UserService):
    authenticated_user = await user_service.authenticate_user("John", "password")

    assert authenticated_user is None
