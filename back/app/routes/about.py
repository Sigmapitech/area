from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .oauth_base import OAuthProvider
import time

router = APIRouter(prefix="")


@router.get("/about.json")
async def about_json(request: Request):
    client = request.client
    client_ip = client.host if client else "unknown"
    services = OAuthProvider.services.keys()
    return JSONResponse(
        {
            "client": {
                "host": client_ip,
            },
            "server": {
                "current_time": int(time.time()),
                "services": [
                    {
                        "name": service_name,
                        "actions": [
                        ],
                        "reactions": [
                        ],
                    } for service_name in services
                ]
            },
        }
    )
