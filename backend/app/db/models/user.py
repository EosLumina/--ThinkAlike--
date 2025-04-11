from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import func
from ...db.database import Base

class User(Base):
    """User model representing platform users.

    This model handles authentication and core user data.
    """
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Add this to fix duplicate table errors

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    communities = relationship("Community", secondary="user_communities", back_populates="members")
    user_communities = relationship("UserCommunity", back_populates="user")
