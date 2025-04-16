"""
SQLAlchemy models for user data.

These models implement our data sovereignty principles by clearly
defining ownership and access boundaries for user data.
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from app.db.database import Base

# Many-to-many relationship for user connections
user_connections = Table(
    'user_connections',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True),
           ForeignKey('users.id'), primary_key=True),
    Column('connected_user_id', UUID(as_uuid=True),
           ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('status', String, default='active')
)


class User(Base):
    """
    SQLAlchemy model for user accounts.

    This model implements user sovereignty by:
    1. Using a unique ID that doesn't expose personal information
    2. Storing only necessary user attributes
    3. Explicitly tracking user activity state
    4. Supporting verifiable creation and update timestamps
    """
    __tablename__ = "users"
    # Add this to fix duplicate table errors
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    value_profile = relationship(
        "ValueProfile", back_populates="user", uselist=False)
    narratives = relationship("Narrative", back_populates="user")

    # Many-to-many relationship for connections
    connections = relationship(
        "User",
        secondary=user_connections,
        primaryjoin=id == user_connections.c.user_id,
        secondaryjoin=id == user_connections.c.connected_user_id,
        backref="connected_by"
    )


class ValueProfile(Base):
    """
    SQLAlchemy model for user value profiles.

    This is central to the ThinkAlike matching system, allowing users to
    connect based on genuine value alignment rather than superficial traits.
    """
    __tablename__ = "value_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    explicit_values = Column(JSONB, default=list)  # List of explicit values
    # Values derived from narratives
    narrative_derived_values = Column(JSONB, default=dict)
    interests = Column(JSONB, default=list)  # List of interests
    skills = Column(JSONB, default=list)  # List of skills
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="value_profile")


class ConnectionRequest(Base):
    """
    SQLAlchemy model for connection requests between users.

    Implements user sovereignty by requiring explicit consent
    for connections between users.
    """
    __tablename__ = "connection_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    # pending, accepted, declined, withdrawn
    status = Column(String, default="pending")
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
