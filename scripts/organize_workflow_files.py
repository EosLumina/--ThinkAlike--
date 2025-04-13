#!/usr/bin/env python3
"""
Organize workflow files in the ThinkAlike repository.
This script helps identify and organize GitHub Actions workflow files.
"""

import os
import shutil
from pathlib import Path
import re

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        ".github/workflows",
        ".github/scripts",
        "scripts/workflows",
        "archive/workflows"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Ensured directory exists: {directory}")

def identify_workflow_files():
    """Identify workflow-related files in the root directory"""
    workflow_files = []
    workflow_patterns = [
        r".*workflow.*\.(yml|yaml|sh|py|js)$",
        r".*deploy.*\.(yml|yaml|sh|py)$",
        r".*gh[-_]pages.*\.(yml|yaml|sh|py)$",
        r".*action.*\.(yml|yaml)$",
        r"^fix_.*\.(py|sh)$"
    ]

    # Get all files in root directory
    for item in os.listdir("."):
        if os.path.isfile(item):
            for pattern in workflow_patterns:
                if re.match(pattern, item, re.IGNORECASE):
                    workflow_files.append(item)
                    break

    return workflow_files

def suggest_organization(workflow_files):
    """Suggest organization for workflow files"""
    if not workflow_files:
        print("No workflow-related files found in the root directory.")
        return

    print(f"\nFound {len(workflow_files)} workflow-related files in root directory:\n")

    for file in workflow_files:
        _, ext = os.path.splitext(file)

        # Determine the best location based on file type
        if ext.lower() in ['.yml', '.yaml']:
            suggested_location = ".github/workflows"
        elif ext.lower() in ['.sh', '.py', '.js']:
            if "fix" in file.lower() or "validate" in file.lower():
                suggested_location = ".github/scripts"
            else:
                suggested_location = "scripts/workflows"
        else:
            suggested_location = "scripts/workflows"

        print(f"- {file:<30} → {suggested_location}")

    print("\nCommands to organize these files:")
    print("--------------------------------")

    for file in workflow_files:
        _, ext = os.path.splitext(file)

        # Determine the best location based on file type
        if ext.lower() in ['.yml', '.yaml']:
            suggested_location = ".github/workflows"
        elif ext.lower() in ['.sh', '.py', '.js']:
            if "fix" in file.lower() or "validate" in file.lower():
                suggested_location = ".github/scripts"
            else:
                suggested_location = "scripts/workflows"
        else:
            suggested_location = "scripts/workflows"

        print(f"mv {file} {suggested_location}/")

def main():
    """Main function"""
    print("🔄 ThinkAlike Workflow File Organizer")
    print("====================================\n")

    # Create directories
    create_directories()

    # Identify workflow files
    workflow_files = identify_workflow_files()

    # Suggest organization
    suggest_organization(workflow_files)

    print("\n✨ Done. Review the suggestions above and run the commands manually.")
    print("Always verify before moving any files to ensure nothing important is misplaced.")

if __name__ == "__main__":
    main()
