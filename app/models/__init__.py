"""
ThinkAlike models package initialization.
Exports the SQLAlchemy Base object and imports all models to register them.
"""
from app.database import Base

# Import all models so they're registered with Base.metadata
# This ensures create_all() creates all model tables
try:
    from app.models.user import User
except ImportError:
    pass  # User model might not exist yet

try:
    from app.models.agent import Agent
except ImportError:
    pass  # Agent model might not exist yet

# Add other model imports as they are created
