#!/usr/bin/env python3
"""Fix CI workflows for GitHub Actions."""
import os
import re
import sys
import subprocess
from pathlib import Path

def fix_frontend_ci():
    """Fix Frontend CI workflow issues."""
    print("📱 Fixing Frontend CI...")
    
    workflow_file = '.github/workflows/frontend.yml'
    
    # Check if workflow file exists
    if not os.path.exists(workflow_file):
        print(f"❌ Frontend workflow file not found: {workflow_file}")
        return False
    
    try:
        # Read the current workflow content
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Ensure we install the missing Babel plugin before running tests
        if 'npm install --save-dev @babel/plugin-proposal-private-property-in-object' not in content:
            # Find the right position to add the npm install command
            if 'steps:' in content and 'npm ci' in content:
                # Add after npm ci
                modified_content = re.sub(
                    r'(npm ci)',
                    r'\1\n      - name: Install missing Babel plugin\n        run: npm install --save-dev @babel/plugin-proposal-private-property-in-object',
                    content
                )
                
                # Write updated content
                with open(workflow_file, 'w') as f:
                    f.write(modified_content)
                    
                print("✅ Added Babel plugin installation to frontend workflow")
            else:
                print("⚠️ Could not locate suitable position to add Babel plugin installation")
        else:
            print("✅ Babel plugin installation already present in workflow")
            
        return True
    except Exception as e:
        print(f"❌ Error fixing frontend workflow: {e}")
        return False

def fix_backend_ci():
    """Fix Backend CI workflow issues."""
    print("🖥️ Fixing Backend CI...")
    
    workflow_file = '.github/workflows/backend.yml'
    
    # Check if workflow file exists
    if not os.path.exists(workflow_file):
        print(f"❌ Backend workflow file not found: {workflow_file}")
        return False
    
    try:
        # Read the current workflow content
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Ensure we install markdown and jinja2 before running tests
        if 'pip install markdown jinja2' not in content:
            # Find the right position to add the pip install command
            if 'pip install -e .' in content:
                # Add after pip install -e .
                modified_content = re.sub(
                    r'(pip install -e \.)',
                    r'\1\n      - name: Install additional dependencies\n        run: pip install markdown jinja2',
                    content
                )
                
                # Write updated content
                with open(workflow_file, 'w') as f:
                    f.write(modified_content)
                    
                print("✅ Added markdown and jinja2 installation to backend workflow")
            else:
                print("⚠️ Could not locate suitable position to add dependency installation")
        else:
            print("✅ Additional dependencies already present in workflow")
            
        # Fix uvicorn version in CI
        if 'uvicorn==0.23.2' in content:
            modified_content = re.sub(
                r'uvicorn==0\.23\.2',
                'uvicorn>=0.24.0',
                content
            )
            
            # Write updated content
            with open(workflow_file, 'w') as f:
                f.write(modified_content)
                
            print("✅ Fixed uvicorn version in backend workflow")
            
        return True
    except Exception as e:
        print(f"❌ Error fixing backend workflow: {e}")
        return False

def fix_doc_sovereignty_ci():
    """Fix Documentation Sovereignty workflow issues."""
    print("📚 Fixing Documentation Sovereignty CI...")
    
    workflow_file = '.github/workflows/doc_sovereignty.yml'
    
    # Check if workflow file exists
    if not os.path.exists(workflow_file):
        print(f"❌ Documentation Sovereignty workflow file not found: {workflow_file}")
        return False
    
    try:
        # Read the current workflow content
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Ensure we create required directories with proper permissions
        if 'mkdir -p docs/integrity' not in content:
            # Find the right position to add the directory creation
            if 'steps:' in content:
                # Add after steps:
                modified_content = re.sub(
                    r'(steps:)',
                    r'\1\n      - name: Create required directories\n        run: mkdir -p docs/integrity',
                    content
                )
                
                # Write updated content
                with open(workflow_file, 'w') as f:
                    f.write(modified_content)
                    
                print("✅ Added directory creation to documentation sovereignty workflow")
            else:
                print("⚠️ Could not locate suitable position to add directory creation")
        else:
            print("✅ Directory creation already present in workflow")
            
        return True
    except Exception as e:
        print(f"❌ Error fixing documentation sovereignty workflow: {e}")
        return False

def main():
    """Main function to fix all CI workflow issues."""
    print("🔧 Fixing CI workflows for GitHub Actions...\n")
    
    # Fix each workflow
    frontend_fixed = fix_frontend_ci()
    backend_fixed = fix_backend_ci()
    doc_sovereignty_fixed = fix_doc_sovereignty_ci()
    
    # Summarize results
    print("\n📋 Summary:")
    print(f"Frontend CI: {'✅ Fixed' if frontend_fixed else '❌ Failed to fix'}")
    print(f"Backend CI: {'✅ Fixed' if backend_fixed else '❌ Failed to fix'}")
    print(f"Documentation Sovereignty: {'✅ Fixed' if doc_sovereignty_fixed else '❌ Failed to fix'}")
    
    if frontend_fixed and backend_fixed and doc_sovereignty_fixed:
        print("\n✅ All workflows fixed successfully!")
        return 0
    else:
        print("\n⚠️ Some workflows could not be fixed automatically.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
