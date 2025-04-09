from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import json

from backend.app.db.database import Base

class Profile(Base):
    """Profile model containing user's public-facing and personal information."""
    __tablename__ = "profiles"

    profile_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)

    # Basic profile information
    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    # We'll store interests as a JSON string in SQLite or ARRAY in PostgreSQL
    _interests = Column(Text, nullable=True)

    # Location information
    location_city = Column(String, nullable=True)
    location_country = Column(String, nullable=True)

    # Media URLs
    profile_image_url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")

    @property
    def interests(self):
        """Get interests as a list"""
        if self._interests is None:
            return []

        # Fix attribute access issue by properly handling various types
        interests_str = None
        if isinstance(self._interests, str):
            interests_str = self._interests
        else:
            # For SQLAlchemy column or other object types
            try:
                interests_str = str(self._interests)
            except Exception:
                return []

        try:
            return json.loads(interests_str)
        except (json.JSONDecodeError, TypeError):
            return []

    @interests.setter
    def interests(self, value):
        """Store interests as JSON string"""
        if value is None:
            self._interests = None
        else:
            self._interests = json.dumps(value)

    def __repr__(self):
        return f"Profile(profile_id={self.profile_id}, user_id={self.user_id}, name='{self.full_name}')"
