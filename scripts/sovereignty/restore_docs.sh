#!/bin/bash
# Documentation Sovereignty Restoration Tool
# This script helps transfer documentation from a local source to our sovereign domains

echo "✦ Documentation Sovereignty Restoration ✦"
echo "This tool will help you restore the knowledge commons from your local system."

# Ask for the local directory containing documentation
read -p "Enter the path to your local documentation directory: " LOCAL_DOCS_DIR

if [ ! -d "$LOCAL_DOCS_DIR" ]; then
    echo "Error: Directory not found. Please check the path and try again."
    exit 1
fi

# Create the target directories if they don't exist
mkdir -p /workspaces/--ThinkAlike--/docs/{core,architecture,vision,components,governance,reference}

# Copy documentation files with structure preservation
echo "Restoring the knowledge commons from $LOCAL_DOCS_DIR to /workspaces/--ThinkAlike--/docs/"
rsync -av --progress "$LOCAL_DOCS_DIR/" /workspaces/--ThinkAlike--/docs/

# Verify the transfer
echo "Verifying documentation integrity..."
find /workspaces/--ThinkAlike--/docs/ -type f -name "*.md" | wc -l

echo "✦ Knowledge Commons Restoration Complete ✦"
echo "You can now generate an integrity map using:"
echo "python scripts/sovereignty/verify_integrity.py --generate"
