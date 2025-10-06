from pydantic import BaseModel

from .graph import (
    NodeCreate,
    NodeRead,
    NodeUpdate,
    WorkflowCreate,
    WorkflowDetail,
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
    "WorkflowDetail",
    "NodeRead",
    "NodeCreate",
    "NodeUpdate",
)
