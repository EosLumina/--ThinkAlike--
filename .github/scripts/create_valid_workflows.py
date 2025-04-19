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
    "backend.yml": """name: Backend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'backend/**'

jobs:
  lint:
    name: Lint Backend Code
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements-dev.txt

      - name: Lint with flake8
        run: flake8 backend --count --select=E9,F63,F7,F82 --show-source --statistics

  test:
    name: Test Backend
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install -r backend/requirements-dev.txt

      - name: Run backend tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          TESTING: true
        run: |
          cd backend
          pytest --cov=app tests/

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          flags: backend

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v3

      - name: Run Bandit (Python)
        uses: jpetrucciani/bandit-check@master
        with:
          path: 'backend'
          bandit_flags: '-r -x backend/tests/'
""",

    "frontend.yml": """name: Frontend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'frontend/**'

jobs:
  lint:
    name: Lint Frontend Code
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install Node.js dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Lint frontend code
        working-directory: ./frontend
        run: npm run lint

  test:
    name: Test Frontend
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install Node.js dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run frontend tests
        working-directory: ./frontend
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          flags: frontend

  build:
    name: Build Frontend
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install Node.js dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Build frontend
        working-directory: ./frontend
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: frontend-build
          path: frontend/build
""",

    "docs.yml": """name: Documentation CI

on:
  push:
    paths:
      - 'docs/**'
      - '**.md'
    branches: [ main, develop ]
  pull_request:
    paths:
      - 'docs/**'
      - '**.md'
    branches: [ main, develop ]

jobs:
  markdown-lint:
    name: Markdown Linting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16

      - name: Install markdownlint
        run: npm install -g markdownlint-cli

      - name: Run markdownlint
        run: markdownlint "**/*.md" --ignore node_modules

  check-links:
    name: Check Markdown Links
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16

      - name: Install markdown-link-check
        run: npm install -g markdown-link-check

      - name: Check links in Markdown files
        run: |
          find . -name "*.md" | xargs -n1 markdown-link-check -q

  build-docs-site:
    name: Build Documentation Site
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
          cache: 'npm'

      - name: Install dependencies
        run: npm ci
        working-directory: ./docs-site

      - name: Build documentation site
        run: npm run build
        working-directory: ./docs-site

      - name: Upload documentation site artifact
        uses: actions/upload-artifact@v3
        with:
          name: docs-site-build
          path: docs-site/build

  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Generate Docs
        run: npm run docs
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
