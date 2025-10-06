from datetime import datetime, timedelta, timezone
from logging import getLogger
from re import compile
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...config import get_package_config
from ...db import User, get_session
from ...schemas import AuthResponse, UserSchema

router = APIRouter(prefix="/auth", tags=["auth"])
logger = getLogger(__name__)

ACCESS_TOKEN_TIMEOUT = 60
ALGORITHM = "HS256"


class Config(BaseModel):
    jwt_secret: str


settings = get_package_config(__package__, Config)

PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=50,
        pattern=compile(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        ),
    ),
]


def decode_access_token(token: str):
    """
    Decodes a JWT access token and returns its payload.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        dict: The decoded payload from the JWT token.

    Raises:
        HTTPException: If the token has expired or is invalid.
    """
    try:
        payload = decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token with an expiration time.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The time duration after which the token will expire. Defaults to None.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_TIMEOUT)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_id_from_token(authorization: str | None = Header(None)) -> int:
    """
    Extracts the user ID from the JWT access token in the authorization header.

    Args:
        authorization (str): The authorization header containing the JWT token.

    Returns:
        int: The user ID extracted from the token.

    Raises:
        HTTPException: If the token is missing or invalid.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="No token, authorization denied"
        )

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    id = payload.get("id")
    if not id:
        raise HTTPException(status_code=401, detail="Token is not valid")
    return id


async def get_user_from_token(
    db: AsyncSession = Depends(get_session),
    authorization: str | None = Header(None),
) -> User:
    """
    Retrieves the user associated with the JWT access token in the authorization header.

    Args:
        db (AsyncSession): The database session to use for querying the user.
        authorization (str): The authorization header containing the JWT token.
    Returns:
        User: The user object associated with the token.
    Raises:
        HTTPException: If the user is not found or the token is invalid.
    """
    id = get_user_id_from_token(authorization)
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, detail="User not found")
    return user


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str


class VerificationRequest(BaseModel):
    code: int


@router.post(
    "/register/",
    response_model=AuthResponse,
    description="Register a new account",
    status_code=201,
    responses={
        201: {"model": AuthResponse, "description": "Account created"},
        409: {"description": "User already exists"},
    },
)
async def register(
    data: RegisterRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    result = await db.execute(select(User).filter(User.email == data.email))
    collected = result.scalars().all()
    if len(collected) > 0:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(
        auth=bcrypt.hash(data.password),
        email=data.email,
        name=data.name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)


@router.post(
    "/login/",
    response_model=AuthResponse,
    description="Login with account",
    responses={
        200: {"model": AuthResponse, "description": "Login successful"},
    },
)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()
    if not user or not bcrypt.verify(data.password, str(user.auth)):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)


@router.get(
    "/me",
    response_model=UserSchema,
    description="Get current user",
    responses={
        200: {"model": UserSchema, "description": "Current user data"},
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"},
    },
)
async def get_me(
    db: AsyncSession = Depends(get_session), authorization: str = Header(None)
) -> UserSchema:
    user = await get_user_from_token(db, authorization)
    return UserSchema.model_validate(user)
