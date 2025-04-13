#!/usr/bin/env python3
"""
Comprehensive test setup script for ThinkAlike project.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a shell command and capture output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"Error: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def fix_null_bytes():
    """Fix null bytes in Python files."""
    script_path = Path(".github/scripts/fix_null_bytes_binary.py")
    if not script_path.exists():
        print(f"Script {script_path} not found!")
        return False

    success, output = run_command(f"python {script_path}")
    print(output)
    return success

def ensure_test_dependencies():
    """Ensure all test dependencies are installed."""
    # Create requirements-test.txt if it doesn't exist
    if not Path("requirements-test.txt").exists():
        with open("requirements-test.txt", "w") as f:
            f.write("""
# Test dependencies for ThinkAlike
pytest>=7.0.0
pytest-cov>=4.0.0
pandas>=1.0.0
httpx>=0.23.0
""")

    # Install dependencies
    success, _ = run_command("pip install -r requirements-test.txt")
    return success

def create_basic_test():
    """Create a basic test file to verify setup."""
    test_file = Path("tests/test_basic.py")
    if not test_file.exists():
        test_dir = Path("tests")
        test_dir.mkdir(exist_ok=True)

        with open(test_file, "w") as f:
            f.write("""
def test_basic():
    \"\"\"Basic test to verify test setup.\"\"\"
    assert True, "Basic test should pass"

def test_imports():
    \"\"\"Test that imports can be resolved.\"\"\"
    try:
        from tests.helpers.fix_imports import add_project_root_to_path
        add_project_root_to_path()

        # Try importing backend modules
        import backend
        assert backend is not None
    except ImportError as e:
        assert False, f"Import failed: {e}"
""")
    return True

def main():
    """Set up the test environment."""
    print("Setting up test environment for ThinkAlike...")

    # Ensure we're in the project root
    if not Path(".github").exists() and Path("../.github").exists():
        os.chdir("..")

    # Create basic directory structure if it doesn't exist
    for directory in ["tests", "tests/helpers", "tests/backend"]:
        Path(directory).mkdir(exist_ok=True)

    # Fix null bytes in Python files
    if not fix_null_bytes():
        print("Warning: Failed to fix null bytes in Python files.")

    # Ensure test dependencies are installed
    if not ensure_test_dependencies():
        print("Warning: Failed to install test dependencies.")

    # Create basic test file
    if not create_basic_test():
        print("Warning: Failed to create basic test file.")

    print("\nTest environment setup complete!")
    print("\nTry running: pytest tests/test_basic.py -v")

if __name__ == "__main__":
    main()
