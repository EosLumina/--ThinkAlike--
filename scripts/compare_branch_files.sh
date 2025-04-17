
#!/usr/bin/env bash
# Compare docs/, frontend/, and backend/ files across branches against main
set -e

git fetch --all

MAIN=origin/main

for remote in $(git branch -r | grep -vE 'HEAD|main$'); do
  br=${remote#origin/}
  echo "\nBranch: $br"
  echo "------------------------------------"
  # List added or modified files under docs/, frontend/, backend/ vs main
  git diff --name-status $MAIN...origin/$br -- docs/ frontend/ backend/ | while read status file; do
    echo "$status $file"
  done
done
