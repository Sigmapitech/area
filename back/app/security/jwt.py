from datetime import datetime, timedelta, timezone
from typing import TypedDict

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from ..config import get_package_config


class Config(BaseModel):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 600


class TokenPayload(TypedDict):
    id: int
    email: str



class AccessTokenPayload(BaseModel):
    id: int
    email: str
    exp: datetime



settings = get_package_config(__package__, Config)


def create_access_token(
    data: TokenPayload, expires_minutes: int = settings.jwt_expires_minutes
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = AccessTokenPayload(exp=expire, **data)
    return jwt.encode(
        payload.model_dump(),
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )



def decode_access_token(token: str) -> AccessTokenPayload:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )

        return AccessTokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
