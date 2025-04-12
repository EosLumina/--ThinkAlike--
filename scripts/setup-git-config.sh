#!/bin/bash

# Set git to use rebase strategy for pulls
git config pull.rebase true

# Configure user information if not already set
if [ -z "$(git config --get user.name)" ]; then
  echo "Setting up git user name as 'ThinkAlike Contributor'"
  git config user.name "ThinkAlike Contributor"
fi

if [ -z "$(git config --get user.email)" ]; then
  echo "Setting up git user email as 'contributor@thinkalike.org'"
  git config user.email "contributor@thinkalike.org"
fi

echo "Git configuration complete!"
echo "Pull strategy set to rebase."
echo "To pull the latest changes, use: git pull origin main"
