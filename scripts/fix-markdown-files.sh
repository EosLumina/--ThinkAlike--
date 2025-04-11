#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Check if new file exists before removing old one
if [ -f "./docs/contributing_quick.md" ]; then
    echo "Removing old contributing-quick.md file..."
    rm -f "./docs/contributing-quick.md"
else
    echo "Warning: New file ./docs/contributing_quick.md doesn't exist. Not removing old file."
fi

# Update cross-references
echo "Updating cross-references in files..."
find ./docs -name "*.md" -type f -exec sed -i 's/contributing-quick\.md/contributing_quick\.md/g' {} \;
find . -name "*.md" -type f -not -path "./docs/*" -not -path "./node_modules/*" -exec sed -i 's/contributing-quick\.md/contributing_quick\.md/g' {} \;

echo "Done!"
