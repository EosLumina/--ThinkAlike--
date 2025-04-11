#!/usr/bin/env python3
"""
Script to fix common markdown linting issues across the project
"""

import os
import re
import sys
from pathlib import Path

def fix_markdown_linting(content):
    """Fix common markdown linting issues"""
    
    # Fix MD032: Lists should be surrounded by blank lines
    # Pattern: text followed immediately by a list item
    content = re.sub(r'([^\n])\n([\*\-\+])', r'\1\n\n\2', content)
    
    # Pattern: list item followed immediately by non-list text
    content = re.sub(r'([\*\-\+].*)\n([^\s\*\-\+\n])', r'\1\n\n\2', content)
    
    # Fix MD022: Headers should be surrounded by blank lines
    content = re.sub(r'([^\n])\n(#+\s)', r'\1\n\n\2', content)
    content = re.sub(r'(#+.*)\n([^\n\s#])', r'\1\n\n\2', content)
    
    # Fix MD023: Headers must start at the beginning of the line
    content = re.sub(r'\n\s+(#+\s)', r'\n\n\1', content)
    
    # Fix MD031: Fenced code blocks should be surrounded by blank lines
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    content = re.sub(r'```\n([^\n\s])', r'