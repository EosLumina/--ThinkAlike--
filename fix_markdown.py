#!/usr/bin/env python3
import os
import re

def fix_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Store original for comparison
    original = content
    
    # Fix: Remove "Document End" lines
    content = re.sub(r'\n+## Document End.*', '', content)
    content = re.sub(r'\n+---\n+## Document End.*', '', content)
    
    # Fix: MD022 (blank lines around headings)
    content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6} .+)\n([^\n])', r'\1\n\n\2', content)
    
    # Fix: MD007 & MD030 (list indentation and spaces)
    content = re.sub(r'^(\s*)\*\s{2,}', r'\1* ', content, flags=re.MULTILINE)
    
    # Only write if changes were made
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.lower().endswith('.md'):
            path = os.path.join(root, file)
            if fix_markdown_file(path):
                print(f"Fixed: {path}")
                count += 1

print(f"\nFixed {count} markdown files")
