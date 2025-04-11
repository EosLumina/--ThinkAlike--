#!/bin/bash

# List of workflows to disable
WORKFLOWS_TO_DISABLE=(
  "Test and Deploy"
  "Build and Deploy"
  "Run Tests"
  "CI Pipeline"
  "Update Documentation"
)

# GitHub CLI must be installed and authenticated
echo "Disabling duplicate workflows..."

for workflow in "${WORKFLOWS_TO_DISABLE[@]}"; do
  echo "Disabling workflow: $workflow"
  gh workflow disable "$workflow"
done

echo "Done! The following workflows have been disabled:"
for workflow in "${WORKFLOWS_TO_DISABLE[@]}"; do
  echo "- $workflow"
done
echo "These have been replaced by the consolidated workflows in backend.yml, frontend.yml, and docs.yml"
