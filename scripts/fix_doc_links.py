#!/usr/bin/env python3
import os
import re
from pathlib import Path


def fix_relative_paths(file_path):
    """Fix relative paths in markdown files."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix relative paths
    replacements = [
        (r'\.\./\.\./guides/', '../guides/'),
        (r'\.\./\.\./core/', '../core/'),
        (r'\.\./\.\./components/', '../components/'),
        (r'\.\./\.\./templates/', '../templates/'),
        (r'\.\./\.\./architecture/', '../architecture/'),
        (r'/docs/core/', '../core/'),
        (r'/docs/guides/', '../guides/'),
        (r'/docs/', '../'),
        (r'\.\.\/\.\.\/readme\.md', '../README.md'),
    ]

    for old, new in replacements:
        content = re.sub(old, new, content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("docs directory not found")
        return

    for file_path in docs_dir.rglob('*.md'):
        print(f"Processing {file_path}")
        fix_relative_paths(file_path)


if __name__ == "__main__":
    main()
