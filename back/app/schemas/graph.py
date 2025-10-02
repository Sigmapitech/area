from typing import Optional

from pydantic import BaseModel, ConfigDict


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
