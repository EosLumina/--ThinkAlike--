#!/bin/bash

# Script to directly repair problematic workflow files

echo "🛠️ Repairing problematic workflow files..."

# Create directory for workflow files if it doesn't exist
mkdir -p .github/workflows

# Deploy to GitHub Pages workflow
cat > .github/workflows/fixed_deploy_to_gh_pages.yml << 'EOF'
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '*.md'
  workflow_dispatch:

jobs:
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
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
EOF

# Unified workflow
cat > .github/workflows/unified-workflow.yml << 'EOF'
name: Unified Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
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

# Run tests workflow
cat > .github/workflows/run-tests.yml << 'EOF'
name: Run Tests

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'tests/**'
      - 'requirements*.txt'
  pull_request:
    branches: [main]
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

# Deploy workflow
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy

on:
  push:
    branches: [main]
    tags:
      - 'v*.*.*'
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

# Documentation workflow
cat > .github/workflows/documentation.yml << 'EOF'
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '*.md'
  pull_request:
    branches: [main]
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

# Settings workflow
cat > .github/workflows/settings.yml << 'EOF'
name: Repository Settings

on:
  schedule:
    - cron: "0 0 * * 0"  # Run weekly on Sundays
  workflow_dispatch:

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
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF

# Fixed deploy workflow
cat > .github/workflows/fixed_deploy.yml << 'EOF'
name: Fixed Deploy

on:
  push:
    branches: [main]
    tags:
      - 'v*.*.*'
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

echo "✅ All workflow files have been repaired."
echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"

# Create repository settings file if it doesn't exist
mkdir -p .github/config
if [ ! -f .github/config/repository-settings.yml ]; then
  echo "Creating repository settings configuration..."
  cat > .github/config/repository-settings.yml << 'EOF'
# Repository settings configuration
repository:
  name: --ThinkAlike--
  description: "Platform for enhancing human autonomy through ethical technology"
  homepage: https://github.com/EosLumina/--ThinkAlike--
  private: false
  has_issues: true
  has_projects: true
  has_wiki: true
  has_downloads: true
  default_branch: main

# Branch protection rules
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      required_status_checks:
        strict: true
      enforce_admins: false
EOF
  echo "✅ Repository settings configuration created"
fi
