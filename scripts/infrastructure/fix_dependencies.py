#!/usr/bin/env python3
# filepath: /workspaces/--ThinkAlike--/scripts/infrastructure/fix_dependencies.py
"""Fix dependency conflicts in requirements.txt files."""
import os
import re
import sys
from pathlib import Path

def fix_requirements(file_path):
    """
    Fix dependency conflicts in the specified requirements file.
    
    Args:
        file_path: Path to the requirements file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'r') as f:
            requirements = f.read()
        
        # Check if the file contains the problematic dependency
        if 'uvicorn==0.23.2' not in requirements:
            print(f"ℹ️ No conflict found in {file_path}")
            return True
            
        # Replace specific uvicorn version with compatible version
        updated_requirements = re.sub(
            r'uvicorn==0\.23\.2',
            'uvicorn>=0.24.0',
            requirements
        )
        
        # Write updated requirements back to file
        with open(file_path, 'w') as f:
            f.write(updated_requirements)
        
        print(f"✅ Updated {file_path} to fix uvicorn dependency conflict")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Find and fix dependency conflicts in requirements files."""
    # Possible locations for requirements files
    possible_paths = [
        'requirements.txt',
        'requirements/requirements.txt',
        'requirements/base.txt',
        'requirements/prod.txt'
    ]
    
    # Find existing requirements files
    existing_paths = [p for p in possible_paths if os.path.exists(p)]
    
    if not existing_paths:
        print("❌ No requirements files found in standard locations")
        return 1
    
    # Fix each requirements file
    success = True
    for path in existing_paths:
        if not fix_requirements(path):
            success = False
    
    # Check if we also need to update pyproject.toml
    pyproject_path = 'pyproject.toml'
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, 'r') as f:
                content = f.read()
                
            if 'uvicorn' in content and '0.23.2' in content:
                updated_content = re.sub(
                    r'uvicorn[~=><]+=?0\.23\.2',
                    'uvicorn>=0.24.0',
                    content
                )
                
                with open(pyproject_path, 'w') as f:
                    f.write(updated_content)
                    
                print(f"✅ Updated {pyproject_path} to fix uvicorn dependency conflict")
        except Exception as e:
            print(f"❌ Error processing {pyproject_path}: {e}")
            success = False
    
    if success:
        print("\n✅ All dependency conflicts fixed successfully!")
        
        # Run pip install to verify the fix worked
        if input("Would you like to verify the fix by running pip install? (y/n): ").lower() == 'y':
            import subprocess
            print("\nRunning pip install to verify fix...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", existing_paths[0]], check=True)
                print("✅ Dependencies installed successfully!")
            except subprocess.CalledProcessError:
                print("❌ Dependencies still have conflicts. Further investigation needed.")
                return 1
                
        return 0
    else:
        print("\n⚠️ Some conflicts could not be fixed automatically.")
        return 1

if __name__ == "__main__":
    sys.exit(main())