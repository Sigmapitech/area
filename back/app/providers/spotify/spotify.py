import uuid
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import get_package_config
from ...db import get_session
from ...db.models.oauth import UserToken
from ...db.models.user import User
from ...security.deps import get_current_user

router = APIRouter(prefix="/spotify", tags=["spotify"])

SPOTIFY_SCOPE = "user-read-email"
token_store = {}


class Config(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str = "http://127.0.0.1:8000/provider/spotify/auth"
    api_base: str = "https://accounts.spotify.com"
    api_resource: str = "https://api.spotify.com/v1"


settings = get_package_config(__package__, Config)


@router.get("/connect")
async def spotify_connect(token: str = Query(...)):
    state = str(uuid.uuid4())
    token_store[state] = token

    url = (
        f"{settings.api_base}/authorize"
        f"?client_id={settings.client_id}"
        f"&response_type=code"
        f"&redirect_uri={settings.redirect_uri}"
        f"&scope={SPOTIFY_SCOPE}"
        f"&state={state}"
    )

    return RedirectResponse(url)


@router.get("/auth")
async def spotify_auth(
    code: str,
    state: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    jwt_token = token_store.pop(state, None)
    if jwt_token is None:
        raise HTTPException(
            status_code=401, detail="No token provided or invalid state"
        )

    user = await get_current_user(f"Bearer {jwt_token}", db)

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.redirect_uri,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = await client.post(
            f"{settings.api_base}/api/token", data=data, headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Failed to authenticate with Spotify: {resp.text}",
        )

    tokens = resp.json()
    print(f"[Spotify] Tokens for user {user.id}: {tokens}")

    token = UserToken(
        user_id=user.id,
        service="spotify",
        access_token=tokens.get("access_token"),
        refresh_token=tokens.get("refresh_token"),
        expires_at=datetime.now()
        + timedelta(seconds=tokens.get("expires_in", 0)),
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)

    return HTMLResponse(
        content=f"""
        <script>
          window.opener.postMessage(
            {{
              type: 'SPOTIFY_CONNECTED',
              payload: {{ userId: {user.id} }}
            }},
            "*"
          );
          window.close();
        </script>
        <p>Spotify linked successfully. You can close this window.</p>
        """
    )


@router.get("/refresh")
async def spotify_refresh(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Refresh the Spotify access token using the stored refresh token.
    """
    token = await db.scalar(
        select(UserToken).where(
            UserToken.user_id == user.id, UserToken.service == "spotify"
        )
    )
    if not token:
        raise HTTPException(
            status_code=401, detail="No refresh token available"
        )

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = await client.post(
            f"{settings.api_base}/api/token", data=data, headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Failed to refresh Spotify token: {resp.text}",
        )

    tokens = resp.json()
    print(f"[Spotify] Refreshed tokens for user {user.id}: {tokens}")

    setattr(token, "access_token", tokens.get("access_token"))
    if "refresh_token" in tokens:  # Spotify may or may not return it
        setattr(token, "refresh_token", tokens.get("refresh_token"))
    setattr(
        token,
        "expires_at",
        datetime.now() + timedelta(seconds=tokens.get("expires_in", 0)),
    )

    db.add(token)
    await db.commit()
    await db.refresh(token)

    return {"access_token": token.access_token, "expires_at": token.expires_at}


@router.get("/me")
async def spotify_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Fetch current user's Spotify profile. Auto-refresh token if expired.
    """
    print(await db.scalars(select(UserToken)))
    token = await db.scalar(
        select(UserToken).where(
            UserToken.user_id == user.id, UserToken.service == "spotify"
        )
    )
    if not token:
        raise HTTPException(status_code=401, detail="Spotify not connected")

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token.access_token}"}
        resp = await client.get(f"{settings.api_resource}/me", headers=headers)

        # If access token expired, try refresh
        if resp.status_code == 401:
            await spotify_refresh(user=user, db=db)
            headers = {"Authorization": f"Bearer {token.access_token}"}
            resp = await client.get(
                f"{settings.api_resource}/me", headers=headers
            )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Failed to fetch Spotify profile: {resp.text}",
        )

    return resp.json()
