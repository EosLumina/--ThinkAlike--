from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from backend.app.db.database import Base

class User(Base):
    """User model representing platform users."""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("Profile", uselist=False, back_populates="user")
    communities = relationship("Community", secondary="user_communities", back_populates="members")
    community_associations = relationship("UserCommunity", back_populates="user")
    matches_as_user_1 = relationship("Match", foreign_keys="Match.user_id_1", back_populates="user_1")
    matches_as_user_2 = relationship("Match", foreign_keys="Match.user_id_2", back_populates="user_2")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}')"
