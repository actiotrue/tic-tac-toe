import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_player_register(client: AsyncClient):
    response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User successfully signed up"


@pytest.mark.asyncio
async def test_player_login(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={"username": "John", "password": "password", "grant_type": "password"},
    )
    assert login_respone.status_code == 200
    respone_data = login_respone.json()
    print(respone_data)
    assert login_respone.cookies["refresh_token"]
    assert respone_data["accessToken"]
    assert respone_data["tokenType"] == "bearer"


@pytest.mark.asyncio
async def test_player_login_error(client: AsyncClient):
    response = await client.post(
        "/api/v1/login/access-token",
        data={
            "username": "unknown_username",
            "password": "password",
            "grant_type": "password",
        },
    )
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_player_login_wrong_password(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={
            "username": "John",
            "password": "wrong_password",
            "grant_type": "password",
        },
    )
    assert login_respone.status_code == 400
    response_data = login_respone.json()
    assert response_data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_player_login_wrong_username(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={
            "username": "wrong_username",
            "password": "password",
            "grant_type": "password",
        },
    )
    assert login_respone.status_code == 400
    response_data = login_respone.json()
    assert response_data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_player_change_password(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={"username": "John", "password": "password", "grant_type": "password"},
    )
    assert login_respone.status_code == 200
    respone_data = login_respone.json()
    access_token = respone_data["accessToken"]
    assert respone_data["tokenType"] == "bearer"

    me_response = await client.patch(
        "/api/v1/change-password",
        json={"current_password": "password", "new_password": "new_password"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    response_data = me_response.json()
    assert response_data["message"] == "Password successfully changed"


@pytest.mark.asyncio
async def test_player_change_password_error(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={"username": "John", "password": "password", "grant_type": "password"},
    )
    assert login_respone.status_code == 200
    respone_data = login_respone.json()
    access_token = respone_data["accessToken"]
    assert respone_data["tokenType"] == "bearer"

    change_response = await client.patch(
        "/api/v1/change-password",
        json={"current_password": "wrong_password", "new_password": "new_password"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert change_response.status_code == 400
    response_data = change_response.json()
    assert response_data["detail"] == "Incorrect password"


@pytest.mark.asyncio
async def test_player_change_password_wrong_password(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/signup",
        json={
            "username": "John",
            "password": "password",
        },
    )
    assert register_response.status_code == 201

    login_respone = await client.post(
        "/api/v1/login/access-token",
        data={"username": "John", "password": "password", "grant_type": "password"},
    )
    assert login_respone.status_code == 200
    respone_data = login_respone.json()
    access_token = respone_data["accessToken"]
    assert respone_data["tokenType"] == "bearer"

    change_response = await client.patch(
        "/api/v1/change-password",
        json={"current_password": "password", "new_password": "password"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert change_response.status_code == 400
    response_data = change_response.json()
    assert (
        response_data["detail"]
        == "New password cannot be the same as the current password"
    )
