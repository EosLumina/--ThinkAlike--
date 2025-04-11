#!/bin/bash

# Directory containing workflow files
WORKFLOWS_DIR=".github/workflows"

# Function to fix common YAML issues
fix_workflow_file() {
  local file=$1
  echo "Fixing $file..."

  # Create a backup
  cp "$file" "${file}.bak"

  # Replace JavaScript-style comments with YAML comments
  sed -i 's|^// |# |g' "$file"

  # Remove merge conflict markers and content between them
  sed -i '/^<<<<<<< HEAD$/,/^>>>>>>> /d' "$file"

  echo "Fixed $file (backup saved as ${file}.bak)"
}

# Process each workflow file
for workflow in $WORKFLOWS_DIR/*.yml; do
  if [ -f "$workflow" ]; then
    fix_workflow_file "$workflow"
  fi
done

echo "Completed fixing workflow files. Please verify the changes manually."
