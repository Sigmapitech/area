from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Workflow, WorkflowNode


async def create_workflow(
    db: AsyncSession, owner_id: int, name: str, description: str
) -> Workflow:
    wf = Workflow(name=name, description=description, owner_id=owner_id)
    db.add(wf)
    await db.commit()
    await db.refresh(wf)
    return wf


async def list_workflows(
    db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 50
) -> Sequence[Workflow]:
    result = await db.execute(
        select(Workflow)
        .where(Workflow.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_workflow(
    db: AsyncSession, workflow_id: int, options=None
) -> Workflow | None:
    query = select(Workflow).where(Workflow.id == workflow_id)
    if options:
        query = query.options(*options)
    result = await db.execute(query)
    return result.scalars().first()


async def update_workflow(
    db: AsyncSession,
    wf: Workflow,
    name: str | None = None,
    description: str | None = None,
) -> Workflow:
    if name is not None:
        setattr(wf, "name", name)
    if description is not None:
        setattr(wf, "description", description)
    await db.commit()
    await db.refresh(wf)
    return wf


async def delete_workflow(db: AsyncSession, wf: Workflow):
    result_roots = await db.execute(
        select(WorkflowNode).where(
            WorkflowNode.workflow_id == wf.id, WorkflowNode.parent_id.is_(None)
        )
    )
    root_nodes = result_roots.scalars().all()
    for node in root_nodes:
        await db.delete(node)

    await db.delete(wf)
    await db.commit()
