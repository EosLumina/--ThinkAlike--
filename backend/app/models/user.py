"""
User models embodying data sovereignty principles.

This module defines the data models for user identity in ThinkAlike,
implementing our core principle that users must have complete
sovereignty over their digital existence.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from backend.app.db.database import Base


class UserBase(BaseModel):
    """
    Base user model with essential shared fields.

    This model embodies our commitment to data minimization -
    collecting only what's necessary for user functionality.
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """
    User creation model with password field.

    The password is only used during creation and never returned
    in API responses, supporting our radical transparency principle.
    """
    password: str


class UserInDB(UserBase):
    """
    User model stored in database with hashed password.

    This model embodies user sovereignty by:
    1. Using a unique ID that doesn't expose personal information
    2. Storing only necessary user attributes
    3. Explicitly tracking user activity state
    4. Supporting verifiable creation and update timestamps
    """
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    value_profile: Optional[dict] = None

    class Config:
        from_attributes = True


class UserValueProfile(BaseModel):
    """
    Value profile for a user, representing their core values and preferences.

    This is central to the ThinkAlike matching system, allowing users to
    connect based on genuine value alignment rather than superficial traits.
    """
    user_id: UUID
    explicit_values: List[str] = Field(default_factory=list)
    narrative_derived_values: dict = Field(default_factory=dict)
    interests: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory.list)

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """
    Public user response model, deliberately excluding sensitive data.

    This model implements radical transparency by clearly separating
    internal data from externally shared data, giving users confidence
    that sensitive information is never exposed.
    """
    id: UUID

    class Config:
        from_attributes = True


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
    communities = relationship(
        "Community", secondary="user_communities", back_populates="members")
    community_associations = relationship(
        "UserCommunity", back_populates="user")
    matches_as_user_1 = relationship(
        "Match", foreign_keys="Match.user_id_1", back_populates="user_1")
    matches_as_user_2 = relationship(
        "Match", foreign_keys="Match.user_id_2", back_populates="user_2")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}')"
