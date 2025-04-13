#!/usr/bin/env python3
"""
Fix repository references in markdown and YAML files.
Converts incorrect 'EosLumina/ThinkAlike' to 'EosLumina/--ThinkAlike--'.
"""

import os
import re
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'='*20} {text} {'='*20}{Style.RESET_ALL}\n")

def print_success(text):
    """Print a success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def fix_file(file_path):
    """Fix repository references in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace incorrect repository references
        incorrect_pattern = r'EosLumina/ThinkAlike'
        correct_pattern = r'EosLumina/--ThinkAlike--'

        # Save original content to check if changes are made
        original_content = content

        # Replace all occurrences
        content = re.sub(incorrect_pattern, correct_pattern, content)

        # Only write back if changes were made
        if original_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print_success(f"Fixed references in {file_path}")
            return 1
        return 0
    except Exception as e:
        print_warning(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Fix repository references in all markdown and YAML files."""
    print_header("Fixing Repository References")

    # Find all markdown and YAML files
    md_files = Path('.').rglob('*.md')
    yml_files = Path('.').rglob('*.yml')

    # Combine file lists
    files = list(md_files) + list(yml_files)

    # Skip files in .git directory
    files = [f for f in files if '.git/' not in str(f)]

    # Track statistics
    fixes = 0
    processed = 0

    # Process all files
    for file_path in files:
        processed += 1
        fixes += fix_file(file_path)

    print_header("Summary")
    print(f"Processed {processed} files")
    print(f"Fixed {fixes} files")

if __name__ == "__main__":
    main()
