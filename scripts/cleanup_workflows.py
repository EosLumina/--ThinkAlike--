#!/usr/bin/env python3
import os
import shutil


def cleanup_workflows():
    """Remove redundant workflow files."""
    workflow_dir = ".github/workflows"
    backup_dir = f"{workflow_dir}/backup"

    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # List of workflow files to keep
    keep_files = {
        "build-and-test.yml",
        "deploy.yml",
        "docs.yml"
    }

    # Move other workflow files to backup
    for filename in os.listdir(workflow_dir):
        if filename.endswith(".yml") and filename not in keep_files:
            src = f"{workflow_dir}/{filename}"
            dst = f"{backup_dir}/{filename}"
            print(f"Moving {src} to {dst}")
            shutil.move(src, dst)


if __name__ == "__main__":
    cleanup_workflows()
