#!/usr/bin/env python3
import os
import re
import glob
import yaml

def clean_yaml_files():
    """Remove shell commands from YAML files while preserving the valid YAML content."""
    workflow_dir = '.github/workflows'
    
    # Find all workflow files
    workflow_files = glob.glob(f"{workflow_dir}/*.yml")
    
    for filepath in workflow_files:
        print(f"Cleaning {filepath}...")
        
        # Read file content
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if file contains shell commands
        shell_patterns = [
            r'cat\s+>\s+.*<<\s+.*EOF',  # cat > file << EOF
            r'EOF\s*$',                 # EOF at the end of a line
            r'^#\s+.*',                 # Comments like # Edit file...
        ]
        
        contains_shell = any(re.search(pattern, content, re.MULTILINE) for pattern in shell_patterns)
        
        if contains_shell:
            print(f"  - Contains shell commands, extracting YAML...")
            
            # Try to extract valid YAML
            try:
                # Load the content as YAML
                yaml_content = yaml.safe_load(content)
                
                if yaml_content and isinstance(yaml_content, dict):
                    # Write back only the valid YAML content
                    with open(filepath, 'w') as f:
                        yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False)
                    print(f"  ✓ Cleaned successfully")
                else:
                    print(f"  ✗ Failed to extract valid YAML structure")
            except Exception as e:
                print(f"  ✗ Error cleaning file: {e}")
        else:
            print(f"  - No shell commands found")

if __name__ == "__main__":
    clean_yaml_files()
