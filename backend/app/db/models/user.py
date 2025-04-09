from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index

from ..database import Base

class User(Base):
    """User model representing platform users.

    This model handles authentication and core user data.
    """
    __tablename__ = "users"

    # Primary key uses Integer for MVP simplicity
    user_id = Column(Integer, primary_key=True, index=True)

    # Authentication fields
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    # Account status fields
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_login_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Authorization fields - stored as array of role names
    # For PostgreSQL, use ARRAY(String)
    # For SQLite, temporarily use a comma-separated string until migration
    roles = Column(String, default="user", nullable=False)  # For MVP simplicity with SQLite

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False,
                         cascade="all, delete-orphan")

    # Additional indexes
    __table_args__ = (
        Index('ix_users_username_email', 'username', 'email'),
    )

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}')"
