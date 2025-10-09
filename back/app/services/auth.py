from logging import getLogger

from fastapi import Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_session
from ..db.crud.users import create_user, get_by_email, get_by_id, update_user
from ..schemas.user import (
    AccountUpdateRequest,
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserSchema,
)
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

    async def update_credentials(
        self, user, data: AccountUpdateRequest
    ) -> UserSchema:
        """
        Update the user's account credentials.
        Sensitive fields (email/password) require current password confirmation.
        """
        update_data = {}

        # If user wants to change email or password, verify current password
        if (data.email or data.password) and not data.current_password:
            raise HTTPException(
                status_code=401, detail="Current password required"
            )

        if data.current_password:
            if not bcrypt.verify(data.current_password, str(user.auth)):
                raise HTTPException(
                    status_code=401, detail="Invalid current password"
                )

        if data.password:
            update_data["password"] = data.password
        if data.email:
            update_data["email"] = data.email
        if data.name:
            update_data["name"] = data.name

        if not update_data:
            raise HTTPException(
                status_code=400, detail="No valid fields to update"
            )

        updated_user = await update_user(self.db, user, update_data)
        return updated_user


async def get_auth_service(
    db: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(db)
