#!/usr/bin/env python3
"""
Verify workflow files have proper 'on' triggers defined
"""
import os
import sys
from pathlib import Path
import re

def verify_workflow(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for 'on:' section using regex
        on_section = re.search(r'\non\s*:', content)

        if not on_section:
            print(f"❌ {file_path}: Missing 'on' trigger section")
            return False

        print(f"✅ {file_path}: Found 'on' trigger")
        return True
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def main():
    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found")
        return 1

    # List of problematic files
    problem_files = [
        "consolidated-ci.yml",
        "fixed_consolidated-ci.yml",
        "fixed_run-tests.yml",
        "fixed_documentation.yml",
        "deploy_to_gh_pages.yml",
        "fixed_settings.yml",
        "fixed_deploy_to_gh_pages.yml",
        "unified-workflow.yml",
        "run-tests.yml",
        "deploy.yml",
        "documentation.yml",
        "settings.yml",
        "fixed_deploy.yml"
    ]

    valid_count = 0
    invalid_count = 0

    # Check all the known problematic files
    for filename in problem_files:
        file_path = workflows_dir / filename
        if file_path.exists():
            if verify_workflow(file_path):
                valid_count += 1
            else:
                invalid_count += 1

    print(f"Results: {valid_count} valid, {invalid_count} invalid")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
