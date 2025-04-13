#!/usr/bin/env python3
"""
Fix the workflow validation script or provide a simple alternative validator
"""

import os
import yaml
import sys
from pathlib import Path
import re

def validate_workflow(file_path):
    """Validate if a GitHub workflow file has correct structure"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for basic syntax errors
        try:
            data = yaml.safe_load(content)
            if data is None:
                print(f"❌ {file_path}: Empty or invalid YAML")
                return False

            # Check for required sections
            if 'on' not in data:
                print(f"❌ {file_path}: Missing 'on' trigger definition")
                return False

            if 'jobs' not in data:
                print(f"❌ {file_path}: Missing 'jobs' section")
                return False

            # Additional checks can be added here if needed

            print(f"✅ {file_path}: Valid workflow file")
            return True

        except yaml.YAMLError as e:
            print(f"❌ {file_path}: YAML parsing error - {e}")
            return False

    except Exception as e:
        print(f"❌ {file_path}: Error reading file - {e}")
        return False

def main():
    """Validate all workflow files in .github/workflows directory"""
    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return 1

    # Find all workflow files
    workflow_files = list(workflows_dir.glob("*.yml"))

    if not workflow_files:
        print("No workflow files found")
        return 0

    print(f"Found {len(workflow_files)} workflow files")

    # Validate each workflow file
    valid_count = 0
    invalid_count = 0

    for workflow_file in workflow_files:
        if validate_workflow(workflow_file):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\nResults: {valid_count} valid files, {invalid_count} invalid files")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
