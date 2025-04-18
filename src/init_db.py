"""
Database initialization script for ThinkAlike.
Handles schema creation and initial data setup.
"""
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use SQLite default
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

def init_database():
    print(f"Initializing database with connection: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)

    # Create tables
    metadata = MetaData()

    # Example table - replace with your schema
    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String, unique=True),
        Column("email", String, unique=True),
    )

    metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
