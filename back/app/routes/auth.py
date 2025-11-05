from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_session
from ..db.crud import users
from ..schemas.user import (
    AccountUpdateRequest,
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserBase,
    UserSchema,
)
from ..security.deps import get_current_user
from ..services import auth

router = APIRouter(prefix="/auth", tags=["auth"])
logger = getLogger(__name__)


@router.post(
    "/register",
    response_model=AuthResponse,
    description="Register a new account",
    status_code=201,
    responses={
        201: {"model": AuthResponse, "description": "Account created"},
        409: {"description": "User already exists"},
    },
)
async def register_user(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_session),
):
    return await auth.register_user(data, db)


@router.post(
    "/login",
    response_model=AuthResponse,
    description="Login with account",
    responses={
        200: {"model": AuthResponse, "description": "Login successful"},
        401: {"description": "Invalid credentials"},
    },
)
async def login_user(
    data: LoginRequest,
    db: AsyncSession = Depends(get_session),
):
    return await auth.login_user(data, db)


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
    current_user=Depends(get_current_user),
) -> UserSchema:
    connected_services = {token.service: True for token in current_user.tokens}

    return UserSchema(
        **current_user.__dict__,
        services=connected_services,
    )


@router.patch(
    "/credentials",
    response_model=UserBase,
    description="Update current user",
    responses={
        200: {"model": UserBase, "description": "Current user data"},
        401: {"description": "Unauthorized"},
    },
)
async def update_me(
    user: AccountUpdateRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await auth.update_credentials(current_user, user, db)


@router.delete(
    "/delete",
    description="Delete current user account",
    responses={
        204: {"description": "Account deleted successfully"},
        401: {"description": "Unauthorized"},
    },
    status_code=204,
)
async def delete_me(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    await users.delete_user(db, current_user.id)
