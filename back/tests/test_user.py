def test_user_registration(client):
    new_user = {
        "name": "pytest_user",
        "email": "pytest_user@test.com",
        "password": "Pytest1234!",
    }
    resp = client.post("/api/auth/register/", json=new_user)
    assert resp.status_code == 201

    resp = client.post("/api/auth/register/", json=new_user)
    assert resp.status_code == 409


def test_user_login(client, registered_user):
    resp = client.post(
        "/api/auth/login/",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert resp.status_code == 200
    assert "token" in resp.json()
