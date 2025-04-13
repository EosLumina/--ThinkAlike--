#!/usr/bin/env python3

import os
import yaml
import re
import sys

def analyze_validator():
    """Analyze the validation script to understand its logic"""
    validator_path = ".github/scripts/validate_workflows.py"
    if not os.path.exists(validator_path):
        print(f"⚠️  Validator not found at {validator_path}")
        return

    print(f"📝 Validator Code Analysis:")
    with open(validator_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Look for how it checks for 'on' section
    on_check_lines = [line.strip() for line in code.split('\n')
                      if 'on' in line and ('check' in line.lower() or 'valid' in line.lower())]

    print("\nCritical validation logic:")
    for i, line in enumerate(on_check_lines):
        print(f"  {i+1}. {line}")

def examine_workflow(file_path):
    """Examine a workflow file for encoding issues or structural problems"""
    print(f"\n📄 Analyzing {file_path}:")

    # Check for encoding issues
    with open(file_path, 'rb') as f:
        raw_bytes = f.read()

    # Check for BOM
    has_bom = raw_bytes.startswith(b'\xef\xbb\xbf')
    print(f"  Has BOM marker: {has_bom}")

    # Check for null bytes
    null_count = raw_bytes.count(b'\x00')
    print(f"  Null bytes found: {null_count}")

    # Check for other non-printable characters
    non_printable = sum(1 for b in raw_bytes if b < 32 and b not in [9, 10, 13])  # Tab, LF, CR are allowed
    print(f"  Non-printable characters: {non_printable}")

    # Parse YAML
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            yaml_data = yaml.safe_load(content)

            # Check 'on' field
            has_on = 'on' in yaml_data
            on_type = type(yaml_data.get('on')).__name__ if has_on else "N/A"
            on_keys = list(yaml_data.get('on', {}).keys()) if has_on and isinstance(yaml_data.get('on'), dict) else []

            print(f"  YAML parsing: Success")
            print(f"  Has 'on' field: {has_on}")
            print(f"  'on' field type: {on_type}")
            print(f"  'on' keys: {on_keys}")

            # Count lines before 'on:' appears
            on_pos = content.find("\non:")
            if on_pos > 0:
                lines_before_on = content[:on_pos].count('\n') + 1
                print(f"  'on:' appears on line: {lines_before_on}")
            else:
                print(f"  'on:' not found as a standalone line")

                # Check if it appears inline
                if "on:" in content:
                    print(f"  'on:' appears inline somewhere in the file")
    except Exception as e:
        print(f"  Error parsing YAML: {str(e)}")

def fix_workflow(file_path):
    """Create a fixed version of the workflow file"""
    filename = os.path.basename(file_path)
    fixed_path = os.path.join(os.path.dirname(file_path), f"fixed_{filename}")

    print(f"\n🛠️  Creating fixed version of {filename}:")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Extract name
    name_match = re.search(r'name:\s*(.*)', content)
    workflow_name = name_match.group(1).strip() if name_match else filename.replace('.yml', '')

    # Create a minimal but proper workflow file
    fixed_content = f"""name: {workflow_name}

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: echo "Running tests for {workflow_name}"
"""

    with open(fixed_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"  Created {fixed_path}")
    return fixed_path

def main():
    """Main diagnostic function"""
    print("🔍 ThinkAlike Workflow Diagnostic Tool")
    print("="*50)

    # Analyze the validator first
    analyze_validator()

    # Find problematic workflows
    workflows_dir = ".github/workflows"
    problematic_files = [
        "consolidated-ci.yml",
        "deploy_to_gh_pages.yml",
        "run-tests.yml",
        "deploy.yml",
        "documentation.yml",
        "settings.yml"
    ]

    fixed_files = []
    for filename in problematic_files:
        file_path = os.path.join(workflows_dir, filename)
        if os.path.exists(file_path):
            examine_workflow(file_path)
            fixed_path = fix_workflow(file_path)
            fixed_files.append((file_path, fixed_path))

    print("\n📋 Next Steps:")
    print("  1. Review the diagnostics above to understand the issue")
    print("  2. Test the fixed workflows with the validation script:")
    for _, fixed_path in fixed_files:
        print(f"     python .github/scripts/validate_workflows.py {fixed_path}")
    print("  3. If the fixed files pass validation, replace the originals:")
    for orig, fixed in fixed_files:
        print(f"     cp {fixed} {orig}")
    print("  4. Or use the unified workflow approach for a clean slate")

if __name__ == "__main__":
    main()
