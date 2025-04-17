#!/usr/bin/env bash
# Rescue docs from all branches and then prune remote branches
set -e

echo "Fetching all branches..."
git fetch --all

# Ensure working on main
git checkout main

echo "Creating rescued_docs directory..."
mkdir -p rescued_docs

# Loop through each remote branch except main and develop
for remote in $(git branch -r | grep -vE 'HEAD|main$|develop$'); do
  br=${remote#origin/}
  echo "\nRescuing docs from branch $br..."
  # Copy any .md or docs/**/* files into rescued_docs preserving path
  git ls-tree -r --name-only origin/$br | grep -E '\.md$|^docs/' | while read file; do
    dst="rescued_docs/$br/$file"
    mkdir -p "$(dirname "$dst")"
    git show origin/$br:"$file" > "$dst" 2>/dev/null || true
  done
done

echo "\nCommitting rescued files to main..."
git add rescued_docs
git commit -m "chore: rescue markdown/docs from all branches"

echo "\nPruning merged and unwanted remote branches..."
# Delete remote branches already merged to main
for remote in $(git branch -r --merged origin/main | grep -vE 'HEAD|main$|develop$'); do
  br=${remote#origin/}
  echo "Deleting remote branch $br..."
  git push origin --delete "$br" || true
  git branch -D "$br" 2>/dev/null || true
done

echo "Rescue and cleanup complete. Remaining branches:" 
git branch -r
