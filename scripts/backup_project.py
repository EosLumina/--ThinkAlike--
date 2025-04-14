#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
from pathlib import Path


def backup_project():
    """Create backup of important project files."""
    backup_dir = Path('.backup') / datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Directories to backup
    dirs_to_backup = ['backend', 'frontend', 'docs', 'scripts']

    # Files to backup
    files_to_backup = [
        'requirements.txt',
        'requirements-test.txt',
        'backend/requirements.txt',
        'mkdocs.yml'
    ]

    # Backup directories
    for dir_name in dirs_to_backup:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, backup_dir / dir_name)
            print(f"Backed up {dir_name}/")

    # Backup individual files
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            dest = backup_dir / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest)
            print(f"Backed up {file_path}")


if __name__ == "__main__":
    backup_project()
