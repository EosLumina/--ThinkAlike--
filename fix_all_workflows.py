#!/usr/bin/env python3
"""
Fix All GitHub Workflow Files

This script runs a series of fixes to ensure all workflow files are valid:
1. Fixes docs.yml with a clean, correct version
2. Adds 'on' sections to all other workflow files
3. Runs the workflow validator to check if all issues are fixed
"""

import os
import sys
import subprocess

# Import the specific fixes
try:
    from fix_docs_yml import fix_docs_yml
    from fix_workflow_on_sections import fix_workflow_files
except ImportError:
    print("❌ Error: Required fix scripts not found. Make sure fix_docs_yml.py and fix_workflow_on_sections.py exist.")
    sys.exit(1)

def ensure_yaml_installed():
    """Make sure PyYAML is installed."""
    try:
        import yaml
        print("✅ PyYAML is already installed")
    except ImportError:
        print("⚠️ Installing PyYAML...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML"])
            print("✅ PyYAML installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyYAML. Please install it manually: pip install PyYAML")
            return False
    return True

def run_workflow_validator(fix=True):
    """Run the workflow validator to check if all issues are fixed."""
    print("\nRunning workflow validator to check results...")

    args = [sys.executable, "workflow_validator.py"]
    if fix:
        args.append("--fix")

    try:
        subprocess.run(args, check=True)
        print("✅ Workflow validator completed successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Workflow validator found remaining issues")
        return False

def main():
    """Fix all workflow files and validate the results."""
    # Ensure PyYAML is installed
    if not ensure_yaml_installed():
        return 1

    # Step 1: Fix docs.yml specifically
    print("\n=== Step 1: Fixing docs.yml ===")
    fix_docs_yml()

    # Step 2: Fix all other workflows
    print("\n=== Step 2: Fixing all other workflow files ===")
    workflow_dir = '.github/workflows'
    file_paths = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                  if f.endswith(('.yml', '.yaml')) and f != 'docs.yml']
    fix_workflow_files(file_paths)

    # Step 3: Run workflow validator to check results
    print("\n=== Step 3: Validating results ===")
    success = run_workflow_validator(fix=True)

    if success:
        print("\n✅ All workflow files have been fixed successfully!")
        return 0
    else:
        print("\n⚠️ Some issues may remain. Please check the validator output.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
