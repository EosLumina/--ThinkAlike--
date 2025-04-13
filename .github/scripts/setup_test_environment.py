#!/usr/bin/env python3
"""
Set up test environment by installing required dependencies
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, text=True)
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")
        return False
    return True

def setup_test_environment():
    """Install test dependencies and ensure environment is ready for testing."""
    # Check if requirements-test.txt exists
    if not os.path.exists('requirements-test.txt'):
        print("⚠️ requirements-test.txt not found. Creating default file...")
        with open('requirements-test.txt', 'w') as f:
            f.write("""# Testing dependencies
pytest>=8.0.0
pytest-cov>=6.0.0
httpx>=0.24.0  # Required by starlette.testclient
pandas>=2.0.0  # Required by tests/test_ethical_compliance.py
""")

    # Install regular requirements first
    if os.path.exists('requirements.txt'):
        print("📦 Installing project dependencies...")
        if not run_command('pip install -r requirements.txt'):
            print("⚠️ Failed to install project dependencies")
            return False

    # Install test dependencies
    print("📦 Installing test dependencies...")
    if not run_command('pip install -r requirements-test.txt'):
        print("⚠️ Failed to install test dependencies")
        return False

    # Fix any files with null bytes
    print("🔍 Checking for files with null bytes...")
    fix_script_path = '.github/scripts/fix_null_bytes.py'

    if not os.path.exists(fix_script_path):
        print("⚠️ fix_null_bytes.py script not found.")
        return False

    if not run_command(f'python {fix_script_path}'):
        print("⚠️ Failed to fix files with null bytes")
        return False

    print("✅ Test environment setup complete!")
    return True

if __name__ == "__main__":
    success = setup_test_environment()
    if not success:
        sys.exit(1)
