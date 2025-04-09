"""
This module imports all SQLAlchemy models to ensure they are registered with
Base.metadata for use with Alembic migrations.
"""

from .database import Base
from .models.user import User
from .models.profile import Profile

# All models need to be imported here for Alembic to detect them
__all__ = ["Base", "User", "Profile"]
