#!/usr/bin/env python3
"""
Update the workflow validator to better detect 'on' sections.

This script adds a more robust detection mechanism for GitHub Actions 'on' triggers.
"""

import os
import re
import sys

def update_validator_script(validator_path='workflow_validator.py'):
    """Update the workflow validator script to better detect 'on' sections."""
    print(f"Updating validator at {validator_path}...")

    if not os.path.exists(validator_path):
        print(f"❌ Error: Validator file {validator_path} not found")
        return False

    with open(validator_path, 'r') as file:
        content = file.read()

    # Store original content for comparison
    original_content = content

    # Find the _validate_on_section method
    on_section_method = re.search(r'def\s+_validate_on_section\([^)]*\):\s*.*?(?=def\s+|$)',
                                 content, re.DOTALL)

    # Create improved on section validation method
    improved_on_section = '''
    def _validate_on_section(self, file_path, yaml_content):
        """Validate the 'on' section of a workflow file."""
        if 'on' not in yaml_content:
            self.add_error(file_path, f"'on' section is missing. Add trigger events like 'push', 'pull_request', etc.")
            return False

        on_section = yaml_content['on']

        # 'on' can be a string (e.g., 'push') or a dictionary with event types
        if isinstance(on_section, str):
            # Simple trigger like 'on: push' is valid
            self.log(f"Found simple 'on' trigger: {on_section}")
            return True

        elif isinstance(on_section, dict):
            # Empty dict is invalid
            if not on_section:
                self.add_error(file_path, f"'on' section is empty. Add trigger events.")
                return False

            # Check if at least one valid event type is specified
            valid_events = {'push', 'pull_request', 'workflow_dispatch', 'schedule',
                           'repository_dispatch', 'issues', 'issue_comment',
                           'watch', 'release', 'page_build', 'deployment',
                           'deployment_status', 'status', 'label', 'milestone',
                           'public', 'project', 'project_card', 'project_column',
                           'discussion', 'discussion_comment', 'registry_package', 'check_run',
                           'check_suite', 'workflow_run', 'create', 'delete', 'fork'}

            events = set(on_section.keys())
            if not events.intersection(valid_events):
                self.add_error(file_path, f"'on' section doesn't contain any valid event types. Valid events include: push, pull_request, workflow_dispatch, etc.")
                return False

            self.log(f"Found valid 'on' triggers: {', '.join(events)}")
            return True

        else:
            self.add_error(file_path, f"'on' section has invalid type: {type(on_section).__name__}")
            return False
    '''

    if on_section_method:
        # Replace existing method with improved version
        new_content = content.replace(on_section_method.group(0), improved_on_section)
        print("✅ Replaced existing _validate_on_section method")
    else:
        # Method doesn't exist, let's find where to add it
        # Look for a class definition with methods
        class_match = re.search(r'class\s+\w+.*?:', content)
        if class_match:
            # Insert after the first method definition
            method_match = re.search(r'def\s+\w+\([^)]*\):', content)
            if method_match:
                # Find end of method
                method_end = content.find('def ', method_match.end())
                if method_end != -1:
                    new_content = content[:method_end] + improved_on_section + content[method_end:]
                    print("✅ Added _validate_on_section method after existing method")
                else:
                    # Add at the end of file
                    new_content = content + "\n" + improved_on_section
                    print("✅ Added _validate_on_section method to end of file")
            else:
                # No methods found, add after class definition
                new_content = content.replace(class_match.group(0), class_match.group(0) + "\n" + improved_on_section)
                print("✅ Added _validate_on_section method after class definition")
        else:
            # Create a simple class with the method
            validator_class = '''
class WorkflowValidator:
    """Validator for GitHub Actions workflow files."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []

    def log(self, message):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def add_error(self, file_path, message):
        """Add an error message."""
        self.errors.append((file_path, message))
        print(f"❌ Error in {file_path}: {message}")
''' + improved_on_section

            new_content = content + "\n\n" + validator_class
            print("✅ Created WorkflowValidator class with _validate_on_section method")

    if new_content == content:
        print("⚠️ No changes made to the validator")
        return False

    with open(validator_path, 'w') as file:
        file.write(new_content)

    print("✅ Updated validator with improved 'on' section detection")
    return True

if __name__ == "__main__":
    validator_path = 'workflow_validator.py'
    if len(sys.argv) > 1:
        validator_path = sys.argv[1]

    update_validator_script(validator_path)
