#!/usr/bin/env python3
# filepath: fix_readme.py

with open('README.md', 'r') as f:
    content = f.read()

# Remove the duplicated badge section
import re
fixed_content = re.sub(
    r'\n\n\n\[\!\[License: MIT\].*\[\!\[Frontend Status\].*\)\n',
    '\n\n',
    content
)

with open('README.md', 'w') as f:
    f.write(fixed_content)

print("✅ Fixed duplicated badges in README.md")
