#!/usr/bin/env python3
"""
Fix GitHub Workflow 'on' Trigger Sections

This script addresses the common "Workflow missing 'on' trigger section" validation error
by ensuring every GitHub workflow file has a correctly formatted trigger section.
"""

import os
import re
import yaml
import sys

def fix_workflow_on_section(file_path):
    """Fix the 'on' trigger section in a GitHub workflow file."""
    print(f"Processing {file_path}...")

    with open(file_path, 'r') as file:
        content = file.read()

    # Store original content for comparison
    original_content = content

    try:
        # Parse YAML content
        yaml_content = yaml.safe_load(content)

        if not yaml_content:
            print(f"⚠️ Warning: {file_path} appears to be empty or invalid YAML")
            return False

        # Check if 'on' section exists and is properly structured
        if 'on' not in yaml_content:
            print(f"❌ Error: 'on' section missing from {file_path}")
            # Add a basic 'on' section for workflow
            new_content = re.sub(
                r'^(name:.*?)(\r?\n+)(jobs:)',
                r'\1\2on:\n  # Workflow triggers\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n\n\3',
                content,
                flags=re.MULTILINE | re.DOTALL
            )

            if new_content == content:  # If regex didn't match, try another approach
                # Try inserting after the document start
                new_content = re.sub(
                    r'^(---\s*\r?\n+)(.*?)',
                    r'\1\2\non:\n  # Workflow triggers\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n\n',
                    content,
                    flags=re.MULTILINE | re.DOTALL
                )

            if new_content != content:
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"✅ Added basic 'on' section to {file_path}")
                return True
            else:
                print(f"⚠️ Unable to automatically add 'on' section to {file_path}")
                return False
        elif isinstance(yaml_content['on'], str) or not yaml_content['on']:
            # Convert simple string trigger (e.g., 'on: push') to a proper structure
            print(f"⚠️ Simple 'on' trigger found in {file_path}, expanding to full structure")
            trigger_type = yaml_content['on'] if isinstance(yaml_content['on'], str) else "push"

            # Replace the simple trigger with a structured one
            new_content = re.sub(
                r'on:\s*([\w-]+)?\s*\r?\n',
                f"on:\n  # Workflow triggers\n  {trigger_type}:\n    branches: [main]\n",
                content,
                flags=re.MULTILINE
            )

            if new_content != content:
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"✅ Expanded simple 'on' trigger to full structure in {file_path}")
                return True
            else:
                print(f"⚠️ Unable to automatically expand 'on' trigger in {file_path}")
                return False
        else:
            # 'on' section exists with structure, but may not be recognized correctly
            # Ensure it's formatted according to GitHub Actions expectations
            print(f"✓ 'on' section exists in {file_path}, ensuring correct format")

            # Try to fix common formatting issues in the 'on' section
            on_section = yaml_content['on']
            has_changes = False

            # Ensure 'on' section has at least one trigger type
            if not on_section:
                yaml_content['on'] = {'push': {'branches': ['main']}}
                has_changes = True

            if has_changes:
                # Create new content with fixed 'on' section
                new_yaml = yaml.safe_dump(yaml_content, default_flow_style=False)

                with open(file_path, 'w') as file:
                    file.write(new_yaml)
                print(f"✅ Fixed 'on' section structure in {file_path}")
                return True

            return False
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML in {file_path}: {e}")
        # If YAML parsing fails, try a regex-based approach to add 'on' section
        if "on:" not in content:
            # Find where to insert the 'on' section (after name, before jobs)
            new_content = re.sub(
                r'^(name:.*?)(\r?\n+)(jobs:)',
                r'\1\2on:\n  # Workflow triggers\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n\n\3',
                content,
                flags=re.MULTILINE | re.DOTALL
            )

            if new_content != content:
                with open(file_path, 'w') as file:
                    file.write(new_content)
                print(f"✅ Added 'on' section to {file_path} using regex")
                return True

        return False

def main():
    """Process all workflow files or specific ones if provided as arguments."""
    # Get workflow files from arguments or default directory
    workflow_files = []

    if len(sys.argv) > 1:
        workflow_files = sys.argv[1:]
    else:
        workflow_dir = '.github/workflows'
        if os.path.isdir(workflow_dir):
            workflow_files = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                             if f.endswith(('.yml', '.yaml'))]
        else:
            print(f"❌ Error: Default workflow directory {workflow_dir} not found")
            return 1

    fixed_count = 0
    error_count = 0

    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: File {file_path} does not exist")
            error_count += 1
            continue

        if fix_workflow_on_section(file_path):
            fixed_count += 1

    print(f"\n=== Summary ===")
    print(f"Processed files: {len(workflow_files)}")
    print(f"Files fixed: {fixed_count}")
    print(f"Errors encountered: {error_count}")

    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} workflow files")
    else:
        print(f"\n⚠️ No files were modified")

    return 0

if __name__ == "__main__":
    sys.exit(main())
