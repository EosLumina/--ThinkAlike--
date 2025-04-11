#!/bin/bash
# Script to run markdown linting and fixes across documentation

echo "Running markdown linting script on documentation files..."

# Make the Python script executable if it isn't already
chmod +x ./scripts/fix_markdown_lint.py

# Run the linting script on all markdown files in docs
python ./scripts/fix_markdown_lint.py

echo "Markdown linting complete!"
echo "You can also run linting on a specific file with:"
echo "python ./scripts/fix_markdown_lint.py path/to/your/file.md"
