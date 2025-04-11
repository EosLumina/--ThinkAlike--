import os
import sys
import yaml
import pathlib
from colorama import init, Fore, Style

# Initialize colorama
init()

def validate_yaml_file(file_path):
    """Validates YAML syntax in the given file."""
    print(f"Checking {file_path}...")

    try:
        with open(file_path, 'r') as f:
            yaml_content = yaml.safe_load(f)
        print(f"{Fore.GREEN}✓ YAML syntax is valid{Style.RESET_ALL}")
        return True, yaml_content
    except yaml.YAMLError as e:
        print(f"{Fore.RED}✗ YAML syntax error: {e}{Style.RESET_ALL}")
        return False, None

def validate_github_workflow(yaml_content):
    """Validates GitHub Actions workflow structure."""
    errors = []

    # Check basic structure
    if not isinstance(yaml_content, dict):
        errors.append("Workflow must be a dictionary/map")
        return False, errors

    # Check required fields
    if 'name' not in yaml_content:
        errors.append("Workflow missing 'name' field")

    if 'on' not in yaml_content:
        errors.append("Workflow missing 'on' trigger definition")

    if 'jobs' not in yaml_content:
        errors.append("Workflow missing 'jobs' section")
    elif not isinstance(yaml_content['jobs'], dict):
        errors.append("'jobs' must be a dictionary/map")
    else:
        # Validate each job
        for job_id, job in yaml_content['jobs'].items():
            if not isinstance(job, dict):
                errors.append(f"Job '{job_id}' must be a dictionary/map")
                continue

            if 'runs-on' not in job:
                errors.append(f"Job '{job_id}' missing 'runs-on' field")

            if 'steps' not in job:
                errors.append(f"Job '{job_id}' missing 'steps' field")
            elif not isinstance(job['steps'], list):
                errors.append(f"Steps for job '{job_id}' must be a list")
            else:
                # Validate each step
                for i, step in enumerate(job['steps']):
                    if not isinstance(step, dict):
                        errors.append(f"Step #{i+1} in job '{job_id}' must be a dictionary/map")
                        continue

                    # Check for duplicate names
                    if i > 0 and 'name' in step and any(s.get('name') == step['name'] for s in job['steps'][:i]):
                        errors.append(f"Duplicate step name '{step['name']}' in job '{job_id}'")

    success = len(errors) == 0
    return success, errors

def main():
    """Main function to validate all workflow files."""
    workflow_dir = pathlib.Path('.github/workflows')
    if not workflow_dir.exists():
        print(f"{Fore.RED}Workflow directory not found: {workflow_dir}{Style.RESET_ALL}")
        return 1

    all_valid = True
    for file_path in workflow_dir.glob('*.yml'):
        print(f"\n{Fore.CYAN}===== Validating {file_path} ====={Style.RESET_ALL}")

        # Validate YAML syntax
        yaml_valid, yaml_content = validate_yaml_file(file_path)
        if not yaml_valid:
            all_valid = False
            continue

        # Validate workflow structure
        workflow_valid, workflow_errors = validate_github_workflow(yaml_content)
        if not workflow_valid:
            all_valid = False
            print(f"{Fore.RED}✗ Workflow structure has issues:{Style.RESET_ALL}")
            for error in workflow_errors:
                print(f"  - {error}")
        else:
            print(f"{Fore.GREEN}✓ Workflow structure is valid{Style.RESET_ALL}")

    if all_valid:
        print(f"\n{Fore.GREEN}All workflows validated successfully!{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.RED}Some workflows have issues that need to be fixed.{Style.RESET_ALL}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
