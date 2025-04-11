#!/usr/bin/env python

import os
import sys
import subprocess
import yaml

def check_python_dependencies():
    """Check if required Python packages are installed correctly."""
    print("Checking Python dependencies...")
    try:
        import pkg_resources
        required = []
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-e '):
                    required.append(line)

        # Check installed packages
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = [pkg for pkg in required if pkg.split('==')[0].lower() not in installed]

        if missing:
            print(f"⚠️ Missing packages: {', '.join(missing)}")
        else:
            print("✅ All Python dependencies installed")
    except Exception as e:
        print(f"⚠️ Error checking dependencies: {e}")

def validate_workflow_files():
    """Check if workflow YAML files are valid."""
    print("Validating workflow files...")
    workflow_dir = '.github/workflows'

    if not os.path.exists(workflow_dir):
        print(f"⚠️ Workflow directory not found: {workflow_dir}")
        return

    for filename in os.listdir(workflow_dir):
        if filename.endswith(('.yml', '.yaml')):
            filepath = os.path.join(workflow_dir, filename)
            print(f"Checking {filepath}...")

            try:
                with open(filepath, 'r') as f:
                    yaml_content = yaml.safe_load(f)
                print(f"✅ {filepath} is valid YAML")

                # Check for common issues
                if 'jobs' not in yaml_content:
                    print(f"⚠️ No jobs defined in {filepath}")

                # Check Python versions
                for job_id, job in yaml_content.get('jobs', {}).items():
                    if 'steps' in job:
                        for step in job['steps']:
                            if step.get('uses', '').startswith('actions/setup-python'):
                                python_version = step.get('with', {}).get('python-version')
                                print(f"   Job '{job_id}' uses Python {python_version}")
            except Exception as e:
                print(f"❌ Error validating {filepath}: {e}")

def check_import_paths():
    """Run a simple test to check import paths."""
    print("Checking import paths...")
    test_script = """
import sys
import os
print("Python path:")
for p in sys.path:
    print(f"  {p}")
try:
    import great_expectations
    print("✅ great_expectations imported successfully")
except ImportError as e:
    print(f"❌ great_expectations import failed: {e}")
    """

    try:
        result = subprocess.run([sys.executable, '-c', test_script],
                                capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
    except Exception as e:
        print(f"⚠️ Error running import test: {e}")

if __name__ == "__main__":
    print("=== ThinkAlike Workflow Diagnostic Tool ===")
    check_python_dependencies()
    print("\n")
    validate_workflow_files()
    print("\n")
    check_import_paths()
