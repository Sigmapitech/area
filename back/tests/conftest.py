import os
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from app.main import app

USER = {
    "name": "test",
    "email": "test@test.com",
    "password": "Test1234!",
}


@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["AREA_CONFIG_PATH"] = "testing.toml"


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def registered_user(client):
    resp = client.post("/api/auth/register/", json=USER)
    assert resp.status_code == HTTPStatus.CREATED
    return USER


@pytest.fixture(scope="session")
def auth_headers(client, registered_user):
    resp = client.post(
        "/api/auth/login/",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert resp.status_code == HTTPStatus.OK
    token = resp.json().get("token")
    assert token
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def workflow(client, auth_headers):
    """Create a fresh workflow for a test."""
    wf_payload = {"name": "My graph", "description": "Demo workflow"}
    resp = client.post("/api/workflow", json=wf_payload, headers=auth_headers)
    assert resp.status_code == HTTPStatus.CREATED
    return resp.json()
