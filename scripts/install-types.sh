#!/bin/bash

# Navigate to frontend directory
cd frontend || exit 1

echo "Installing TypeScript type definitions..."

# Install React and Redux type definitions
npm install --save-dev @types/react @types/react-dom @types/react-redux

# Install Material UI type definitions
npm install --save-dev @types/material-ui

# Install D3 type definitions
npm install --save-dev @types/d3

echo "Creating project-specific type definitions..."

# Create directory for custom type definitions if it doesn't exist
mkdir -p src/types

# For modules without @types packages, create custom declarations
