from pydantic import BaseModel

from .user import AuthResponse, UserSchema


class SimpleMessage(BaseModel):
    message: str


__all__ = ("SimpleMessage", "UserSchema", "AuthResponse")
