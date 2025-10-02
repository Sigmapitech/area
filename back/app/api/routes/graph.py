from http import HTTPStatus
from typing import Callable, List, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...db import get_session
from ...db.models.graph import Workflow
from ...schemas import (
    WorkflowCreate,
    WorkflowDetail,
    WorkflowRead,
    WorkflowUpdate,
)
from .auth import get_user_id_from_token

router = APIRouter(prefix="/workflow", tags=["workflow"])


async def get_workflow_or_404(
    db: AsyncSession, user_id: int, workflow_id: int, *, options: Sequence = ()
) -> Workflow:
    result = await db.execute(
        select(Workflow)
        .where(Workflow.id == workflow_id, Workflow.owner_id == user_id)
        .options(*options)
    )
    wf = result.scalar_one_or_none()
    if wf is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Workflow not found")
    return wf


def workflow_dependency(*, options: Sequence = ()) -> Callable:
    async def _dep(
        workflow_id: int,
        db: AsyncSession = Depends(get_session),
        user_id: int = Depends(get_user_id_from_token),
    ) -> Workflow:
        return await get_workflow_or_404(
            db, user_id, workflow_id, options=options
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
    user_id: int = Depends(get_user_id_from_token),
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
    user_id: int = Depends(get_user_id_from_token),
):
    result = await db.execute(
        select(Workflow)
        .where(Workflow.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    items = result.scalars().all()
    return [WorkflowRead.model_validate(i) for i in items]


@router.get("/{workflow_id}", response_model=WorkflowDetail)
async def get_workflow(
    wf: Workflow = Depends(
        workflow_dependency(options=[selectinload(Workflow.nodes)])
    ),
):
    return WorkflowDetail.model_validate(wf)


@router.patch("/{workflow_id}", response_model=WorkflowRead)
async def patch_workflow(
    payload: WorkflowUpdate,
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    if payload.name is not None:
        setattr(wf, "name", payload.name)
    if payload.description is not None:
        setattr(wf, "description", payload.description)

    await db.commit()
    await db.refresh(wf)
    return WorkflowRead.model_validate(wf)


@router.put("/{workflow_id}", response_model=WorkflowRead)
async def update_workflow(
    payload: WorkflowCreate,
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    setattr(wf, "name", payload.name)
    setattr(wf, "description", payload.description)

    await db.commit()
    await db.refresh(wf)
    return WorkflowRead.model_validate(wf)


@router.delete("/{workflow_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_workflow(
    wf: Workflow = Depends(workflow_dependency()),
    db: AsyncSession = Depends(get_session),
):
    await db.delete(wf)
    await db.commit()
