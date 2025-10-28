import logging

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...security.deps import get_current_user
from ..oauth_base import OAuthProvider

logger = logging.getLogger(__name__)


class Config(BaseModel):
	service: str = "discord"
	client_id: str
	client_secret: str
	# Note: Discord's OAuth authorize/token endpoints are under /api/oauth2
	auth_base: str = "https://discord.com/api/oauth2"
	token_url: str = "https://discord.com/api/oauth2/token"
	api_base: str = "https://discord.com"
	api_resource: str = "https://discord.com/api"
	profile_endpoint: str = "/users/@me"
	redirect_uri: str = "http://127.0.0.1:8080/discord/auth"
	scope: str = "identify email"
	# Discord supports PKCE with S256
	pkce: bool = True


router = APIRouter(prefix="/discord", tags=["discord"])

provider = OAuthProvider(package=__package__, config_model=Config)


@router.get("/connect")
async def discord_connect(token: str = Query(...)):
	return await provider.connect(token)


@router.get("/auth")
async def discord_auth(
	code: str,
	state: str = Query(...),
	db: AsyncSession = Depends(get_session),
):
	return await provider.auth(code, state, db)


@router.get("/refresh")
async def discord_refresh(
	user=Depends(get_current_user),
	db: AsyncSession = Depends(get_session),
):
	return await provider.refresh(user, db)


@router.get("/me")
async def discord_me(
	user=Depends(get_current_user),
	db: AsyncSession = Depends(get_session),
):
	return await provider.me(user, db)

