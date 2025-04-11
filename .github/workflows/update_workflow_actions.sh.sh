#!/bin/bash
# filepath: /workspaces/--ThinkAlike--/update_workflow_actions.sh

echo "Creating backup directory for workflow files..."
mkdir -p .github/workflows/backups
cp .github/workflows/*.yml .github/workflows/backups/

echo "Updating GitHub Actions versions in all workflow files..."
# Update actions/checkout from v3 to v4
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/checkout@v3/actions\/checkout@v4/g' {} \;

# Update actions/setup-python from v4 to v5
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/setup-python@v4/actions\/setup-python@v5/g' {} \;

# Update actions/cache from v3 to v4
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/cache@v3/actions\/cache@v4/g' {} \;

echo "Validating updated workflow files..."
for file in .github/workflows/*.yml; do
  echo "Checking $file..."
  actionlint "$file" || echo "Issues found in $file"
done

echo "Done! Please review the changes before committing."