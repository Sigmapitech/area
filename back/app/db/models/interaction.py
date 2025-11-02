from sqlalchemy import Column, Integer, String

from ..base import Base


class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
