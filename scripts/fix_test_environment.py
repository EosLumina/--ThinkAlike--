#!/usr/bin/env python3
"""
Test Environment Repair Tool

This script addresses two common issues in ThinkAlike's test environment:
1. Missing test dependencies (httpx, pandas)
2. Corrupted Python files containing null bytes
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def display_banner(title):
    """Display a formatted banner title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def install_dependencies():
    """Install missing dependencies required by tests."""
    display_banner("Installing Test Dependencies")

    # Define required packages
    dependencies = [
        "httpx>=0.24.0",     # Required for FastAPI TestClient
        "pandas>=2.0.0",     # Required for ethical compliance tests
        "pytest>=7.3.1",     # Ensure consistent pytest version
        "pytest-cov>=4.1.0"  # For test coverage
    ]

    print(f"Installing {len(dependencies)} packages...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + dependencies,
            check=True
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def fix_corrupted_files():
    """Fix Python files with null bytes."""
    display_banner("Fixing Corrupted Files")

    # Files identified from error logs
    corrupted_files = [
        "backend/app/development/ai_application_developer.py",
        "backend/app/documentation/doc_parser.py",
        "backend/app/services/value_based_matcher.py"
    ]

    fixed_files = 0
    for file_path in corrupted_files:
        full_path = Path(file_path)
        if not full_path.exists():
            print(f"⚠️ File not found: {file_path}")
            continue

        print(f"Processing {file_path}...")

        # Create backup
        backup_path = full_path.with_suffix(full_path.suffix + ".bak")
        try:
            shutil.copy2(full_path, backup_path)
            print(f"  ✓ Backup created: {backup_path}")
        except Exception as e:
            print(f"  ❌ Failed to create backup: {e}")
            continue

        # Remove null bytes
        try:
            content = full_path.read_bytes()
            fixed_content = content.replace(b'\x00', b'')

            if content != fixed_content:
                full_path.write_bytes(fixed_content)
                print(f"  ✅ Removed null bytes from {file_path}")
                fixed_files += 1
            else:
                print(f"  ℹ️ No null bytes found in {file_path}")
        except Exception as e:
            print(f"  ❌ Error fixing file: {e}")
            try:
                shutil.copy2(backup_path, full_path)
                print(f"  ↩️ Restored original file from backup")
            except Exception as restore_err:
                print(f"  ⚠️ Failed to restore backup: {restore_err}")

    print(f"\nFixed {fixed_files} of {len(corrupted_files)} corrupted files")
    return fixed_files > 0

def create_test_requirements():
    """Create a requirements-test.txt file with test dependencies."""
    display_banner("Creating Test Requirements File")

    requirements = [
        "# Test dependencies for ThinkAlike",
        "httpx>=0.24.0",
        "pandas>=2.0.0",
        "pytest>=7.3.1",
        "pytest-cov>=4.1.0",
        "fastapi>=0.95.0"  # Include FastAPI for tests
    ]

    req_path = "requirements-test.txt"
    try:
        with open(req_path, "w") as f:
            f.write("\n".join(requirements))
        print(f"✅ Created {req_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating requirements file: {e}")
        return False

def create_github_workflow():
    """Create GitHub workflow file for tests."""
    display_banner("Creating GitHub Workflow")

    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)

    workflow_path = workflow_dir / "run-tests.yml"

    workflow_content = """# GitHub workflow for running ThinkAlike tests
name: Run Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements-test.txt ]; then
            pip install -r requirements-test.txt
          else
            pip install httpx pandas pytest pytest-cov
          fi
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi

      - name: Fix corrupted files
        run: |
          python -c "
import pathlib;
files = [
  'backend/app/development/ai_application_developer.py',
  'backend/app/documentation/doc_parser.py',
  'backend/app/services/value_based_matcher.py'
];
for f in files:
  p = pathlib.Path(f);
  if p.exists():
    content = p.read_bytes();
    fixed = content.replace(b'\\\\x00', b'');
    p.write_bytes(fixed);
    print(f'Fixed {f}' if content != fixed else f'No nulls in {f}');
          "

      - name: Run tests
        run: |
          pytest
"""

    try:
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
        print(f"✅ Created GitHub workflow at {workflow_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating workflow file: {e}")
        return False

def main():
    """Main function."""
    display_banner("ThinkAlike Test Environment Repair")

    # Install dependencies
    install_dependencies()

    # Fix corrupted files
    fix_corrupted_files()

    # Create requirements file
    create_test_requirements()

    # Create GitHub workflow
    create_github_workflow()

    display_banner("Next Steps")
    print("1. Run tests:")
    print("   pytest")
    print("2. Add the new files to Git:")
    print("   git add requirements-test.txt .github/workflows/run-tests.yml")
    print("3. Push changes to GitHub:")
    print("   git commit -m \"fix: resolve test environment issues\"")
    print("   git push")

if __name__ == "__main__":
    main()
