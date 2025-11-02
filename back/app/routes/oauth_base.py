import base64
import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Mapping
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_package_config
from ..db.crud import users
from ..db.models.oauth import UserToken
from ..db.models.user import User
from ..security.jwt import decode_access_token


@dataclass
class OAuthConfig:
    service: str
    client_id: str
    client_secret: str
    redirect_uri: str
    auth_base: str
    token_url: str
    resource_base: str
    scope: str | None = None
    profile_endpoint: str = "me"
    # Optional extra authorize parameters specific to a provider
    auth_extra: Mapping[str, str] | None = None
    # PKCE support (recommended for public clients like mobile)
    pkce: bool = True
    code_challenge_method: str = "S256"


class OAuthProvider:
    """Generic OAuth 2.0 Authorization Code provider helper."""

    def __init__(self, package: str | None, config_model: Any):
        # Load provider-specific config from config.toml based on package path
        assert package is not None, "Package name must be provided"
        settings = get_package_config(package, config_model)
        # Normalize into OAuthConfig
        token_url = (
            getattr(settings, "token_url", None)
            or f"{settings.api_base}/api/token"
        )
        resource_base = getattr(settings, "api_resource", "")
        scope = getattr(settings, "scope", None)
        auth_extra = getattr(settings, "auth_extra", None)

        self.cfg = OAuthConfig(
            service=getattr(settings, "service", package.split(".")[-1]),
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            redirect_uri=settings.redirect_uri,
            auth_base=getattr(settings, "auth_base", None)
            or settings.api_base,
            token_url=token_url,
            resource_base=resource_base,
            scope=scope,
            profile_endpoint=getattr(settings, "profile_endpoint", "/me"),
            auth_extra=auth_extra,
        )
        # in-memory state -> { token, code_verifier }
        self._state_store = {}

    # ---- Shared endpoints implementations ----

    async def connect(self, token: str, platform: str):
        print(platform)

        state = str(uuid.uuid4())
        # Prepare PKCE if enabled
        code_verifier = None
        pkce_params: dict[str, str] = {}

        if self.cfg.pkce:
            # Generate a high-entropy code_verifier (64 chars)
            code_verifier = secrets.token_urlsafe(64)[:128]
            digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
            code_challenge = (
                base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
            )
            pkce_params = {
                "code_challenge": code_challenge,
                "code_challenge_method": self.cfg.code_challenge_method,
            }

        self._state_store[state] = {
            "token": token,
            "code_verifier": code_verifier,
            "platform": platform,
        }

        params: dict[str, str] = {
            "client_id": self.cfg.client_id,
            "response_type": "code",
            "redirect_uri": self.cfg.redirect_uri,
            "state": state,
        }
        if self.cfg.scope:
            params["scope"] = self.cfg.scope
        if self.cfg.auth_extra:
            params.update(dict(self.cfg.auth_extra))
        if pkce_params:
            params.update(pkce_params)

        url = f"{self.cfg.auth_base}?{urlencode(params)}"
        return RedirectResponse(url)

    async def auth(self, code: str, state: str, db: AsyncSession):
        state_payload = self._state_store.pop(state, None)
        if state_payload is None:
            raise HTTPException(
                status_code=401, detail="No token provided or invalid state"
            )
        jwt_token = state_payload.get("token")
        code_verifier = state_payload.get("code_verifier")

        if not jwt_token:
            raise HTTPException(
                status_code=401, detail="Missing bearer token in state"
            )

        payload = decode_access_token(jwt_token)
        user = await users.get_by_id(db, payload.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.cfg.redirect_uri,
                "client_id": self.cfg.client_id,
                "client_secret": self.cfg.client_secret,
            }
            # For PKCE, include verifier and omit client_secret
            if self.cfg.pkce and code_verifier:
                data["code_verifier"] = code_verifier
            else:
                # Confidential client flow (server-side web) may include secret
                data["client_secret"] = self.cfg.client_secret
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = await client.post(
                self.cfg.token_url, data=data, headers=headers
            )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to authenticate: {resp.text}",
            )

        tokens = resp.json()

        token = UserToken(
            user_id=user.id,
            service=self.cfg.service,
            access_token=tokens.get("access_token"),
            refresh_token=tokens.get("refresh_token"),
            scope=self.cfg.scope,
            expires_at=datetime.now()
            + timedelta(seconds=tokens.get("expires_in", 0)),
        )
        db.add(token)
        await db.commit()
        await db.refresh(token)

        if state_payload["platform"] == "mobile":
            # just assume it works
            # because deep links dont works
            return HTMLResponse(content="<script>window.close()</script>")

        return HTMLResponse(
            content=f"""
            <script>
              window.opener.postMessage(
                {{
                  type: '{self.cfg.service.upper()}_CONNECTED',
                  payload: {{ userId: {user.id} }}
                }},
                "*"
              );
              window.close();
            </script>
            <p>{self.cfg.service.title()} linked successfully. You can close this window.</p>
            """
        )

    async def refresh(self, user: User, db: AsyncSession):
        token = await db.scalar(
            select(UserToken).where(
                UserToken.user_id == user.id,
                UserToken.service == self.cfg.service,
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
                "client_id": self.cfg.client_id,
            }
            # For PKCE-based public clients (e.g., mobile), omit client_secret on refresh
            # if not self.cfg.pkce:
            data["client_secret"] = self.cfg.client_secret
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = await client.post(
                self.cfg.token_url, data=data, headers=headers
            )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to refresh token: {resp.text}",
            )

        tokens = resp.json()
        setattr(token, "access_token", tokens.get("access_token"))
        if "refresh_token" in tokens:
            setattr(token, "refresh_token", tokens.get("refresh_token"))
        setattr(
            token,
            "expires_at",
            datetime.now() + timedelta(seconds=tokens.get("expires_in", 0)),
        )

        db.add(token)
        await db.commit()
        await db.refresh(token)

        return {
            "access_token": token.access_token,
            "expires_at": token.expires_at,
        }

    async def me(self, user: User, db: AsyncSession):
        token = await db.scalar(
            select(UserToken).where(
                UserToken.user_id == user.id,
                UserToken.service == self.cfg.service,
            )
        )
        if not token:
            raise HTTPException(
                status_code=401,
                detail=f"{self.cfg.service.title()} not connected",
            )

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token.access_token}"}
            resp = await client.get(
                f"{self.cfg.resource_base}{self.cfg.profile_endpoint}",
                headers=headers,
            )
            if resp.status_code == 401:
                await self.refresh(user=user, db=db)
                headers = {"Authorization": f"Bearer {token.access_token}"}
                resp = await client.get(
                    f"{self.cfg.resource_base}/{self.cfg.profile_endpoint}",
                    headers=headers,
                )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to fetch profile: {resp.text}",
            )

        return resp.json()
