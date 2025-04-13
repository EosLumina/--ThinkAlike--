#!/usr/bin/env python3
"""
Fix null bytes in test files that cause "ValueError: source code string cannot contain null bytes".
"""

import os
import sys
from pathlib import Path

def fix_file_with_null_bytes(file_path):
    """Remove null bytes from a file."""
    try:
        print(f"Processing {file_path}...")

        # Try to read the file with errors ignored
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check if there are null bytes
        if '\0' in content:
            print(f"Found null bytes in {file_path}")
            # Remove null bytes
            content = content.replace('\0', '')

            # Write back the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {file_path}")
            return True
        else:
            print(f"No null bytes found in {file_path}")
            return False
    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")

        # Try with binary mode as a fallback
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Remove null bytes from binary content
            content = content.replace(b'\x00', b'')

            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"✅ Fixed binary file {file_path}")
            return True
        except Exception as e2:
            print(f"⚠️ Failed to fix binary file {file_path}: {e2}")
            return False

def main():
    """Fix test files with null bytes."""
    test_dir = Path('tests')
    if not test_dir.exists():
        print(f"Test directory {test_dir} not found!")
        return False

    # Get list of Python files in the tests directory
    test_files = test_dir.glob('**/*.py')
    files_to_fix = [str(f) for f in test_files]

    if not files_to_fix:
        print("No test files found!")
        return False

    print(f"Found {len(files_to_fix)} test files to check")

    fixed_count = 0
    for file in files_to_fix:
        if fix_file_with_null_bytes(file):
            fixed_count += 1

    print(f"Fixed {fixed_count} files with null bytes")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
