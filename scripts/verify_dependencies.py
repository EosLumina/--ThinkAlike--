#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path


def check_requirements_file(filepath):
    """Verify all packages in a requirements file can be installed."""
    if not Path(filepath).exists():
        print(f"Warning: {filepath} not found")
        return True

    try:
        # Try installing in check-only mode
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", filepath, "--dry-run"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {filepath} dependencies are installable")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error checking {filepath}:")
        print(e.stderr)
        return False


def main():
    files_to_check = [
        "requirements.txt",
        "requirements-test.txt",
        "backend/requirements.txt"
    ]

    success = True
    for req_file in files_to_check:
        if not check_requirements_file(req_file):
            success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
