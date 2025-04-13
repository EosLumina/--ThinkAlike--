#!/bin/bash

# Workflow generator for ThinkAlike project
# This script creates a new workflow file with the correct format

# Check for required arguments
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <filename> <workflow-name> [type]"
  echo "Types: basic, test, docs, deploy, settings"
  exit 1
fi

FILENAME="$1"
WORKFLOW_NAME="$2"
TYPE="${3:-basic}"

# Create workflows directory if it doesn't exist
mkdir -p .github/workflows

# Base template with proper 'on' format
cat > ".github/workflows/${FILENAME}" << EOF
name: ${WORKFLOW_NAME}

'on':
  push:
    branches:
    - main
  pull_request:
    branches:
    - main
  workflow_dispatch: {}

EOF

# Add jobs section based on type
case "$TYPE" in
  test)
    cat >> ".github/workflows/${FILENAME}" << EOF
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Test with pytest
        run: pytest
EOF
    ;;
  docs)
    cat >> ".github/workflows/${FILENAME}" << EOF
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material
      - name: Build docs
        run: mkdocs build
EOF
    ;;
  deploy)
    cat >> ".github/workflows/${FILENAME}" << EOF
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Deploy
        run: echo "Deploying application..."
EOF
    ;;
  settings)
    cat >> ".github/workflows/${FILENAME}" << EOF
jobs:
  settings:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Apply repository settings
        uses: probot/settings@v1
        with:
          settings_file: .github/config/repository-settings.yml
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
EOF
    ;;
  *)
    cat >> ".github/workflows/${FILENAME}" << EOF
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
EOF
    ;;
esac

echo "✅ Created workflow file: .github/workflows/${FILENAME}"
echo "Run validation to verify:"
echo "python .github/scripts/simple_workflow_validator.py"
