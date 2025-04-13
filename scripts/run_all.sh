#!/bin/bash
# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running tests..."
pytest

echo "Building documentation..."
mkdocs build

echo "All tasks completed."
