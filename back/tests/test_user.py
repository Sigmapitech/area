from http import HTTPStatus

import pytest

from app.db.crud.users import create_user


def test_user_registration(client, override_db):
    new_user = {
        "name": "pytest_user",
        "email": "pytest_user@test.com",
        "password": "Pytest1234!",
    }
    resp = client.post("/auth/register/", json=new_user)
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.json()
    assert "token" in data
    resp = client.get(
        "/auth/me", headers={"authorization": f"Bearer {data['token']}"}
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
    assert "token" in resp.json()


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
