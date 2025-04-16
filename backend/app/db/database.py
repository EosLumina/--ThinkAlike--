"""
ThinkAlike Database Connection

This module handles database connections and session management,
embodying our commitment to data sovereignty and transparent
data handling.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection string from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./thinkalike.db"  # Default SQLite for development
)

# Create database engine
engine = create_engine(
    DATABASE_URL, 
    # Echo SQL for development transparency, disable in production
    echo=os.getenv("ENVIRONMENT", "development") == "development",
    # Enable connection pooling for better performance
    pool_pre_ping=True
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Database dependency for FastAPI endpoints
def get_db():
    """
    Get a database session for use in API endpoints.
    
    This pattern ensures sessions are properly closed even if
    exceptions occur, supporting our commitment to data integrity.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
