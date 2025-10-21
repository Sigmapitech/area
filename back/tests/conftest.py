import asyncio
import os
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.base import Base, get_session
from app.db.crud.users import create_user
from app.main import app
from app.security.jwt import create_access_token


@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["AREA_CONFIG_PATH"] = "testing.toml"


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def override_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session_instance():
        async with async_session() as session:
            return session

    session = asyncio.run(get_session_instance())

    async def test_session():
        yield session

    asyncio.run(init_models())
    app.dependency_overrides[get_session] = test_session
    yield session
    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())


@pytest.fixture
def auth_header(override_db):
    registered_user = asyncio.run(
        create_user(
            db=override_db,
            email="pytest_user@test.com",
            name="Pytest User",
            password="Pytest1234!",
        )
    )

    token = create_access_token(
        user_id=cast(int, registered_user.id),
        user_email=cast(str, registered_user.email),
    )

    return {"Authorization": f"Bearer {token}"}
