import os
import re
import sys
from pathlib import Path

def ensure_directory(directory_path):
    """Ensure a directory exists."""
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True)
        print(f"✅ Created directory: {path}")
    return path

def create_init_files():
    """Create __init__.py files in all directories under backend/."""
    print("Creating __init__.py files...")

    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("⚠️ Backend directory not found!")
        return

    # Find all subdirectories and create __init__.py
    for path in backend_dir.glob('**/'):
        if path.is_dir() and not path.name.startswith(".") and not path.name.startswith("__"):
            init_file = path / '__init__.py'
            if not init_file.exists():
                with open(init_file, 'w') as f:
                    module_name = path.relative_to(backend_dir).as_posix().replace('/', '.')
                    f.write(f'"""{module_name} package."""\n')
                print(f"✅ Created {init_file}")

def fix_database_imports():
    """Fix database import in narrative_model.py."""
    file_path = Path("backend/app/models/narrative_model.py")

    if not file_path.exists():
        print(f"⚠️ File not found: {file_path}")
        return

    content = file_path.read_text()

    # Fix the import
    updated_content = re.sub(
        r'from \.database import Base',
        'from backend.app.db.database import Base',
        content
    )

    if content != updated_content:
        file_path.write_text(updated_content)
        print(f"✅ Fixed imports in {file_path}")

def create_database_module():
    """Ensure database module exists."""
    db_dir = ensure_directory("backend/app/db")

    # Create __init__.py
    init_file = db_dir / "__init__.py"
    if not init_file.exists():
        with open(init_file, "w") as f:
            f.write('"""Database module."""\n')
        print(f"✅ Created {init_file}")

    # Create database.py
    db_file = db_dir / "database.py"
    if not db_file.exists():
        with open(db_file, "w") as f:
            f.write('''
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
''')
        print(f"✅ Created {db_file}")

def fix_sqlalchemy_comparisons():
    """Fix SQLAlchemy comparison issues in Python files."""
    backends_dir = Path("backend")

    if not backends_dir.exists():
        print("⚠️ Backend directory not found!")
        return

    # Find all Python files
    python_files = list(backends_dir.glob('**/*.py'))

    # Common SQLAlchemy comparison patterns to fix
    patterns = [
        (r'if\s+([a-zA-Z0-9_\.]+?)\.is_active:', r'if \1 is not None and \1.is_active is True:'),
        (r'if\s+not\s+([a-zA-Z0-9_\.]+?)\.is_active:', r'if \1 is None or \1.is_active is False:'),
        (r'if\s+([a-zA-Z0-9_\.]+?):', r'if \1 is not None:'),
        (r'if\s+existing_user:', r'if existing_user is not None:')
    ]

    for file_path in python_files:
        content = file_path.read_text()
        updated = content

        for pattern, replacement in patterns:
            updated = re.sub(pattern, replacement, updated)

        if content != updated:
            file_path.write_text(updated)
            print(f"✅ Fixed SQLAlchemy comparisons in {file_path}")

def fix_missing_imports():
    """Add missing module imports handling code."""
    core_dir = ensure_directory("backend/app/core")

    # Fix security.py
    security_file = core_dir / "security.py"
    if security_file.exists():
        content = security_file.read_text()
        if "import importlib.util" not in content:
            updated_content = re.sub(
                r'from typing import.*?\n',
                '''from typing import Any, Optional, Union, List

import sys
import importlib.util

# Define module checker function
def is_module_available(module_name):
    return importlib.util.find_spec(module_name) is not None

# Handle jose package
if is_module_available("jose"):
    from jose import JWTError, jwt
else:
    # Define stub classes for type checking
    class jwt:
        @staticmethod
        def encode(claims, key, algorithm): pass
        @staticmethod
        def decode(token, key, algorithms): pass
    class JWTError(Exception): pass
    # Show warning at import time
    print("WARNING: python-jose not found. Install with: pip install python-jose[cryptography]")

# Handle passlib package
if is_module_available("passlib"):
    from passlib.context import CryptContext
else:
    # Define stub class for type checking
    class CryptContext:
        def __init__(self, **kwargs): pass
        def verify(self, plain, hashed): return False
        def hash(self, password): return "hashed_password_stub"
    # Show warning at import time
    print("WARNING: passlib not found. Install with: pip install passlib[bcrypt]")

''',
                content,
                count=1
            )
            security_file.write_text(updated_content)
            print(f"✅ Fixed imports in {security_file}")

def fix_alembic_env():
    """Fix Alembic environment.py file."""
    env_file = Path("backend/alembic/env.py")

    if not env_file.exists():
        print(f"⚠️ File not found: {env_file}")
        return

    content = env_file.read_text()

    # Add proper imports
    updated_content = re.sub(
        r'from alembic import context',
        '''import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alembic import context''',
        content
    )

    if content != updated_content:
        env_file.write_text(updated_content)
        print(f"✅ Fixed imports in {env_file}")

def create_setup_py():
    """Create setup.py file for development mode installation."""
    setup_file = Path("setup.py")

    with open(setup_file, "w") as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="thinkalike",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "sqlalchemy>=2.0.9",
        "alembic>=1.10.3",
        "python-dotenv>=1.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic[email]>=1.10.7",
        "psycopg2-binary>=2.9.6",
        "python-multipart>=0.0.6",
    ],
)
''')

    print(f"✅ Created {setup_file}")

def fix_config_py():
    """Fix BaseSettings in config.py."""
    config_file = Path("backend/app/core/config.py")

    if not config_file.exists():
        print(f"⚠️ File not found: {config_file}")
        return

    content = config_file.read_text()

    # Fix BaseSettings
    updated_content = re.sub(
        r'class Settings\(.*?\):',
        'class Settings(BaseSettings):',
        content
    )

    if content != updated_content:
        config_file.write_text(updated_content)
        print(f"✅ Fixed BaseSettings in {config_file}")

def main():
    print("===== Fixing ThinkAlike Project =====")

    # Create necessary directories and __init__.py files
    create_init_files()

    # Create or fix database module
    create_database_module()

    # Fix imports in narrative_model.py
    fix_database_imports()

    # Fix SQLAlchemy comparisons
    fix_sqlalchemy_comparisons()

    # Fix security.py imports
    fix_missing_imports()

    # Fix Alembic env.py
    fix_alembic_env()

    # Fix config.py
    fix_config_py()

    # Create setup.py
    create_setup_py()

    print("\n===== Project Fixes Complete =====")
    print("\nTo fully install the project in development mode:")
    print("1. Open a terminal/command prompt")
    print("2. Navigate to the ThinkAlike directory")
    print("3. Run: pip install -e .")
    print("\nThis will make all imports work correctly.")
    print("\nRestart your code editor to see the fixes applied!")

if __name__ == "__main__":
    main()
