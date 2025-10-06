from logging import getLogger

from fastapi import Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_session
from ..db.crud.users import create_user, get_by_email
from ..schemas.user import AuthResponse, LoginRequest, RegisterRequest
from ..security.jwt import create_access_token, decode_access_token

logger = getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, data: RegisterRequest) -> AuthResponse:
        existing_user = await get_by_email(self.db, data.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        user = await create_user(
            self.db, email=data.email, password=data.password, name=data.name
        )

        token = create_access_token(
            {"id": user.id, "email": user.email},
        )
        return AuthResponse(token=token)

    async def login_user(self, data: LoginRequest) -> AuthResponse:
        user = await get_by_email(self.db, data.email)
        if not user or not bcrypt.verify(data.password, str(user.auth)):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(
            {"id": user.id, "email": user.email},
        )
        return AuthResponse(token=token)

    def decode_token(self, token: str) -> dict:
        try:
            payload = decode_access_token(token)
            return payload
        except Exception as e:
            logger.warning("Invalid token: %s", e)
            raise HTTPException(
                status_code=401, detail="Invalid or expired token"
            )


async def get_auth_service(
    db: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(db)
