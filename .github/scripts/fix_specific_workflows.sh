#!/bin/bash

# Quick fix for specific workflow files
# Usage: bash fix_specific_workflows.sh file1.yml file2.yml ...

set -e  # Exit on error

if [ $# -eq 0 ]; then
  echo "Please specify workflow files to fix, e.g.:"
  echo "bash $0 settings.yml consolidated-ci.yml"
  exit 1
fi

for file in "$@"; do
  filepath=".github/workflows/$file"

  echo "Fixing $filepath..."

  # Extract existing workflow name and jobs section
  name=$(grep "^name:" "$filepath" | sed 's/name: //')
  jobs_section=$(sed -n '/^jobs:/,$p' "$filepath")

  # Recreate the file with proper 'on' section
  cat > "$filepath" << EOF
name: $name

'on':
  push:
    branches:
    - main
  pull_request:
    branches:
    - main
  workflow_dispatch: {}

$jobs_section
EOF

  echo "✅ Fixed $file"
done

echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"
