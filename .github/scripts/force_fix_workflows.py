#!/usr/bin/env python3
"""
Force fix for GitHub workflow files with missing 'on' triggers
by completely overwriting problematic files with correct versions.
"""

import os
from pathlib import Path
import yaml

# Map of problematic files and their complete correct content
WORKFLOW_FIXES = {
    "fixed_consolidated-ci.yml": """name: Consolidated CI (Fixed)

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
""",

    "fixed_run-tests.yml": """name: Run Tests (Fixed)

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
          if [ -f requirements.txt]; then pip install -r requirements.txt; fi
      - name: Test with pytest
        run: pytest
""",

    "fixed_documentation.yml": """name: Documentation (Fixed)

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
""",

    "deploy_to_gh_pages.yml": """name: Deploy to GitHub Pages

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
""",

    "fixed_settings.yml": """name: Repository Settings (Fixed)

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
""",

    "fixed_deploy_to_gh_pages.yml": """name: Deploy to GitHub Pages (Fixed)

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
""",

    "unified-workflow.yml": """name: Unified Workflow

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
""",

    "run-tests.yml": """name: Run Tests

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
""",

    "deploy.yml": """name: Deploy

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
""",

    "documentation.yml": """name: Documentation

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
""",

    "settings.yml": """name: Repository Settings

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
""",

    "fixed_deploy.yml": """name: Fixed Deploy

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
}

def is_valid_workflow(file_path):
    """Check if a workflow file has a valid structure"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Try to parse as YAML
        try:
            data = yaml.safe_load(content)
            if not data or not isinstance(data, dict):
                return False
            # Check if 'on' is present and properly formed
            if 'on' not in data or not data['on']:
                return False
            # Check if jobs is present
            if 'jobs' not in data or not data['jobs']:
                return False
            return True
        except Exception as e:
            print(f"YAML parsing error in {file_path}: {e}")
            return False
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def force_fix_workflow(file_path, correct_content):
    """Completely overwrite workflow file with correct content"""
    try:
        # First check if the file is already valid
        if is_valid_workflow(file_path):
            print(f"✅ {file_path} already has a valid structure")
            return False

        # If not valid, completely overwrite
        with open(file_path, 'w') as f:
            f.write(correct_content)

        print(f"✅ Fixed {file_path} by complete replacement")
        return True
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix specific workflow files with missing 'on' triggers"""
    # Ensure we're in repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found in {os.getcwd()}")
        return

    fixed_count = 0

    # Process each problematic file
    for filename, correct_content in WORKFLOW_FIXES.items():
        file_path = workflows_dir / filename
        if file_path.exists():
            if force_fix_workflow(str(file_path), correct_content):
                fixed_count += 1
        else:
            print(f"⚠️ File {filename} not found")

    print(f"\n🎉 Fixed {fixed_count} workflow files")
    print("Run validation to check if all issues are resolved:")
    print("python .github/scripts/validate_workflows.py")

if __name__ == "__main__":
    main()
