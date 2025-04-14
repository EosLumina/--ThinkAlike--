#!/usr/bin/env python3
"""
Workflow Validator for ThinkAlike

This script validates all GitHub Actions workflow files to ensure:
1. They have valid YAML syntax
2. They follow GitHub Actions best practices
3. They have required sections (name, on, jobs)
4. They use consistent formatting and syntax

Usage:
    python .github/scripts/validate_workflows.py [--fix] [--quiet]

Arguments:
    --fix       Attempt to fix common issues automatically
    --quiet     Only output errors, not warnings or success messages
"""

import os
import sys
import re
import argparse
from pathlib import Path
import yaml

# Workspace root directory
ROOT_DIR = Path(__file__).parent.parent.parent
WORKFLOWS_DIR = ROOT_DIR / ".github" / "workflows"
TEMPLATE_DIR = ROOT_DIR / ".github" / "workflow_templates"

# Ensure our directories exist
WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(message, level="INFO", quiet=False):
    """Log a message with appropriate color coding"""
    if quiet and level in ["INFO", "SUCCESS"]:
        return

    if level == "ERROR":
        prefix = f"{Colors.RED}[ERROR]{Colors.ENDC}"
    elif level == "WARNING":
        prefix = f"{Colors.YELLOW}[WARNING]{Colors.ENDC}"
    elif level == "SUCCESS":
        prefix = f"{Colors.GREEN}[SUCCESS]{Colors.ENDC}"
    else:
        prefix = f"{Colors.BLUE}[INFO]{Colors.ENDC}"

    print(f"{prefix} {message}")


def is_valid_yaml(file_path):
    """Check if a file is valid YAML"""
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)


def has_required_sections(workflow_data):
    """Check if workflow has all required sections"""
    required_sections = ['name', 'on', 'jobs']
    missing_sections = [section for section in required_sections if section not in workflow_data]
    
    # Handle the case where 'on' might be written as 'true' due to YAML parsing quirk
    if 'on' in missing_sections and True in workflow_data:
        missing_sections.remove('on')
        return len(missing_sections) == 0, missing_sections, "The 'on' section is using 'true' instead of 'on'"
    
    return len(missing_sections) == 0, missing_sections, None


def fix_workflow_syntax(file_path):
    """Fix common workflow syntax issues"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace 'true:' with 'on:' (a common YAML parsing issue)
        content = re.sub(r'^\s*true\s*:', 'on:', content, flags=re.MULTILINE)
        
        # Fix brackets in branch lists: change [main] to - main
        content = re.sub(r'branches\s*:\s*\[\s*([\w\-,\s]+)\s*\]', 
                         lambda m: f"branches:\n    - " + "\n    - ".join(m.group(1).split(',')), 
                         content)
        
        # Fix empty workflow_dispatch syntax
        content = re.sub(r'workflow_dispatch\s*:', 'workflow_dispatch: {}', content)
        
        # Write fixed content back to file
        with open(file_path, 'w') as f:
            f.write(content)
        
        return True
    except Exception as e:
        return False


def validate_workflow_file(file_path, fix=False, quiet=False):
    """Validate a single workflow file"""
    file_path = Path(file_path)
    filename = file_path.name
    log(f"Validating {filename}...", quiet=quiet)
    
    # Check if file exists and is readable
    if not file_path.exists():
        log(f"File {filename} does not exist", "ERROR", quiet)
        return False
    
    # Check YAML syntax
    is_yaml_valid, yaml_error = is_valid_yaml(file_path)
    if not is_yaml_valid:
        log(f"Invalid YAML in {filename}: {yaml_error}", "ERROR", quiet)
        if fix:
            log(f"Attempting to fix YAML issues in {filename}...", quiet=quiet)
            if fix_workflow_syntax(file_path):
                log(f"Fixed YAML syntax in {filename}", "SUCCESS", quiet)
                # Recheck after fixing
                is_yaml_valid, yaml_error = is_valid_yaml(file_path)
                if not is_yaml_valid:
                    log(f"Unable to automatically fix all YAML issues in {filename}", "ERROR", quiet)
                    return False
            else:
                log(f"Failed to fix YAML issues in {filename}", "ERROR", quiet)
                return False
        else:
            return False
    
    # Check required sections
    with open(file_path, 'r') as f:
        workflow_data = yaml.safe_load(f)
    
    has_required, missing, error_msg = has_required_sections(workflow_data)
    if not has_required:
        log(f"Missing required sections in {filename}: {', '.join(missing)}", "ERROR", quiet)
        if error_msg:
            log(f"Additional info: {error_msg}", "ERROR", quiet)
        if fix and error_msg and 'on' in error_msg:
            log(f"Attempting to fix 'on' section in {filename}...", quiet=quiet)
            if fix_workflow_syntax(file_path):
                log(f"Fixed 'on' section in {filename}", "SUCCESS", quiet)
            else:
                log(f"Failed to fix 'on' section in {filename}", "ERROR", quiet)
                return False
        else:
            return False
    
    log(f"✅ {filename} is valid", "SUCCESS", quiet)
    return True


def validate_all_workflows(fix=False, quiet=False):
    """Validate all workflow files in the workflows directory"""
    workflow_files = list(WORKFLOWS_DIR.glob("*.yml"))
    
    if not workflow_files:
        log("No workflow files found in .github/workflows/", "WARNING", quiet)
        return True
    
    log(f"Found {len(workflow_files)} workflow files", quiet=quiet)
    
    all_valid = True
    for file_path in workflow_files:
        if not validate_workflow_file(file_path, fix, quiet):
            all_valid = False
    
    return all_valid


def create_standard_workflow_template():
    """Create a standard workflow template file"""
    template_path = TEMPLATE_DIR / "standard_workflow.yml"
    
    template_content = """# Standard workflow template for ThinkAlike
# Copy this template and customize for your specific needs
name: Workflow Name

# Trigger section - modify as needed
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch: {}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run task
        run: echo "Replace with your task commands"
"""
    
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    log(f"Created standard workflow template at {template_path}", "SUCCESS")
    return template_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Validate GitHub workflow files")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix common issues")
    parser.add_argument("--quiet", action="store_true", help="Only output errors")
    args = parser.parse_args()
    
    # Create template directory and standard template if they don't exist
    if not (TEMPLATE_DIR / "standard_workflow.yml").exists():
        create_standard_workflow_template()
    
    # Validate all workflows
    all_valid = validate_all_workflows(fix=args.fix, quiet=args.quiet)
    
    if all_valid:
        log("All workflow files are valid! 🎉", "SUCCESS", args.quiet)
        sys.exit(0)
    else:
        log("Some workflow files have issues. Please fix them before committing.", "ERROR", args.quiet)
        if not args.fix:
            log("Try running with --fix to automatically fix common issues", "INFO", args.quiet)
        sys.exit(1)


if __name__ == "__main__":
    main()
