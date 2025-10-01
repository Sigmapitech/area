from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import WorkflowNode


async def create_node(
    db: AsyncSession, workflow_id: int, data: dict
) -> WorkflowNode:
    node = WorkflowNode(**data, workflow_id=workflow_id)
    db.add(node)
    await db.commit()
    await db.refresh(node)
    return node


async def get_node(db: AsyncSession, node_id: int) -> Optional[WorkflowNode]:
    result = await db.execute(
        select(WorkflowNode).where(WorkflowNode.id == node_id)
    )
    return result.scalars().first()


async def update_node(
    db: AsyncSession, node: WorkflowNode, data: dict
) -> WorkflowNode:
    for key, value in data.items():
        setattr(node, key, value)
    await db.commit()
    await db.refresh(node)
    return node


async def delete_node(db: AsyncSession, node: WorkflowNode):
    await db.delete(node)
    await db.commit()
