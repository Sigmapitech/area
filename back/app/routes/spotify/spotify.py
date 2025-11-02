import logging

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...security.deps import get_current_user
from ..oauth_base import OAuthProvider

logger = logging.getLogger(__name__)


class Config(BaseModel):
    service: str = "spotify"
    client_id: str
    client_secret: str
    redirect_uri: str = "http://127.0.0.1:8080/spotify/auth"
    api_base: str = "https://accounts.spotify.com"
    api_resource: str = "https://api.spotify.com/v1"
    auth_base: str = "https://accounts.spotify.com/authorize"
    scope: str = "user-read-email"
    pkce: bool = True


router = APIRouter(prefix="/spotify", tags=["spotify"])

provider = OAuthProvider(package=__package__, config_model=Config)


@router.get("/connect")
async def spotify_connect(token: str = Query(...), platform: str = Query(...)):
    return await provider.connect(token, platform)


@router.get("/auth")
async def spotify_auth(
    code: str,
    state: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await provider.auth(code, state, db)


@router.get("/refresh")
async def spotify_refresh(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.refresh(user, db)


@router.get("/me")
async def spotify_me(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.me(user, db)
