#!/usr/bin/env python3
"""Clean up workflow files."""

import os
import shutil
from pathlib import Path

# Constants
WORKFLOW_DIR = Path('.github/workflows')
BACKUP_DIR = WORKFLOW_DIR / 'backup'
ESSENTIAL_FILES = {
    'build-and-test.yml',
    'deploy.yml',
    'docs.yml'
}


def cleanup_workflows():
    """Move all workflows except essential ones to backup."""
    print("\n=== Starting workflow cleanup ===")

    # Create backup directory
    BACKUP_DIR.mkdir(exist_ok=True)

    # Move non-essential workflows to backup
    for file_path in WORKFLOW_DIR.glob('*.yml'):
        if file_path.name not in ESSENTIAL_FILES:
            dest = BACKUP_DIR / file_path.name
            print(f"Moving {file_path.name} to backup")
            shutil.move(str(file_path), str(dest))

    print("=== Cleanup complete ===")
    print("Run 'git status' to review changes")


if __name__ == "__main__":
    cleanup_workflows()
