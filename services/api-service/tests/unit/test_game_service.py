import uuid

import pytest

from app.models import GameResult, Player, PlayerType
from app.schemas.game import GameCreate, GamePlayerCreate
from app.services.game import GameService


@pytest.fixture(scope="function")
def game_service(db, redis_client):
    return GameService(db, redis_client)


@pytest.mark.asyncio
async def test_get_all_games(game_service: GameService):
    games = await game_service.get_all_games()

    assert len(games) == 0


@pytest.mark.asyncio
async def test_get_game_by_id(game_service: GameService):
    game_id = uuid.uuid7()
    game = await game_service.get_game_by_id(game_id)

    assert game is None


@pytest.mark.asyncio
async def test_get_create_game_by_id(game_service: GameService, test_player: Player):
    game_id = uuid.uuid7()
    created_game = await game_service.create_game(
        GameCreate(
            id=game_id,
            result=GameResult.X_WIN,
            duration=10,
            players=[
                GamePlayerCreate(
                    game_id=game_id,
                    player_id=test_player.user_id,
                    side="X",
                    type=PlayerType.HUMAN,
                ),
                GamePlayerCreate(
                    game_id=game_id,
                    player_id=test_player.user_id,
                    side="O",
                    type=PlayerType.HUMAN,
                ),
            ],
        )
    )
    game = await game_service.get_game_by_id(created_game.id)

    assert game.id == created_game.id
    assert game.result == created_game.result
    assert game.duration == created_game.duration
    assert game.created_at is not None
    assert len(game.players) == 0


@pytest.mark.asyncio
async def test_create_game(game_service: GameService, test_player: Player):
    game_id = uuid.uuid7()
    game_in = GameCreate(
        id=uuid.uuid7(),
        result=GameResult.X_WIN,
        duration=10,
        players=[
            GamePlayerCreate(
                game_id=game_id,
                player_id=test_player.user_id,
                side="X",
                type=PlayerType.HUMAN,
            ),
            GamePlayerCreate(
                game_id=game_id,
                player_id=test_player.user_id,
                side="O",
                type=PlayerType.HUMAN,
            ),
        ],
    )

    game = await game_service.create_game(game_in)

    assert game.id == game_in.id
    assert game.result == game_in.result
    assert game.duration == game_in.duration
    assert game.created_at is not None
    assert len(game.players) == 0
