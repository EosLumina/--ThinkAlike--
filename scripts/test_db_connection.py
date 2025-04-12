#!/usr/bin/env python3
"""
Database Connection Test Script

This script tests a connection to the PostgreSQL database using SQLAlchemy.
Use this to verify your database credentials and connection string.
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def test_connection(connection_string):
    """Test the database connection using the provided connection string."""
    try:
        print(f"Attempting to connect to database with: {connection_string}")
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            print("\n✅ Connection successful!")
            return True
    except SQLAlchemyError as e:
        print(f"\n❌ Connection failed: {e}")
        return False

def get_connection_string():
    """Get the database connection string from user input."""
    print("\n=== ThinkAlike Database Connection Tester ===\n")

    host = input("Database Host (default: localhost): ") or "localhost"
    port = input("Database Port (default: 5432): ") or "5432"
    dbname = input("Database Name (default: thinkalike_test): ") or "thinkalike_test"
    username = input("Database Username (default: postgres): ") or "postgres"
    password = input("Database Password (default: postgres): ") or "postgres"

    # Build the connection string
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    return connection_string

if __name__ == "__main__":
    # If connection string is provided as command line argument, use it
    if len(sys.argv) > 1:
        connection_string = sys.argv[1]
    else:
        # Otherwise, ask for connection details
        connection_string = get_connection_string()

    # Test the connection
    success = test_connection(connection_string)

    if success:
        print("\nYou can use this connection string in your GitHub Actions secrets.")
        print(f"DATABASE_URL: {connection_string}")
    else:
        print("\nPlease check your database credentials and ensure the database server is running.")
