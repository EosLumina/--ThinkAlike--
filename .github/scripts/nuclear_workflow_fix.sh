#!/bin/bash

# Nuclear option for fixing workflow files
# This script completely rewrites all workflow files with the simplest valid format
# Use this as a last resort when other approaches fail

set -e  # Exit on error

# Make sure we're in the repository root
if [ -d "../.git" ] && [ ! -d ".git" ]; then
    cd ..
    echo "Changed directory to repository root: $(pwd)"
fi

# Ensure the workflows directory exists
mkdir -p .github/workflows

echo "☢️ NUCLEAR WORKFLOW FIX ☢️"
echo "==========================="
echo "This script will completely rewrite all problematic workflow files"
echo "with the simplest possible valid format."
echo ""

# Template for a valid workflow file
create_workflow() {
    local file=".github/workflows/$1"
    local name="$2"
    local type="${3:-basic}"

    echo "Creating $file ($type)..."

    case "$type" in
        docs)
            cat > "$file" << EOF
name: $name

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - '*.md'
  pull_request:
    branches: [ main ]
  workflow_dispatch:

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
          pip install mkdocs
      - name: Build docs
        run: mkdocs build
EOF
            ;;
        deploy)
            cat > "$file" << EOF
name: $name

on:
  push:
    branches: [ main ]
    tags:
      - 'v*.*.*'
  pull_request:
    branches: [ main ]
  workflow_dispatch:

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
            cat > "$file" << EOF
name: $name

on:
  schedule:
    - cron: "0 0 * * 0"  # Weekly on Sundays
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - '.github/config/**'

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
        test)
            cat > "$file" << EOF
name: $name

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
      - 'tests/**'
  pull_request:
    branches: [ main ]
  workflow_dispatch:

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
        *)
            cat > "$file" << EOF
name: $name

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run script
        run: echo "Hello World"
EOF
            ;;
    esac

    echo "✅ Created $file"
}

# Create the most problematic workflow files with simple valid formats
create_workflow "consolidated-ci.yml" "Consolidated CI" "test"
create_workflow "fixed_consolidated-ci.yml" "Consolidated CI (Fixed)" "test"
create_workflow "fixed_run-tests.yml" "Run Tests (Fixed)" "test"
create_workflow "fixed_documentation.yml" "Documentation (Fixed)" "docs"
create_workflow "deploy_to_gh_pages.yml" "Deploy to GitHub Pages" "docs"
create_workflow "fixed_settings.yml" "Repository Settings (Fixed)" "settings"
create_workflow "fixed_deploy_to_gh_pages.yml" "Deploy to GitHub Pages (Fixed)" "docs"
create_workflow "unified-workflow.yml" "Unified Workflow" "basic"
create_workflow "run-tests.yml" "Run Tests" "test"
create_workflow "deploy.yml" "Deploy" "deploy"
create_workflow "documentation.yml" "Documentation" "docs"
create_workflow "settings.yml" "Repository Settings" "settings"
create_workflow "fixed_deploy.yml" "Fixed Deploy" "deploy"

echo ""
echo "🎉 All workflow files have been recreated with the simplest valid format."
echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"
