#!/usr/bin/env python3
"""
Verification script to check if all GitHub workflow files are properly formatted.

This script scans all workflow files and verifies that they have valid 'on' sections
and conform to other GitHub Actions standards.
"""

import os
import yaml
import sys
from pathlib import Path

def verify_workflow_file(file_path):
    """Verify that a GitHub workflow file is properly formatted."""
    print(f"Verifying {file_path}...")

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Check for document start marker
        if not content.startswith('---'):
            print(f"⚠️ Warning: {file_path} is missing document start marker '---'")

        # Parse YAML content
        yaml_content = yaml.safe_load(content)

        # Check for required sections
        if not yaml_content.get('name'):
            print(f"⚠️ Warning: {file_path} is missing 'name' attribute")

        # Verify 'on' section
        if 'on' not in yaml_content:
            print(f"❌ Error: {file_path} is missing 'on' section")
            return False

        on_section = yaml_content['on']

        # Check type of 'on' section
        if isinstance(on_section, str):
            print(f"✓ {file_path} has simple 'on' trigger: {on_section}")
        elif isinstance(on_section, dict):
            if not on_section:
                print(f"❌ Error: {file_path} has empty 'on' section")
                return False

            valid_triggers = set(on_section.keys())
            print(f"✓ {file_path} has 'on' triggers: {', '.join(valid_triggers)}")
        else:
            print(f"❌ Error: {file_path} has invalid 'on' section type: {type(on_section).__name__}")
            return False

        # Check jobs section
        if 'jobs' not in yaml_content:
            print(f"❌ Error: {file_path} is missing 'jobs' section")
            return False

        if not yaml_content['jobs']:
            print(f"❌ Error: {file_path} has empty 'jobs' section")
            return False

        # Check job properties
        for job_id, job in yaml_content['jobs'].items():
            if not isinstance(job, dict):
                print(f"❌ Error: Job '{job_id}' in {file_path} has invalid format")
                return False

            if 'runs-on' not in job:
                print(f"❌ Error: Job '{job_id}' in {file_path} is missing 'runs-on' attribute")
                return False

            if 'steps' not in job:
                print(f"❌ Error: Job '{job_id}' in {file_path} is missing 'steps' attribute")
                return False

        print(f"✅ {file_path} is valid")
        return True

    except yaml.YAMLError as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def main():
    """Verify all workflow files in the .github/workflows directory."""
    workflow_dir = '.github/workflows'

    if not os.path.exists(workflow_dir):
        print(f"❌ Error: Workflow directory {workflow_dir} not found")
        return 1

    workflow_files = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                     if f.endswith(('.yml', '.yaml'))]

    if not workflow_files:
        print(f"⚠️ Warning: No workflow files found in {workflow_dir}")
        return 0

    all_valid = True
    for file_path in workflow_files:
        if not verify_workflow_file(file_path):
            all_valid = False

    if all_valid:
        print("\n✅ All workflow files are valid")
        return 0
    else:
        print("\n❌ Some workflow files have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
