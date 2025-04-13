#!/usr/bin/env python3
"""
Inspect the workflow validation process to understand why some files
are failing validation despite having proper 'on' sections.
This script analyzes both passing and failing workflows to find differences.
"""

import os
import sys
import re
import yaml
import difflib
from pathlib import Path

# Define files known to pass and fail validation
VALID_WORKFLOWS = [
    "frontend.yml",
    "lint-workflows.yml",
    "main.yml",
    "test.yml",
    "cd.yml",
    "backend.yml",
    "docs.yml",
    "ci.yml"
]

INVALID_WORKFLOWS = [
    "consolidated-ci.yml",
    "fixed_consolidated-ci.yml",
    "documentation.yml",
    "settings.yml",
    "fixed_deploy.yml"
]

def load_file_content(file_path):
    """Load file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def extract_yaml_structure(content):
    """Extract the YAML structure safely"""
    if not content:
        return None

    try:
        data = yaml.safe_load(content)
        return data
    except Exception as e:
        print(f"YAML parsing error: {e}")
        return None

def compare_files(valid_file, invalid_file):
    """Compare a valid and invalid workflow file to find differences"""
    valid_content = load_file_content(valid_file)
    invalid_content = load_file_content(invalid_file)

    if not valid_content or not invalid_content:
        return

    print(f"\n🔍 Comparing {valid_file.name} (valid) with {invalid_file.name} (invalid):")

    # 1. Basic content differences
    diff = difflib.unified_diff(
        valid_content.splitlines(),
        invalid_content.splitlines(),
        fromfile=valid_file.name,
        tofile=invalid_file.name,
        lineterm=''
    )

    # Only show first few lines of diff to avoid overwhelming output
    diff_lines = list(diff)[:20]
    if diff_lines:
        print("\nContent differences (first few lines):")
        for line in diff_lines:
            print(line)
        if len(diff_lines) == 20:
            print("... (more differences not shown) ...")

    # 2. Compare YAML structure
    valid_yaml = extract_yaml_structure(valid_content)
    invalid_yaml = extract_yaml_structure(invalid_content)

    if valid_yaml and invalid_yaml:
        # Check 'on' section
        print("\nYAML structure analysis:")

        if 'on' in valid_yaml and 'on' in invalid_yaml:
            print("✅ Both files have 'on' key in YAML")

            # Check type of 'on' value
            print(f"   Valid file 'on' type: {type(valid_yaml['on'])}")
            print(f"   Invalid file 'on' type: {type(invalid_yaml['on'])}")

            # Check if 'on' is empty
            if not valid_yaml['on']:
                print("⚠️ Valid file has EMPTY 'on' value")
            if not invalid_yaml['on']:
                print("⚠️ Invalid file has EMPTY 'on' value")
        else:
            if 'on' not in valid_yaml:
                print("❌ Valid file missing 'on' key in YAML")
            if 'on' not in invalid_yaml:
                print("❌ Invalid file missing 'on' key in YAML")

    # 3. Check line endings
    valid_has_cr = '\r\n' in valid_content
    invalid_has_cr = '\r\n' in invalid_content
    print(f"\nLine endings:")
    print(f"   Valid file uses CRLF: {valid_has_cr}")
    print(f"   Invalid file uses CRLF: {invalid_has_cr}")

    # 4. Check whitespace around 'on' section
    valid_on_pattern = re.search(r'(\n[^\n]*on:[^\n]*\n)', valid_content)
    invalid_on_pattern = re.search(r'(\n[^\n]*on:[^\n]*\n)', invalid_content)

    if valid_on_pattern and invalid_on_pattern:
        valid_on_whitespace = repr(valid_on_pattern.group(1))
        invalid_on_whitespace = repr(invalid_on_pattern.group(1))
        print(f"\nWhitespace around 'on' section:")
        print(f"   Valid: {valid_on_whitespace}")
        print(f"   Invalid: {invalid_on_whitespace}")

def main():
    """Inspect workflow files to understand validation issues"""
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return 1

    # Check if the specified files exist
    available_valid_files = []
    for filename in VALID_WORKFLOWS:
        file_path = workflows_dir / filename
        if file_path.exists():
            available_valid_files.append(file_path)
        else:
            print(f"Warning: Valid file {filename} not found, skipping")

    available_invalid_files = []
    for filename in INVALID_WORKFLOWS:
        file_path = workflows_dir / filename
        if file_path.exists():
            available_invalid_files.append(file_path)
        else:
            print(f"Warning: Invalid file {filename} not found, skipping")

    if not available_valid_files or not available_invalid_files:
        print("Error: Not enough files to compare")
        return 1

    # Compare a sample of files
    for valid_file in available_valid_files[:2]:  # Limit to first two for brevity
        for invalid_file in available_invalid_files[:2]:  # Limit to first two for brevity
            compare_files(valid_file, invalid_file)

    print("\n⚠️ NOTE: If the YAML structure analysis shows both files have 'on' key but validation still fails,")
    print("   the issue may be with whitespace, line endings, or how the validator parses the YAML.")
    print("   Try running files through a YAML linter or use 'git show --pretty=raw <file>' to check for hidden issues.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
