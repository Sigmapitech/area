from pydantic import BaseModel

from .graph import (
    WorkflowCreate,
    WorkflowRead,
    WorkflowUpdate,
)
from .user import AuthResponse, UserSchema


class SimpleMessage(BaseModel):
    message: str


__all__ = (
    "SimpleMessage",
    "AuthResponse",
    "UserSchema",
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowRead",
)
