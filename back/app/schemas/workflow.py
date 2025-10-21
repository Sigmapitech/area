from __future__ import annotations

from typing import Dict, List, Optional, Tuple, TypeAlias, Union

from pydantic import BaseModel

# Consideration: The Value type can be a nested dictionary, a list of strings, or a string.
# Value: TypeAlias = Union[Dict[str, "Value"], List[str], str]


class WorkflowNodeConfigSchema(BaseModel):
    id: int
    node_id: int
    key: str
    value: str


class WorkflowNodeSchema(BaseModel):
    id: int
    workflow_id: int
    config: List[WorkflowNodeConfigSchema]

class WorkflowReadBaseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int

class WorkflowReadOneSchema(WorkflowReadBaseSchema):
    nodes: List[WorkflowNodeSchema]

class WorkflowReadManySchema(WorkflowReadBaseSchema):
    pass


class WorkflowCreateSchema(BaseModel):
    name: str
    description: Optional[str]


class WorkflowUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]


class WorkflowsNodeBaseSchema(BaseModel):
    pairs: Optional[List[Tuple[str, str]]]


class WorkflowNodeCreateSchema(WorkflowsNodeBaseSchema):
    pass


class WorkflowNodeUpdateSchema(WorkflowsNodeBaseSchema):
    pass


class WorkflowNodeConfigCreateSchema(BaseModel):
    key: str
    value: str


class WorkflowNodeConfigUpdateSchema(BaseModel):
    value: Optional[str]
