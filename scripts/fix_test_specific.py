#!/usr/bin/env python3
"""
Helper script to fix a specific test file or issue.
"""

import os
import sys
import time
import argparse
import importlib.util
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def analyze_imports(content: str) -> List[Tuple[str, str]]:
    """Extract and analyze imports from test file content."""
    imports = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
            # Extract module name from import statement
            module = line.split()[1].split('.')[0]
            imports.append((line, module))
    return imports


def check_missing_packages(imports: List[Tuple[str, str]]) -> List[str]:
    """Check if imported modules are available and return missing ones."""
    missing = []
    for import_stmt, module in imports:
        if module != 'backend':  # Skip our local backend module
            try:
                importlib.util.find_spec(module)
            except ImportError:
                missing.append(module)
    return missing


def fix_specific_test(test_file: str, auto_fix: bool = False, verbose: bool = False) -> bool:
    """Fix issues in a specific test file.

    Args:
        test_file: Path to the test file
        auto_fix: Automatically fix detected issues
        verbose: Print verbose diagnostics

    Returns:
        bool: True if file was analyzed/fixed successfully
    """
    start_time = time.time()
    issues_found = 0
    issues_fixed = 0

    if not os.path.exists(test_file):
        print(f"Error: Test file {test_file} does not exist.")
        return False

    print(f"Examining {test_file}...")

    # Read the test file
    try:
        # Check for null bytes first (binary mode)
        with open(test_file, 'rb') as f:
            binary_content = f.read()

        # Then read as text for other analysis
        with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
            text_content = f.read()

        # Collect diagnostics information
        diagnostics: Dict[str, any] = {
            "file_size": len(binary_content),
            "line_count": len(text_content.split('\n')),
            "has_tests": "def test_" in text_content or "class Test" in text_content,
            "imports": analyze_imports(text_content)
        }

        issues_list = []

        # Check for null bytes
        if b'\x00' in binary_content:
            issues_found += 1
            issues_list.append("Contains null bytes")
            print(f"⚠️ Found null bytes in {test_file}")

            if auto_fix:
                cleaned = binary_content.replace(b'\x00', b'')
                with open(test_file, 'wb') as f:
                    f.write(cleaned)
                print(f"✅ Fixed null bytes in {test_file}")
                issues_fixed += 1
            else:
                print("  To fix: Use --auto-fix option or manually run:")
                print(f"  python .github/scripts/fix_null_bytes_aggressive.py {test_file}")

        # Check for potential missing backend imports
        if any('backend.' in imp for imp, _ in diagnostics["imports"]):
            if not os.path.exists('backend'):
                issues_found += 1
                issues_list.append("Missing backend module structure")
                print("⚠️ Test imports from 'backend' package but directory doesn't exist")
                print("  To fix: Run 'python scripts/fix_tests.py --skip-deps --skip-null-bytes'")

        # Check for missing package dependencies
        missing_packages = check_missing_packages(diagnostics["imports"])
        if missing_packages:
            issues_found += 1
            issues_list.append(f"Missing package dependencies: {', '.join(missing_packages)}")
            print(f"⚠️ Missing package dependencies: {', '.join(missing_packages)}")
            print(f"  To fix: pip install {' '.join(missing_packages)}")

        # Check for actual test functions
        if not diagnostics["has_tests"]:
            issues_found += 1
            issues_list.append("No test functions found")
            print("⚠️ No test functions found in this file")
            print("  Tests should be defined as 'def test_*' or 'class Test*'")

        # Print diagnostic summary
        if verbose:
            print("\n📊 File diagnostics:")
            print(f"  File size: {diagnostics['file_size']} bytes")
            print(f"  Line count: {diagnostics['line_count']}")
            print(f"  Contains tests: {'Yes' if diagnostics['has_tests'] else 'No'}")
            print(f"  Import statements: {len(diagnostics['imports'])}")
            if diagnostics["imports"]:
                print("\n  Imports:")
                for imp, _ in diagnostics["imports"]:
                    print(f"    {imp}")

        # Summary
        elapsed_time = time.time() - start_time
        print(f"\n📋 Analysis complete in {elapsed_time:.2f}s")

        if issues_found == 0:
            print(f"✅ No issues found in {test_file}")
            return True
        else:
            print(f"⚠️ Found {issues_found} issue(s), fixed {issues_fixed}")
            for i, issue in enumerate(issues_list, 1):
                print(f"  {i}. {issue}")

            if issues_found > issues_fixed and not auto_fix:
                print("\nRun with --auto-fix to attempt automatic fixes")

            return issues_fixed == issues_found

    except Exception as e:
        print(f"❌ Error processing {test_file}: {e}")
        return False


def run_test(test_file: str) -> bool:
    """Run the test file with pytest."""
    print(f"\nRunning test: {test_file}")
    cmd = f"pytest {test_file} -v"
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error output: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run test: {e}")
        return False


def main():
    """Parse arguments and fix specific tests."""
    parser = argparse.ArgumentParser(description='Fix and analyze a specific test file')
    parser.add_argument('test_file', help='Path to the test file to fix')
    parser.add_argument('--auto-fix', '-f', action='store_true', help='Automatically fix detected issues')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed diagnostics')
    parser.add_argument('--run', '-r', action='store_true', help='Run the test after fixing')
    args = parser.parse_args()

    success = fix_specific_test(args.test_file, args.auto_fix, args.verbose)

    if success and args.run:
        run_success = run_test(args.test_file)
        if not run_success:
            print("\n⚠️ Test execution failed")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
