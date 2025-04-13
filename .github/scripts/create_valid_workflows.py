#!/usr/bin/env python3
"""
Create valid GitHub Actions workflow files directly.
This script creates workflow files with correct structure from scratch
and includes self-validation to ensure the files pass validation.
"""

import os
import sys
import re
import yaml
from pathlib import Path

# Dictionary of workflow files to create with their content
WORKFLOW_TEMPLATES = {
    "consolidated-ci.yml": """name: Consolidated CI

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

def validate_workflow(file_path):
    """
    Validate a workflow file to ensure it has all required sections
    and proper formatting.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for 'on:' section with regex first
        on_match = re.search(r'(?:^|\n)\s*on\s*:', content)
        if not on_match:
            print(f"❌ {file_path}: Missing 'on:' section (string check)")
            return False

        # Verify YAML parsing
        try:
            data = yaml.safe_load(content)
            if not data:
                print(f"❌ {file_path}: Empty YAML")
                return False

            # Check for required keys
            if 'on' not in data:
                print(f"❌ {file_path}: Missing 'on' key in YAML")
                return False

            if 'jobs' not in data:
                print(f"❌ {file_path}: Missing 'jobs' key in YAML")
                return False

            print(f"✅ {file_path}: Valid workflow file")
            return True
        except yaml.YAMLError as e:
            print(f"❌ {file_path}: YAML parsing error - {e}")
            return False

    except Exception as e:
        print(f"❌ {file_path}: Error reading file - {e}")
        return False

def create_and_validate_workflow_file(workflows_dir, filename, content):
    """Create a workflow file and validate it"""
    file_path = workflows_dir / filename

    try:
        # Ensure content has proper line endings
        normalized_content = content.replace('\r\n', '\n').strip() + '\n'

        # Write the file with proper line endings
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(normalized_content)

        # Validate the file
        is_valid = validate_workflow(file_path)

        if is_valid:
            print(f"✅ Created and validated: {filename}")
            return True
        else:
            print(f"⚠️ File created but failed validation: {filename}")
            return False

    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return False

def fix_on_section_manually(file_path):
    """
    Manually fix the on section by replacing the file content with a
    known good structure that ensures the 'on:' section is correctly formatted.
    """
    try:
        # Read the current file to get name and jobs sections
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract the name if present
        name_match = re.search(r'name:\s*([^\n]+)', content)
        name = name_match.group(1).strip() if name_match else "Workflow"

        # Extract jobs section if present
        jobs_match = re.search(r'jobs:[\s\S]+$', content)
        jobs_section = jobs_match.group(0) if jobs_match else """jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a command
        run: echo "Hello, world!"
"""

        # Create new content with properly formatted on section
        new_content = f"""name: {name}

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

{jobs_section}
"""

        # Write the corrected content
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)

        print(f"🔧 Manually fixed on section in {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def create_workflow_files():
    """Create all workflow files with valid content"""
    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)

    valid_count = 0
    invalid_count = 0
    fixed_count = 0

    # Install PyYAML if needed for validation
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML for validation...")
        os.system("pip install PyYAML")
        try:
            import yaml
        except ImportError:
            print("❌ Failed to install PyYAML. Continuing without validation.")

    for filename, content in WORKFLOW_TEMPLATES.items():
        file_path = workflows_dir / filename

        # Create and validate the file
        if create_and_validate_workflow_file(workflows_dir, filename, content):
            valid_count += 1
        else:
            invalid_count += 1
            # Try to fix the file manually
            if fix_on_section_manually(file_path):
                fixed_count += 1

    print(f"\n🎉 Results: {valid_count} files valid, {fixed_count}/{invalid_count} invalid files fixed")
    print("Run validation to verify:")
    print("python .github/scripts/validate_workflows.py")

    return valid_count + fixed_count

def emergency_direct_creation():
    """
    Create workflow files in the most direct way possible,
    avoiding any complex processing that might cause issues.
    """
    print("🚨 Performing emergency direct workflow file creation")

    # Ensure we're in the repository root
    if os.path.exists('../.git') and not os.path.exists('.git'):
        os.chdir('..')
        print("Changed to repository root")

    os.makedirs(".github/workflows", exist_ok=True)

    # Create a test workflow file directly to diagnose issues
    test_workflow = """name: Test Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test
        run: echo "Testing"
"""

    try:
        with open(".github/workflows/emergency_test.yml", 'w', encoding='utf-8', newline='\n') as f:
            f.write(test_workflow)
        print("✅ Created emergency test workflow")

        # Run validation script if it exists
        if os.path.exists(".github/scripts/validate_workflows.py"):
            os.system("python .github/scripts/validate_workflows.py .github/workflows/emergency_test.yml")
    except Exception as e:
        print(f"❌ Failed to create emergency test workflow: {e}")

if __name__ == "__main__":
    try:
        result = create_workflow_files()
        if result == 0:
            # If no files were created successfully, try emergency creation
            emergency_direct_creation()
        sys.exit(0 if result > 0 else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        emergency_direct_creation()
        sys.exit(1)
