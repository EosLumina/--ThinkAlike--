#!/usr/bin/env python3
"""Clean up workflow files by moving old ones to backup."""

import os
import shutil
import yaml
from pathlib import Path

# Constants
WORKFLOW_DIR = Path('.github/workflows')
BACKUP_DIR = WORKFLOW_DIR / 'backup'
ESSENTIAL_FILES = {
    'build-and-test.yml',
    'deploy.yml',
    'docs.yml'
}


def print_header(msg):
    """Print a formatted header."""
    print(f"\n=== {msg} ===")


def print_success(msg):
    """Print a success message."""
    print(f"✓ {msg}")


def print_warning(msg):
    """Print a warning message."""
    print(f"! {msg}")


def print_error(msg):
    """Print an error message."""
    print(f"✕ {msg}")


def backup_workflow(file_path):
    """Create a backup of the workflow file."""
    source = Path(file_path)
    dest = BACKUP_DIR / source.name
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.copy2(source, dest)
    print_success(f"Created backup of {source.name}")


def cleanup_workflows():
    """Move all workflows except the main one to backup."""
    print_header("Starting workflow cleanup")

    # Create backup directory
    BACKUP_DIR.mkdir(exist_ok=True)

    # Move non-essential workflows to backup
    for file_path in WORKFLOW_DIR.glob('*.yml'):
        if file_path.name not in ESSENTIAL_FILES:
            backup_workflow(file_path)
            file_path.unlink()
            print_success(f"Moved {file_path.name} to backup")

    print_header("Cleanup complete")
    print("Run 'git status' to review changes")


if __name__ == "__main__":
    cleanup_workflows()
