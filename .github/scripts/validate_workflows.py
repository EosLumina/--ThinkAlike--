#!/usr/bin/env python3
import os
import sys
import yaml

def validate_workflows():
    workflow_dir = '.github/workflows'
    all_valid = True
    
    for filename in os.listdir(workflow_dir):
        if not (filename.endswith('.yml') or filename.endswith('.yaml')):
            continue
            
        if os.path.isdir(os.path.join(workflow_dir, filename)):
            continue
            
        file_path = os.path.join(workflow_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                yaml_content = yaml.safe_load(content)
                
            # Basic structure validation
            if not isinstance(yaml_content, dict):
                print(f"❌ Error in {file_path}: Root element must be a mapping")
                all_valid = False
                continue
                
            required_keys = ['name', 'on', 'jobs']
            for key in required_keys:
                if key not in yaml_content:
                    print(f"❌ Error in {file_path}: Missing required key: '{key}'")
                    all_valid = False
                    continue
                    
            print(f"✅ {file_path} is valid YAML")
            
        except yaml.YAMLError as e:
            print(f"❌ Error in {file_path}: YAML parsing failed: {str(e)}")
            all_valid = False
        except Exception as e:
            print(f"❌ Error in {file_path}: {str(e)}")
            all_valid = False
    
    if all_valid:
        print("\n✅ All workflow files are valid! ✓")
        return 0
    else:
        print("\n❌ Some workflow files have errors ✗")
        return 1

if __name__ == "__main__":
    sys.exit(validate_workflows())
