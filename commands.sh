#!/bin/bash

# Make the badge verification script executable
chmod +x scripts/verify_badges.sh

# Run the badge verification script
./scripts/verify_badges.sh

# Fetch all changes from the remote
git fetch origin

# Pull the latest changes from the remote repository
git pull --rebase origin integration-temp

# After resolving any conflicts, try pushing again
git push origin integration-temp
