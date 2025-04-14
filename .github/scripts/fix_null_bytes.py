#!/usr/bin/env python3
"""
Fix Python files containing null bytes, which cause 'ValueError: source code string cannot contain null bytes'
"""

import os
import re
import sys
from pathlib import Path

def fix_file_null_bytes(file_path):
    """Remove null bytes from a file."""
    try:
        # First try to read the file normally
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

    except UnicodeDecodeError:
        # For binary-like files with serious encoding issues
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Remove null bytes from binary content
            content = content.replace(b'\x00', b'')

            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"✅ Fixed binary file {file_path}")
            return True
        except Exception as e:
            print(f"⚠️ Error fixing binary file {file_path}: {e}")
            return False
    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")
        return False

def main():
    """Fix null bytes in Python files."""
    # Get list of Python files specified as arguments or scan the entire repository
    files_to_fix = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files_to_fix:
        print("Scanning for Python files in the repository...")
        repo_files = Path('.').rglob('*.py')
        files_to_fix = [str(f) for f in repo_files]

    if not files_to_fix:
        print("No Python files found to fix.")
        return

    print(f"Found {len(files_to_fix)} files to check.")

    fixed_count = 0
    for file in files_to_fix:
        if fix_file_null_bytes(file):
            fixed_count += 1

    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()
