from http import HTTPStatus
from typing import Callable, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...db.crud import workflow_nodes, workflows
from ...db.models.graph import Workflow, WorkflowNode
from ...schemas import (
    NodeCreate,
    NodeRead,
    NodeUpdate,
    WorkflowCreate,
    WorkflowDetail,
    WorkflowRead,
    WorkflowUpdate,
)
from ...schemas.user import UserSchema
from ...security.deps import get_current_user

router = APIRouter(prefix="/workflow", tags=["workflow"])


async def get_workflow_or_404(
    db: AsyncSession, user_id: int, workflow_id: int
) -> Workflow:
    wf = await workflows.get_workflow(db, workflow_id)

    if wf is None or getattr(wf, "owner_id") != user_id:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")

    return wf


async def get_workflow_node_or_404(
    db: AsyncSession, user_id: int, workflow_id: int, node_id: int
) -> WorkflowNode:
    result = await db.execute(
        select(WorkflowNode)
        .join(Workflow)
        .where(
            WorkflowNode.id == node_id,
            WorkflowNode.workflow_id == workflow_id,
            Workflow.owner_id == user_id,
        )
    )
    node = result.scalar_one_or_none()
    if node is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Node not found")
    return node


def workflow_dependency() -> Callable:
    async def _dep(
        workflow_id: int = Path(..., ge=1),
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(get_current_user),
    ) -> Workflow:
        return await get_workflow_or_404(db, current_user.id, workflow_id)

    return _dep


def workflow_node_dependency() -> Callable:
    async def _dep(
        workflow_id: int = Path(..., ge=1),
        node_id: int = Path(..., ge=1),
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(get_current_user),
    ) -> WorkflowNode:
        return await get_workflow_node_or_404(
            db, current_user.id, workflow_id, node_id
        )

    return _dep


@router.post(
    "",
    response_model=WorkflowRead,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {
            "model": WorkflowRead,
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "My flow",
                        "description": "demo",
                    }
                }
            },
        }
    },
)
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
):
    return await workflows.create_workflow(
        db,
        name=payload.name,
        description=payload.description or "",
        owner_id=current_user.id,
    )


@router.get(
    "",
    response_model=List[WorkflowRead],
    description="List workflows with optional pagination",
)
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
):
    return await workflows.list_workflows(db, current_user.id, skip, limit)


@router.get("/{workflow_id}", response_model=WorkflowDetail)
async def get_workflow(wf: Workflow = Depends(workflow_dependency())):
    return wf


@router.patch("/{workflow_id}", response_model=WorkflowRead)
async def patch_workflow(
    payload: WorkflowUpdate,
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflows.update_workflow(db, wf, **payload.model_dump())


@router.put("/{workflow_id}", response_model=WorkflowRead)
async def update_workflow(
    payload: WorkflowCreate,
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflows.update_workflow(db, wf, **payload.model_dump())


@router.delete("/{workflow_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_workflow(
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflows.delete_workflow(db, wf)


@router.get("/{workflow_id}/{node_id}", response_model=NodeRead)
async def get_workflow_node(
    node: WorkflowNode = Depends(workflow_node_dependency()),
):
    return node


@router.post(
    "/{workflow_id}",
    response_model=NodeRead,
    status_code=HTTPStatus.CREATED,
)
async def create_node(
    payload: NodeCreate,
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflow_nodes.create_node(
        db, getattr(wf, "id"), payload.model_dump(exclude_unset=True)
    )


@router.patch("/{workflow_id}/{node_id}", response_model=NodeRead)
async def patch_node(
    payload: NodeUpdate,
    node: WorkflowNode = Depends(workflow_node_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflow_nodes.update_node(
        db, node, payload.model_dump(exclude_unset=True)
    )


@router.put("/{workflow_id}/{node_id}", response_model=NodeRead)
async def update_node(
    payload: NodeCreate,
    node: WorkflowNode = Depends(workflow_node_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflow_nodes.update_node(
        db, node, payload.model_dump(exclude_unset=True)
    )


@router.delete("/{workflow_id}/{node_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_node(
    node: WorkflowNode = Depends(workflow_node_dependency()),
    db: AsyncSession = Depends(get_session),
):
    return await workflow_nodes.delete_node(db, node)
