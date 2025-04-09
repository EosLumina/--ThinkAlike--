from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.db.database import Base

# Association table for many-to-many relationship between users and communities
user_community_association = Table(
    'user_communities',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('community_id', Integer, ForeignKey('communities.community_id')),
    Column('joined_at', DateTime, default=datetime.utcnow)
)

class Community(Base):
    """Model representing a community of users"""
    __tablename__ = "communities"

    community_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    members = relationship("User", secondary=user_community_association, back_populates="communities")

    def __repr__(self):
        return f"Community(community_id={self.community_id}, name='{self.name}')"

# Class to represent the association table ORM-style for direct access
class UserCommunity(Base):
    """Model representing a user's membership in a community"""
    __tablename__ = "user_communities"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    community_id = Column(Integer, ForeignKey("communities.community_id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="member")  # member, moderator, admin

    # Relationships
    user = relationship("User", back_populates="community_associations")
    community = relationship("Community")

    def __repr__(self):
        return f"UserCommunity(user_id={self.user_id}, community_id={self.community_id})"
