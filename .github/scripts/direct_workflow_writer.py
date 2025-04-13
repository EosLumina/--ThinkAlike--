#!/usr/bin/env python3
"""
Direct file writer for GitHub workflow files with validation issues.
This script completely overwrites problematic files with known good versions.
"""

import os
from pathlib import Path
import sys
import re

def write_workflow(file_path, content):
    """Write content to a file, ensuring it has standard line endings"""
    try:
        # Normalize line endings to Unix style
        content = content.replace('\r\n', '\n')

        # Ensure there's no BOM or other encoding issues
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Wrote file: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error writing {file_path}: {e}")
        return False

def fix_workflows():
    """Fix all workflow files with validation issues"""
    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return False

    # Create a marker to determine if we made any changes
    fixed_count = 0

    # Fix consolidated-ci.yml
    consolidated_ci_content = """name: Consolidated CI

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
"""
    if write_workflow(workflows_dir / "consolidated-ci.yml", consolidated_ci_content):
        fixed_count += 1

    # Fix fixed_consolidated-ci.yml
    fixed_consolidated_ci_content = """name: Consolidated CI (Fixed)

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
"""
    if write_workflow(workflows_dir / "fixed_consolidated-ci.yml", fixed_consolidated_ci_content):
        fixed_count += 1

    # Fix fixed_run-tests.yml
    fixed_run_tests_content = """name: Run Tests (Fixed)

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
"""
    if write_workflow(workflows_dir / "fixed_run-tests.yml", fixed_run_tests_content):
        fixed_count += 1

    # Fix fixed_documentation.yml
    fixed_documentation_content = """name: Documentation (Fixed)

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
"""
    if write_workflow(workflows_dir / "fixed_documentation.yml", fixed_documentation_content):
        fixed_count += 1

    # Fix deploy_to_gh_pages.yml
    deploy_to_gh_pages_content = """name: Deploy to GitHub Pages

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
"""
    if write_workflow(workflows_dir / "deploy_to_gh_pages.yml", deploy_to_gh_pages_content):
        fixed_count += 1

    # Fix fixed_settings.yml
    fixed_settings_content = """name: Repository Settings (Fixed)

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
"""
    if write_workflow(workflows_dir / "fixed_settings.yml", fixed_settings_content):
        fixed_count += 1

    # Fix fixed_deploy_to_gh_pages.yml
    fixed_deploy_to_gh_pages_content = """name: Deploy to GitHub Pages (Fixed)

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
"""
    if write_workflow(workflows_dir / "fixed_deploy_to_gh_pages.yml", fixed_deploy_to_gh_pages_content):
        fixed_count += 1

    # Fix unified-workflow.yml
    unified_workflow_content = """name: Unified Workflow

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
"""
    if write_workflow(workflows_dir / "unified-workflow.yml", unified_workflow_content):
        fixed_count += 1

    # Fix run-tests.yml
    run_tests_content = """name: Run Tests

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
"""
    if write_workflow(workflows_dir / "run-tests.yml", run_tests_content):
        fixed_count += 1

    # Fix deploy.yml
    deploy_content = """name: Deploy

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
"""
    if write_workflow(workflows_dir / "deploy.yml", deploy_content):
        fixed_count += 1

    # Fix documentation.yml
    documentation_content = """name: Documentation

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
"""
    if write_workflow(workflows_dir / "documentation.yml", documentation_content):
        fixed_count += 1

    # Fix settings.yml
    settings_content = """name: Repository Settings

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
"""
    if write_workflow(workflows_dir / "settings.yml", settings_content):
        fixed_count += 1

    # Fix fixed_deploy.yml
    fixed_deploy_content = """name: Fixed Deploy

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
"""
    if write_workflow(workflows_dir / "fixed_deploy.yml", fixed_deploy_content):
        fixed_count += 1

    print(f"\n🎉 Fixed {fixed_count} workflow files")
    print("Run validation to check if all issues are resolved:")
    print("python .github/scripts/validate_workflows.py")

    return fixed_count > 0

if __name__ == "__main__":
    try:
        success = fix_workflows()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
