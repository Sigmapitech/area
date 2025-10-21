from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
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
    key = Column(String, index=True)
    value = Column(String, index=True)

    node = relationship("WorkflowNode", back_populates="config")


class WorkflowEdge(Base):
    """
    Represents a directed connection between two WorkflowNode entities in the workflow graph.

    This SQLAlchemy ORM model stores edges that originate from one node and point to another.
    A uniqueness constraint on `to_node_id` guarantees that a node can have at most one
    incoming edge, while a single node may emit multiple outgoing edges. Deleting a node
    cascades to its associated edges.

    Attributes:
        id (int): Primary key identifier of the edge.
        from_node_id (int): Foreign key to the source WorkflowNode (workflow_node.id), cascades on delete.
        to_node_id (int): Foreign key to the target WorkflowNode (workflow_node.id), cascades on delete.
                          Uniquely constrained to enforce at most one incoming edge per node.

    Relationships:
        from_node (WorkflowNode): Source node; back-populates 'outgoing_edges'.
        to_node (WorkflowNode): Target node; back-populates 'incoming_edge'.

    Constraints and behavior:
        - Directed edge: from_node -> to_node.
        - ondelete="CASCADE" ensures edges are removed when their associated nodes are deleted.
        - Unique to_node_id enforces in-degree <= 1, enabling a one-to-many (source->edges) and
          one-to-one (target<-edge) structure.
    """

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
