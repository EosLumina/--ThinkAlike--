#!/bin/bash
# Script to rebuild docs and sync generated index.html into docs/
# Usage: ./scripts/update_docs.sh

set -e

echo "Building MkDocs site..."
mkdocs build --clean

echo "Updating docs/index.html with generated site entry point..."
cp site/index.html docs/index.html

echo "Docs updated successfully!"
