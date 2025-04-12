from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class User(Base):
    """
    User model for ThinkAlike platform.

    This model incorporates ThinkAlike's ethical principles by including fields
    specifically designed for data transparency and user control.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    display_name = Column(String, nullable=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Ethical components specific to ThinkAlike
    has_ethical_profile = Column(Boolean, default=False)
    data_transparency_level = Column(String, default="full")
    data_retention_preference = Column(String, default="standard")

    def __repr__(self):
        return f"<User {self.username}>"
