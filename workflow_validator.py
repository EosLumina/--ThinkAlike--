#!/usr/bin/env python3
"""
GitHub Actions Workflow Validator

This script validates GitHub Actions workflow files to ensure they are properly formatted
and contain all required sections.
"""

import os
import sys
import re
import yaml
from typing import Dict, List, Tuple, Optional, Any, Set

class WorkflowValidator:
    """Validator for GitHub Actions workflow files."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.fixes = []

    def log(self, message: str) -> None:
        """Log verbose messages if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def add_error(self, file_path: str, message: str, line: int = None, fixed: bool = False) -> None:
        """Add an error message with optional line number."""
        location = f" at line {line}" if line else ""
        self.errors.append((file_path, f"{message}{location}", fixed))
        if not self.verbose and not fixed:
            print(f"❌ Error in {file_path}{location}: {message}")

    def add_warning(self, file_path: str, message: str, line: int = None, fixed: bool = False) -> None:
        """Add a warning message with optional line number."""
        location = f" at line {line}" if line else ""
        self.warnings.append((file_path, f"{message}{location}", fixed))
        if not self.verbose and not fixed:
            print(f"⚠️ Warning in {file_path}{location}: {message}")

    def add_fix(self, file_path: str, message: str) -> None:
        """Add a fix message."""
        self.fixes.append((file_path, message))
        if not self.verbose:
            print(f"🔧 Fixed in {file_path}: {message}")

    def validate_and_fix_workflows(self, file_paths: List[str], fix: bool = False) -> bool:
        """
        Validate and optionally fix all specified workflow files.

        Args:
            file_paths: List of workflow file paths to validate
            fix: Whether to attempt fixing issues

        Returns:
            bool: True if all files are valid (or fixed), False otherwise
        """
        all_valid = True

        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"❌ Error: File {file_path} does not exist")
                all_valid = False
                continue

            try:
                is_valid = self.validate_and_fix_workflow(file_path, fix)
                all_valid = all_valid and is_valid
            except Exception as e:
                self.add_error(file_path, f"Unexpected error during validation: {e}")
                all_valid = False

        # Print summary
        if self.verbose:
            print("\n=== Validation Summary ===")
            print(f"Files processed: {len(file_paths)}")
            print(f"Errors found: {len([e for e in self.errors if not e[2]])}")
            print(f"Warnings found: {len([w for w in self.warnings if not w[2]])}")
            if fix:
                print(f"Fixes applied: {len(self.fixes)}")
                print(f"Errors fixed: {len([e for e in self.errors if e[2]])}")
                print(f"Warnings fixed: {len([w for w in self.warnings if w[2]])}")

            if self.errors:
                print("\n=== Errors ===")
                for file_path, message, fixed in self.errors:
                    status = "[FIXED]" if fixed else ""
                    print(f"{file_path}: {message} {status}")

            if self.warnings:
                print("\n=== Warnings ===")
                for file_path, message, fixed in self.warnings:
                    status = "[FIXED]" if fixed else ""
                    print(f"{file_path}: {message} {status}")

            if fix and self.fixes:
                print("\n=== Fixes Applied ===")
                for file_path, message in self.fixes:
                    print(f"{file_path}: {message}")

        return all_valid

    def validate_and_fix_workflow(self, file_path: str, fix: bool = False) -> bool:
        """
        Validate and optionally fix a single workflow file.

        Args:
            file_path: Path to the workflow file
            fix: Whether to attempt fixing issues

        Returns:
            bool: True if file is valid (or fixed), False otherwise
        """
        self.log(f"Validating {file_path}...")

        # Read the original content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        original_content = content

        # Perform checks and fixes
        is_valid = True

        # Check 1: Document start marker
        if not content.startswith('---'):
            self.add_warning(file_path, "Missing document start marker '---'")
            if fix:
                content = f"---\n{content}"
                self.add_fix(file_path, "Added document start marker '---'")

        # Check 2: Fix bracket spacing
        if re.search(r'\[ +', content) or re.search(r' +\]', content):
            self.add_warning(file_path, "Inconsistent spacing inside brackets")
            if fix:
                content = re.sub(r'\[ +', '[', content)
                content = re.sub(r' +\]', ']', content)
                self.add_fix(file_path, "Fixed spacing inside brackets")

        # Try to parse YAML to validate structure
        try:
            yaml_content = yaml.safe_load(content)
            if yaml_content is None:
                self.add_error(file_path, "File appears to be empty or invalid YAML")
                is_valid = False
            else:
                # Directly check for jobs in content
                jobs_match = re.search(r'^\s*jobs\s*:', content, re.MULTILINE)
                if not jobs_match:
                    self.add_error(file_path, "Jobs section is missing")
                    is_valid = False

                # Check for basic structure
                if not self._validate_workflow_structure(file_path, yaml_content, content):
                    is_valid = False

                # Check jobs section
                if not self._validate_jobs_section(file_path, yaml_content, content):
                    is_valid = False

                # If YAML parsing succeeded but jobs don't appear in the parsed YAML
                if 'jobs' not in yaml_content and jobs_match:
                    self.log(f"Warning: Found 'jobs:' in content but not in parsed YAML. Possible YAML parsing issue.")

        except yaml.YAMLError as e:
            self.add_error(file_path, f"Invalid YAML: {e}")
            is_valid = False

        # Save changes if fixing is enabled and content has changed
        if fix and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            self.log(f"Updated {file_path}")

        return is_valid

    def _validate_workflow_structure(self, file_path: str, yaml_content: Dict, raw_content: str) -> bool:
        """
        Validate the basic structure of a workflow file including 'on' section.

        Args:
            file_path: Path to the workflow file
            yaml_content: Parsed YAML content
            raw_content: Raw file content as string

        Returns:
            bool: True if structure is valid, False otherwise
        """
        is_valid = True

        # Check for name
        if not yaml_content.get('name'):
            self.add_warning(file_path, "Workflow missing 'name' attribute")

        # Check for 'on' section by regex first (most reliable)
        on_section_found = False
        on_match = re.search(r'^\s*on\s*:', raw_content, re.MULTILINE)
        if on_match:
            self.log(f"Found 'on:' section directly in file content at position {on_match.start()}")
            on_section_found = True

        # If not found by regex, check the parsed YAML
        if not on_section_found and 'on' not in yaml_content:
            self.add_error(file_path, "Workflow missing 'on' trigger section")
            is_valid = False
        elif 'on' in yaml_content:
            on_section_found = True

        # Additional check: if we found 'on' in the content but it's not in the parsed YAML,
        # there might be a YAML parsing issue
        if on_section_found and 'on' not in yaml_content:
            self.log(f"Warning: Found 'on:' in content but not in parsed YAML. Possible YAML parsing issue.")

        # Check for jobs section
        jobs_match = re.search(r'^\s*jobs\s*:', raw_content, re.MULTILINE)
        if not jobs_match:
            self.add_error(file_path, "Workflow missing 'jobs' section")
            is_valid = False

        return is_valid

    def _validate_jobs_section(self, file_path: str, yaml_content: Dict, raw_content: str) -> bool:
        """Validate the 'jobs' section of a workflow file."""
        # Check for jobs section in raw content first
        jobs_match = re.search(r'^\s*jobs\s*:', raw_content, re.MULTILINE)
        if not jobs_match:
            return False  # Already reported in _validate_workflow_structure

        # Check if there's actual content in the jobs section
        # Look for indented content after "jobs:"
        jobs_content_match = re.search(r'^\s*jobs\s*:\s*\n(\s+\S+)', raw_content, re.MULTILINE)
        if not jobs_content_match:
            self.add_error(file_path, "Jobs section appears to be empty")
            return False

        # If 'jobs' is in the parsed YAML, check it has proper structure
        if 'jobs' in yaml_content:
            jobs = yaml_content['jobs']
            if not isinstance(jobs, dict) or not jobs:
                self.add_error(file_path, "Jobs section is empty or not a dictionary")
                return False

            is_valid = True
            for job_id, job in jobs.items():
                # Check if job is a dictionary
                if not isinstance(job, dict):
                    self.add_error(file_path, f"Job '{job_id}' is not a dictionary")
                    is_valid = False
                    continue

                # Check for required 'runs-on'
                if 'runs-on' not in job:
                    self.add_error(file_path, f"Job '{job_id}' missing 'runs-on' attribute")
                    is_valid = False

                # Check for steps
                if 'steps' not in job:
                    self.add_error(file_path, f"Job '{job_id}' missing 'steps' attribute")
                    is_valid = False
                elif not job['steps']:
                    self.add_warning(file_path, f"Job '{job_id}' has empty 'steps' list")

            return is_valid
        else:
            # Jobs section exists in raw content but not in parsed YAML
            self.log(f"Warning: Found 'jobs:' in content but not in parsed YAML. Possible YAML parsing issue.")
            # Since we can't verify the structure without parsed YAML, we'll assume it's valid
            # based on the regex match showing content after the jobs section
            return True

def main():
    """Main function to execute the script from command line."""
    import re
    import argparse

    parser = argparse.ArgumentParser(description='Validate and fix GitHub Actions workflow files.')
    parser.add_argument('--fix', action='store_true', help='Fix issues in workflow files')
    parser.add_argument('--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('files', nargs='*', help='Workflow files to validate')
    args = parser.parse_args()

    # If no files specified, use default paths
    if not args.files:
        workflow_dir = '.github/workflows'
        if os.path.isdir(workflow_dir):
            args.files = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                         if f.endswith(('.yml', '.yaml'))]
        else:
            print(f"❌ Error: Default workflow directory {workflow_dir} not found")
            return 1

    # Create validator and process files
    validator = WorkflowValidator(verbose=args.verbose)
    all_valid = validator.validate_and_fix_workflows(args.files, fix=args.fix)

    # Print final summary
    if all_valid:
        if args.fix:
            print("\n✅ All workflow files are now valid")
        else:
            print("\n✅ All workflow files are valid")
        return 0
    else:
        if args.fix:
            print("\n❌ Some workflow files still have issues")
        else:
            print("\n❌ Some workflow files have issues")
            print("   Run with --fix to attempt automatic fixes")
        return 1

if __name__ == "__main__":
    sys.exit(main())
