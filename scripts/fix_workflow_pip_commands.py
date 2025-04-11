#!/usr/bin/env python3

import os
import re
import yaml
import glob
from pathlib import Path

def detect_invalid_pip_commands(workflow_dir='.github/workflows'):
    """Find workflow files with invalid pip install -e commands."""
    issues_found = False
    workflow_files = glob.glob(f"{workflow_dir}/*.yml") + glob.glob(f"{workflow_dir}/*.yaml")

    print(f"Scanning {len(workflow_files)} workflow files for invalid pip commands...")

    for wf_file in workflow_files:
        try:
            with open(wf_file, 'r') as f:
                content = f.read()

            # Look for patterns that indicate invalid editable installs
            if re.search(r'pip\s+install\s+-e\s+pip\s+install', content):
                print(f"\n⚠️ Found potential invalid pip command in {wf_file}")
                issues_found = True

                # Extract problematic lines for better context
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if re.search(r'pip\s+install\s+-e\s+pip\s+install', line):
                        print(f"  Line {i+1}: {line.strip()}")

                        # Suggest fix based on content
                        if 'pip install -e pip install' in line:
                            fixed_line = line.replace('pip install -e pip install', 'pip install')
                            print(f"  Suggested fix: {fixed_line.strip()}")

                print("\nThis is likely causing your workflow failures.")
        except Exception as e:
            print(f"Error processing {wf_file}: {e}")

    if not issues_found:
        print("No obvious invalid pip commands found in workflow files.")
        print("The issue might be in a script called by the workflows. Check:")
        print("1. Any custom installation scripts")
        print("2. requirements.txt file format")
        print("3. setup.py if it exists")

    return issues_found

def fix_requirements_file():
    """Check and fix the requirements.txt file if it exists."""
    req_file = 'requirements.txt'
    if not os.path.exists(req_file):
        print(f"{req_file} not found.")
        return False

    try:
        with open(req_file, 'r') as f:
            lines = f.readlines()

        fixed_lines = []
        issues_fixed = False

        for line in lines:
            # Fix lines that might contain invalid editable installs
            if line.strip().startswith('-e pip install'):
                fixed_line = line.replace('-e pip install', '')
                fixed_lines.append(fixed_line)
                issues_fixed = True
                print(f"Fixed invalid requirement: {line.strip()} -> {fixed_line.strip()}")
            else:
                fixed_lines.append(line)

        if issues_fixed:
            # Backup original file
            os.rename(req_file, f"{req_file}.bak")

            # Write fixed file
            with open(req_file, 'w') as f:
                f.writelines(fixed_lines)

            print(f"✅ Fixed {req_file} and created backup {req_file}.bak")
        else:
            print(f"No issues found in {req_file}")

        return issues_fixed
    except Exception as e:
        print(f"Error processing {req_file}: {e}")
        return False

if __name__ == "__main__":
    print("ThinkAlike Workflow Pip Command Fix Tool")
    print("=======================================")

    workflow_issues = detect_invalid_pip_commands()
    requirements_fixed = fix_requirements_file()

    if workflow_issues or requirements_fixed:
        print("\n🔧 NEXT STEPS:")
        print("1. Review the identified issues and suggested fixes")
        print("2. Manually update the workflow files or requirements.txt")
        print("3. Commit the changes and push to trigger a new workflow run")
        print("4. Monitor the workflow execution for success")
    else:
        print("\n⚠️ No obvious pip command issues found in workflow files or requirements.txt")
        print("Check if there are other places where pip commands might be malformed.")
