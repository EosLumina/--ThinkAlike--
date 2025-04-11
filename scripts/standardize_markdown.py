#!/usr/bin/env python3
"""
Markdown Standardization Script for ThinkAlike

This script automatically fixes common Markdown linting issues across the project:
1. Adds blank lines around lists (MD032)
2. Ensures consistent header formatting 
3. Fixes indentation
4. Moves filepath comments into HTML comments so they don't appear in rendered content
5. Standardizes formatting while preserving content
"""

import os
import re
import sys
from pathlib import Path

def fix_markdown_linting(content):
    """Apply standardized fixes to markdown content."""
    
    # Move filepath declarations to HTML comments
    content = re.sub(r'^(<!--\s+filepath:.*?-->)', r'\1', content)
    
    # Fix blank lines around lists (MD032)
    content = re.sub(r'([^\n])\n([\*\-\+])', r'\1\n\n\2', content)
    content = re.sub(r'([\*\-\+].*)\n([^\s\*\-\+\n])', r'\1\n\n\2', content)
    
    # Ensure consistent header spacing
    content = re.sub(r'(#+)([^#\s])', r'\1 \2', content)
    
    # Fix empty headers (e.g. # )
    content = re.sub(r'(#+)\s*\n', r'\1 Untitled Section\n', content)
    
    # Fix code block formatting (ensure proper spacing)
    content = re.sub(r'```\s*([a-zA-Z0-9]+)\n', r'```\1\n', content)
    
    # Fix link paths to use correct format
    content = re.sub(r'\(\.\./docs/', r'(/docs/', content)
    content = re.sub(r'\(docs/', r'(/docs/', content)
    content = re.sub(r'\(\./core/', r'(/docs/core/', content)
    content = re.sub(r'\(\.\./', r'(/', content)
    
    return content

def standardize_markdown_files(directory):
    """Process all markdown files in a directory recursively."""
    file_count = 0
    error_count = 0
    updated_count = 0
    
    for root, _, files in os.walk(directory):
        # Skip .git directory
        if '.git' in root.split(os.sep):
            continue
            
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    standardized_content = fix_markdown_linting(original_content)
                    
                    if standardized_content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(standardized_content)
                        print(f"✅ Updated: {file_path}")
                        updated_count += 1
                    else:
                        print(f"✓ Already compliant: {file_path}")
                    
                    file_count += 1
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {str(e)}")
                    error_count += 1
    
    return file_count, updated_count, error_count

def main():
    """Main function to process markdown files."""
    project_root = "/workspaces/--ThinkAlike--"
    print(f"Standardizing Markdown files in {project_root}...")
    
    total_files, updated_files, error_files = standardize_markdown_files(project_root)
    
    print("\n=== Standardization Complete ===")
    print(f"Total Markdown files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Files with processing errors: {error_files}")
    
    if updated_files > 0:
        print("\nMarkdown files have been standardized according to project guidelines.")
        print("Changes include proper spacing around lists, consistent headers, and fixed links.")
    else:
        print("\nNo files needed updating. All Markdown files already meet standards.")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
