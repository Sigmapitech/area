from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=True)

    nodes = relationship("WorkflowNode", back_populates="workflow")


class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"

    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("workflow_nodes.id"), nullable=True)

    workflow = relationship("Workflow", back_populates="nodes")
    parent = relationship("WorkflowNode", remote_side=[id], backref="children")

    node_type = Column(
        Enum(
            "receive",
            "send",
        ),
        nullable=False,
    )
    content = Column(JSON, nullable=True)
