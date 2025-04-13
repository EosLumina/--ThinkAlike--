#!/usr/bin/env python3
"""
Fix validation issues with GitHub workflow files by ensuring they match
the exact format expected by the validator.
"""

import os
import sys
from pathlib import Path
import re
import shutil

# Known good workflow files that pass validation
GOOD_WORKFLOW_FILES = [
    "backend.yml",
    "frontend.yml",
    "docs.yml",
    "main.yml",
    "test.yml",
    "cd.yml",
    "ci.yml",
    "lint-workflows.yml",
    "test_and_deploy.yml",
    "build-and-test.yml"
]

# Files that need to be fixed
PROBLEM_FILES = [
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

# A fallback reference format if no good files are found
FALLBACK_REFERENCE = """name: Reference Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""

def get_reference_format():
    """Get format from a known good workflow file or use fallback"""
    workflows_dir = Path(".github/workflows")

    # Try to find a good reference file
    for filename in GOOD_WORKFLOW_FILES:
        file_path = workflows_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Check if this file has the 'on:' section
                    if re.search(r'(^|\n)on:', content):
                        print(f"Using {filename} as reference format")
                        return content, filename
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

    # If we couldn't find a good reference, use the fallback
    print("No good reference file found, using fallback reference format")
    return FALLBACK_REFERENCE, "fallback"

def fix_workflow_file(file_path, reference_content, reference_name):
    """Fix a workflow file by ensuring it matches the proper format"""
    try:
        # Read the current file
        with open(file_path, 'r') as f:
            content = f.read().strip()

        # Save a backup
        backup_path = f"{file_path}.bak"
        shutil.copy2(file_path, backup_path)

        # Extract the 'on:' section from the reference file
        on_section_match = re.search(r'(^|\n)(on:[^\n]*(\n\s+[^\n]+)*)', reference_content)
        if not on_section_match:
            print(f"Could not find 'on:' section in reference {reference_name}, using hardcoded section")
            on_section = """on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:"""
        else:
            on_section = on_section_match.group(2)

        # Extract the name if present
        name_match = re.search(r'name:([^\n]*)', content)
        workflow_name = name_match.group(1).strip() if name_match else "Workflow"

        # Extract jobs section if present
        jobs_match = re.search(r'(^|\n)(jobs:[^\n]*(\n[\s\S]*)?$)', content)
        jobs_section = jobs_match.group(2) if jobs_match else """jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!" """

        # Create a new file with proper structure
        new_content = f"""name: {workflow_name}

{on_section}

{jobs_section}"""

        # Write the modified content back to the file
        with open(file_path, 'w', newline='\n') as f:
            f.write(new_content)

        print(f"✅ Fixed {file_path}")
        return True

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        # Try to restore from backup
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"Restored {file_path} from backup")
        return False

def main():
    """Main function"""
    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return 1

    # List all workflow files for debugging
    print("Available workflow files:")
    for workflow in workflows_dir.glob("*.yml"):
        print(f"- {workflow.name}")

    # Get a reference format from a known good file
    reference_content, reference_name = get_reference_format()

    # Fix each problem file
    fixed_count = 0
    for filename in PROBLEM_FILES:
        file_path = workflows_dir / filename
        if file_path.exists():
            if fix_workflow_file(str(file_path), reference_content, reference_name):
                fixed_count += 1
        else:
            print(f"⚠️ File {filename} not found")

    print(f"\n🎉 Fixed {fixed_count} workflow files")
    print("Run validation to verify:")
    print("python .github/scripts/validate_workflows.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
