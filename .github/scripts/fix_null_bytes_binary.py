#!/usr/bin/env python3
"""
Fix null bytes in Python files using binary mode for more reliable detection and repair.
"""

import os
import sys
from pathlib import Path

def fix_file_with_null_bytes(file_path):
    """Remove null bytes from a file using binary mode."""
    try:
        print(f"Processing {file_path}...")
        fixed = False

        # Read in binary mode to properly detect all null bytes
        with open(file_path, 'rb') as f:
            content = f.read()

        # Check for null bytes in binary content
        if b'\x00' in content:
            print(f"Found null bytes in {file_path}")
            # Replace null bytes
            cleaned_content = content.replace(b'\x00', b'')

            # Write back in binary mode
            with open(file_path, 'wb') as f:
                f.write(cleaned_content)
            print(f"✅ Fixed {file_path}")
            fixed = True

        return fixed
    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")
        return False

def main():
    """Fix test files with null bytes using binary mode."""
    # Get file paths from args or default to test directory
    if len(sys.argv) > 1:
        files_to_fix = [f for f in sys.argv[1:] if os.path.exists(f)]
    else:
        test_dir = Path('tests')
        if not test_dir.exists():
            print(f"Test directory {test_dir} not found!")
            return False

        # Get list of Python files in the tests directory
        files_to_fix = [str(f) for f in test_dir.glob('**/*.py')]

    if not files_to_fix:
        print("No test files found!")
        return False

    print(f"Found {len(files_to_fix)} files to check")

    fixed_count = 0
    for file in files_to_fix:
        if fix_file_with_null_bytes(file):
            fixed_count += 1

    print(f"Fixed {fixed_count} files with null bytes")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
