from sqlalchemy import Column, Integer, String

from ..base import Base


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
