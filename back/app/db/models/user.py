from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    auth = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    workflows = relationship(
        "Workflow",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tokens = relationship(
        "UserToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin"
    )
