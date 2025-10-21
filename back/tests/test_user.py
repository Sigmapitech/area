from http import HTTPStatus

import pytest

from app.db.crud.users import create_user
from app.security.jwt import decode_access_token, decode_refresh_token


def test_user_registration(client, override_db):
    new_user = {
        "name": "pytest_user",
        "email": "pytest_user@test.com",
        "password": "Pytest1234!",
    }
    resp = client.post("/auth/register/", json=new_user)
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.json()
    assert "access_token" in data
    resp = client.get(
        "/auth/me", headers={"authorization": f"Bearer {data['access_token']}"}
    )
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert data["email"] == new_user["email"]
    assert data["name"] == new_user["name"]
    assert data["id"] == 1

    resp = client.post("/auth/register/", json=new_user)
    assert resp.status_code == HTTPStatus.CONFLICT


@pytest.mark.asyncio
async def test_user_login(client, override_db):
    password = "Pytest1234!"
    registered_user = await create_user(
        db=override_db,
        email="pytest_user@test.com",
        name="pytest_user",
        password=password,
    )
    resp = client.post(
        "/auth/login/",
        json={
            "email": registered_user.email,
            "password": password,
        },
    )

    assert resp.status_code == HTTPStatus.OK
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_user_login_bad(client, override_db):
    password = "Pytest1234!"
    registered_user = await create_user(
        db=override_db,
        email="pytest_user@test.com",
        name="pytest_user",
        password=password,
    )
    resp = client.post(
        "/auth/login/",
        json={
            "email": registered_user.email,
            "password": password + "nope",
        },
    )

    assert resp.status_code != HTTPStatus.OK


def test_user_update(client, auth_header):
    resp = client.patch(
        "/auth/credentials",
        json={"name": "new name"},
        headers=auth_header,
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json().get("name") == "new name"
    assert resp.json().get("email") == "pytest_user@test.com"


def test_user_update_sensitive(client, auth_header):
    resp = client.patch(
        "/auth/credentials",
        json={
            "email": "new_email@test.com",
            "current_password": "Pytest1234!",
        },
        headers=auth_header,
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json().get("email") == "new_email@test.com"
    assert resp.json().get("name") == "Pytest User"
    resp = client.patch(
        "/auth/credentials",
        json={
            "password": "NewPassword123!",
            "current_password": "WrongPassword123!",
        },
        headers=auth_header,
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED




@pytest.mark.asyncio
async def test_refresh_token(client, override_db):
    password = "Pytest1234!"
    user = await create_user(
        db=override_db,
        email="refresh_user@test.com",
        name="refresh_user",
        password=password,
    )

    login_resp = client.post(
        "/auth/login/",
        json={"email": user.email, "password": password},
    )

    assert login_resp.status_code == HTTPStatus.OK
    tokens = login_resp.json()
    refresh_token = tokens.get("refresh_token")
    assert refresh_token is not None

    refresh_resp = client.post(
        "/auth/refresh/",
        headers={"authorization": f"Bearer {refresh_token}"}
    )
    assert refresh_resp.status_code == HTTPStatus.OK
    new_tokens = refresh_resp.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens

    access_payload = decode_access_token(new_tokens["access_token"])
    refresh_payload = decode_refresh_token(new_tokens["refresh_token"])

    assert access_payload.id == user.id
    assert refresh_payload.id == user.id

    invalid_resp = client.post(
        "/auth/refresh/",
        headers={"authorization": "Bearer invalidtoken"}
    )

    assert invalid_resp.status_code == HTTPStatus.UNAUTHORIZED
