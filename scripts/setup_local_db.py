#!/usr/bin/env python3
"""
Local SQLite Database Setup Script for ThinkAlike

This script creates a SQLite database file for local development
and testing without requiring PostgreSQL.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# SQLite connection string - creates a file in the current directory
SQLITE_CONNECTION = "sqlite:///./thinkalike_local.db"

def setup_sqlite_database():
    """Create and initialize a SQLite database for local development."""
    try:
        print(f"Creating SQLite database at: {SQLITE_CONNECTION}")
        engine = create_engine(SQLITE_CONNECTION)

        # Test the connection
        with engine.connect() as conn:
            # Execute a simple test query
            result = conn.execute(text("SELECT sqlite_version()"))
            version = result.scalar()

            print(f"\n✅ SQLite database created successfully! (SQLite version: {version})")
            print("\nFor local development, use this connection string:")
            print(f"DATABASE_URL={SQLITE_CONNECTION}")

            # Create an environment file for easy loading
            with open(".env.local", "w") as f:
                f.write(f"DATABASE_URL={SQLITE_CONNECTION}\n")
            print("\nCreated .env.local file with database configuration.")

            return True
    except SQLAlchemyError as e:
        print(f"\n❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_sqlite_database()
