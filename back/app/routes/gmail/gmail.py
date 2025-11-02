import base64
import json
import logging
import pathlib
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...db.models.oauth import OAuthToken
from ...security.deps import get_current_user
from ..oauth_base import OAuthProvider

logger = logging.getLogger(__name__)


class Config(BaseModel):
    service: str = "gmail"
    client_id: str
    client_secret: str
    # Google OAuth 2.0 endpoints
    auth_base: str = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url: str = "https://oauth2.googleapis.com/token"
    # Gmail API base and profile endpoint
    api_resource: str = "https://gmail.googleapis.com/gmail/v1/users"
    profile_endpoint: str = "/me/profile"
    # Redirect URI must be whitelisted in Google Cloud Console
    redirect_uri: str = "http://127.0.0.1:8080/gmail/auth"
    # Request read-only Gmail scope (plus openid/email for good measure)
    scope: str = (
        "https://www.googleapis.com/auth/gmail.readonly openid email profile"
    )
    # Ensure refresh token issuance
    auth_extra: dict[str, str] = {
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    # Enable PKCE for public clients
    pkce: bool = True


router = APIRouter(prefix="/gmail", tags=["gmail"])

provider = OAuthProvider(
    package=__package__,
    config_model=Config,
    icon=(pathlib.Path(__file__).parent / "icon.svg").read_text()
)


@router.get("/connect")
async def gmail_connect(token: str = Query(...), platform: str = Query(...)):
    return await provider.connect(token, platform)


@router.get("/auth")
async def gmail_auth(
    code: str,
    state: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await provider.auth(code, state, db)


@router.get("/refresh")
async def gmail_refresh(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.refresh(user, db)


@router.get("/me")
async def gmail_me(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.me(user, db)


def _b64url_decode(data: str) -> bytes:
    # Gmail returns base64url without padding
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


async def _get_gmail_token(
    user_id: int, db: AsyncSession
) -> Optional[OAuthToken]:
    return await db.scalar(
        select(OAuthToken).where(
            OAuthToken.owner_id == user_id, OAuthToken.service == "gmail"
        )
    )


@router.get("/last-email")
async def gmail_last_email(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    token = await _get_gmail_token(user.id, db)
    if not token:
        raise HTTPException(status_code=401, detail="Gmail not connected")

    headers = {"Authorization": f"Bearer {token.access_token}"}

    async with httpx.AsyncClient() as client:
        # Get most recent message from INBOX
        list_resp = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            params={"maxResults": 1, "labelIds": "INBOX"},
            headers=headers,
        )
        if list_resp.status_code != 200:
            raise HTTPException(
                status_code=list_resp.status_code,
                detail=f"Failed to list messages: {list_resp.text}",
            )
        items = list_resp.json().get("messages", [])
        if not items:
            return {"message": "No emails found"}

        msg_id = items[0]["id"]
        msg_resp = await client.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
            params={"format": "full"},
            headers=headers,
        )
        if msg_resp.status_code != 200:
            raise HTTPException(
                status_code=msg_resp.status_code,
                detail=f"Failed to fetch message: {msg_resp.text}",
            )
        msg = msg_resp.json()

    # Extract useful fields
    payload = msg.get("payload", {})
    headers_list = payload.get("headers", [])

    def _header(name: str) -> Optional[str]:
        for h in headers_list:
            if h.get("name", "").lower() == name.lower():
                return h.get("value")
        return None

    subject = _header("Subject")
    sender = _header("From")
    date = _header("Date")
    snippet = msg.get("snippet")

    # Try to get plain text body
    body_text: Optional[str] = None

    def _extract_text(part) -> Optional[str]:
        if not part:
            return None
        mime = part.get("mimeType")
        body = part.get("body", {})
        data = body.get("data")
        if mime == "text/plain" and data:
            try:
                return _b64url_decode(data).decode("utf-8", errors="replace")
            except Exception:
                return None
        # If multipart, recurse into parts
        for p in part.get("parts", []) or []:
            text = _extract_text(p)
            if text:
                return text
        return None

    body_text = _extract_text(payload)

    return {
        "id": msg.get("id"),
        "threadId": msg.get("threadId"),
        "subject": subject,
        "from": sender,
        "date": date,
        "snippet": snippet,
        "body_text": body_text,
    }


@router.post("/watch")
async def gmail_watch(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    token = await _get_gmail_token(user.id, db)
    if not token:
        raise HTTPException(status_code=401, detail="Gmail not connected")

    headers = {"Authorization": f"Bearer {token.access_token}"}
    body = {
        "topicName": "projects/area-476516/topics/gmail-notifications",
        "labelIds": ["INBOX"],  # optional: limit to inbox
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/watch",
            headers=headers,
            json=body,
        )
        if resp.status_code == 401:
            await provider.refresh(user=user, db=db)
            # update token after refresh
            headers = {"Authorization": f"Bearer {token.access_token}"}
            resp = await client.post(
                f"https://gmail.googleapis.com/gmail/v1/users/me/watch",
                headers=headers,
                json=body,
            )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Failed to start Gmail watch: {resp.text}",
        )

    data = resp.json()
    # Save the historyId somewhere (e.g., in DB)
    logger.info("Started Gmail watch: %s", data)
    return data


@router.post("/notifications")
async def gmail_notifications(request: Request):
    """
    Receives push notifications from Gmail via Pub/Sub.
    """
    envelope = await request.json()
    message = envelope.get("message")
    if not message:
        logger.warning("No Pub/Sub message in request")
        return {"status": "no message"}

    data_b64 = message.get("data")
    if not data_b64:
        logger.warning("Missing data in Pub/Sub message")
        return {"status": "no data"}

    decoded = base64.b64decode(data_b64).decode("utf-8")
    payload = json.loads(decoded)

    email = payload.get("emailAddress")
    history_id = payload.get("historyId")
    logger.info(f"Gmail change for {email} - historyId: {history_id}")
    logger.debug(f"Gmail notification payload: {payload}")

    # TODO: fetch new messages (see below)
    # await process_gmail_history(email, history_id)

    return {"status": "ok"}
