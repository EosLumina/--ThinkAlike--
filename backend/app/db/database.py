import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Get DATABASE_URL from environment, with SQLite fallback for development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

# SQLite connect_args needed only for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine with appropriate parameters
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Dependency function to get DB session for FastAPI
def get_db():
    """FastAPI dependency that provides a database session.

    Yields:
        Session: SQLAlchemy session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
