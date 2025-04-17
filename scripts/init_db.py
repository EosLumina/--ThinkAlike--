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
        Column("hashed_password", String, nullable=False),
        Column("is_active", Integer, default=1),
        Column("created_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    value_profiles = Table(
        "value_profiles",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, nullable=False),
        Column("profile_data", String, nullable=False),
        Column("created_at", String, default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    narratives = Table(
        "narratives",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, nullable=False),
        Column("state", String, nullable=False),
        Column("completed", Integer, default=0),
        Column("created_at", String, default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    connections = Table(
        "connections",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("requester_id", Integer, nullable=False),
        Column("addressee_id", Integer, nullable=False),
        Column("status", String, nullable=False),
        Column("match_percentage", String),
        Column("created_at", String, default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    communities = Table(
        "communities",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("description", String),
        Column("creator_id", Integer, nullable=False),
        Column("is_private", Integer, default=0),
        Column("created_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    community_members = Table(
        "community_members",
        metadata,
        Column("community_id", Integer, nullable=False),
        Column("user_id", Integer, nullable=False),
        Column("role", String, default="member"),
        Column("joined_at", String, default=text("CURRENT_TIMESTAMP")),
    )

    verification_audit_logs = Table(
        "verification_audit_logs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("action_type", String, nullable=False),
        Column("user_id", Integer),
        Column("request_data", String),
        Column("result", String, nullable=False),
        Column("reason", String),
        Column("timestamp", String, default=text("CURRENT_TIMESTAMP")),
    )

    metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
