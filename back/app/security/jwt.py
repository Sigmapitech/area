from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Type, TypedDict, TypeVar

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from ..config import get_package_config


class Config(BaseModel):
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    access_token_minutes: int = 60
    refresh_token_days: int = 60


settings = get_package_config(__package__, Config)


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AccessTokenPayload(BaseModel):
    id: int
    email: str
    exp: datetime
    type: TokenType = TokenType.ACCESS


class RefreshTokenPayload(BaseModel):
    id: int
    exp: datetime
    type: TokenType = TokenType.REFRESH


class TokenPayload(TypedDict):
    id: int
    email: str


def create_access_token(user_id: int, user_email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_minutes
    )
    payload = AccessTokenPayload(id=user_id, email=user_email, exp=expire)
    return jwt.encode(
        payload.model_dump(),
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_days
    )
    payload = RefreshTokenPayload(id=user_id, exp=expire)
    return jwt.encode(
        payload.model_dump(),
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


T = TypeVar("T")


def _decode_token(token: str, model: Type[T]) -> T:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return model(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid"
        )


def decode_access_token(token: str) -> AccessTokenPayload:
    return _decode_token(token, AccessTokenPayload)


def decode_refresh_token(token: str) -> RefreshTokenPayload:
    return _decode_token(token, RefreshTokenPayload)
