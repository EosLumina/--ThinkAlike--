#!/usr/bin/env python3
import os
import sys
import yaml
import re

def validate_workflows():
    workflow_dir = '.github/workflows'
    all_valid = True

    # Skip these directories
    skip_dirs = ['backup', 'templates']

    for filename in os.listdir(workflow_dir):
        # Skip directories
        if os.path.isdir(os.path.join(workflow_dir, filename)):
            continue

        # Skip files in backup directories
        if any(skip_dir in os.path.join(workflow_dir, filename) for skip_dir in skip_dirs):
            continue

        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflow_dir, filename)

            # First check for shell script patterns
            with open(filepath, 'r') as f:
                content = f.read()

            shell_patterns = [
                r'cat\s+>\s+.*<<\s+.*EOF',  # cat > file << EOF
                r'EOF\s*$',  # EOF at the end of a line
                r'^#\s+(?!\s*-)',  # Comments not part of YAML list
            ]

            if any(re.search(pattern, content, re.MULTILINE) for pattern in shell_patterns):
                print(f"✗ {filepath}: Contains shell script commands")
                all_valid = False
                continue

            # Then validate as YAML
            with open(filepath, 'r') as f:
                try:
                    content = yaml.safe_load(f)
                    if not isinstance(content, dict):
                        print(f"✗ {filepath}: Not a valid YAML mapping")
                        all_valid = False
                        continue

                    if 'on' not in content:
                        print(f"✗ {filepath}: Missing required key 'on'")
                        all_valid = False
                        continue

                    if 'jobs' not in content:
                        print(f"✗ {filepath}: Missing required key 'jobs'")
                        all_valid = False
                        continue

                    print(f"✓ {filepath} is valid")
                except Exception as e:
                    print(f"✗ {filepath}: Error parsing YAML: {e}")
                    all_valid = False

    if all_valid:
        print("\nAll workflow files are valid!")
        return 0
    else:
        print("\nSome workflow files have errors!")
        return 1

if __name__ == "__main__":
    sys.exit(validate_workflows())
