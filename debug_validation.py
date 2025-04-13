import os
import subprocess
import yaml

# Function to extract the script's validation logic
def extract_validation_logic():
    script_path = ".github/scripts/validate_workflows.py"
    with open(script_path, 'r') as file:
        content = file.read()
        print("=== VALIDATION SCRIPT ANALYSIS ===")
        print(content)
        print("=================================")

# Function to check file contents directly
def check_workflow_file(file_path):
    print(f"\n=== EXAMINING {file_path} ===")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)

            # Try to parse as YAML to check structure
            try:
                yaml_content = yaml.safe_load(content)
                print("\nYAML Structure:")
                has_on = 'on' in yaml_content
                print(f"Has 'on' key: {has_on}")
                if has_on:
                    print(f"'on' value type: {type(yaml_content['on'])}")
                    print(f"'on' contents: {yaml_content['on']}")
            except Exception as e:
                print(f"YAML parsing error: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")

# Main function to run diagnosis
def run_diagnosis():
    try:
        extract_validation_logic()
    except Exception as e:
        print(f"Could not extract validation logic: {e}")

    # Check problematic files
    problem_files = [
        ".github/workflows/consolidated-ci.yml",
        ".github/workflows/deploy_to_gh_pages.yml",
        ".github/workflows/documentation.yml",
        ".github/workflows/settings.yml",
        ".github/workflows/run-tests.yml",
        ".github/workflows/deploy.yml"
    ]

    for file in problem_files:
        check_workflow_file(file)

if __name__ == "__main__":
    run_diagnosis()
