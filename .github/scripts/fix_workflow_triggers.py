#!/usr/bin/env python3
import yaml
import pathlib
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def add_missing_trigger(file_path):
    """Add missing 'on' trigger to GitHub workflow file if needed."""
    print(f"Processing {file_path}...")

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Parse YAML content
        yaml_content = yaml.safe_load(content)

        # Skip if not a valid workflow file or already has 'on' trigger
        if not isinstance(yaml_content, dict):
            print(f"{Fore.YELLOW}⚠ Not a valid workflow file, skipping{Style.RESET_ALL}")
            return False

        if 'on' in yaml_content:
            print(f"{Fore.GREEN}✓ Already has trigger definition{Style.RESET_ALL}")
            return False

        # Add standard trigger (push to main, pull requests to main)
        yaml_content['on'] = {
            'push': {
                'branches': ['main']
            },
            'pull_request': {
                'branches': ['main']
            },
            'workflow_dispatch': {}
        }

        # Write updated content back to file
        with open(file_path, 'w') as f:
            # Make sure 'name' comes first, then 'on' trigger
            ordered_content = {}
            if 'name' in yaml_content:
                ordered_content['name'] = yaml_content['name']
                del yaml_content['name']

            ordered_content['on'] = yaml_content['on']
            del yaml_content['on']

            # Add the rest of the content
            for key, value in yaml_content.items():
                ordered_content[key] = value

            # Write to file with proper formatting
            yaml.dump(ordered_content, f, default_flow_style=False, sort_keys=False)

        print(f"{Fore.GREEN}✓ Added trigger definition{Style.RESET_ALL}")
        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Error processing file: {e}{Style.RESET_ALL}")
        return False

def main():
    """Process all workflow files in the .github/workflows directory."""
    workflow_dir = pathlib.Path('.github/workflows')
    if not workflow_dir.exists():
        print(f"{Fore.RED}Workflow directory not found: {workflow_dir}{Style.RESET_ALL}")
        return 1

    fixed_count = 0
    for file_path in workflow_dir.glob('*.yml'):
        if add_missing_trigger(file_path):
            fixed_count += 1

    if fixed_count > 0:
        print(f"\n{Fore.GREEN}Fixed {fixed_count} workflow files{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}No workflows needed fixing{Style.RESET_ALL}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
