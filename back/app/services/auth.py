from fastapi import Depends, HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_session
from ..db.crud import users
from ..schemas.user import (
    AccountUpdateRequest,
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserSchema,
)
from ..security.jwt import create_access_token


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)


async def register_user(
    data: RegisterRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    if await users.get_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    user = await users.create_user(
        db, email=data.email, password=data.password, name=data.name
    )
    return _create_auth_response(user)


async def login_user(
    data: LoginRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    user = await users.get_by_email(db, data.email)
    if not user or not bcrypt.verify(data.password, str(user.auth)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return _create_auth_response(user)


async def update_credentials(
    user, data: AccountUpdateRequest, db: AsyncSession = Depends(get_session)
) -> UserSchema:
    update_data = _validate_update_request(user, data)
    return await users.update_user(db, user, update_data)


def _create_auth_response(user) -> AuthResponse:
    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)


def _validate_update_request(user, data: AccountUpdateRequest) -> dict:
    update_data = {}
    if data.email:
        update_data["email"] = data.email
    if data.name:
        update_data["name"] = data.name
    if data.password:
        update_data["password"] = data.password

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    if "email" in update_data or "password" in update_data:
        if not data.current_password or not bcrypt.verify(
            data.current_password, str(user.auth)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid current password",
            )

    return update_data
