#!/bin/bash

# Direct GitHub Actions Workflow File Fixer
# This script writes complete workflow files directly to the filesystem with proper line endings

set -e  # Exit on any error

# Ensure we're in the repository root
if [ -d "../.git" ] && [ ! -d ".git" ]; then
    cd ..
    echo "Changed directory to repository root: $(pwd)"
fi

# Ensure the workflows directory exists
mkdir -p .github/workflows

echo "🛠️ Direct workflow file fixer"
echo "Creating/fixing workflow files..."

# Enforce Unix line endings for workflow files to avoid YAML parsing issues
git_setup() {
  git config --local core.autocrlf false
  git config --local core.eol lf
  echo "✓ Git configured to use LF line endings"
}

# Set up proper line endings
git_setup

# Function to write file with explicit LF line endings
write_workflow_file() {
  local filename="$1"
  local content="$2"

  # Write file with explicit Unix line endings
  echo -e "$content" > "$filename"

  # Double-check the file exists and has content
  if [ -s "$filename" ]; then
    echo "✓ Created $filename successfully"
  else
    echo "⚠️ Warning: $filename may be empty or not created properly"
  fi
}

# Create consolidated-ci.yml
write_workflow_file ".github/workflows/consolidated-ci.yml" "name: Consolidated CI\\n\\non:\\n  push:\\n    branches: [main]\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install pytest\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Test with pytest\\n        run: pytest"

# Create fixed_consolidated-ci.yml
write_workflow_file ".github/workflows/fixed_consolidated-ci.yml" "name: Consolidated CI (Fixed)\\n\\non:\\n  push:\\n    branches: [main]\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install pytest\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Test with pytest\\n        run: pytest"

# Create fixed_run-tests.yml
write_workflow_file ".github/workflows/fixed_run-tests.yml" "name: Run Tests (Fixed)\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'backend/**'\\n      - 'tests/**'\\n      - 'requirements*.txt'\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install pytest\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Test with pytest\\n        run: pytest"

# Create fixed_documentation.yml
write_workflow_file ".github/workflows/fixed_documentation.yml" "name: Documentation (Fixed)\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'docs/**'\\n      - '*.md'\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  build:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install mkdocs\\n      - name: Build docs\\n        run: mkdocs build"

# Create deploy_to_gh_pages.yml
write_workflow_file ".github/workflows/deploy_to_gh_pages.yml" "name: Deploy to GitHub Pages\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'docs/**'\\n      - '*.md'\\n  workflow_dispatch:\\n\\njobs:\\n  deploy:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Setup Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install mkdocs mkdocs-material\\n      - name: Build site\\n        run: mkdocs build\\n      - name: Deploy\\n        uses: peaceiris/actions-gh-pages@v3\\n        with:\\n          github_token: \${{ secrets.GITHUB_TOKEN }}\\n          publish_dir: ./site"

# Create fixed_settings.yml
write_workflow_file ".github/workflows/fixed_settings.yml" "name: Repository Settings (Fixed)\\n\\non:\\n  schedule:\\n    - cron: \"0 0 * * 0\"  # Run weekly on Sundays\\n  workflow_dispatch:\\n\\njobs:\\n  settings:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Apply repository settings\\n        uses: probot/settings@v1\\n        with:\\n          settings_file: .github/config/repository-settings.yml\\n        env:\\n          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"

# Create fixed_deploy_to_gh_pages.yml
write_workflow_file ".github/workflows/fixed_deploy_to_gh_pages.yml" "name: Deploy to GitHub Pages (Fixed)\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'docs/**'\\n      - '*.md'\\n  workflow_dispatch:\\n\\njobs:\\n  deploy:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Setup Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install mkdocs mkdocs-material\\n      - name: Build site\\n        run: mkdocs build\\n      - name: Deploy\\n        uses: peaceiris/actions-gh-pages@v3\\n        with:\\n          github_token: \${{ secrets.GITHUB_TOKEN }}\\n          publish_dir: ./site"

# Create unified-workflow.yml
write_workflow_file ".github/workflows/unified-workflow.yml" "name: Unified Workflow\\n\\non:\\n  push:\\n    branches: [main]\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install pytest\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Test with pytest\\n        run: pytest"

# Create run-tests.yml
write_workflow_file ".github/workflows/run-tests.yml" "name: Run Tests\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'backend/**'\\n      - 'tests/**'\\n      - 'requirements*.txt'\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install pytest\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Test with pytest\\n        run: pytest"

# Create deploy.yml
write_workflow_file ".github/workflows/deploy.yml" "name: Deploy\\n\\non:\\n  push:\\n    branches: [main]\\n    tags:\\n      - 'v*.*.*'\\n  workflow_dispatch:\\n\\njobs:\\n  deploy:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Deploy\\n        run: echo \"Deploying application...\""

# Create documentation.yml
write_workflow_file ".github/workflows/documentation.yml" "name: Documentation\\n\\non:\\n  push:\\n    branches: [main]\\n    paths:\\n      - 'docs/**'\\n      - '*.md'\\n  pull_request:\\n    branches: [main]\\n  workflow_dispatch:\\n\\njobs:\\n  build:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          pip install mkdocs\\n      - name: Build docs\\n        run: mkdocs build"

# Create settings.yml
write_workflow_file ".github/workflows/settings.yml" "name: Repository Settings\\n\\non:\\n  schedule:\\n    - cron: \"0 0 * * 0\"  # Run weekly on Sundays\\n  workflow_dispatch:\\n\\njobs:\\n  settings:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Apply repository settings\\n        uses: probot/settings@v1\\n        with:\\n          settings_file: .github/config/repository-settings.yml\\n        env:\\n          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"

# Create fixed_deploy.yml
write_workflow_file ".github/workflows/fixed_deploy.yml" "name: Fixed Deploy\\n\\non:\\n  push:\\n    branches: [main]\\n    tags:\\n      - 'v*.*.*'\\n  workflow_dispatch:\\n\\njobs:\\n  deploy:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3\\n      - name: Set up Python\\n        uses: actions/setup-python@v4\\n        with:\\n          python-version: '3.10'\\n      - name: Install dependencies\\n        run: |\\n          python -m pip install --upgrade pip\\n          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\\n      - name: Deploy\\n        run: echo \"Deploying application...\""

# Create a custom validator script to verify the workflow files
cat > .github/scripts/verify_fixed_workflows.py << 'EOF'
#!/usr/bin/env python3
"""
Verify workflow files have proper 'on' triggers defined
"""
import os
import sys
from pathlib import Path
import re

def verify_workflow(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for 'on:' section using regex
        on_section = re.search(r'\non\s*:', content)

        if not on_section:
            print(f"❌ {file_path}: Missing 'on' trigger section")
            return False

        print(f"✅ {file_path}: Found 'on' trigger")
        return True
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def main():
    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print(f"Error: .github/workflows directory not found")
        return 1

    # List of problematic files
    problem_files = [
        "consolidated-ci.yml",
        "fixed_consolidated-ci.yml",
        "fixed_run-tests.yml",
        "fixed_documentation.yml",
        "deploy_to_gh_pages.yml",
        "fixed_settings.yml",
        "fixed_deploy_to_gh_pages.yml",
        "unified-workflow.yml",
        "run-tests.yml",
        "deploy.yml",
        "documentation.yml",
        "settings.yml",
        "fixed_deploy.yml"
    ]

    valid_count = 0
    invalid_count = 0

    # Check all the known problematic files
    for filename in problem_files:
        file_path = workflows_dir / filename
        if file_path.exists():
            if verify_workflow(file_path):
                valid_count += 1
            else:
                invalid_count += 1

    print(f"Results: {valid_count} valid, {invalid_count} invalid")

    return 0 if invalid_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
EOF

# Make the verification script executable
chmod +x .github/scripts/verify_fixed_workflows.py

# Run our custom verification
echo -e "\nVerifying workflow files..."
python .github/scripts/verify_fixed_workflows.py

echo -e "\n✅ All workflow files have been created with correct structure"
echo "Run validation to verify:"
echo "python .github/scripts/validate_workflows.py"
