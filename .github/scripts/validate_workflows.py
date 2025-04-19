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

            # Validate security-scan job
            if 'jobs' in yaml_content and 'security-scan' in yaml_content['jobs']:
                security_scan_job = yaml_content['jobs']['security-scan']
                if 'steps' not in security_scan_job:
                    print(f"❌ Error in {file_path}: 'security-scan' job missing 'steps'")
                    all_valid = False
                else:
                    for step in security_scan_job['steps']:
                        if 'uses' in step and 'jpetrucciani/bandit-check' in step['uses']:
                            if 'path' not in step or 'bandit_flags' not in step:
                                print(f"❌ Error in {file_path}: 'security-scan' job missing 'path' or 'bandit_flags' in Bandit step")
                                all_valid = False
                        if 'run' in step and 'npm audit' in step['run']:
                            if 'working-directory' not in step:
                                print(f"❌ Error in {file_path}: 'security-scan' job missing 'working-directory' in npm audit step")
                                all_valid = False

            # Validate build job
            if 'jobs' in yaml_content and 'build' in yaml_content['jobs']:
                build_job = yaml_content['jobs']['build']
                if 'steps' not in build_job:
                    print(f"❌ Error in {file_path}: 'build' job missing 'steps'")
                    all_valid = False
                else:
                    for step in build_job['steps']:
                        if 'uses' in step and 'docker/login-action' in step['uses']:
                            if 'username' not in step['with'] or 'password' not in step['with']:
                                print(f"❌ Error in {file_path}: 'build' job missing 'username' or 'password' in Docker login step")
                                all_valid = False
                        if 'uses' in step and 'docker/build-push-action' in step['uses']:
                            if 'context' not in step['with'] or 'push' not in step['with'] or 'tags' not in step['with']:
                                print(f"❌ Error in {file_path}: 'build' job missing 'context', 'push', or 'tags' in Docker build step")
                                all_valid = False

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
