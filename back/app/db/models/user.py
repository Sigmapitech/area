from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)

    email = Column(String(256), unique=True, index=True, nullable=False)
    auth = Column(String(256), nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    workflows = relationship(
        "Workflow",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tokens = relationship(
        "OAuthToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )
