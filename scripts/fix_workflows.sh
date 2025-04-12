#!/bin/bash

# Script to fix common workflow issues
echo "🔧 Starting workflow fixes..."

# Check if workflow directory exists
if [ ! -d ".github/workflows" ]; then
    echo "Creating workflows directory..."
    mkdir -p .github/workflows
fi

# Function to check and fix workflow files
check_workflow() {
    local workflow=$1
    local file=".github/workflows/${workflow}.yml"

    echo "Checking ${workflow} workflow..."

    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "⚠️ $file does not exist. Creating from template..."
        cp "templates/workflows/${workflow}.yml" "$file" 2>/dev/null ||
            echo "No template found for $workflow"
        return
    fi

    # Check for merge conflicts
    if grep -q "<<<<<<< HEAD\|=======" "$file"; then
        echo "🚨 Found merge conflicts in $file. Fixing..."
        # Back up the file
        cp "$file" "${file}.bak"

        # Remove conflict markers and keep the HEAD version
        sed '/<<<<<<< HEAD/,/=======/!d; /=======/d; /<<<<<<< HEAD/d' "$file" > "${file}.tmp"
        sed '/=======/,/>>>>>>> /d' "$file" >> "${file}.tmp"
        mv "${file}.tmp" "$file"
        echo "✅ Merge conflicts fixed. Original backed up as ${file}.bak"
    fi

    # Check YAML syntax
    if command -v yamllint >/dev/null 2>&1; then
        echo "Verifying YAML syntax..."
        yamllint -d relaxed "$file" || echo "⚠️ YAML syntax issues detected in $file"
    else
        echo "⚠️ yamllint not available, skipping YAML syntax check"
    fi
}

# Fix each workflow file
check_workflow "docs"
check_workflow "backend"
check_workflow "frontend"

# Fix GitHub README badges
if [ -f "scripts/fix-markdown-linting.js" ]; then
    echo "Fixing README badges..."
    node scripts/fix-markdown-linting.js README.md
fi

echo "✅ Workflow fixes completed!"
chmod +x scripts/fix_workflows.sh
