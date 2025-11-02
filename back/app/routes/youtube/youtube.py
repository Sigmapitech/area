import logging
import pathlib

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...security.deps import get_current_user
from ..oauth_base import OAuthProvider

logger = logging.getLogger(__name__)


class Config(BaseModel):
    service: str = "youtube"
    client_id: str
    client_secret: str
    # Google OAuth 2.0 endpoints
    auth_base: str = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url: str = "https://oauth2.googleapis.com/token"
    # YouTube Data API base
    api_resource: str = "https://www.googleapis.com/youtube/v3"
    # Return channel of authenticated user
    profile_endpoint: str = "/channels?mine=true&part=snippet"
    redirect_uri: str = "http://127.0.0.1:8080/youtube/auth"
    scope: str = (
        "https://www.googleapis.com/auth/youtube.readonly openid email profile"
    )
    auth_extra: dict[str, str] = {
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    pkce: bool = True


router = APIRouter(prefix="/youtube", tags=["youtube"])

provider = OAuthProvider(
    package=__package__,
    config_model=Config,
    icon=(pathlib.Path(__file__).parent / "icon.svg").read_text()
)

@router.get("/connect")
async def youtube_connect(token: str = Query(...), platform: str = Query(...)):
    return await provider.connect(token, platform)


@router.get("/auth")
async def youtube_auth(
    code: str,
    state: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await provider.auth(code, state, db)


@router.get("/refresh")
async def youtube_refresh(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.refresh(user, db)


@router.get("/me")
async def youtube_me(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.me(user, db)
