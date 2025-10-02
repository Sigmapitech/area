from typing import Optional

from pydantic import BaseModel, ConfigDict

from .user import AuthResponse, UserSchema


class SimpleMessage(BaseModel):
    message: str


class AuthResponse(BaseModel):
    token: str


class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    verified_email: bool = False


class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkflowRead(WorkflowBase):
    id: int
    # allow building from SQLAlchemy ORM objects without manual mapping
    model_config = ConfigDict(from_attributes=True)


__all__ = (
    "SimpleMessage",
    "AuthResponse",
    "UserSchema",
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowRead",
)
