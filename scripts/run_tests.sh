#!/bin/bash
# Helper script to run tests with proper setup

# Exit on error
set -e

# Display commands being run
set -x

# Ensure we're in the project root directory
cd "$(git rev-parse --show-toplevel)" || exit 1

# Install test dependencies
echo "Installing test dependencies..."
pip install -r requirements-test.txt 2>/dev/null || pip install httpx pandas pytest pytest-cov

# Fix test files with null bytes
echo "Fixing test files with null bytes..."
python .github/scripts/fix_test_files.py

# Run tests
echo "Running tests..."
pytest "$@"
