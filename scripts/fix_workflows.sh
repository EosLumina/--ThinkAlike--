#!/bin/bash

# Script to diagnose and fix common workflow issues
echo "🔍 Checking for common workflow issues..."

# 1. Check workflow files syntax
echo "Validating workflow YAML syntax..."
for workflow in .github/workflows/*.yml; do
  echo "Checking $workflow..."
  yamllint "$workflow" || echo "⚠️ Warning: Syntax issues in $workflow"
done

# 2. Check references to repository name
echo "Checking repository references..."
grep -r "EosLumina/--ThinkAlike--" .github/workflows/ || echo "⚠️ Warning: Repository reference may be incorrect"

# 3. Check local dependencies in requirements.txt
echo "Checking requirements.txt for local dependencies..."
if [ -f requirements.txt ]; then
  if grep -E "^-e .*|^file:.*" requirements.txt; then
    echo "⚠️ Warning: Local dependencies found in requirements.txt that might cause CI failures"
    echo "Creating CI-compatible requirements file..."
    grep -v -E "^-e .*|^file:.*" requirements.txt > ci_requirements.txt
    echo "✅ Created ci_requirements.txt - Use this file in GitHub Actions"
  else
    echo "✅ No local dependencies found in requirements.txt"
  fi
fi

# 4. Check README badges
echo "Checking README badges..."
if [ -f README.md ]; then
  if grep -q "badge.svg" README.md; then
    echo "✅ Badges found in README"
  else
    echo "⚠️ Warning: README badges might be missing"
  fi
fi

echo "✅ Done checking workflow issues"
echo "Run this script after making changes to workflow files or requirements"
