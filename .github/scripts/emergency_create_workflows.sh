#!/bin/bash

# Emergency script to create GitHub workflow files with the simplest possible method
# This script avoids complex parsing and just creates files directly with known good content

set -e  # Exit on error

# Ensure we're in the repository root
if [ -d "../.git" ] && [ ! -d ".git" ]; then
    cd ..
    echo "Changed directory to repository root: $(pwd)"
fi

# Create workflows directory if needed
mkdir -p .github/workflows

echo "🚨 Emergency Workflow Creation"
echo "============================="

# Function to create a workflow file
create_workflow() {
    local filename="$1"
    cat > ".github/workflows/$filename" << EOF
name: ${2:-Workflow}

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  ${3:-build}:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
${4:-      - name: Run a command
        run: echo "Hello, world!"}
EOF
    echo "✅ Created $filename"
}

# Create workflow files
create_workflow "consolidated-ci.yml" "Consolidated CI" "test" "      - name: Set up Python
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

create_workflow "fixed_consolidated-ci.yml" "Consolidated CI (Fixed)" "test" "      - name: Set up Python
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

create_workflow "fixed_run-tests.yml" "Run Tests (Fixed)" "test" "      - name: Set up Python
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

create_workflow "fixed_documentation.yml" "Documentation (Fixed)" "build" "      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs
      - name: Build docs
        run: mkdocs build"

create_workflow "deploy_to_gh_pages.yml" "Deploy to GitHub Pages" "deploy" "      - name: Setup Python
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

create_workflow "fixed_settings.yml" "Repository Settings (Fixed)" "settings" "      - name: Apply repository settings
        uses: probot/settings@v1
        with:
          settings_file: .github/config/repository-settings.yml
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"

create_workflow "fixed_deploy_to_gh_pages.yml" "Deploy to GitHub Pages (Fixed)" "deploy" "      - name: Setup Python
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

create_workflow "unified-workflow.yml" "Unified Workflow" "test" "      - name: Set up Python
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

create_workflow "run-tests.yml" "Run Tests" "test" "      - name: Set up Python
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

create_workflow "deploy.yml" "Deploy" "deploy" "      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Deploy
        run: echo \"Deploying application...\""

create_workflow "documentation.yml" "Documentation" "build" "      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs
      - name: Build docs
        run: mkdocs build"

create_workflow "settings.yml" "Repository Settings" "settings" "      - name: Apply repository settings
        uses: probot/settings@v1
        with:
          settings_file: .github/config/repository-settings.yml
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"

create_workflow "fixed_deploy.yml" "Fixed Deploy" "deploy" "      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Deploy
        run: echo \"Deploying application...\""

echo ""
echo "🎉 Created all workflow files"
echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"
