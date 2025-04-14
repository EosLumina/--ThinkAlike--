#!/usr/bin/env python3
"""
Fix markdown files by updating repository references and badge URLs.
"""

import os
import re
import sys
from pathlib import Path

def fix_markdown_file(file_path):
    """Fix repository references and badge URLs in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Save original content to check if changes were made
        original_content = content

        # Fix repository references
        content = re.sub(r'EosLumina/ThinkAlike', r'EosLumina/--ThinkAlike--', content)

        # Fix badge URLs
        badge_pattern = r'\[\!\[(.*?)\]\((https://github\.com/EosLumina/ThinkAlike/.*?)\)\]\((.*?)\)'
        badge_replacement = r'[![\1](https://github.com/EosLumina/--ThinkAlike--\2)](https://github.com/EosLumina/--ThinkAlike--\3)'
        content = re.sub(badge_pattern, badge_replacement, content)

        # Only write back if changes were made
        if original_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {file_path}")
            return True
        else:
            print(f"No changes needed in {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix markdown files provided as arguments or in default locations."""
    files_to_fix = sys.argv[1:] if len(sys.argv) > 1 else list(Path('.').rglob('*.md'))

    print("Fixing markdown files...")

    fixed_count = 0
    for file in files_to_fix:
        if fix_markdown_file(file):
            fixed_count += 1

    print(f"Fixed {fixed_count} file(s)")

if __name__ == "__main__":
    main()
