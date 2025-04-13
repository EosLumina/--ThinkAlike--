"""
Helper script to fix import errors in tests.
"""
import os
import sys

def add_project_root_to_path():
    """Add the project root to Python path to ensure imports work."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"Added {project_root} to Python path")
    return project_root
