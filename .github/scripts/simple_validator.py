#!/usr/bin/env python3
"""
A simple validator for GitHub Actions workflow files.
This script checks if workflow files have the basic required structure.
"""

import os
import sys
from pathlib import Path
import yaml
import re

def validate_workflow_file(file_path):
    """
    Validate a GitHub Actions workflow file.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for 'on:' trigger with regular expression first
        if not re.search(r'(^|\n)on:', content):
            print(f"❌ {file_path.name}: No 'on:' trigger found (string check)")
            return False

        # Try parsing as YAML
        try:
            data = yaml.safe_load(content)

            # Check for minimum required structure
            if not data:
                print(f"❌ {file_path.name}: Empty YAML")
                return False

            if 'on' not in data:
                print(f"❌ {file_path.name}: Missing 'on' section (YAML check)")
                return False

            if not data['on']:
                print(f"❌ {file_path.name}: Empty 'on' section")
                return False

            if 'jobs' not in data:
                print(f"❌ {file_path.name}: Missing 'jobs' section")
                return False

            print(f"✅ {file_path.name}: Valid workflow file")
            return True

        except yaml.YAMLError as e:
            print(f"❌ {file_path.name}: YAML parsing error - {e}")
            return False

    except Exception as e:
        print(f"❌ {file_path.name}: Error reading file - {e}")
        return False

def main():
    """
    Main function to validate all workflow files.
    """
    # Make sure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')

    workflows_dir = Path('.github/workflows')

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return 1

    workflow_files = list(workflows_dir.glob('*.yml'))

    if not workflow_files:
        print("No workflow files found")
        return 0

    print(f"Found {len(workflow_files)} workflow files")

    valid_count = 0
    invalid_count = 0

    for workflow_file in workflow_files:
        if validate_workflow_file(workflow_file):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\nResults: {valid_count} valid files, {invalid_count} invalid files")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
