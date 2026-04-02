import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_players(client: AsyncClient):
    response = await client.get("/api/v1/players/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_current_player(client: AsyncClient, auth_header: dict[str, str]):
    response = await client.get("/api/v1/players/me", headers=auth_header)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "test_username"


@pytest.mark.asyncio
async def test_update_player(client: AsyncClient, auth_header: dict[str, str]):
    response = await client.patch(
        "/api/v1/players/me",
        headers=auth_header,
        json={"username": "John2"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "John2"


@pytest.mark.asyncio
async def test_update_player_error(client: AsyncClient, auth_header: dict[str, str]):
    create_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert create_response.status_code == 201

    update_response = await client.patch(
        "/api/v1/players/me",
        headers=auth_header,
        json={"username": "John"},
    )
    assert update_response.status_code == 409
    response_data = update_response.json()
    assert response_data["detail"] == "User with this username already exists"


@pytest.mark.asyncio
async def test_update_player_not_auth(client: AsyncClient):
    response = await client.patch(
        "/api/v1/players/me",
        json={"username": "John2"},
    )
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_player_recent_games(
    client: AsyncClient, auth_header: dict[str, str]
):
    response = await client.get("/api/v1/players/me/recent-games", headers=auth_header)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_player_rank(client: AsyncClient, auth_header: dict[str, str]):
    response = await client.get("/api/v1/players/me/rank", headers=auth_header)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["rank"] == 1


@pytest.mark.asyncio
async def test_get_player_rank_not_auth(client: AsyncClient):
    response = await client.get("/api/v1/players/me/rank")
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"
