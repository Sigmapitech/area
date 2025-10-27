from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..db.crud import workflow
from ..schemas.workflow import (
    WorkflowCreateSchema,
    WorkflowNodeCreateSchema,
    WorkflowNodeSchema,
    WorkflowNodeUpdateSchema,
    WorkflowReadManySchema,
    WorkflowReadOneSchema,
    WorkflowUpdateSchema,
)
from ..security.deps import get_current_user

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.get(
    "/{workflow_id}",
    response_model=WorkflowReadOneSchema,
    description="Get a workflow by its ID",
    responses={
        404: {"description": "Workflow not found"},
        200: {"description": "Workflow retrieved successfully"},
    },
)
async def get_workflow(
    workflow_id: int, db: AsyncSession = Depends(get_session)
):
    graph = await workflow.get_by_id(db, workflow_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return graph


@router.get(
    "/",
    response_model=list[WorkflowReadManySchema],
    description="Get all workflows",
    responses={
        200: {"description": "Workflows retrieved successfully"},
    },
)
async def get_workflows(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
):
    return await workflow.list_workflows(db, user.id, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=WorkflowReadOneSchema,
    description="Create a new workflow",
    responses={
        201: {"description": "Workflow created successfully"},
    },
)
async def create_workflow(
    data: WorkflowCreateSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    return await workflow.create_workflow(
        db, name=data.name, description=data.description, owner_id=user.id
    )


@router.patch(
    "/{workflow_id}",
    response_model=WorkflowReadOneSchema,
    description="Update an existing workflow",
    responses={
        200: {"description": "Workflow updated successfully"},
        404: {"description": "Workflow not found"},
    },
)
async def update_workflow(
    workflow_id: int,
    data: WorkflowUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    wf = await workflow.get_by_id(db, workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await workflow.update_workflow(
        db,
        workflow_id,
        name=data.name,
        description=data.description,
    )


@router.delete(
    "/{workflow_id}",
    description="Delete a workflow by its ID",
    responses={
        204: {"description": "Workflow deleted successfully"},
        404: {"description": "Workflow not found"},
    },
    status_code=204,
)
async def delete_workflow(
    workflow_id: int, db: AsyncSession = Depends(get_session)
):
    existing_workflow = await workflow.get_by_id(db, workflow_id)
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    await workflow.delete_workflow(db, workflow_id)


@router.get(
    "/{workflow_id}/nodes",
    response_model=list[WorkflowNodeSchema],
    description="Get all nodes for a specific workflow",
    responses={
        200: {"description": "Nodes retrieved successfully"},
        404: {"description": "Workflow not found"},
    },
)
async def get_workflow_nodes(
    workflow_id: int, db: AsyncSession = Depends(get_session)
):
    wf = await workflow.get_by_id(db, workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return wf.nodes


@router.get(
    "/{workflow_id}/nodes/{node_id}",
    response_model=WorkflowNodeSchema,
    description="Get a specific node from a workflow",
    responses={
        200: {"description": "Node retrieved successfully"},
        404: {"description": "Node not found"},
    },
)
async def get_one_node(
    workflow_id: int,
    node_id: int,
    db: AsyncSession = Depends(get_session)
):
    wf = await workflow.get_by_id(db, workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    node = await workflow.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.post(
    "/{workflow_id}/nodes",
    response_model=WorkflowNodeSchema,
    description="Create a new node in a specific workflow",
    responses={
        201: {"description": "Node created successfully"},
        404: {"description": "Workflow not found"},
    },
)
async def create_workflow_node(
    workflow_id: int,
    data: WorkflowNodeCreateSchema,
    db: AsyncSession = Depends(get_session),
):
    wf = await workflow.get_by_id(db, workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await workflow.create_workflow_node(
        db,
        workflow_id=workflow_id,
        config=dict(*(data.pairs or [])),
    )

@router.patch(
    "/nodes/{node_id}",
    response_model=WorkflowNodeSchema,
    description="Update an existing node in a specific workflow",
    responses={
        200: {"description": "Node updated successfully"},
        404: {"description": "Node not found"},
    },
)
async def update_workflow_node(
    node_id: int,
    data: WorkflowNodeUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    node = await workflow.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    updated_config = dict(*(data.pairs or []))
    return await workflow.update_workflow_node(
        db,
        node_id=node_id,
        config=updated_config,
    )


@router.delete(
    "/nodes/{node_id}",
    description="Delete a node by its ID",
    responses={
        204: {"description": "Node deleted successfully"},
        404: {"description": "Node not found"},
    },
    status_code=204,
)
async def delete_workflow_node(
    node_id: int, db: AsyncSession = Depends(get_session)
):
    existing_node = await workflow.get_node_by_id(db, node_id)
    if not existing_node:
        raise HTTPException(status_code=404, detail="Node not found")
    await workflow.delete_workflow_node(db, node_id)
