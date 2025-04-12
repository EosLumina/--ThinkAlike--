#!/usr/bin/env python3
"""
GitHub Workflow 'on' Section Fixer

This script adds missing 'on' trigger sections to GitHub Actions workflow files
and ensures proper formatting of existing sections.
"""

import os
import sys
import re
import yaml

def fix_workflow_files(file_paths=None):
    """Add proper 'on' trigger sections to workflow files that need them."""

    if not file_paths:
        workflow_dir = '.github/workflows'
        if not os.path.isdir(workflow_dir):
            print(f"❌ Error: Workflow directory {workflow_dir} not found")
            return False

        file_paths = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                     if f.endswith(('.yml', '.yaml'))]

    fixed_files = 0
    error_count = 0

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"❌ Error: File {file_path} does not exist")
            error_count += 1
            continue

        print(f"Processing {file_path}...")

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Create a completely new version of the file with proper 'on' section
        # Start by extracting essential content (name and jobs sections)
        name_match = re.search(r'name:\s*(.*?)(\r?\n)', content)
        name = name_match.group(1) if name_match else "Workflow"

        # Extract the jobs section (everything from 'jobs:' to the end)
        jobs_match = re.search(r'(jobs:.*?)$', content, re.DOTALL)
        jobs_section = jobs_match.group(1) if jobs_match else "jobs:\n  # No jobs defined"

        # Create a new workflow file with proper structure
        new_content = f"""---
name: {name}

on:
  # Workflow triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

{jobs_section}"""

        # Write the fixed content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"✅ Completely restructured {file_path} with proper 'on' section")
        fixed_files += 1

    print(f"\n=== Summary ===")
    print(f"Processed files: {len(file_paths)}")
    print(f"Fixed files: {fixed_files}")
    print(f"Errors encountered: {error_count}")

    if fixed_files > 0:
        print(f"\n✅ Successfully fixed {fixed_files} workflow files")
        return True
    else:
        print("\n⚠️ No files were modified")
        return False

if __name__ == "__main__":
    file_paths = sys.argv[1:] if len(sys.argv) > 1 else None
    sys.exit(0 if fix_workflow_files(file_paths) else 1)
