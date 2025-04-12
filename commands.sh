#!/bin/bash

# Make the badge verification script executable
chmod +x scripts/verify_badges.sh

# Run the badge verification script
./scripts/verify_badges.sh

# Fetch all changes from the remote
git fetch origin

# First, fetch the latest changes
git fetch origin

# Option 1: Merge remote changes with yours
git pull origin integration-temp

# Option 2: If you prefer rebase (cleaner history)
git pull --rebase origin integration-temp

# After resolving any conflicts, try pushing again
git push origin integration-temp
