#!/bin/bash

# Badge Verification Script
# This script checks if the README.md badge URLs are correctly formatted and accessible

echo "Verifying README.md badges..."
echo "============================="

README_FILE="/workspaces/--ThinkAlike--/README.md"

# Check if file exists
if [ ! -f "$README_FILE" ]; then
  echo "❌ README.md not found at $README_FILE"
  exit 1
fi

# Extract badge URLs from README.md
echo "Extracting badge URLs from README.md..."
DOCS_BADGE_URL=$(grep -o 'https://github.com/EosLumina/--ThinkAlike--/actions/workflows/docs.yml/badge.svg' "$README_FILE")
BACKEND_BADGE_URL=$(grep -o 'https://github.com/EosLumina/--ThinkAlike--/actions/workflows/backend.yml/badge.svg' "$README_FILE")
FRONTEND_BADGE_URL=$(grep -o 'https://github.com/EosLumina/--ThinkAlike--/actions/workflows/frontend.yml/badge.svg' "$README_FILE")

# Check if badge URLs were found
if [ -z "$DOCS_BADGE_URL" ]; then
  echo "❌ Documentation CI badge URL not found or incorrectly formatted"
else
  echo "✅ Documentation CI badge URL found: $DOCS_BADGE_URL"
fi

if [ -z "$BACKEND_BADGE_URL" ]; then
  echo "❌ Backend CI badge URL not found or incorrectly formatted"
else
  echo "✅ Backend CI badge URL found: $BACKEND_BADGE_URL"
fi

if [ -z "$FRONTEND_BADGE_URL" ]; then
  echo "❌ Frontend CI badge URL not found or incorrectly formatted"
else
  echo "✅ Frontend CI badge URL found: $FRONTEND_BADGE_URL"
fi

# Check if workflow files exist
echo
echo "Checking workflow files..."

if [ -f ".github/workflows/docs.yml" ]; then
  echo "✅ docs.yml workflow file exists"
else
  echo "❌ docs.yml workflow file does not exist"
fi

if [ -f ".github/workflows/backend.yml" ]; then
  echo "✅ backend.yml workflow file exists"
else
  echo "❌ backend.yml workflow file does not exist"
fi

if [ -f ".github/workflows/frontend.yml" ]; then
  echo "✅ frontend.yml workflow file exists"
else
  echo "❌ frontend.yml workflow file does not exist"
fi

echo
echo "Badge verification complete."
echo

# Optional: Provide fix instructions if issues were found
if [ -z "$DOCS_BADGE_URL" ] || [ -z "$BACKEND_BADGE_URL" ] || [ -z "$FRONTEND_BADGE_URL" ] || \
   [ ! -f ".github/workflows/docs.yml" ] || [ ! -f ".github/workflows/backend.yml" ] || [ ! -f ".github/workflows/frontend.yml" ]; then
  echo "Issues were found. To fix:"
  echo "1. Ensure all workflow files exist in .github/workflows/ directory"
  echo "2. Make sure README.md contains correctly formatted badge URLs:"
  echo "   - https://github.com/EosLumina/--ThinkAlike--/actions/workflows/docs.yml/badge.svg"
  echo "   - https://github.com/EosLumina/--ThinkAlike--/actions/workflows/backend.yml/badge.svg"
  echo "   - https://github.com/EosLumina/--ThinkAlike--/actions/workflows/frontend.yml/badge.svg"
fi
