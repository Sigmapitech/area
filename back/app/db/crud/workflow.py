from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.workflow import Workflow, WorkflowNode, WorkflowNodeConfig


async def get_by_id(db: AsyncSession, workflow_id: int) -> Workflow | None:
    result = await db.execute(
        select(Workflow)
        .where(Workflow.id == workflow_id)
        .options(
            selectinload(Workflow.nodes).selectinload(WorkflowNode.config)
        )
    )
    return result.scalars().first()


async def create_workflow(
    db: AsyncSession,
    *,
    name: str,
    owner_id: int,
    description: str | None = None,
) -> Workflow:
    workflow = Workflow(name=name, owner_id=owner_id, description=description)
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    workflow = await get_by_id(db, getattr(workflow, "id"))
    assert workflow is not None, "This should never happen"
    return workflow


async def delete_workflow(db: AsyncSession, workflow_id: int) -> None:
    workflow = await get_by_id(db, workflow_id)
    if workflow:
        await db.delete(workflow)
        await db.commit()


async def update_workflow(
    db: AsyncSession,
    workflow_id: int,
    *,
    name: str | None = None,
    description: str | None = None,
) -> Workflow | None:
    workflow = await get_by_id(db, workflow_id)
    if not workflow:
        return None
    if name is not None:
        setattr(workflow, "name", name)
    if description is not None:
        setattr(workflow, "description", description)
    await db.commit()
    await db.refresh(workflow)
    return workflow


async def list_workflows(
    db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100
) -> Sequence[Workflow]:
    result = await db.execute(
        select(Workflow)
        .where(Workflow.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_node_by_id(
    db: AsyncSession, node_id: int
) -> WorkflowNode | None:
    result = await db.execute(
        select(WorkflowNode).where(WorkflowNode.id == node_id)
    )
    return result.scalars().first()
