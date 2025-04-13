#!/bin/bash

# Create correct workflow files for GitHub Actions
# This script directly creates workflow files with known correct formats

set -e  # Exit on error

# Ensure we're in the repository root
if [ -d "../.git" ] && [ ! -d ".git" ]; then
    cd ..
    echo "Changed to repository root: $(pwd)"
fi

# Create workflows directory if needed
mkdir -p .github/workflows

# Function to create workflow file
create_workflow() {
    local file="$1"
    local name="$2"
    local on_section="$3"
    local jobs_section="$4"

    cat > ".github/workflows/$file" << EOF
name: $name

$on_section

$jobs_section
EOF
    echo "✅ Created/fixed $file"
}

# Default 'on' sections
STANDARD_ON_SECTION="on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:"

DOCS_ON_SECTION="on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '*.md'
  pull_request:
    branches: [main]
  workflow_dispatch:"

DEPLOY_ON_SECTION="on:
  push:
    branches: [main]
    tags:
      - 'v*.*.*'
  workflow_dispatch:"

SETTINGS_ON_SECTION="on:
  schedule:
    - cron: \"0 0 * * 0\"  # Run weekly on Sundays
  workflow_dispatch:"

# Default jobs sections
TEST_JOBS_SECTION="jobs:
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
        run: pytest"

DOCS_JOBS_SECTION="jobs:
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
        run: mkdocs build"

DEPLOY_JOBS_SECTION="jobs:
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
        run: echo \"Deploying application...\""

SETTINGS_JOBS_SECTION="jobs:
  settings:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Apply repository settings
        uses: probot/settings@v1
        with:
          settings_file: .github/config/repository-settings.yml
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"

GHPAGES_JOBS_SECTION="jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material
      - name: Build site
        run: mkdocs build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site"

echo "🛠️ Creating/fixing workflow files with correct formats..."

# Create/fix all the problematic files
create_workflow "consolidated-ci.yml" "Consolidated CI" "$STANDARD_ON_SECTION" "$TEST_JOBS_SECTION"
create_workflow "fixed_consolidated-ci.yml" "Consolidated CI (Fixed)" "$STANDARD_ON_SECTION" "$TEST_JOBS_SECTION"
create_workflow "fixed_run-tests.yml" "Run Tests (Fixed)" "$DOCS_ON_SECTION" "$TEST_JOBS_SECTION"
create_workflow "fixed_documentation.yml" "Documentation (Fixed)" "$DOCS_ON_SECTION" "$DOCS_JOBS_SECTION"
create_workflow "deploy_to_gh_pages.yml" "Deploy to GitHub Pages" "$DOCS_ON_SECTION" "$GHPAGES_JOBS_SECTION"
create_workflow "fixed_settings.yml" "Repository Settings (Fixed)" "$SETTINGS_ON_SECTION" "$SETTINGS_JOBS_SECTION"
create_workflow "fixed_deploy_to_gh_pages.yml" "Deploy to GitHub Pages (Fixed)" "$DOCS_ON_SECTION" "$GHPAGES_JOBS_SECTION"
create_workflow "unified-workflow.yml" "Unified Workflow" "$STANDARD_ON_SECTION" "$TEST_JOBS_SECTION"
create_workflow "run-tests.yml" "Run Tests" "$DOCS_ON_SECTION" "$TEST_JOBS_SECTION"
create_workflow "deploy.yml" "Deploy" "$DEPLOY_ON_SECTION" "$DEPLOY_JOBS_SECTION"
create_workflow "documentation.yml" "Documentation" "$DOCS_ON_SECTION" "$DOCS_JOBS_SECTION"
create_workflow "settings.yml" "Repository Settings" "$SETTINGS_ON_SECTION" "$SETTINGS_JOBS_SECTION"
create_workflow "fixed_deploy.yml" "Fixed Deploy" "$DEPLOY_ON_SECTION" "$DEPLOY_JOBS_SECTION"

echo ""
echo "🎉 All workflow files have been created/fixed with correct formats"
echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"
