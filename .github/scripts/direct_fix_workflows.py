#!/usr/bin/env python3
"""
Direct fix for GitHub workflow files missing 'on' trigger definitions.
This script takes a more aggressive approach by completely replacing or
prepending the trigger section rather than trying to parse and modify the files.
"""

import os
import yaml
import sys
from pathlib import Path

def fix_workflow_file(file_path):
    """
    Fix a workflow file by directly prepending the 'on' trigger section.
    """
    try:
        # Read the original content
        with open(file_path, 'r') as f:
            content = f.read().strip()

        # Check if 'on:' already exists at the start of a line
        if '\non:' in f"\n{content}" or content.startswith('on:'):
            return False  # Already has an 'on' trigger

        # Determine appropriate trigger based on file name
        if 'test' in file_path.lower() or 'ci' in file_path.lower():
            trigger = """on:
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
            trigger = """on:
  push:
    branches: [main]
    tags:
      - 'v*.*.*'
  workflow_dispatch:

"""
        elif 'doc' in file_path.lower():
            trigger = """on:
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
            trigger = """on:
  schedule:
    - cron: "0 0 * * 0"  # Run weekly on Sundays
  workflow_dispatch:

"""
        else:
            # Default trigger
            trigger = """on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

"""

        # Create a completely new file
        with open(file_path, 'w') as f:
            # If there's a name line, keep it at the top
            if content.startswith('name:'):
                name_end = content.find('\n')
                if name_end != -1:
                    f.write(content[:name_end+1] + '\n')
                    f.write(trigger)
                    f.write(content[name_end+1:])
                else:
                    f.write(content + '\n')
                    f.write(trigger)
            else:
                f.write(trigger + content)

        print(f"✅ Fixed {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    # Define problematic files that need fixing
    problem_files = [
        ".github/workflows/consolidated-ci.yml",
        ".github/workflows/fixed_consolidated-ci.yml",
        ".github/workflows/fixed_run-tests.yml",
        ".github/workflows/fixed_documentation.yml",
        ".github/workflows/deploy_to_gh_pages.yml",
        ".github/workflows/fixed_settings.yml",
        ".github/workflows/fixed_deploy_to_gh_pages.yml",
        ".github/workflows/unified-workflow.yml",
        ".github/workflows/run-tests.yml",
        ".github/workflows/deploy.yml",
        ".github/workflows/documentation.yml",
        ".github/workflows/settings.yml",
        ".github/workflows/fixed_deploy.yml",
    ]

    fixed = 0
    for file_path in problem_files:
        if os.path.exists(file_path):
            if fix_workflow_file(file_path):
                fixed += 1

    print(f"\n✅ Fixed {fixed} workflow files")
    print("Run validation to verify:")
    print("python .github/scripts/validate_workflows.py")

if __name__ == "__main__":
    main()
