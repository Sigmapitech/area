from logging import getLogger

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..db.base import AsyncSession, get_session
from ..db.crud import users
from ..schemas.user import (
    AccountUpdateRequest,
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserSchema,
)
from ..security.deps import get_current_user
from ..services.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
logger = getLogger(__name__)


class VerificationRequest(BaseModel):
    code: int


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
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register_user(data)


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
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login_user(data)


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
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    return current_user


@router.patch(
    "/credentials",
    response_model=UserSchema,
    description="Update current user",
    responses={
        200: {"model": UserSchema, "description": "Current user data"},
        401: {"description": "Unauthorized"},
    },
)
async def update_me(
    user: AccountUpdateRequest,
    current_user=Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.update_credentials(current_user, user)
