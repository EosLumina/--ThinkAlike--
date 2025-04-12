#!/usr/bin/env python3
"""
GitHub Workflow YAML Fixer

This script fixes common issues in GitHub workflow YAML files:
1. Adds missing document start markers (---)
2. Fixes spacing inside brackets ([ main ] → [main])
3. Ensures proper 'on' section formatting
4. Converts Python-style booleans (True/False) to YAML style (true/false)

Usage: python fix_github_workflows.py [workflow_file.yml]
"""

import os
import sys
import re
import yaml

def fix_workflow_file(file_path):
    """Fix common issues in GitHub workflow files."""
    print(f"Fixing {file_path}...")

    with open(file_path, 'r') as file:
        content = file.read()

    # Store original content to check for changes
    original_content = content

    # Fix 1: Add document start marker if missing
    if not content.startswith('---'):
        content = f"---\n{content}"
        print(f"✅ Added document start marker")

    # Fix 2: Fix spacing inside brackets
    if re.search(r'\[ +', content) or re.search(r' +\]', content):
        content = re.sub(r'\[ +', '[', content)
        content = re.sub(r' +\]', ']', content)
        print(f"✅ Fixed bracket spacing")

    # Fix 3: Ensure proper 'on' section format
    if 'on:' in content and not re.search(r'on:\s*\n\s+\w+:', content):
        content = re.sub(r'on:\s*(\w+):', r'on:\n  \1:', content)
        print(f"✅ Fixed 'on' section format")

    # Fix 4: Fix boolean values
    if re.search(r':\s*True\b', content) or re.search(r':\s*False\b', content):
        content = re.sub(r':\s*True\b', r': true', content)
        content = re.sub(r':\s*False\b', r': false', content)
        print(f"✅ Converted Python-style booleans to YAML style")

    # Fix 5: Fix if statement in shell commands (space issue)
    if re.search(r'if\s*\[-', content):
        content = re.sub(r'if\s*\[-', r'if [ -', content)
        print(f"✅ Fixed 'if' statement in shell commands")

    # Write changes back to file
    if content != original_content:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"✅ Saved changes to {file_path}")
    else:
        print(f"ℹ️ No changes needed for {file_path}")

    # Validate the file using pyyaml
    try:
        yaml_content = yaml.safe_load(content)
        if yaml_content and isinstance(yaml_content, dict):
            if 'on' in yaml_content:
                print(f"✅ Validated: 'on' section present")
            else:
                print(f"❌ Validation failed: 'on' section missing")
            if 'jobs' in yaml_content:
                print(f"✅ Validated: 'jobs' section present")
            else:
                print(f"❌ Validation failed: 'jobs' section missing")
        else:
            print(f"❌ Validation failed: Invalid YAML structure")
    except yaml.YAMLError as e:
        print(f"❌ YAML validation error: {e}")

def main():
    """Main function to process workflow files."""
    # If files specified as arguments, process those
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    # Otherwise, find all workflow files
    else:
        workflow_dir = '.github/workflows'
        if not os.path.exists(workflow_dir):
            print(f"❌ Error: Workflow directory {workflow_dir} not found")
            return 1

        files = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                if f.endswith(('.yml', '.yaml'))]

    # Process each file
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"❌ Error: File {file_path} does not exist")
            continue

        fix_workflow_file(file_path)
        print()  # Empty line for spacing

    return 0

if __name__ == "__main__":
    sys.exit(main())
