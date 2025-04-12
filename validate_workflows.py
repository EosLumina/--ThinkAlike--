import yaml
import sys
import os
import re

def fix_yaml_spacing(file_path):
    """Fix common YAML spacing issues in workflow files"""
    print(f"Fixing spacing in {file_path}...")

    with open(file_path, 'r') as file:
        content = file.read()

    # Fix spacing inside brackets
    content = re.sub(r'\[ +', '[', content)
    content = re.sub(r' +\]', ']', content)

    # Add document start if missing
    if not content.startswith('---'):
        content = f"---\n{content}"

    # Write back the fixed content
    with open(file_path, 'w') as file:
        file.write(content)

    print(f"✅ Fixed spacing issues in {file_path}")
    return content

def validate_workflow(file_path, fix=True):
    print(f"Validating {file_path}...")

    try:
        # First fix formatting issues if requested
        if fix:
            content = fix_yaml_spacing(file_path)
        else:
            with open(file_path, 'r') as file:
                content = file.read()

        # Parse YAML content
        yaml_content = yaml.safe_load(content)

        # Basic structure checks
        if not yaml_content.get('name'):
            print(f"⚠️ Warning: Workflow missing 'name' attribute")

        if 'on' not in yaml_content:
            print(f"❌ Error: Workflow missing 'on' trigger section")
            return False

        if 'jobs' not in yaml_content:
            print(f"❌ Error: Workflow missing 'jobs' section")
            return False

        # Check for basic job structure
        for job_id, job in yaml_content['jobs'].items():
            if 'runs-on' not in job:
                print(f"❌ Error: Job '{job_id}' missing 'runs-on' attribute")
                return False
            if 'steps' not in job or not job['steps']:
                print(f"⚠️ Warning: Job '{job_id}' has no steps defined")

        print(f"✅ {file_path} passed basic validation")
        return True
    except yaml.YAMLError as e:
        print(f"❌ Error: Invalid YAML in {file_path}")
        print(f"   Details: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: Failed to validate {file_path}")
        print(f"   Details: {e}")
        return False

if __name__ == "__main__":
    workflow_dir = ".github/workflows"
    if not os.path.exists(workflow_dir):
        print(f"❌ Error: Workflow directory {workflow_dir} not found")
        sys.exit(1)

    workflow_files = [
        os.path.join(workflow_dir, "docs.yml"),
        os.path.join(workflow_dir, "backend.yml"),
        os.path.join(workflow_dir, "frontend.yml")
    ]

    fix_files = "--fix" in sys.argv

    all_valid = True
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ Error: Workflow file {workflow_file} not found")
            all_valid = False
            continue

        file_valid = validate_workflow(workflow_file, fix=fix_files)
        if not file_valid:
            all_valid = False

    if all_valid:
        print("\n✅ All workflow files passed basic validation")
        sys.exit(0)
    else:
        print("\n❌ Some workflow files failed validation")
        print("   Run with --fix to attempt automatic fixes")
        sys.exit(1)
