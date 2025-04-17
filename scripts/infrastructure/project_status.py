#!/usr/bin/env python3
"""
Project Status Checker for ThinkAlike

Reports on the status of various components and their sovereignty boundaries.
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def check_workflow_files():
    """Check status of GitHub workflow files."""
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        return False, "Workflow directory not found"
    
    workflow_files = list(workflow_dir.glob('*.yml'))
    if not workflow_files:
        return False, "No workflow files found"
    
    # Run the validator if it exists
    validator = Path('.github/scripts/validate_workflows.py')
    if validator.exists() and os.access(validator, os.X_OK):
        try:
            result = subprocess.run([sys.executable, str(validator)], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
            if result.returncode != 0:
                return False, f"Workflow validation failed: {result.stdout}"
            return True, f"{len(workflow_files)} workflow files validated"
        except Exception as e:
            return False, f"Error validating workflows: {e}"
    
    return True, f"{len(workflow_files)} workflow files found (not validated)"

def check_documentation():
    """Check status of project documentation."""
    docs_dir = Path('docs')
    if not docs_dir.exists():
        return False, "Documentation directory not found"
    
    doc_files = list(docs_dir.glob('**/*.md'))
    return True, f"{len(doc_files)} documentation files found"

def check_security():
    """Check security status of the project."""
    security_script = Path('scripts/infrastructure/check_security.py')
    if security_script.exists() and os.access(security_script, os.X_OK):
        try:
            result = subprocess.run([sys.executable, str(security_script)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
            if result.returncode != 0:
                return False, "Security vulnerabilities found"
            return True, "No security vulnerabilities detected"
        except Exception as e:
            return False, f"Error checking security: {e}"
    
    return False, "Security check script not found or not executable"

def main():
    """Run all checks and report status."""
    checks = {
        "Workflow Files": check_workflow_files(),
        "Documentation": check_documentation(),
        "Security": check_security(),
    }
    
    print("ThinkAlike Project Status Report")
    print("===============================")
    
    all_checks_passed = True
    
    for name, (status, message) in checks.items():
        status_symbol = "✓" if status else "✗"
        print(f"{status_symbol} {name}: {message}")
        if not status:
            all_checks_passed = False
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
