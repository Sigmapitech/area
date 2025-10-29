import datetime as dt
import logging
import xml.etree.ElementTree as ET
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...db.models.oauth import UserToken
from ...security.deps import get_current_user
from ..oauth_base import OAuthProvider

logger = logging.getLogger(__name__)


class Config(BaseModel):
    service: str = "caldav"
    client_id: str
    client_secret: str
    # Google OAuth 2.0 endpoints
    auth_base: str = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url: str = "https://oauth2.googleapis.com/token"
    # Google CalDAV base (v2)
    api_resource: str = "https://apidata.googleusercontent.com/caldav/v2"
    # We won't use provider.me for CalDAV; custom endpoints below
    profile_endpoint: str = "/user"
    redirect_uri: str = "http://127.0.0.1:8080/caldav/auth"
    scope: str = (
        "https://www.googleapis.com/auth/calendar.readonly openid email profile"
    )
    auth_extra: dict[str, str] = {
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    pkce: bool = True


router = APIRouter(prefix="/caldav", tags=["caldav"])

provider = OAuthProvider(package=__package__, config_model=Config)


async def _get_token(user_id: int, db: AsyncSession) -> UserToken:
    token = await db.scalar(
        select(UserToken).where(
            UserToken.user_id == user_id, UserToken.service == provider.cfg.service
        )
    )
    if not token:
        raise ValueError("CalDAV not connected for this user")
    return token


async def _get_user_email(access_token: str) -> Optional[str]:
    """Fetch primary email from Google's OpenID userinfo endpoint.
    Requires that OAuth scope includes: openid email.
    """
    userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(userinfo_url, headers=headers)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data.get("email")


@router.get("/connect")
async def caldav_connect(token: str = Query(...)):
    return await provider.connect(token)


@router.get("/auth")
async def caldav_auth(
    code: str,
    state: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await provider.auth(code, state, db)


@router.get("/refresh")
async def caldav_refresh(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await provider.refresh(user, db)


@router.get("/me")
async def caldav_me(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Lightweight health-check style endpoint to verify CalDAV is connected.
    Performs a PROPFIND on the principal URL and returns key links in JSON.
    """
    token = await _get_token(user.id, db)
    email = await _get_user_email(str(token.access_token))
    if not email:
        refreshed = await provider.refresh(user, db)
        email = await _get_user_email(refreshed["access_token"])
        if not email:
            return {"ok": False, "status": 400, "error": "failed to resolve user email"}
    url = f"{provider.cfg.resource_base}/{email}/user"
    body = (
        """
<?xml version="1.0" encoding="utf-8"?>
<propfind xmlns="DAV:" xmlns:cd="urn:ietf:params:xml:ns:caldav">
  <prop>
    <current-user-principal/>
    <cd:calendar-home-set/>
  </prop>
  </propfind>
        """
    ).strip()
    headers = {
        "Authorization": f"Bearer {str(token.access_token)}",
        "Depth": "0",
        "Content-Type": "application/xml; charset=utf-8",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.request("PROPFIND", url, headers=headers, content=body)
        # Try one refresh if unauthorized
        if resp.status_code == 401:
            refreshed = await provider.refresh(user, db)
            headers["Authorization"] = f"Bearer {refreshed['access_token']}"
            resp = await client.request("PROPFIND", url, headers=headers, content=body)

    ns = {"d": "DAV:", "cd": "urn:ietf:params:xml:ns:caldav"}
    try:
        root = ET.fromstring(resp.text)
        principal_href_el = root.find(".//d:current-user-principal/d:href", ns)
        homeset_href_el = root.find(".//cd:calendar-home-set/d:href", ns)
        return {
            "ok": resp.status_code < 300,
            "status": resp.status_code,
            "principal_href": principal_href_el.text if principal_href_el is not None else None,
            "calendar_home_set": homeset_href_el.text if homeset_href_el is not None else None,
        }
    except ET.ParseError:
        # Return raw if not XML (or on error)
        return {"ok": False, "status": resp.status_code, "raw": resp.text}


@router.get("/principal")
async def caldav_principal(
    user=Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    token = await _get_token(user.id, db)
    email = await _get_user_email(str(token.access_token))
    if not email:
        refreshed = await provider.refresh(user, db)
        email = await _get_user_email(refreshed["access_token"])
        if not email:
            return {"ok": False, "status": 400, "error": "failed to resolve user email"}
    url = f"{provider.cfg.resource_base}/{email}/user"
    body = (
        """
<?xml version="1.0" encoding="utf-8"?>
<propfind xmlns="DAV:" xmlns:cd="urn:ietf:params:xml:ns:caldav">
  <prop>
    <current-user-principal/>
    <cd:calendar-home-set/>
  </prop>
</propfind>
        """
    ).strip()
    headers = {
        "Authorization": f"Bearer {str(token.access_token)}",
        "Depth": "0",
        "Content-Type": "application/xml; charset=utf-8",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.request("PROPFIND", url, headers=headers, content=body)
    return Response(content=resp.text, media_type="application/xml", status_code=resp.status_code)


def _find_text(elem: ET.Element, path: str, ns: dict) -> Optional[str]:
    found = elem.find(path, ns)
    return found.text if found is not None else None


@router.get("/calendars")
async def caldav_calendars(
    user=Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    token = await _get_token(user.id, db)
    email = await _get_user_email(str(token.access_token))
    if not email:
        refreshed = await provider.refresh(user, db)
        email = await _get_user_email(refreshed["access_token"])
        if not email:
            return {"ok": False, "status": 400, "error": "failed to resolve user email"}
    # First resolve home-set for the authenticated user
    url = f"{provider.cfg.resource_base}/{email}/user"
    propfind = (
        """
<?xml version="1.0" encoding="utf-8"?>
<propfind xmlns="DAV:" xmlns:cd="urn:ietf:params:xml:ns:caldav">
  <prop>
    <cd:calendar-home-set/>
  </prop>
</propfind>
        """
    ).strip()
    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "Depth": "0",
        "Content-Type": "application/xml; charset=utf-8",
    }
    async with httpx.AsyncClient() as client:
        r1 = await client.request("PROPFIND", url, headers=headers, content=propfind)
        if r1.status_code >= 300:
            return Response(content=r1.text, media_type="application/xml", status_code=r1.status_code)
        ns = {"d": "DAV:", "cd": "urn:ietf:params:xml:ns:caldav"}
        root = ET.fromstring(r1.text)
        homeset_href = root.find(".//cd:calendar-home-set/d:href", ns)
        if homeset_href is None or not homeset_href.text:
            return {"error": "calendar-home-set not found"}
        home_url = homeset_href.text
        # List child collections at home
        headers["Depth"] = "1"
        propfind2 = (
            """
<?xml version="1.0" encoding="utf-8"?>
<propfind xmlns="DAV:">
  <prop>
    <displayname/>
    <resourcetype/>
  </prop>
</propfind>
            """
        ).strip()
        r2 = await client.request("PROPFIND", home_url, headers=headers, content=propfind2)
    if r2.status_code >= 300:
        return Response(content=r2.text, media_type="application/xml", status_code=r2.status_code)
    # Return raw XML for now; clients can extract calendar collection hrefs
    return Response(content=r2.text, media_type="application/xml")


@router.get("/events")
async def caldav_events(
    href: str = Query(..., description="Calendar collection URL to query"),
    start: Optional[str] = Query(None, description="UTC start, e.g., 2025-10-29T00:00:00Z"),
    end: Optional[str] = Query(None, description="UTC end, e.g., 2025-11-05T00:00:00Z"),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    token = await _get_token(user.id, db)
    # Convert times to CalDAV format YYYYMMDDTHHMMSSZ if provided
    def to_caldav(ts: Optional[str]) -> Optional[str]:
        if not ts:
            return None
        try:
            # parse RFC3339-ish
            dtv = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(dt.timezone.utc)
            return dtv.strftime("%Y%m%dT%H%M%SZ")
        except Exception:
            return None

    start_c = to_caldav(start)
    end_c = to_caldav(end)

    time_filter = ""
    if start_c or end_c:
        attrs = []
        if start_c:
            attrs.append(f"start=\"{start_c}\"")
        if end_c:
            attrs.append(f"end=\"{end_c}\"")
        time_filter = f"<time-range {' '.join(attrs)}/>"

    report = f"""
<?xml version="1.0" encoding="utf-8"?>
<calendar-query xmlns="urn:ietf:params:xml:ns:caldav" xmlns:D="DAV:">
  <D:prop>
    <D:getetag/>
    <calendar-data/>
  </D:prop>
  <filter>
    <comp-filter name="VCALENDAR">
      <comp-filter name="VEVENT">
        {time_filter}
      </comp-filter>
    </comp-filter>
  </filter>
</calendar-query>
    """.strip()

    headers = {
        "Authorization": f"Bearer {str(token.access_token)}",
        "Depth": "1",
        "Content-Type": "application/xml; charset=utf-8",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.request("REPORT", href, headers=headers, content=report)
    return Response(content=resp.text, media_type="application/xml", status_code=resp.status_code)
