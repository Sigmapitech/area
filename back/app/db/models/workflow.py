from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)

    description = Column(String(512), index=True, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    nodes = relationship(
        "WorkflowNode",
        back_populates="workflow",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    owner = relationship("User", back_populates="workflows")


class WorkflowNode(Base):
    __tablename__ = "workflow_node"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(
        Integer, ForeignKey("workflow.id", ondelete="CASCADE")
    )

    interaction_id = Column(Integer, ForeignKey("interaction.id"))

    config = relationship(
        "WorkflowNodeConfig",
        back_populates="node",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Outgoing: one-to-many
    outgoing_edges = relationship(
        "WorkflowEdge",
        foreign_keys="WorkflowEdge.from_node_id",
        back_populates="from_node",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Incoming: one-to-one
    incoming_edge = relationship(
        "WorkflowEdge",
        foreign_keys="WorkflowEdge.to_node_id",
        back_populates="to_node",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )

    workflow = relationship("Workflow", back_populates="nodes")


class WorkflowNodeConfig(Base):
    __tablename__ = "workflow_node_config"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(
        Integer, ForeignKey("workflow_node.id", ondelete="CASCADE")
    )

    key = Column(String(32), index=True)
    value = Column(String(128), index=True)

    node = relationship("WorkflowNode", back_populates="config")


class WorkflowEdge(Base):
    """Represents a directed connection between two WorkflowNode its graph."""

    __tablename__ = "workflow_edge"

    id = Column(Integer, primary_key=True, index=True)

    from_node_id = Column(
        Integer, ForeignKey("workflow_node.id", ondelete="CASCADE")
    )
    to_node_id = Column(
        Integer,
        ForeignKey("workflow_node.id", ondelete="CASCADE"),
        unique=True,
    )

    from_node = relationship(
        "WorkflowNode",
        back_populates="outgoing_edges",
        foreign_keys=[from_node_id],
    )
    to_node = relationship(
        "WorkflowNode",
        back_populates="incoming_edge",
        foreign_keys=[to_node_id],
    )
