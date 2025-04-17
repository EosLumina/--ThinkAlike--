#!/usr/bin/env python3
"""
Comprehensive workflow fixer for ThinkAlike project.
Run this script to automatically detect and fix all workflow issues.
"""
import os
import re
import sys
import subprocess
import importlib.util

# Auto-install required packages
required_packages = ['pyyaml']
for package in required_packages:
    if importlib.util.find_spec(package) is None:
        print(f"Installing required package: {package}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Now import yaml after ensuring it's installed
import yaml
import shutil
import glob
from pathlib import Path

# ANSI color codes for better terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Add this near the top of your script
with open('/workspaces/--ThinkAlike--/workflow_fix_log.txt', 'w') as log_file:
    log_file.write("Script started\n")
    
# And modify your print functions to write to the log file
def print_to_log(message):
    with open('/workspaces/--ThinkAlike--/workflow_fix_log.txt', 'a') as log_file:
        log_file.write(message + "\n")
    print(message)  # Also print normally

# Replace your print functions with this
def print_success(message):
    """Print success message in green"""
    print(f"{GREEN}{message}{RESET}")
    print_to_log(f"SUCCESS: {message}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{YELLOW}{message}{RESET}")
    print_to_log(f"WARNING: {message}")

def print_error(message):
    """Print error message in red"""
    print(f"{RED}{message}{RESET}")
    print_to_log(f"ERROR: {message}")

def print_section(message):
    """Print section header"""
    print(f"\n{BOLD}{'=' * 50}{RESET}")
    print(f"{BOLD}{message}{RESET}")
    print(f"{BOLD}{'=' * 50}{RESET}")
    print_to_log(f"SECTION: {message}")

def backup_workflows():
    """Create a backup of all workflow files"""
    backup_dir = '.github/workflows/backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    print_section("Creating workflow backups")
    
    # Find all workflow files
    workflow_files = glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml')
    
    for workflow in workflow_files:
        filename = os.path.basename(workflow)
        backup_path = os.path.join(backup_dir, f"{filename}.bak")
        try:
            shutil.copy2(workflow, backup_path)
            print(f"✅ Backed up {workflow} to {backup_path}")
        except Exception as e:
            print_warning(f"⚠️ Couldn't back up {workflow}: {e}")
    
    return len(workflow_files)

def fix_pip_installation_commands():
    """Fix invalid pip installation commands in workflow files"""
    print_section("Fixing pip installation commands")
    
    workflow_files = glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml')
    fixed_count = 0
    
    # Patterns to find invalid pip installation commands
    patterns = [
        (r'pip\s+install\s+-e\s+(?![\./])', 'pip install -e .'),  # -e without path
        (r'pip\s+install\s+-e\s+git\+', 'pip install git+'),      # -e with git URL
    ]
    
    for workflow in workflow_files:
        with open(workflow, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Apply all pattern fixes
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        if content != original:
            with open(workflow, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print_success(f"✅ Fixed pip installation commands in {workflow}")
    
    if fixed_count == 0:
        print_warning("No invalid pip installation commands found")
    else:
        print_success(f"Fixed pip installation commands in {fixed_count} files")
    
    return fixed_count

def fix_devcontainer_dockerfile():
    """Fix the DevContainer Dockerfile"""
    print_section("Fixing DevContainer Dockerfile")
    
    dockerfile = '.devcontainer/Dockerfile'
    if not os.path.exists(dockerfile):
        print_warning(f"⚠️ Dockerfile not found at {dockerfile}")
        return False
    
    with open(dockerfile, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if using Alpine commands on Debian image
    if 'slim-bookworm' in content and 'apk add' in content:
        # Create a fixed Dockerfile
        fixed_content = """# Use the latest secure Python 3.10 version
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install additional dependencies for development environment
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \\
    && apt-get -y install --no-install-recommends \\
    git \\
    curl \\
    nodejs \\
    npm \\
    # Add additional security packages
    ca-certificates \\
    # Add build dependencies
    gcc \\
    python3-dev \\
    libffi-dev \\
    libssl-dev \\
    libpq-dev \\
    # Clean up
    && apt-get autoremove -y \\
    && apt-get clean -y \\
    && rm -rf /var/lib/apt/lists/*

# Security hardening
RUN pip install --no-cache-dir --upgrade pip \\
    && pip config set global.index-url https://pypi.org/simple/ \\
    && pip config set global.trusted-host pypi.org \\
    && pip install pip-audit

# Set the working directory in the container
WORKDIR /workspaces

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
"""
        
        # Back up the original file
        shutil.copy2(dockerfile, f"{dockerfile}.bak")
        
        # Write the fixed content
        with open(dockerfile, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print_success(f"✅ Fixed Dockerfile - replaced Alpine commands with Debian equivalents")
        return True
    else:
        print_warning("Dockerfile appears to be correctly configured")
        return False

def fix_workflow_files():
    """Fix all workflow files with proper structure"""
    print_section("Fixing workflow files structure")
    
    # Create workflows directory if it doesn't exist
    workflows_dir = '.github/workflows'
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Define standard workflow files
    workflows = {
        'frontend.yml': """name: Frontend CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend.yml'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend.yml'

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install missing Babel plugin
        run: npm install --save-dev @babel/plugin-proposal-private-property-in-object
      
      - name: Create .npmrc for legacy dependencies
        run: echo "legacy-peer-deps=true" > .npmrc
      
      - name: Run tests
        run: npm test -- --passWithNoTests
        env:
          CI: true
""",

        'backend.yml': """name: Backend CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'backend/**'
      - '.github/workflows/backend.yml'
      - 'requirements.txt'
      - 'pyproject.toml'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'backend/**'
      - '.github/workflows/backend.yml'
      - 'requirements.txt'
      - 'pyproject.toml'

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
          pip install pytest pytest-cov
          pip install -r requirements.txt
          pip install -e .
          pip install markdown jinja2
          
      - name: Run tests
        run: |
          pytest backend/tests --cov=backend
          
      - name: Lint with flake8
        run: |
          pip install flake8
          # Stop the build if there are Python syntax errors or undefined names
          flake8 backend --count --select=E9,F63,F7,F82 --show-source --statistics
""",

        'docs.yml': """name: Documentation CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'docs/**'
      - '**.md'
      - 'mkdocs.yml'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'docs/**'
      - '**.md'
      - 'mkdocs.yml'
  workflow_dispatch: {}

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
          node-version: '16'

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
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material
          pip install -e .
          pip install markdown jinja2

      - name: Build docs
        run: mkdocs build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: docs-build
          path: ./site
"""
    }
    
    # Create validator script
    os.makedirs('.github/scripts', exist_ok=True)
    validator_script = """#!/usr/bin/env python3
import os
import sys
import yaml

def validate_workflows():
    workflow_dir = '.github/workflows'
    all_valid = True
    
    for filename in os.listdir(workflow_dir):
        if not (filename.endswith('.yml') or filename.endswith('.yaml')):
            continue
            
        if os.path.isdir(os.path.join(workflow_dir, filename)):
            continue
            
        file_path = os.path.join(workflow_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                yaml_content = yaml.safe_load(content)
                
            # Basic structure validation
            if not isinstance(yaml_content, dict):
                print(f"❌ Error in {file_path}: Root element must be a mapping")
                all_valid = False
                continue
                
            required_keys = ['name', 'on', 'jobs']
            for key in required_keys:
                if key not in yaml_content:
                    print(f"❌ Error in {file_path}: Missing required key: '{key}'")
                    all_valid = False
                    continue
                    
            print(f"✅ {file_path} is valid YAML")
            
        except yaml.YAMLError as e:
            print(f"❌ Error in {file_path}: YAML parsing failed: {str(e)}")
            all_valid = False
        except Exception as e:
            print(f"❌ Error in {file_path}: {str(e)}")
            all_valid = False
    
    if all_valid:
        print("\\n✅ All workflow files are valid! ✓")
        return 0
    else:
        print("\\n❌ Some workflow files have errors ✗")
        return 1

if __name__ == "__main__":
    sys.exit(validate_workflows())
"""
    
    with open('.github/scripts/validate_workflows.py', 'w') as f:
        f.write(validator_script)
    os.chmod('.github/scripts/validate_workflows.py', 0o755)
    print("✅ Created validator script at .github/scripts/validate_workflows.py")
    
    # Write workflow files
    for filename, content in workflows.items():
        with open(f'.github/workflows/{filename}', 'w') as f:
            f.write(content)
        print(f"✅ Created .github/workflows/{filename}")
    
    return True

def fix_markdown_linting_script():
    """Create an improved markdown linting script"""
    print_section("Creating enhanced markdown linting script")
    
    script_content = """// filepath: scripts/fix-markdown-linting.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');
const chalk = require('chalk');

// Configuration
const config = {
  lineLength: 100,           // Maximum line length
  standardListMarker: '*',   // Preferred list marker (* or -)
  orderedListStyle: '1.',    // Style for ordered lists
};

function fixMarkdownFile(filePath) {
  console.log(chalk.blue(`Processing ${filePath}...`));
  let content = fs.readFileSync(filePath, 'utf8');
  let fixed = false;

  // Fix line length (MD013)
  const longLines = content.split('\\n').filter(line => 
    line.length > config.lineLength && 
    !line.startsWith('```') && 
    !line.startsWith('http')
  );
  
  if (longLines.length > 0) {
    // We're not actually wrapping lines here as it's complex
    // Just reporting them for manual review
    console.log(chalk.yellow(`  Found ${longLines.length} lines exceeding ${config.lineLength} characters`));
    fixed = true;
  }

  // Fix missing blank lines around headings (MD022)
  const newContent = content.replace(/^(#+\\s+.+?)$\\n([^\\n])/gm, '$1\\n\\n$2');
  if (newContent !== content) {
    content = newContent;
    console.log(chalk.green('  Fixed missing blank lines after headings'));
    fixed = true;
  }

  // Standardize list markers (MD004)
  const listMarkers = content.match(/^[ \\t]*[-*+][ \\t]+/gm);
  if (listMarkers && listMarkers.some(marker => !marker.includes(config.standardListMarker))) {
    // Replace all list markers with the standard one
    const standardized = content.replace(/^([ \\t]*)[-*+]([ \\t]+)/gm, `$1${config.standardListMarker}$2`);
    if (standardized !== content) {
      content = standardized;
      console.log(chalk.green(`  Standardized list markers to ${config.standardListMarker}`));
      fixed = true;
    }
  }

  // Fix multiple consecutive blank lines (MD012)
  const multipleBlankLines = content.replace(/\\n{3,}/g, '\\n\\n');
  if (multipleBlankLines !== content) {
    content = multipleBlankLines;
    console.log(chalk.green('  Fixed multiple consecutive blank lines'));
    fixed = true;
  }

  // Fix ordered list numbering (MD029)
  // This is a simple approach - for more complex lists, a full parser would be needed
  let inOrderedList = false;
  let currentNumber = 1;
  const lines = content.split('\\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const listMatch = line.match(/^([ \\t]*)(\\d+)\\.[ \\t]/);
    
    if (listMatch) {
      if (!inOrderedList) {
        inOrderedList = true;
        currentNumber = 1;
      }
      
      if (parseInt(listMatch[2]) !== currentNumber) {
        lines[i] = line.replace(/^([ \\t]*)\\d+\\./, `$1${currentNumber}.`);
        fixed = true;
      }
      
      currentNumber++;
    } else if (line.trim() === '') {
      inOrderedList = false;
    }
  }
  
  content = lines.join('\\n');

  // Handle document details sections consistently
  // Look for patterns like "**Document Details**" and format them consistently
  const docDetailsPattern = /\\*\\*Document Details\\*\\*\\s*\\n/g;
  if (content.match(docDetailsPattern)) {
    // Format is found, we could standardize it here
    console.log(chalk.blue('  Document details section found - ensure consistent formatting'));
  }

  // Save changes if we fixed anything
  if (fixed) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(chalk.green('  Saved changes'));
  } else {
    console.log(chalk.gray('  No issues to fix'));
  }
  
  return fixed;
}

function fixAllMarkdownFiles() {
  // Find all markdown files in the docs directory
  const files = glob.sync('docs/**/*.md');
  
  console.log(chalk.blue(`Found ${files.length} markdown files to process`));
  
  let fixedCount = 0;
  
  for (const file of files) {
    if (fixMarkdownFile(file)) {
      fixedCount++;
    }
  }
  
  console.log(chalk.green(`Fixed issues in ${fixedCount} out of ${files.length} files`));
}

// Also process README.md
fixMarkdownFile('README.md');
fixAllMarkdownFiles();
"""
    
    with open('scripts/fix-markdown-linting.js', 'w') as f:
        f.write(script_content)
    
    print_success("✅ Created enhanced markdown linting script at scripts/fix-markdown-linting.js")
    return True

def create_workflow_integration_script():
    """Create a workflow integration script to help with PRs"""
    print_section("Creating workflow integration script")
    
    script_content = """#!/usr/bin/env python3
\"\"\"
Script to integrate workflow fixes into a clean branch for PR submission
\"\"\"
import subprocess
import sys
import os
import argparse

def run_command(command, exit_on_error=True):
    \"\"\"Run a shell command and optionally exit on error\"\"\"
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0 and exit_on_error:
        print(f"Error executing: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    return result

def create_integration_branch(source_branch="main", target_branch="workflow-fixes"):
    \"\"\"Create or update the integration branch from source\"\"\"
    # Check if we're on the right branch
    current_branch = run_command("git branch --show-current").stdout.strip()
    if (current_branch != source_branch):
        print(f"Switching from {current_branch} to {source_branch}")
        run_command(f"git checkout {source_branch}")
    
    # Pull latest from source branch
    run_command(f"git pull origin {source_branch}")
    
    # Check if target branch exists
    branches = run_command("git branch").stdout
    
    if target_branch in branches:
        print(f"Target branch {target_branch} exists, checking out")
        run_command(f"git checkout {target_branch}")
        
        # Update with latest from source
        print(f"Updating {target_branch} with latest from {source_branch}")
        merge_result = run_command(f"git merge {source_branch}", exit_on_error=False)
        
        if merge_result.returncode != 0:
            print("Merge conflict detected. You have options:")
            print("1. Resolve conflicts manually and continue")
            print("2. Abort the merge and start over")
            choice = input("Enter choice (1/2): ")
            
            if choice == "1":
                print("Resolve conflicts manually, then run 'git add' on the resolved files")
                print("Then run 'git commit' to complete the merge")
                sys.exit(0)
            else:
                run_command("git merge --abort")
                print("Merge aborted. Starting over with fresh branch")
                run_command(f"git branch -D {target_branch}")
                run_command(f"git checkout -b {target_branch}")
    else:
        # Create the target branch
        print(f"Creating new branch {target_branch} from {source_branch}")
        run_command(f"git checkout -b {target_branch}")
    
    return True

def apply_workflow_fixes():
    \"\"\"Apply workflow fixes to the current branch\"\"\"
    # Run the comprehensive workflow fixer
    run_command("python scripts/fix_all_workflows.py")
    
    # Check for changes
    status = run_command("git status --porcelain").stdout
    
    if not status.strip():
        print("No changes made by the fix scripts")
        return False
    
    # Commit changes
    run_command('git add .')
    run_command('git commit -m "fix: integrated workflow fixes for CI/CD pipeline issues"')
    return True

def push_changes(target_branch="fix/workflow-improvements"):
    \"\"\"Push changes to the specified branch\"\"\"
    current_branch = run_command("git branch --show-current").stdout.strip()
    
    # Create a new branch for the PR
    run_command(f"git checkout -b {target_branch}")
    
    # Push to remote
    push_result = run_command(f"git push -u origin {target_branch}", exit_on_error=False)
    
    if push_result.returncode != 0:
        print(f"Error pushing to {target_branch}")
        print(push_result.stderr)
        
        # Ask if forced push is okay
        force_push = input("Force push? This will overwrite remote branch (y/n): ")
        if force_push.lower() == 'y':
            run_command(f"git push -f -u origin {target_branch}")
        else:
            print("Push aborted")
            return False
    
    print(f"Changes pushed to {target_branch}")
    
    # Print PR creation link
    remote_url = run_command("git remote get-url origin").stdout.strip()
    if "github.com" in remote_url:
        # Extract owner and repo
        repo_info = remote_url.split("github.com/")[1].replace(".git", "")
        print(f"\\nCreate PR: https://github.com/{repo_info}/compare/main...{target_branch}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Integrate workflow fixes")
    parser.add_argument("--source", default="main", help="Source branch (default: main)")
    parser.add_argument("--temp", default="workflow-fixes-temp", help="Temporary integration branch")
    parser.add_argument("--target", default="fix/workflow-improvements", help="Target PR branch")
    parser.add_argument("--no-push", action="store_true", help="Skip pushing changes")
    
    args = parser.parse_args()
    
    # Create integration branch
    create_integration_branch(args.source, args.temp)
    
    # Apply fixes
    changes_made = apply_workflow_fixes()
    
    if not changes_made:
        print("No changes to push")
        return
    
    if not args.no_push:
        # Push changes
        push_changes(args.target)
    else:
        print("Changes applied but not pushed (--no-push flag used)")

if __name__ == "__main__":
    main()
"""
    
    with open('scripts/workflow_integration.py', 'w') as f:
        f.write(script_content)
    os.chmod('scripts/workflow_integration.py', 0o755)
    
    print_success("✅ Created workflow integration script at scripts/workflow_integration.py")
    return True

def validate_fixes():
    """Validate the fixed workflow files"""
    print_section("Validating workflow fixes")
    
    # Check if validation script exists
    validator_path = '.github/scripts/validate_workflows.py'
    if not os.path.exists(validator_path):
        print_warning(f"⚠️ Validator script not found at {validator_path}")
        return False
    
    print("Running workflow validation...")
    try:
        result = subprocess.run(['python', validator_path], capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode == 0:
            print_success("✅ All workflow files validated successfully!")
            return True
        else:
            print_error("❌ Some workflow files still have issues!")
            return False
    except Exception as e:
        print_error(f"❌ Error running validator: {e}")
        return False

def main():
    """Main function to run all fixes"""
    print_section("ThinkAlike Comprehensive Workflow Fix Tool")
    
    # Count of files backed up
    backup_count = backup_workflows()
    
    # Fix pip installation commands
    pip_fix_count = fix_pip_installation_commands()
    
    # Fix DevContainer Dockerfile
    dockerfile_fixed = fix_devcontainer_dockerfile()
    
    # Fix workflow files
    workflows_fixed = fix_workflow_files()
    
    # Create improved markdown linting script
    markdown_script_created = fix_markdown_linting_script()
    
    # Create workflow integration script
    integration_script_created = create_workflow_integration_script()
    
    # Validate fixes
    validation_successful = validate_fixes()
    
    # Print summary
    print_section("Fix Summary")
    print(f"Workflow files backed up: {backup_count}")
    print(f"Pip installation commands fixed: {pip_fix_count}")
    print(f"DevContainer Dockerfile fixed: {dockerfile_fixed}")
    print(f"Workflow files created/fixed: {workflows_fixed}")
    print(f"Markdown linting script created: {markdown_script_created}")
    print(f"Workflow integration script created: {integration_script_created}")
    print(f"Validation successful: {validation_successful}")
    
    # Next steps
    print_section("Next Steps")
    print("1. Run the following command to validate all workflow files:")
    print("   python .github/scripts/validate_workflows.py")
    print()
    print("2. Run the markdown linting script to fix documentation issues:")
    print("   node scripts/fix-markdown-linting.js")
    print()
    print("3. Create a PR with the workflow fixes:")
    print("   python scripts/workflow_integration.py")
    print()
    print("4. Review and test the workflow files before merging")

if __name__ == "__main__":
    main()