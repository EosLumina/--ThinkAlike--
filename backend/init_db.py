import os
import sqlite3
import sys
from pathlib import Path

def init_database():
    """Initialize SQLite database for local development."""
    # Create instance directory if it doesn't exist
    instance_dir = Path('instance')
    instance_dir.mkdir(exist_ok=True)
    
    # Database path
    db_path = instance_dir / 'thinkalike.db'
    
    # Check if schema.sql exists
    schema_path = Path('backend/schema.sql')
    if not schema_path.exists():
        print("Error: schema.sql not found in backend directory.")
        print("Creating minimal schema.sql file...")
        
        with open(schema_path, 'w') as f:
            f.write("""-- ThinkAlike Database Schema
-- SQLite Version (Development)

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Value Profiles table 
CREATE TABLE IF NOT EXISTS value_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    profile_data JSON NOT NULL, -- Stores the JSON representation of value profile
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Narratives table (for Mode 1)
CREATE TABLE IF NOT EXISTS narratives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    state JSON NOT NULL, -- Stores current narrative state
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- User connections (for Mode 2)
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER NOT NULL,
    addressee_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'rejected')),
    match_percentage REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES users (id),
    FOREIGN KEY (addressee_id) REFERENCES users (id),
    UNIQUE (requester_id, addressee_id)
);

-- Communities (for Mode 3)
CREATE TABLE IF NOT EXISTS communities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    creator_id INTEGER NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Community membership
CREATE TABLE IF NOT EXISTS community_members (
    community_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('member', 'moderator', 'admin')),
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (community_id, user_id),
    FOREIGN KEY (community_id) REFERENCES communities (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Verification system audit log
CREATE TABLE IF NOT EXISTS verification_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    user_id INTEGER,
    request_data JSON,
    result TEXT NOT NULL CHECK (result IN ('pass', 'fail', 'modified')),
    reason TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
""")
        print("Created minimal schema.sql file.")

    print(f"Initializing database at {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    try:
        # Read and execute the schema file
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        conn.executescript(schema)
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    if init_database():
        print("Database setup complete.")
    else:
        sys.exit(1)
