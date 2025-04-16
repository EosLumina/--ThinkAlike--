#!/usr/bin/env python3
"""
ThinkAlike Project Management Script
"""
import sys
from pathlib import Path

# Add the project root to the Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from backend.run import main
except ImportError:
    print("Error: Could not import main function from backend.run")
    print("Make sure the backend module is properly installed")
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
