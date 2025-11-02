from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class OAuthToken(Base):
    __tablename__ = "oauth_token"

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey("user.id"), nullable=False)
    access_token = Column(String(128), nullable=False)
    refresh_token = Column(String(128), nullable=True)

    service_id = Column(Integer, ForeignKey("service.id"), nullable=False)

    scope = Column(String(512), nullable=True)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tokens")
