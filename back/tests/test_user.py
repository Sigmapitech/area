from http import HTTPStatus


def test_user_registration(client):
    new_user = {
        "name": "pytest_user",
        "email": "pytest_user@test.com",
        "password": "Pytest1234!",
    }
    resp = client.post("/api/auth/register/", json=new_user)
    assert resp.status_code == HTTPStatus.CREATED

    resp = client.post("/api/auth/register/", json=new_user)
    assert resp.status_code == HTTPStatus.CONFLICT


def test_user_login(client, registered_user):
    resp = client.post(
        "/api/auth/login/",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert resp.status_code == HTTPStatus.OK
    assert "token" in resp.json()


def test_user_update(client, auth_headers):
    resp = client.patch(
        "/api/auth/me", json={"email": "new@email.com"}, headers=auth_headers
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json().get("email") == "new@email.com"


def test_user_update_password(client, auth_headers):
    resp = client.post(
        "/api/auth/update-password",
        json={"new_password": "#plop123plop#"},
        headers=auth_headers,
    )

    assert resp.status_code == HTTPStatus.OK
