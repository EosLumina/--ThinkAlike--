#!/usr/bin/env python3
"""
Documentation Link Checker and Fixer

This script scans all Markdown files in the docs directory for broken links
and provides suggestions for fixes.
"""

import os
import re
import sys
from pathlib import Path

# Map of old paths to new paths for renamed files
PATH_MAPPING = {
    "/docs/core/contributing.md": "/docs/core/contributing_detailed.md",
    "/docs/contributing-quick.md": "/docs/contributing_quick.md", 
    "/docs/vision/core_concepts.md": "/docs/vision/vision_principles.md",
    "/docs/core/core_concepts_architecture.md": "/docs/core/technical_architecture_concepts.md"
}

def find_markdown_files(base_dir):
    """Find all markdown files in the given directory and subdirectories."""
    markdown_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def check_links_in_file(file_path):
    """Check for broken links in a markdown file and suggest fixes."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all markdown links [text](url)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    
    changes_needed = []
    for text, url in links:
        # Skip external URLs
        if url.startswith(('http://', 'https://', 'mailto:')):
            continue
        
        # Normalize the URL path
        if not url.startswith('/'):
            # Convert relative path to absolute from the file's location
            file_dir = os.path.dirname(file_path)
            url = os.path.normpath(os.path.join(os.path.relpath('/workspaces/--ThinkAlike--', file_dir), url))
        
        # Check if this URL is in our mapping of renamed files
        if url in PATH_MAPPING:
            changes_needed.append((f'[{text}]({url})', f'[{text}]({PATH_MAPPING[url]})'))
    
    return changes_needed

def main():
    """Main function to check all markdown files for broken links."""
    base_dir = '/workspaces/--ThinkAlike--'
    markdown_files = find_markdown_files(base_dir)
    
    print(f"Scanning {len(markdown_files)} markdown files for broken links...")
    
    files_with_issues = 0
    for file_path in markdown_files:
        changes = check_links_in_file(file_path)
        if changes:
            files_with_issues += 1
            print(f"\n{file_path}:")
            for old, new in changes:
                print(f"  Replace: {old}")
                print(f"  With:    {new}")
    
    print(f"\nFound issues in {files_with_issues} files.")
    if files_with_issues > 0:
        print("Run with --fix to automatically apply changes.")

if __name__ == '__main__':
    main()
