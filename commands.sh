#!/bin/bash

# Make the badge verification script executable
chmod +x scripts/verify_badges.sh

# Run the badge verification script
./scripts/verify_badges.sh

# Fetch all changes from the remote
git fetch origin
