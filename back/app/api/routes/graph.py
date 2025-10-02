from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_session
from ...db.models.graph import Workflow
from ...schemas import WorkflowCreate, WorkflowRead, WorkflowUpdate

router = APIRouter(prefix="/workflow", tags=["workflow"])


async def get_current_user_id(
    x_user_id: int | None = Header(default=None),
) -> int:
    """Temporary user identification via header.

    In production, replace with poper auth and token verification.
    """
    if x_user_id is None:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, detail="Missing user context"
        )
    return x_user_id


@router.post(
    "",
    response_model=WorkflowRead,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "My flow",
                        "description": "demo",
                    }
                }
            }
        }
    },
)
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    wf = Workflow(
        name=payload.name, description=payload.description, owner_id=user_id
    )
    db.add(wf)
    await db.commit()
    await db.refresh(wf)
    return WorkflowRead.model_validate(wf)


@router.get(
    "",
    response_model=List[WorkflowRead],
    description="List workflows with optional pagination",
)
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Workflow)
        .where(Workflow.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    items = result.scalars().all()
    return [WorkflowRead.model_validate(i) for i in items]


@router.get(
    "/{workflow_id}",
    response_model=WorkflowRead,
)
async def get_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Workflow).where(
            Workflow.id == workflow_id, Workflow.owner_id == user_id
        )
    )
    wf = result.scalar_one_or_none()
    if wf is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")
    return WorkflowRead.model_validate(wf)


@router.patch(
    "/{workflow_id}",
    response_model=WorkflowRead,
)
async def patch_workflow(
    workflow_id: int,
    payload: WorkflowUpdate,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Workflow).where(
            Workflow.id == workflow_id, Workflow.owner_id == user_id
        )
    )
    wf = result.scalar_one_or_none()
    if wf is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")

    if payload.name is not None:
        setattr(wf, "name", payload.name)
    if payload.description is not None:
        setattr(wf, "description", payload.description)

    await db.commit()
    await db.refresh(wf)
    return WorkflowRead.model_validate(wf)


@router.put(
    "/{workflow_id}",
    response_model=WorkflowRead,
)
async def update_workflow(
    workflow_id: int,
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Workflow).where(
            Workflow.id == workflow_id, Workflow.owner_id == user_id
        )
    )
    wf = result.scalar_one_or_none()
    if wf is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")

    setattr(wf, "name", payload.name)
    setattr(wf, "description", payload.description)
    await db.commit()
    await db.refresh(wf)
    return WorkflowRead.model_validate(wf)


@router.delete(
    "/{workflow_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    result = await db.execute(
        select(Workflow).where(
            Workflow.id == workflow_id, Workflow.owner_id == user_id
        )
    )
    wf = result.scalar_one_or_none()
    if wf is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")
    await db.delete(wf)
    await db.commit()
