#!/usr/bin/env python

import re
import os

def fix_requirements():
    """Fix common issues in requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("requirements.txt not found")
        return

    with open('requirements.txt', 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    has_changes = False

    for line in lines:
        original = line
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            fixed_lines.append(original)
            continue

        # Fix local package references that can break in CI
        if line.startswith('-e ') or line.startswith('.'):
            print(f"⚠️ Commenting out local package reference: {line}")
            fixed_lines.append(f"# {original} # Commented by fix_requirements.py\n")
            has_changes = True
            continue

        # Ensure great_expectations has a specific version
        if line.startswith('great_expectations') and '==' not in line:
            fixed_line = 'great_expectations==0.15.50\n'
            print(f"Changed: {line} → {fixed_line.strip()}")
            fixed_lines.append(fixed_line)
            has_changes = True
            continue

        fixed_lines.append(original)

    if has_changes:
        # Backup original
        os.rename('requirements.txt', 'requirements.txt.bak')

        with open('requirements.txt', 'w') as f:
            f.writelines(fixed_lines)

        print("✅ requirements.txt has been fixed and original backed up to requirements.txt.bak")
    else:
        print("No issues found in requirements.txt")

if __name__ == "__main__":
    fix_requirements()
