#!/bin/bash
# This script deletes legacy workflow files to ensure only the unified workflow is used.
OLD_FILES=(
  "/workspaces/--ThinkAlike--/.github/workflows/backup/build-and-test.yml"
  "/workspaces/--ThinkAlike--/.github/workflows/build-and-test.yml"
)
for file in "${OLD_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "Deleting legacy workflow file: $file"
    rm "$file"
  else
    echo "No legacy workflow file found at: $file"
  fi
done
