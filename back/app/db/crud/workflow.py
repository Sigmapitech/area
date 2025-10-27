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


async def list_workflow_nodes(
    db: AsyncSession, workflow_id: int
) -> Sequence[WorkflowNode]:
    result = await db.execute(
        select(WorkflowNode).where(WorkflowNode.workflow_id == workflow_id)
    )
    return result.scalars().all()

async def create_workflow_node(
    db: AsyncSession,
    *,
    workflow_id: int,
    config: dict[str, str],
) -> WorkflowNode:
    node = WorkflowNode(
        workflow_id=workflow_id,
        config=WorkflowNodeConfig(**config),
    )
    db.add(node)
    await db.commit()
    await db.refresh(node)
    return node

async def update_workflow_node(
    db: AsyncSession,
    node_id: int,
    *,
    config: dict[str, str] | None = None,
) -> WorkflowNode | None:
    node = await get_node_by_id(db, node_id)
    if not node:
        return None
    if config is not None:
        setattr(node, "config", WorkflowNodeConfig(**config))
    await db.commit()
    await db.refresh(node)
    return node

async def delete_workflow_node(db: AsyncSession, node_id: int) -> None:
    node = await get_node_by_id(db, node_id)
    if node:
        await db.delete(node)
        await db.commit()
