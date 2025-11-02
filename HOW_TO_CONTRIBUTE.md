Here’s a concise `HOW_TO_CONTRIBUTE.md` for adding a new OAuth service to your project based on the Discord example:

---

# How to Contribute a New OAuth Service

This guide explains how to add a new OAuth service to our platform using the existing Discord integration as a reference.

## 1. Create a Config Model

In your service module, create a `Config` Pydantic model that defines the OAuth configuration:

```python
from pydantic import BaseModel

class Config(BaseModel):
    service: str = "google"
    client_id: str
    client_secret: str
    auth_base: str = "..."
    token_url: str = "..."
    api_base: str = "..."
    api_resource: str = "..."
    profile_endpoint: str = "..."
    redirect_uri: str = "..."
    scope: str = "..."
    pkce: bool = True
```

* Set `service` to a unique identifier for the platform.
* Specify the authorization URL (`auth_base`), token URL (`token_url`), API endpoints, and scopes.
* `redirect_uri` should point to your API route for handling the callback.

## 2. Instantiate the OAuth Provider

Use the shared `OAuthProvider` class:

```python
from fastapi import APIRouter
import pathlib
from .oauth_base import OAuthProvider

router = APIRouter(prefix="/[my_service]", tags=["[my_service]"])

provider = OAuthProvider(
    package=__package__,
    config_model=Config,
    icon=(pathlib.Path(__file__).parent / "icon.svg").read_text()
)
```

* The `icon` will be displayed in the frontend service cards.

## 3. Add API Routes

Define FastAPI routes to handle connecting, authentication, token refresh, and user info:

```python
@router.get("/connect")
async def google_connect(token: str, platform: str):
    return await provider.connect(token, platform)

@router.get("/auth")
async def google_auth(code: str, state: str, db=Depends(get_session)):
    return await provider.auth(code, state, db)

@router.get("/refresh")
async def google_refresh(user=Depends(get_current_user), db=Depends(get_session)):
    return await provider.refresh(user, db)

@router.get("/me")
async def google_me(user=Depends(get_current_user), db=Depends(get_session)):
    return await provider.me(user, db)
```

* `/connect` initiates the OAuth connection.
* `/auth` handles the callback from the OAuth provider.
* `/refresh` refreshes the access token.
* `/me` retrieves the current user’s profile info from the service.

## 4. Add Service Icon

Place an SVG icon named `icon.svg` in the service module folder. This will be displayed in the frontend cards for connecting services.

## 5. Test

1. Login in to the area
2. Go to `/services`
3. You should see you newly added service and be able to connect to it
