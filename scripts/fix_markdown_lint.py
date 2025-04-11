#!/usr/bin/env python3
"""
Script to automatically fix common markdown linting issues in documentation files.
"""
import os
import re
import sys
from pathlib import Path

def fix_markdown_lint_issues(file_path):
    """Fix common markdown linting issues in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix MD032: Lists should be surrounded by blank lines
    content = re.sub(r'([^\n])\n([\*\-\+]|\d+\.)', r'\1\n\n\2', content)
    
    # Fix MD022: Headings should be surrounded by blank lines
    content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6} .*)\n([^\n])', r'\1\n\n\2', content)
    
    # Fix MD047: Files should end with a single newline character
    if not content.endswith('\n'):
        content += '\n'
    content = re.sub(r'\n+$', '\n', content)
    
    # Fix MD004: Change dash lists to asterisk lists
    content = re.sub(r'^(\s*)-\s', r'\1* ', content, flags=re.MULTILINE)
    
    # Fix MD030: Spaces after list markers
    content = re.sub(r'^(\s*\d+)\.\s\s+', r'\1. ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*[\*\-\+])\s\s+', r'\1 ', content, flags=re.MULTILINE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main function to find and fix markdown files."""
    if len(sys.argv) > 1:
        # Process specific file
        fix_markdown_lint_issues(sys.argv[1])
        print(f"Fixed linting issues in {sys.argv[1]}")
    else:
        # Process all markdown files in the docs directory
        for file_path in Path('docs').rglob('*.md'):
            fix_markdown_lint_issues(str(file_path))
            print(f"Fixed linting issues in {file_path}")

if __name__ == "__main__":
    main()