#!/usr/bin/env python3
"""
A focused validator script that only checks for proper 'on' section formatting
in GitHub Actions workflow files.
"""

import os
import sys
import re
from pathlib import Path

def verify_on_section(file_path):
    """Verify if a workflow file has a properly formatted 'on' section"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for 'on:' with regex
        on_match = re.search(r'(?:^|\n)\s*on\s*:', content)
        if not on_match:
            print(f"❌ {file_path}: Missing 'on:' section")
            return False

        print(f"✅ {file_path}: Contains 'on:' section")
        return True

    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def main():
    """Check all workflow files in the repository"""
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return 1

    workflow_files = list(workflows_dir.glob("*.yml"))

    if not workflow_files:
        print("No workflow files found")
        return 0

    print(f"Found {len(workflow_files)} workflow files")

    valid_count = 0
    invalid_count = 0

    for file_path in workflow_files:
        if verify_on_section(file_path):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\nResults: {valid_count} valid files, {invalid_count} invalid files")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
