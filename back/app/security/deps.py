from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..db.crud import users
from .jwt import decode_access_token


async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_session),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token isn't a bearer",
        )
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    assert payload["id"] is not None and isinstance(
        payload["id"], int
    ), "Token payload must contain 'id'"

    user = await users.get_by_id(db, payload["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
