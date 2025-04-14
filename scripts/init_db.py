"""
Database initialization script for ThinkAlike.

This script creates initial data for development purposes.
"""
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app import models
import hashlib

def get_password_hash(password: str) -> str:
    """
    Simple password hashing for demonstration purposes.
    In production, use a proper password hashing library like passlib or bcrypt.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)

    # Create a database session
    db = SessionLocal()

    # Check if we already have users
    user_count = db.query(models.User).count()
    if user_count == 0:
        print("Creating sample users...")

        # Create sample users
        sample_users = [
            models.User(
                username="user1",
                email="user1@example.com",
                display_name="Enlightened User",
                hashed_password=get_password_hash("password123"),
                has_ethical_profile=True,
                data_transparency_level="full"
            ),
            models.User(
                username="user2",
                email="user2@example.com",
                display_name="Conscious Explorer",
                hashed_password=get_password_hash("password456"),
                has_ethical_profile=False,
                data_transparency_level="partial"
            )
        ]

        db.add_all(sample_users)
        db.commit()
        print(f"Added {len(sample_users)} sample users")
    else:
        print(f"Database already contains {user_count} users. Skipping initialization.")

    db.close()

if __name__ == "__main__":
    print("Initializing the database...")
    init_db()
    print("Database initialization completed.")
