#!/bin/bash
# Script to update GitHub Actions versions across all workflow files

echo "Creating backup directory for workflow files..."
mkdir -p .github/workflows/backups
cp .github/workflows/*.yml .github/workflows/backups/

echo "Updating GitHub Actions versions in all workflow files..."
# Update actions/checkout from v3 to v4
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/checkout@v3/actions\/checkout@v4/g' {} \;

# Count the number of files updated
checkout_updated=$(grep -l "actions/checkout@v4" .github/workflows/*.yml | wc -l)
echo "✅ Updated actions/checkout in $checkout_updated files"

# Update actions/setup-python from v4 to v5
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/setup-python@v4/actions\/setup-python@v5/g' {} \;

# Update actions/cache from v3 to v4
find .github/workflows -name "*.yml" -exec sed -i 's/actions\/cache@v3/actions\/cache@v4/g' {} \;

echo "Validating updated workflow files..."
for file in .github/workflows/*.yml; do
  echo "Checking $file..."
  actionlint "$file" || echo "Issues found in $file"
done

echo "Summary of updates:"
echo "- actions/checkout: v3 → v4 ($checkout_updated files)"
echo "- actions/setup-python: v4 → v5 ($(grep -l "actions/setup-python@v5" .github/workflows/*.yml | wc -l) files)"
echo "- actions/cache: v3 → v4 ($(grep -l "actions/cache@v4" .github/workflows/*.yml | wc -l) files)"

echo "Done! Please review the changes before committing."
echo "Suggested commit command: git commit -m \"ci: update GitHub Actions to latest versions\""
