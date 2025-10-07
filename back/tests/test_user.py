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
