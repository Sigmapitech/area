from typing import Optional

from pydantic import BaseModel, ConfigDict, JsonValue


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


class WorkflowNodeRead(BaseModel):
    id: int
    parent_id: Optional[int] = None
    node_type: str
    content: Optional[JsonValue] = None

    model_config = ConfigDict(from_attributes=True)


class WorkflowDetail(WorkflowRead):
    nodes: list[WorkflowNodeRead]
