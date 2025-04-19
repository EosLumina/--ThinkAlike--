#!/usr/bin/env python3
"""
Verify workflow files have proper 'on' triggers defined and validate specific jobs
"""
import os
import sys
from pathlib import Path
import re
import yaml

def verify_workflow(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for 'on:' section using regex
        on_section = re.search(r'\non\s*:', content)

        if not on_section:
            print(f"❌ {file_path}: Missing 'on' trigger section")
            return False

        # Load YAML content
        yaml_content = yaml.safe_load(content)

        # Validate security-scan job
        if 'jobs' in yaml_content and 'security-scan' in yaml_content['jobs']:
            security_scan_job = yaml_content['jobs']['security-scan']
            if 'steps' not in security_scan_job:
                print(f"❌ {file_path}: 'security-scan' job missing 'steps'")
                return False
            else:
                for step in security_scan_job['steps']:
                    if 'uses' in step and 'jpetrucciani/bandit-check' in step['uses']:
                        if 'path' not in step or 'bandit_flags' not in step:
                            print(f"❌ {file_path}: 'security-scan' job missing 'path' or 'bandit_flags' in Bandit step")
                            return False
                    if 'run' in step and 'npm audit' in step['run']:
                        if 'working-directory' not in step:
                            print(f"❌ {file_path}: 'security-scan' job missing 'working-directory' in npm audit step")
                            return False

        # Validate build job
        if 'jobs' in yaml_content and 'build' in yaml_content['jobs']:
            build_job = yaml_content['jobs']['build']
            if 'steps' not in build_job:
                print(f"❌ {file_path}: 'build' job missing 'steps'")
                return False
            else:
                for step in build_job['steps']:
                    if 'uses' in step and 'docker/login-action' in step['uses']:
                        if 'username' not in step['with'] or 'password' not in step['with']:
                            print(f"❌ {file_path}: 'build' job missing 'username' or 'password' in Docker login step")
                            return False
                    if 'uses' in step and 'docker/build-push-action' in step['uses']:
                        if 'context' not in step['with'] or 'push' not in step['with'] or 'tags' not in step['with']:
                            print(f"❌ {file_path}: 'build' job missing 'context', 'push', or 'tags' in Docker build step")
                            return False

        print(f"✅ {file_path}: Found 'on' trigger and valid jobs")
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
