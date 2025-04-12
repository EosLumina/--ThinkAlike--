#!/usr/bin/env python3
"""
Fix docs.yml workflow file specifically to ensure it has exactly one correct 'on' section.
"""

import os

def fix_docs_yml():
    """Fix the docs.yml workflow file with a clean, correct version."""

    file_path = '.github/workflows/docs.yml'

    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} does not exist")
        return False

    print(f"Fixing {file_path}...")

    # Prepare the correct content for docs.yml with proper 'on' section
    correct_content = """---
name: Documentation CI

on:
  # Workflow triggers
  push:
    branches: [main]
    paths:
      - "docs/**"
      - "**.md"
  pull_request:
    branches: [main]
    paths:
      - "docs/**"
      - "**.md"

jobs:
  markdown_lint:
    name: Markdown Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "16"

      - name: Install markdownlint
        run: npm install -g markdownlint-cli

      - name: Create markdownlint config
        run: |
          echo '{
            "default": true,
            "MD013": false,
            "MD024": false,
            "MD033": false,
            "MD041": false
          }' > .markdownlint.json

      - name: Run markdownlint
        run: markdownlint "**/*.md" --ignore node_modules

      - name: Fix common issues
        run: |
          npm install -g markdownlint-cli2
          npx markdownlint-cli2-fix "**/*.md" --ignore node_modules

  build_docs:
    name: Build Documentation
    runs-on: ubuntu-latest
    needs: markdown_lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material
          pip install -e .  # Install local package in development mode
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Build docs
        run: mkdocs build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: docs-build
          path: ./site

  deploy_docs:
    name: Deploy Documentation
    runs-on: ubuntu-latest
    needs: build_docs
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: docs-build
          path: ./site

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
"""

    # Write the correct content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(correct_content)

    print(f"✅ Fixed {file_path} with a clean, correct version")
    return True

if __name__ == "__main__":
    fix_docs_yml()
