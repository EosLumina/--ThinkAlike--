from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.db.database import Base

class Match(Base):
    """Model representing a match between two users"""
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)
    user_id_1 = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    compatibility_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, accepted, rejected

    # Relationships
    user_1 = relationship("User", foreign_keys=[user_id_1], back_populates="matches_as_user_1")
    user_2 = relationship("User", foreign_keys=[user_id_2], back_populates="matches_as_user_2")

    def __repr__(self):
        return f"Match(match_id={self.match_id}, user_id_1={self.user_id_1}, user_id_2={self.user_id_2})"
