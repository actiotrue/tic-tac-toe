import uuid

from asyncpg import Connection
import pytest
from redis import Redis
from app.models import Game, Player, PlayerType, User
from app.services.player import PlayerService
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.exceptions import EntityNotFound


@pytest.fixture(scope="function")
def player_service(db: Connection, redis_client: Redis) -> PlayerService:
    return PlayerService(db, redis_client)


@pytest.mark.asyncio
async def test_get_all_players(player_service: PlayerService):
    players = await player_service.get_all_players()

    assert len(players) == 0


@pytest.mark.asyncio
async def test_get_player_by_id(player_service: PlayerService):
    player_id = uuid.uuid7()
    player = await player_service.get_player_by_id(player_id)

    assert player is None


@pytest.mark.asyncio
async def test_get_player_by_username(player_service: PlayerService):
    player_username = "John"
    player = await player_service.get_player_by_username(player_username)

    assert player is None


@pytest.mark.asyncio
async def test_get_player_with_rank(player_service: PlayerService):
    player_id = uuid.uuid7()
    player = await player_service.get_player_with_rank(player_id)

    assert player is None


@pytest.mark.asyncio
async def test_get_create_player_with_rank(
    player_service: PlayerService, test_user: User
):
    created_player = await player_service.create_player(
        PlayerCreate(
            username="John",
            user_id=test_user.id,
            image_url="https://example.com/image.png",
        )
    )
    player = await player_service.get_player_with_rank(created_player.user_id)

    assert player.user_id == test_user.id
    assert player.username == "John"
    assert player.rating == 1000
    assert player.draws == 0
    assert player.losses == 0
    assert player.wins == 0
    assert player.created_at is not None
    assert player.updated_at is not None


@pytest.mark.asyncio
async def test_create_player(player_service: PlayerService, test_user: User):
    player = await player_service.create_player(
        PlayerCreate(
            username="John",
            user_id=test_user.id,
            image_url="https://example.com/image.png",
        )
    )

    assert player.user_id == test_user.id
    assert player.username == "John"
    assert player.rating == 1000
    assert player.draws == 0
    assert player.losses == 0
    assert player.wins == 0
    assert player.created_at is not None
    assert player.updated_at is not None


@pytest.mark.asyncio
async def test_get_create_player(player_service: PlayerService, test_user: User):
    created_player = await player_service.create_player(
        PlayerCreate(
            username="John",
            user_id=test_user.id,
            image_url="https://example.com/image.png",
        )
    )
    player = await player_service.get_player_by_id(created_player.user_id)

    assert player.user_id == test_user.id
    assert player.username == "John"
    assert player.rating == 1000
    assert player.draws == 0
    assert player.losses == 0
    assert player.wins == 0
    assert player.created_at is not None
    assert player.updated_at is not None


@pytest.mark.asyncio
async def test_update_player(player_service: PlayerService, test_user: User):
    created_player = await player_service.create_player(
        PlayerCreate(
            username="John",
            user_id=test_user.id,
            image_url="https://example.com/image.png",
        )
    )

    updated_player = await player_service.update_player(
        created_player.user_id, PlayerUpdate(username="John2")
    )

    assert updated_player.username == "John2"


@pytest.mark.asyncio
async def test_update_player_error(player_service: PlayerService):
    player_id = uuid.uuid7()

    with pytest.raises(EntityNotFound):
        await player_service.update_player(player_id, PlayerUpdate(username="John2"))


@pytest.mark.asyncio
async def test_get_leaderboard(player_service: PlayerService):
    leaderboard = await player_service.get_leaderboard()

    assert len(leaderboard) == 0


async def test_get_games_summary(
    player_service: PlayerService, test_player: Player, test_game: Game
):
    games = await player_service.get_games_summary_by_player_id(test_player.user_id)

    assert len(games) == 1
    assert games[0].id == test_game.id
    assert games[0].result == test_game.result
    assert games[0].duration == test_game.duration
    assert games[0].players[0].side == "X"
    assert games[0].players[0].type == PlayerType.HUMAN
    assert games[0].players[0].player_id == str(test_player.user_id)
    assert games[0].players[0].player.username == test_player.username
    assert games[0].players[0].player.image_url == test_player.image_url
    assert games[0].players[1].side == "O"
    assert games[0].players[1].type == PlayerType.HUMAN
    assert games[0].players[1].player.user_id == str(test_player.user_id)
    assert games[0].players[1].player.username == test_player.username
    assert games[0].players[1].player.image_url == test_player.image_url
