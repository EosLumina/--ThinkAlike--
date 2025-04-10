"""
This script helps fix common issues in the ThinkAlike project structure.
Run it from the root directory to create necessary __init__.py files,
update import paths, delete unused branches, and analyze workflows.
"""

import os
import sys
from pathlib import Path
import re
import subprocess

def create_init_files():
    """Create __init__.py files in all directories under backend/app."""
    app_dir = Path('backend/app')

    if not app_dir.exists():
        print(f"Directory {app_dir} not found. Creating it...")
        os.makedirs(app_dir)

    # Create app/__init__.py
    app_init = app_dir / '__init__.py'
    if not app_init.exists():
        with open(app_init, 'w') as f:
            f.write('"""ThinkAlike application package."""\n')
        print(f"Created {app_init}")

    # Find all subdirectories and create __init__.py
    for path in app_dir.glob('**/'):
        if path.is_dir():
            init_file = path / '__init__.py'
            if not init_file.exists():
                with open(init_file, 'w') as f:
                    module_name = path.relative_to(app_dir).as_posix().replace('/', '.')
                    f.write(f'"""{module_name} package."""\n')
                print(f"Created {init_file}")

def ensure_db_directory():
    """Ensure the db directory exists with database.py."""
    db_dir = Path('backend/app/db')

    if not db_dir.exists():
        print(f"Creating {db_dir}...")
        os.makedirs(db_dir)

    # Create db/__init__.py
    db_init = db_dir / '__init__.py'
    if not db_init.exists():
        with open(db_init, 'w') as f:
            f.write('"""Database package."""\n')
        print(f"Created {db_init}")

    # Create database.py if it doesn't exist
    database_py = db_dir / 'database.py'
    if not database_py.exists():
        with open(database_py, 'w') as f:
            f.write("""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")
        print(f"Created {database_py}")

def delete_unused_branches():
    """Delete unused branches from the repository."""
    print("Deleting unused branches...")
    result = subprocess.run(['git', 'fetch', '--prune'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching branches: {result.stderr}")
        return

    branches = subprocess.run(['git', 'branch', '-r'], capture_output=True, text=True)
    if branches.returncode != 0:
        print(f"Error listing branches: {branches.stderr}")
        return

    for branch in branches.stdout.splitlines():
        branch = branch.strip()
        if branch not in ['origin/main', 'origin/master']:
            delete_result = subprocess.run(['git', 'branch', '-d', branch], capture_output=True, text=True)
            if delete_result.returncode == 0:
                print(f"Deleted branch: {branch}")
            else:
                print(f"Error deleting branch {branch}: {delete_result.stderr}")

def analyze_and_fix_workflows():
    """Analyze and fix workflow problems."""
    print("Analyzing and fixing workflow problems...")
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print(f"Workflows directory {workflows_dir} not found!")
        return

    for workflow_file in workflows_dir.glob('*.yml'):
        with open(workflow_file, 'r') as f:
            content = f.read()

        # Example fix: ensure all workflows use the latest actions/checkout version
        updated_content = re.sub(r'uses: actions/checkout@v[0-9]+', 'uses: actions/checkout@v3', content)

        if content != updated_content:
            with open(workflow_file, 'w') as f:
                f.write(updated_content)
            print(f"Updated {workflow_file}")

if __name__ == "__main__":
    print("Fixing ThinkAlike project structure...")
    create_init_files()
    ensure_db_directory()
    delete_unused_branches()
    analyze_and_fix_workflows()
    print("Done! The structure has been updated.")
    print("Remember to install required packages:")
    print("pip install python-jose[cryptography] passlib[bcrypt]")
