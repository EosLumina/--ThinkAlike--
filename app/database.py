import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging for database operations (supports DataTraceability)
logging.basicConfig(level=logging.INFO)
db_logger = logging.getLogger("thinkalike.database")

# Get database URL from environment variable or use SQLite default
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

# Log database connection (part of transparency principle)
db_logger.info(f"Connecting to database: {DATABASE_URL.split('://')[0]}://*****")

# Create SQLAlchemy engine with appropriate options
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    # Echo SQL statements in development mode for transparency
    echo=os.environ.get("DEBUG", "False").lower() == "true"
)

# Add event listener for SQL operations to support DataTraceability
if os.environ.get("TRACE_SQL", "False").lower() == "true":
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(datetime.datetime.now())
        db_logger.debug(f"SQL: {statement}")

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = datetime.datetime.now() - conn.info['query_start_time'].pop(-1)
        db_logger.debug(f"SQL Time: {total.total_seconds():.3f}s")

# Create SessionLocal class with ThinkAlike's data integrity options
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session with automatic cleanup
def get_db():
    """
    Provides a database session that automatically closes when the request is complete.

    This pattern ensures data integrity and resource cleanup, supporting ThinkAlike's
    data transparency principles by preventing connection leaks.

    Returns:
        SQLAlchemy session: Active database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
