#!/usr/bin/env python3
"""
Emergency fix for GitHub workflow files.

This script completely rebuilds all workflow files to ensure they have proper 'on' sections.
"""

import os
import sys
import re

def fix_all_workflows():
    """Fix all workflow files with proper 'on' sections."""
    workflow_dir = '.github/workflows'
    if not os.path.isdir(workflow_dir):
        print(f"❌ Error: Workflow directory {workflow_dir} not found")
        return False

    file_paths = [os.path.join(workflow_dir, f) for f in os.listdir(workflow_dir)
                 if f.endswith(('.yml', '.yaml'))]

    fixed_count = 0

    # First handle docs.yml specially
    docs_yml_path = os.path.join(workflow_dir, "docs.yml")
    if os.path.exists(docs_yml_path):
        fix_docs_workflow(docs_yml_path)
        fixed_count += 1
        # Remove from the list to avoid processing twice
        if docs_yml_path in file_paths:
            file_paths.remove(docs_yml_path)

    # Fix all other workflow files
    for file_path in file_paths:
        if fix_generic_workflow(file_path):
            fixed_count += 1

    print(f"\n=== Summary ===")
    print(f"Total workflow files processed: {len(file_paths) + 1}")  # +1 for docs.yml
    print(f"Files fixed: {fixed_count}")

    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} workflow files")
        return True
    else:
        print("\n⚠️ No files were modified")
        return False

def fix_docs_workflow(file_path):
    """Fix the docs.yml workflow with a predefined correct structure."""
    print(f"Fixing specialized workflow: {file_path}")

    content = """---
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

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"✅ Fixed {file_path} with predefined structure")
    return True

def fix_generic_workflow(file_path):
    """Fix a generic workflow file with a simple structure."""
    print(f"Fixing generic workflow: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract workflow name
        name_match = re.search(r'name:\s*(.*?)(\r?\n)', content)
        name = name_match.group(1) if name_match else os.path.basename(file_path).replace('.yml', '').replace('.yaml', '')

        # Extract jobs section or create a basic one
        jobs_match = re.search(r'(jobs:.*?)$', content, re.DOTALL)
        jobs_section = jobs_match.group(1) if jobs_match else """jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Placeholder step
        run: echo "Add workflow steps here"
"""

        # Create a clean workflow file
        new_content = f"""---
name: {name}

on:
  # Workflow triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

{jobs_section}"""

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"✅ Fixed {file_path} with proper structure")
        return True

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

if __name__ == "__main__":
    fix_all_workflows()
    print("\nNow validate the fixes by running:")
    print("python workflow_validator.py --verbose")
