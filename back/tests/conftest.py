import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["AREA_CONFIG_PATH"] = "testing.toml"


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
