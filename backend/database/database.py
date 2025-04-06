from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure your database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./thinkalike.db"  # Using SQLite for example

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function that will be imported in other modules
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
