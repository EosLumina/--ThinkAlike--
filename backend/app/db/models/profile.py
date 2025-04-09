from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index

from ..database import Base

class Profile(Base):
    """Profile model containing user's public-facing and personal information.

    This model extends the core User model with additional profile information.
    """
    __tablename__ = "profiles"

    profile_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),
                    unique=True, nullable=False)

    # Basic profile information
    full_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    birthdate = Column(DateTime, nullable=True)

    # Location information
    static_location_city = Column(String, nullable=True)
    static_location_country = Column(String, nullable=True)

    # Media URLs
    profile_image_url = Column(String, nullable=True)
    profile_video_url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now(),
                        onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    # Additional indexes
    __table_args__ = (
        Index('ix_profiles_user_id', 'user_id'),
    )

    def __repr__(self):
        return f"Profile(profile_id={self.profile_id}, user_id={self.user_id}, name='{self.full_name}')"
