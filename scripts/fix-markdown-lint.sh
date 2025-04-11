#!/bin/bash

# This script fixes common markdown linting issues
echo "Fixing trailing whitespace..."
find ./docs -name "*.md" -exec sed -i 's/[[:space:]]*$//' {} \;

echo "Fixing multiple consecutive blank lines..."
find ./docs -name "*.md" -exec sed -i '/^$/N;/^\n$/D' {} \;

echo "Ensuring files end with single newline..."
find ./docs -name "*.md" -exec sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' {} \;
find ./docs -name "*.md" -exec sed -i -e '$a\' {} \;

echo "Running markdownlint with auto-fix..."
npx markdownlint "**/*.md" --ignore-path .markdownlintignore --config .markdownlint.json --fix

echo "Linting fixes complete!"
