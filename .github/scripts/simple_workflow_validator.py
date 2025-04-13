#!/usr/bin/env python3
"""
A simple validator for GitHub Actions workflow files.
This script checks if workflow files have the required structure with proper 'on' format.
"""

import os
import sys
import yaml
from pathlib import Path

def validate_workflow(file_path):
    """Validate a workflow file's structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML content
        try:
            data = yaml.safe_load(content)

            # Check if YAML structure is valid
            if not data:
                print(f"❌ {file_path.name}: Empty YAML structure")
                return False

            # Check for 'on' section (may be quoted or unquoted)
            on_key = None
            for key in data:
                if str(key).lower() == "on" or str(key).lower() == "'on'" or str(key).lower() == '"on"':
                    on_key = key
                    break

            if not on_key:
                print(f"❌ {file_path.name}: Missing 'on' trigger definition")
                return False

            # Check if the 'on' section has content
            if not data[on_key]:
                print(f"❌ {file_path.name}: Empty 'on' trigger definition")
                return False

            # Check for jobs section
            if 'jobs' not in data:
                print(f"❌ {file_path.name}: Missing 'jobs' section")
                return False

            if not data['jobs']:
                print(f"❌ {file_path.name}: Empty 'jobs' section")
                return False

            print(f"✅ {file_path.name}: Valid workflow structure")
            return True

        except yaml.YAMLError as e:
            print(f"❌ {file_path.name}: YAML parsing error - {e}")
            return False

    except Exception as e:
        print(f"❌ {file_path.name}: Error reading file - {e}")
        return False

def main():
    """Validate all workflow files"""
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

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
        if validate_workflow(file_path):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\nResults: {valid_count} valid files, {invalid_count} invalid files")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
