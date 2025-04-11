#!/usr/bin/env python3
"""
Contributing Documentation Reorganizer

This script reorganizes the contributing documentation files by creating
symlinks to prevent duplication while maintaining proper structure.
"""

import os
import sys
import shutil
from pathlib import Path

def create_symlinks():
    """Create symlinks for contributing documentation."""
    project_root = Path("/workspaces/--ThinkAlike--")
    
    # Define the main files and their targets
    file_mapping = {
        # Main contributing file at root (canonical source)
        project_root / "CONTRIBUTING.md": None,
        
        # Detailed core contributing file
        project_root / "docs/core/contributing_detailed.md": project_root / "CONTRIBUTING.md",
        
        # Quick contributing guide
        project_root / "docs/contributing_quick.md": None,
        
        # Contributing overview
        project_root / "docs/contributing.md": None
    }
    
    # Back up existing files
    backup_dir = project_root / "backup_contributing"
    backup_dir.mkdir(exist_ok=True)
    
    print("Creating backup of existing contributing files...")
    for source_file in file_mapping.keys():
        if source_file.exists():
            backup_file = backup_dir / source_file.name
            shutil.copy2(source_file, backup_file)
            print(f"✅ Backed up: {source_file} → {backup_file}")
    
    # Create symlinks where specified
    print("\nCreating symlinks for contributing documentation...")
    for source_file, target_file in file_mapping.items():
        if target_file is not None and source_file.exists() and target_file.exists():
            # Create relative symlink
            source_file.unlink(missing_ok=True)
            source_file.symlink_to(os.path.relpath(target_file, source_file.parent))
            print(f"✅ Created symlink: {source_file} → {target_file}")
    
    print("\nContributing files have been reorganized with symlinks.")
    print("All original files were backed up to the 'backup_contributing' directory.")
    
def main():
    """Execute the reorganization."""
    try:
        create_symlinks()
        return 0
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
