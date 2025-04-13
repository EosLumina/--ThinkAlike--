#!/usr/bin/env python3
"""
Analyze the output of validate_workflows.py to understand the validation issues
"""

import os
import sys
import re
import subprocess
from pathlib import Path

def analyze_validation_issues():
    """Run the validator and analyze its output"""
    print("Running workflow validator and analyzing output...")

    # Run the validator and capture its output
    try:
        result = subprocess.run(
            ["python", ".github/scripts/validate_workflows.py"],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout or ""
        error = result.stderr or ""

        if error:
            print("Error running validator:")
            print(error)
            return 1

    except Exception as e:
        print(f"Failed to run validator: {e}")
        return 1

    # Analyze the output
    print("\n🔍 Validation Output Analysis:")
    print("============================")

    # Extract validation results for each file
    validation_results = re.findall(r'===== Validating (.*?) =====.*?Checking.*?\n((?:.*?\n)+?)(?====|$)', output, re.MULTILINE)

    # Group files by validation status
    valid_files = []
    invalid_files = []

    for file_path, result_text in validation_results:
        if "✓ Workflow structure is valid" in result_text:
            valid_files.append((file_path, result_text))
        else:
            invalid_files.append((file_path, result_text))

    # Print summary
    print(f"Total files validated: {len(validation_results)}")
    print(f"Valid files: {len(valid_files)}")
    print(f"Invalid files: {len(invalid_files)}")

    if invalid_files:
        print("\n❌ Files with validation issues:")
        for file_path, result_text in invalid_files:
            issues = re.findall(r'- (.*)', result_text)
            print(f"  • {file_path}: {', '.join(issues)}")

    # Find patterns in valid files to help fix invalid ones
    if valid_files and invalid_files:
        print("\n🔍 Examining file format differences:")

        # Try to open one valid and one invalid file to compare
        valid_path = valid_files[0][0].strip()
        invalid_path = invalid_files[0][0].strip()

        try:
            valid_content = Path(valid_path).read_text()
            print(f"✅ Sample valid file ({valid_path}):")
            print("-" * 40)
            # Print the first few lines that typically contain the "on" section
            for line in valid_content.split('\n')[:15]:
                print(line)
            print("...")

        except Exception as e:
            print(f"Error reading valid file: {e}")

        try:
            invalid_content = Path(invalid_path).read_text()
            print(f"\n❌ Sample invalid file ({invalid_path}):")
            print("-" * 40)
            # Print the first few lines that typically contain the "on" section
            for line in invalid_content.split('\n')[:15]:
                print(line)
            print("...")

        except Exception as e:
            print(f"Error reading invalid file: {e}")

    return 0

if __name__ == "__main__":
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    sys.exit(analyze_validation_issues())
