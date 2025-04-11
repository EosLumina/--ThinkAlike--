from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.database import Base

# Fix the association table definition
user_community_association = Table(
    "user_communities",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("community_id", Integer, ForeignKey("communities.id"), primary_key=True),
    extend_existing=True  # Added this line to fix duplicate table definition
)

class Community(Base):
    """Model representing a community of users"""
    __tablename__ = "communities"
    __table_args__ = {'extend_existing': True}  # Add this to fix duplicate table errors

    community_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_private = Column(Boolean, default=False)

    # Relationships
    members = relationship("User", secondary=user_community_association, back_populates="communities")

    def __repr__(self):
        return f"Community(community_id={self.community_id}, name='{self.name}')"

# Fix the UserCommunity class
class UserCommunity(Base):
    __tablename__ = "user_communities"
    __table_args__ = {'extend_existing': True}  # Added this line to fix duplicate table definition

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    community_id = Column(Integer, ForeignKey("communities.community_id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="member")  # member, moderator, admin
    is_admin = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="community_associations")
    community = relationship("Community")

    def __repr__(self):
        return f"UserCommunity(user_id={self.user_id}, community_id={self.community_id})"
