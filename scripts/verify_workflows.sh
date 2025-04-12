#!/bin/bash

# Verify Workflows Script
# This script runs the workflow validator and checks if all workflow files are valid

echo "Verifying workflow files..."
echo "============================"

# Run the workflow validator with verbose output
python workflow_validator.py --verbose

# Check the exit status
if [ $? -eq 0 ]; then
  echo "============================"
  echo "✅ All workflow files are valid and working correctly!"
  echo ""
  echo "Frontend, Backend, and Documentation workflows are configured properly."
  echo "GitHub badges in the README should now display correctly."
else
  echo "============================"
  echo "❌ Some workflow files still have issues."
  echo ""
  echo "Run 'python regenerate_workflows.py' to fix issues, then try again."
fi
