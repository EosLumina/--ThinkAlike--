#!/bin/bash

set -e

# Get all remote branches except HEAD
branches=$(git branch -r | grep -v '\->' | sed 's/origin\///')

for branch in $branches; do
    echo "========================================"
    echo "Processing branch: $branch"
    echo "========================================"
    git checkout $branch

    # Pull latest changes
    git pull origin $branch

    # Run the workflow fixer
    python3 scripts/fix_all_workflows.py

    # Check if there are changes to commit
    if ! git diff --quiet; then
        git add .github/workflows/
        git commit -m "fix: standardize and repair workflow files (automated)"
        git push origin $branch
        echo "✅ Pushed workflow fixes to $branch"
    else
        echo "No workflow changes needed for $branch"
    fi
done

echo "🎉 All branches processed. Workflow files are now standardized and fixed."