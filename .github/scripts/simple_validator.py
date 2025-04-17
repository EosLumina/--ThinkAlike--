#!/usr/bin/env python3
import os
import sys
import yaml

def validate_workflows():
    workflow_dir = '.github/workflows'
    all_valid = True
    
    for filename in os.listdir(workflow_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflow_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    content = yaml.safe_load(f)
                    if not isinstance(content, dict):
                        print(f"✗ {filepath}: Not a valid YAML mapping")
                        all_valid = False
                        continue
                    
                    if 'on' not in content:
                        print(f"✗ {filepath}: Missing required key 'on'")
                        all_valid = False
                        continue
                    
                    if 'jobs' not in content:
                        print(f"✗ {filepath}: Missing required key 'jobs'")
                        all_valid = False
                        continue
                    
                    print(f"✓ {filepath} is valid")
                except Exception as e:
                    print(f"✗ {filepath}: Error parsing YAML: {e}")
                    all_valid = False
    
    if all_valid:
        print("\nAll workflow files are valid!")
        return 0
    else:
        print("\nSome workflow files have errors!")
        return 1

if __name__ == "__main__":
    sys.exit(validate_workflows())
