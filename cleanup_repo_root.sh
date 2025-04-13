#!/bin/bash

# Cleanup Script for ThinkAlike Repository
# This script helps identify and organize unnecessary files in the repository root
# while preserving important project files

set -e  # Exit on error

echo "🧹 ThinkAlike Repository Root Cleanup"
echo "======================================"
echo "This script will help identify files that can be organized or archived."
echo "No files will be deleted without your explicit confirmation."
echo ""

# Repository structure recommendations
DIRS_TO_CREATE=(
    "scripts"         # For utility scripts
    "tools"           # For development tools
    "archive"         # For archiving old or temporary files
    "config"          # For configuration files
)

# Files that should remain in the root directory
ROOT_FILES=(
    "README.md"
    "LICENSE"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    ".gitignore"
    ".github"
    "docs"
    "backend"
    "frontend"
    "requirements.txt"
    "pyproject.toml"
    "setup.py"
    "Dockerfile"
    "docker-compose.yml"
    ".env.example"
    ".editorconfig"
    ".pre-commit-config.yaml"
)

# Create directories if they don't exist
create_org_dirs() {
    echo "Creating organization directories..."
    for dir in "${DIRS_TO_CREATE[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "✅ Created directory: $dir"
        else
            echo "✓ Directory already exists: $dir"
        fi
    done
    echo ""
}

# List all files in the root directory
list_root_files() {
    echo "Files in root directory:"
    echo "----------------------"

    # Count to track if there are any files to display
    local count=0

    # List all files but exclude directories
    for file in *; do
        if [ -f "$file" ]; then
            echo "- $file"
            ((count++))
        fi
    done

    if [ $count -eq 0 ]; then
        echo "No files found in root directory."
    fi
    echo ""
}

# Identify script files that could be moved
identify_script_files() {
    echo "Script files that could be moved to 'scripts/' directory:"
    echo "------------------------------------------------------"

    local count=0

    for file in *.sh *.py *.js; do
        # Skip if the pattern doesn't match any files
        [ -e "$file" ] || continue

        # Skip if the file is in the protected list
        if [[ " ${ROOT_FILES[@]} " =~ " ${file} " ]]; then
            continue
        fi

        echo "- $file"
        ((count++))
    done

    if [ $count -eq 0 ]; then
        echo "No script files found that need to be moved."
    fi
    echo ""
}

# Identify workflow related files
identify_workflow_files() {
    echo "Workflow related files that could be organized:"
    echo "--------------------------------------------"

    local count=0

    # List workflow related files that aren't in the .github/workflows directory
    for file in *workflow*.sh *workflow*.py *workflow*.yml; do
        # Skip if the pattern doesn't match any files
        [ -e "$file" ] || continue

        # Skip if the file is in the protected list
        if [[ " ${ROOT_FILES[@]} " =~ " ${file} " ]]; then
            continue
        fi

        echo "- $file (could be moved to .github/scripts or scripts/)"
        ((count++))
    done

    if [ $count -eq 0 ]; then
        echo "No workflow related files found in root directory."
    fi
    echo ""
}

# Identify backup or temporary files
identify_temp_files() {
    echo "Temporary or backup files that could be archived:"
    echo "----------------------------------------------"

    local count=0

    # Common patterns for temporary or backup files
    for file in *.bak *.tmp *.temp *~ *.swp *.old *.orig *.back; do
        # Skip if the pattern doesn't match any files
        [ -e "$file" ] || continue

        echo "- $file"
        ((count++))
    done

    # Also check for files with common backup patterns in the name
    for file in *; do
        if [ -f "$file" ] && [[ "$file" =~ \.(bak|old|backup|[0-9]{8}|[0-9]{6}|save) ]]; then
            echo "- $file"
            ((count++))
        fi
    done

    if [ $count -eq 0 ]; then
        echo "No temporary or backup files found."
    fi
    echo ""
}

# Suggest organization plan
suggest_organization() {
    echo "📋 Organization Recommendations:"
    echo "=============================="
    echo "1. Script files (.sh, .py) -> scripts/"
    echo "2. Workflow related files -> .github/scripts/"
    echo "3. Tool configurations -> config/"
    echo "4. Temporary/backup files -> archive/"
    echo ""
    echo "Would you like to preview the commands that would move these files? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy] ]]; then
        # Generate move commands but don't execute them
        echo ""
        echo "# Here are the commands that would organize your files:"
        echo "# ------------------------------------------------"

        # Move script files
        for file in *.sh *.py *.js; do
            # Skip if the pattern doesn't match any files
            [ -e "$file" ] || continue

            # Skip if the file is in the protected list
            if [[ " ${ROOT_FILES[@]} " =~ " ${file} " ]]; then
                continue
            fi

            echo "mv \"$file\" scripts/"
        done

        # Move workflow files
        for file in *workflow*.sh *workflow*.py *workflow*.yml; do
            # Skip if the pattern doesn't match any files
            [ -e "$file" ] || continue

            # Skip if the file is in the protected list
            if [[ " ${ROOT_FILES[@]} " =~ " ${file} " ]]; then
                continue
            fi

            echo "mv \"$file\" .github/scripts/"
        done

        # Move backup/temporary files
        for file in *.bak *.tmp *.temp *~ *.swp *.old *.orig *.back; do
            # Skip if the pattern doesn't match any files
            [ -e "$file" ] || continue

            echo "mv \"$file\" archive/"
        done

        # Also check for files with common backup patterns in the name
        for file in *; do
            if [ -f "$file" ] && [[ "$file" =~ \.(bak|old|backup|[0-9]{8}|[0-9]{6}|save) ]]; then
                echo "mv \"$file\" archive/"
            fi
        done

        echo ""
        echo "# To execute these commands, create a script with the above commands."
        echo "# Always review carefully before running to ensure no important files are moved incorrectly."
    fi
}

# Main execution
main() {
    create_org_dirs
    list_root_files
    identify_script_files
    identify_workflow_files
    identify_temp_files
    suggest_organization

    echo ""
    echo "✨ Cleanup suggestions complete"
    echo "To execute any organization actions, please review the suggested commands"
    echo "and run them manually after careful review."
}

# Run the main function
main
