#!/usr/bin/env python3
"""
Markdown linting helper script.
Checks markdown files for common issues and suggests fixes.
"""

import os
import re
import sys
import subprocess
import argparse
from pathlib import Path

def find_markdown_files(root_dir='.', exclude_dirs=None):
    """Find all markdown files in the given directory."""
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', 'venv', '.venv', 'dist', 'build']
    
    markdown_files = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    return markdown_files

def check_long_lines(file_path, max_length=120):
    """Check for lines exceeding max_length in the file."""
    long_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines(), 1):
            if len(line) > max_length:
                # Ignore code blocks and tables
                if not re.match(r'^\s*```', line) and not re.match(r'^\s*\|', line):
                    long_lines.append((i, len(line), line.strip()))
    
    return long_lines

def check_multiple_blank_lines(file_path):
    """Check for multiple consecutive blank lines in the file."""
    blank_line_sequences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        blank_count = 0
        start_line = 0
        
        for i, line in enumerate(lines):
            if line.strip() == '':
                if blank_count == 0:
                    start_line = i + 1  # 1-indexed line numbers
                blank_count += 1
            else:
                if blank_count > 1:
                    blank_line_sequences.append((start_line, blank_count))
                blank_count = 0
                
        # Check for multiple blank lines at the end of file
        if blank_count > 1:
            blank_line_sequences.append((start_line, blank_count))
    
    return blank_line_sequences

def check_trailing_spaces(file_path):
    """Check for trailing whitespace in the file."""
    trailing_spaces = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines(), 1):
            if line.rstrip() != line.rstrip('\n'):
                trailing_spaces.append(i)
    
    return trailing_spaces

def main():
    parser = argparse.ArgumentParser(description='Check markdown files for linting issues')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues automatically')
    parser.add_argument('--dir', default='.', help='Directory to search for markdown files')
    args = parser.parse_args()
    
    print(f"Checking markdown files in {args.dir}...")
    
    markdown_files = find_markdown_files(args.dir)
    print(f"Found {len(markdown_files)} markdown files")
    
    issues_found = False
    
    for file_path in markdown_files:
        file_issues = False
        print(f"\nChecking {file_path}")
        
        # Check for long lines
        long_lines = check_long_lines(file_path)
        if long_lines:
            file_issues = True
            print(f"  Line length issues ({len(long_lines)}):")
            for line_num, length, content in long_lines[:5]:  # Show first 5 issues
                print(f"    Line {line_num}: {length} chars - '{content[:50]}...'")
            if len(long_lines) > 5:
                print(f"    ...and {len(long_lines) - 5} more")
        
        # Check for multiple blank lines
        blank_lines = check_multiple_blank_lines(file_path)
        if blank_lines:
            file_issues = True
            print(f"  Multiple consecutive blank lines ({len(blank_lines)}):")
            for start_line, count in blank_lines[:5]:  # Show first 5 issues
                print(f"    Starting at line {start_line}: {count} blank lines")
            if len(blank_lines) > 5:
                print(f"    ...and {len(blank_lines) - 5} more")
        
        # Check for trailing spaces
        trailing_spaces = check_trailing_spaces(file_path)
        if trailing_spaces:
            file_issues = True
            print(f"  Trailing whitespace ({len(trailing_spaces)}):")
            for line_num in trailing_spaces[:5]:  # Show first 5 issues
                print(f"    Line {line_num}")
            if len(trailing_spaces) > 5:
                print(f"    ...and {len(trailing_spaces) - 5} more")
                
        if not file_issues:
            print("  ✅ No issues found")
        else:
            issues_found = True
            
            # Try to fix issues if --fix is provided
            if args.fix:
                try:
                    # Remove trailing whitespace
                    subprocess.run(['sed', '-i', 's/[[:space:]]*$//', file_path], check=True)
                    
                    # Replace multiple blank lines with single blank lines
                    # This requires a more complex sed command
                    subprocess.run(['sed', '-i', '/^$/N;/^\\n$/D', file_path], check=True)
                    
                    print("  🔧 Applied automatic fixes")
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ Error applying fixes: {e}")
    
    if issues_found:
        print("\n⚠️  Markdown linting issues found")
        if not args.fix:
            print("Run with --fix to attempt automatic fixes")
        sys.exit(1)
    else:
        print("\n✅ All markdown files passed checks")

if __name__ == "__main__":
    main()
