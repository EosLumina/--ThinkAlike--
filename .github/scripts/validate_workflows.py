#!/usr/bin/env python3
import os
import sys
import yaml

try:
    from colorama import init, Fore, Style
    has_colorama = True
    init()
except ImportError:
    has_colorama = False

def color_text(text, color_code):
    if has_colorama:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text

def success(text):
    return color_text(text, Fore.GREEN)

def error(text):
    return color_text(text, Fore.RED)

def validate_workflow(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            yaml_content = yaml.safe_load(content)
            
        # Basic structure validation
        if not isinstance(yaml_content, dict):
            return False, "Root element must be a mapping"
            
        required_keys = ['name', 'on', 'jobs']
        for key in required_keys:
            if key not in yaml_content:
                return False, f"Missing required key: '{key}'"
                
        print(success(f"✓ {file_path} is valid YAML"))
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def main():
    workflow_dir = '.github/workflows'
    if not os.path.exists(workflow_dir):
        print(error(f"Directory not found: {workflow_dir}"))
        return 1
        
    all_valid = True
    
    for filename in os.listdir(workflow_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            file_path = os.path.join(workflow_dir, filename)
            valid, message = validate_workflow(file_path)
            
            if not valid:
                print(error(f"✗ {file_path} has errors: {message}"))
                all_valid = False
    
    if all_valid:
        print(success("\nAll workflow files are valid! ✓"))
        return 0
    else:
        print(error("\nSome workflow files have errors ✗"))
        return 1

if __name__ == "__main__":
    sys.exit(main())
