#!/usr/bin/env python3
"""
Fix README.md badges to ensure they use the correct repository reference.
"""

import re
from pathlib import Path

def fix_readme_badges():
    """Fix repository references in README.md badges."""
    readme_path = 'README.md'

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix repository references in badges
        incorrect_pattern = r'EosLumina/ThinkAlike'
        correct_pattern = r'EosLumina/--ThinkAlike--'

        # Save original content to check if changes are made
        original_content = content

        # Replace all occurrences
        content = re.sub(incorrect_pattern, correct_pattern, content)

        # Write back if changes were made
        if original_content != content:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed badges in {readme_path}")
            return True
        else:
            print(f"No changes needed in {readme_path}")
            return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False

def fix_all_markdown_files():
    """Fix repository references in all markdown files."""
    markdown_files = Path('.').rglob('*.md')
    fixed_count = 0

    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix repository references in badges
            incorrect_pattern = r'EosLumina/ThinkAlike'
            correct_pattern = r'EosLumina/--ThinkAlike--'

            # Save original content to check if changes are made
            original_content = content

            # Replace all occurrences
            content = re.sub(incorrect_pattern, correct_pattern, content)

            # Write back if changes were made
            if original_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Fixed badges in {file_path}")
                fixed_count += 1
            else:
                print(f"No changes needed in {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Total files fixed: {fixed_count}")

if __name__ == "__main__":
    fix_readme_badges()
    fix_all_markdown_files()
