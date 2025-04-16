"""
SQLAlchemy models for user narratives and related data.

These models implement our principles of value-based connections
and user sovereignty over personal stories.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from app.db.database import Base


class Narrative(Base):
    """
    SQLAlchemy model for user narratives.

    Narratives are personal stories that help define a user's
    values and provide context for matching.
    """
    __tablename__ = "narratives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    values = Column(JSONB, default=list)  # Values expressed in this narrative
    # public, connections_only, private
    privacy_level = Column(String, default="connections_only")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="narratives")
    comments = relationship(
        "NarrativeComment", back_populates="narrative", cascade="all, delete-orphan")


class NarrativeComment(Base):
    """
    SQLAlchemy model for comments on narratives.

    Enables meaningful interaction between users based on shared values.
    """
    __tablename__ = "narrative_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id = Column(UUID(as_uuid=True), ForeignKey("narratives.id"))


    # filepath: /workspaces/--ThinkAlike--/backend/app/db/models/narrative.py
"""
SQLAlchemy models for user narratives and related data.

These models implement our principles of value-based connections
and user sovereignty over personal stories.
"""


class Narrative(Base):
    """
    SQLAlchemy model for user narratives.

    Narratives are personal stories that help define a user's
    values and provide context for matching.
    """
    __tablename__ = "narratives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    values = Column(JSONB, default=list)  # Values expressed in this narrative
    # public, connections_only, private
    privacy_level = Column(String, default="connections_only")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="narratives")
    comments = relationship(
        "NarrativeComment", back_populates="narrative", cascade="all, delete-orphan")


class NarrativeComment(Base):
    """
    SQLAlchemy model for comments on narratives.

    Enables meaningful interaction between users based on shared values.
    """
    __tablename__ = "narrative_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id = Column(UUID(as_uuid=True), ForeignKey("narratives.id"))
