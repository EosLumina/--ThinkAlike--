#!/usr/bin/env python3
"""
ThinkAlike Project Management Script
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# Check if the backend module structure is correct
backend_dir = ROOT_DIR / 'backend'
run_file = backend_dir / 'run.py'
init_file = backend_dir / '__init__.py'

if not backend_dir.exists():
    print(f"Error: Backend directory not found at {backend_dir}")
    sys.exit(1)

if not run_file.exists():
    print(f"Error: run.py not found at {run_file}")
    sys.exit(1)

if not init_file.exists():
    print(f"Warning: Creating missing __init__.py in backend directory")
    with open(init_file, 'w') as f:
        f.write("# Auto-generated __init__.py file\n")

try:
    from backend.run import main
except ImportError as e:
    print(f"Error importing main function from backend.run: {e}")
    print("Make sure the backend module is properly installed")
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
