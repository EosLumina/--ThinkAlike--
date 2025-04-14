#!/usr/bin/env python3
"""
Workflow Cleanup Tool for ThinkAlike

This script analyzes, deduplicates, and fixes workflow files to prevent redundant runs.
"""

import os
import yaml
import glob
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Create backup directory
BACKUP_DIR = Path('.github/workflows/backup')
BACKUP_DIR.mkdir(exist_ok=True, parents=True)

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'='*20} {text} {'='*20}{Style.RESET_ALL}\n")

def print_success(text):
    """Print a success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print an error message."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def backup_workflow(file_path):
    """Create a backup of the workflow file."""
    source = Path(file_path)
    dest = BACKUP_DIR / source.name
    with open(source, 'r') as src_file:
        content = src_file.read()
        with open(dest, 'w') as dst_file:
            dst_file.write(content)
    print_success(f"Created backup of {source.name}")

def load_workflow(file_path):
    """Load a workflow file and return its content."""
    try:
        with open(file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        return workflow
    except Exception as e:
        print_error(f"Failed to load {file_path}: {e}")
        return None

def save_workflow(file_path, workflow):
    """Save workflow content to file."""
    try:
        with open(file_path, 'w') as f:
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)
        print_success(f"Updated {file_path}")
        return True
    except Exception as e:
        print_error(f"Failed to save {file_path}: {e}")
        return False

def analyze_workflows():
    """Analyze all workflows and find duplicates and issues."""
    workflow_dir = Path('.github/workflows')

    if not workflow_dir.exists():
        print_error(f"Workflow directory not found: {workflow_dir}")
        return []

    workflows = []

    # Load all workflows
    for file_path in workflow_dir.glob('*.yml'):
        if file_path.name.startswith('.'):
            continue

        workflow = load_workflow(file_path)
        if workflow:
            workflows.append({
                'path': file_path,
                'content': workflow,
                'name': workflow.get('name', file_path.stem),
                'triggers': workflow.get('on', {}),
                'jobs': list(workflow.get('jobs', {}).keys())
            })

    # Analyze workflows for duplication
    workflow_groups = {}
    for wf in workflows:
        key = wf['name'].lower().replace(' ', '_')
        if key in workflow_groups:
            workflow_groups[key].append(wf)
        else:
            workflow_groups[key] = [wf]

    duplicates = {k: v for k, v in workflow_groups.items() if len(v) > 1}

    return workflows, duplicates

def fix_workflow_triggers(workflow):
    """Fix workflow triggers to be more specific."""
    if not workflow:
        return None

    # Add path filters to prevent unnecessary runs
    triggers = workflow.get('on', {})

    if isinstance(triggers, dict):
        # Fix push events
        if 'push' in triggers:
            push_config = triggers['push']
            if isinstance(push_config, dict):
                # Add path filters based on workflow purpose
                name = workflow.get('name', '').lower()

                # Path filtering
                if 'frontend' in name or 'ui' in name:
                    push_config['paths'] = push_config.get('paths', []) + ['frontend/**', '*.js', '*.ts', '*.jsx', '*.tsx']
                elif 'backend' in name or 'api' in name:
                    push_config['paths'] = push_config.get('paths', []) + ['backend/**', '*.py']
                elif 'doc' in name:
                    push_config['paths'] = push_config.get('paths', []) + ['docs/**', '**/*.md']

                # Ensure we have branches
                if 'branches' not in push_config:
                    push_config['branches'] = ['main']

            # If push is just boolean or string, convert to dict
            elif not isinstance(push_config, dict):
                triggers['push'] = {'branches': ['main']}

        # Fix pull_request events
        if 'pull_request' in triggers:
            pr_config = triggers['pull_request']
            if isinstance(pr_config, dict):
                # Add same path filters as push
                if 'push' in triggers and isinstance(triggers['push'], dict) and 'paths' in triggers['push']:
                    pr_config['paths'] = triggers['push']['paths']

                # Ensure we have branches
                if 'branches' not in pr_config:
                    pr_config['branches'] = ['main']

            # If pull_request is just boolean or string, convert to dict
            elif not isinstance(pr_config, dict):
                triggers['pull_request'] = {'branches': ['main']}

        # Add workflow_dispatch for manual runs if not present
        if 'workflow_dispatch' not in triggers:
            triggers['workflow_dispatch'] = {}

    # If triggers is not a dict (e.g., just a string), fix it
    else:
        workflow['on'] = {
            'push': {'branches': ['main']},
            'pull_request': {'branches': ['main']},
            'workflow_dispatch': {}
        }

    return workflow

def remove_redundant_workflows():
    """Remove redundant workflows from the backup directory."""
    backup_dir = Path('.github/workflows/backup')
    redundant_files = ['ci.yml', 'docs.yml']

    for filename in redundant_files:
        file_path = backup_dir / filename
        if file_path.exists():
            file_path.unlink()
            print_success(f"Removed redundant workflow: {filename}")

def main():
    """Main function to analyze and fix workflows."""
    print_header("Analyzing workflows")

    workflows, duplicates = analyze_workflows()

    if not workflows:
        print_error("No workflows found")
        return

    print_success(f"Found {len(workflows)} workflows")

    if duplicates:
        print_warning(f"Found {len(duplicates)} duplicate workflow groups:")
        for name, dupes in duplicates.items():
            print(f"  - {name}: {', '.join(str(d['path']) for d in dupes)}")

    print_header("Fixing workflow triggers")

    # First back up all workflows
    for wf in workflows:
        backup_workflow(wf['path'])

    # Now fix each workflow
    for wf in workflows:
        print(f"Fixing {wf['path']}...")
        fixed_workflow = fix_workflow_triggers(wf['content'])
        if fixed_workflow:
            save_workflow(wf['path'], fixed_workflow)

    print_header("Removing redundant workflows")
    remove_redundant_workflows()

    print_header("Suggested Next Steps")

    if duplicates:
        print("1. You have many duplicate workflows that trigger on the same events.")
        print("   Consider consolidating them into fewer workflows:")
        print("   - ci.yml - For all continuous integration jobs")
        print("   - deploy.yml - For deployment jobs")
        print("   - docs.yml - For documentation jobs")

    print("\nRun the following to validate the fixed workflows:")
    print("python .github/scripts/validate_workflows.py")

if __name__ == "__main__":
    main()
