#!/usr/bin/env python3
"""
Fix missing 'on' triggers in GitHub workflow files - Enhanced version
"""

import os
import yaml
import sys
from pathlib import Path
import re

# YAML handling is more strict than what GitHub Actions accepts
# This function will directly modify files without YAML parsing when needed
def fix_workflow_file(file_path, force=False):
    """Add missing 'on' trigger to workflow file"""
    try:
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()

        # First try normal YAML parsing
        try:
            yaml_content = yaml.safe_load(content)
            has_on_field = 'on' in yaml_content
        except Exception as e:
            print(f"⚠️ YAML parsing issue in {file_path}: {e}")
            has_on_field = 'on:' in content

        if not has_on_field or force:
            print(f"Adding 'on' trigger to {file_path}")

            # Determine appropriate triggers based on file name
            if 'test' in file_path.lower() or 'ci' in file_path.lower():
                on_trigger = """
on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'tests/**'
      - 'requirements*.txt'
  pull_request:
    branches: [main]
  workflow_dispatch:
"""
            elif 'deploy' in file_path.lower() or 'cd' in file_path.lower() or 'gh_pages' in file_path.lower():
                on_trigger = """
on:
  push:
    branches: [main]
    tags:
      - 'v*.*.*'
  workflow_dispatch:
"""
            elif 'doc' in file_path.lower():
                on_trigger = """
on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '*.md'
  pull_request:
    branches: [main]
  workflow_dispatch:
"""
            elif 'settings' in file_path.lower():
                on_trigger = """
on:
  schedule:
    - cron: "0 0 * * 0"  # Run weekly on Sundays
  workflow_dispatch:
"""
            else:
                # Default trigger
                on_trigger = """
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
"""

            # Insert trigger after name more robustly
            if 'name:' in content:
                # Find the line that starts with 'name:' and match the line ending
                name_pattern = r'(name:.*?)(\r?\n)'
                modified_content = re.sub(name_pattern, r'\1\2' + on_trigger, content, count=1)

                # If that didn't work, try an alternative approach
                if modified_content == content:
                    parts = content.split('name:', 1)
                    name_line_end = parts[1].find('\n')
                    if name_line_end != -1:
                        modified_content = parts[0] + 'name:' + parts[1][:name_line_end+1] + on_trigger + parts[1][name_line_end+1:]
                    else:
                        modified_content = content + on_trigger
            else:
                # If there's no name field, just add the trigger at the beginning
                modified_content = on_trigger + content

            # Write the modified content back
            with open(file_path, 'w') as f:
                f.write(modified_content)

            return True
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")

    return False

def check_workflow_validity(file_path):
    """Check if workflow file has valid 'on' trigger"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Simple text-based check for 'on:' field
        if 'on:' not in content:
            return False

        # Basic structure check using YAML
        try:
            yaml_content = yaml.safe_load(content)
            return 'on' in yaml_content and yaml_content['on'] is not None
        except:
            # If YAML parsing fails, fall back to simple check
            return 'on:' in content
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def main():
    """Main function to fix workflow files"""
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return

    # Find all workflow files
    workflow_files = list(workflows_dir.glob("*.yml"))

    if not workflow_files:
        print("No workflow files found")
        return

    print(f"Found {len(workflow_files)} workflow files")

    # First pass: Fix files that don't have 'on' trigger
    fixed_count = 0
    for workflow_file in workflow_files:
        if fix_workflow_file(str(workflow_file)):
            fixed_count += 1

    print(f"First pass: Fixed {fixed_count} workflow files")

    # Second pass: Force fix for any remaining issues
    problem_files = []
    for workflow_file in workflow_files:
        if not check_workflow_validity(str(workflow_file)):
            problem_files.append(workflow_file)

    if problem_files:
        print(f"Found {len(problem_files)} files that still need fixing")
        for workflow_file in problem_files:
            if fix_workflow_file(str(workflow_file), force=True):
                fixed_count += 1

    print(f"Total fixed: {fixed_count} workflow files")
    print("Run validation to see if all issues are resolved:")
    print("python .github/scripts/validate_workflows.py")

if __name__ == "__main__":
    main()
