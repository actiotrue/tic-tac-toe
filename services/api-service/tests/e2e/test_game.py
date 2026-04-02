import uuid

from httpx import AsyncClient
import pytest

from app.models import Player


@pytest.mark.asyncio
async def test_get_all_games(client: AsyncClient):
    response = await client.get("/api/v1/games/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_game_by_id_error(client: AsyncClient):
    game_id = uuid.uuid7()
    response = await client.get(f"/api/v1/games/{game_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Game not found"


@pytest.mark.asyncio
async def test_get_create_game_by_id(client: AsyncClient, test_player: Player):
    game_id = uuid.uuid7()
    created_game_response = await client.post(
        "/api/v1/games/",
        json={
            "id": str(game_id),
            "result": "x_won",
            "duration": 10,
            "players": [
                {
                    "gameId": str(game_id),
                    "playerId": str(test_player.user_id),
                    "side": "X",
                    "type": "human",
                },
                {
                    "gameId": str(game_id),
                    "playerId": str(test_player.user_id),
                    "side": "O",
                    "type": "human",
                },
            ],
        },
    )
    assert created_game_response.status_code == 201

    response = await client.get(f"/api/v1/games/{game_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(game_id)
    assert response_data["result"] == "x_won"
    assert response_data["duration"] == 10
    assert len(response_data["players"]) == 0


@pytest.mark.asyncio
async def test_create_game(client: AsyncClient, test_player: Player):
    game_id = uuid.uuid7()
    response = await client.post(
        "/api/v1/games/",
        json={
            "id": str(game_id),
            "result": "x_won",
            "duration": 10,
            "players": [
                {
                    "gameId": str(game_id),
                    "playerId": str(test_player.user_id),
                    "side": "X",
                    "type": "human",
                },
                {
                    "gameId": str(game_id),
                    "playerId": str(test_player.user_id),
                    "side": "O",
                    "type": "human",
                },
            ],
        },
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == str(game_id)
    assert response_data["result"] == "x_won"
    assert response_data["duration"] == 10
    assert len(response_data["players"]) == 0
