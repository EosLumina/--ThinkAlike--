#!/bin/bash
# Setup Script for Workflow Protection System
# This script installs the workflow protection system for ThinkAlike

set -e

echo "🛡️  Setting up ThinkAlike Workflow Protection System..."

# Make scripts directory if it doesn't exist
mkdir -p .github/scripts
mkdir -p .github/hooks
mkdir -p .github/workflow_templates

# Make validator script executable
if [ -f ".github/scripts/validate_workflows.py" ]; then
    chmod +x .github/scripts/validate_workflows.py
    echo "✅ Made validator script executable"
else
    echo "❌ Validator script not found. Please ensure .github/scripts/validate_workflows.py exists."
    exit 1
fi

# Make pre-commit hook executable
if [ -f ".github/hooks/pre-commit" ]; then
    chmod +x .github/hooks/pre-commit
    echo "✅ Made pre-commit hook executable"
else
    echo "❌ Pre-commit hook not found. Please ensure .github/hooks/pre-commit exists."
    exit 1
fi

# Install git hooks
if [ -d ".git/hooks" ]; then
    cp .github/hooks/pre-commit .git/hooks/
    echo "✅ Installed pre-commit hook"
else
    echo "❌ .git/hooks directory not found. Is this a git repository?"
    exit 1
fi

# Install dependencies
echo "Installing required Python packages..."
pip install PyYAML

# Run initial validation on existing workflow files
echo "Running initial validation on existing workflow files..."
python .github/scripts/validate_workflows.py --fix

echo "🎉 Workflow Protection System setup complete!"
echo ""
echo "The system will now automatically validate and fix workflow files before commits."
echo "If you want to validate workflows manually, run: python .github/scripts/validate_workflows.py --fix"
echo ""
echo "To create a new workflow file from the template, copy from .github/workflow_templates/standard_workflow.yml"