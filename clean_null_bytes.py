#!/usr/bin/env python3
"""
Documentation Sovereignty Null Byte Cleaner

A revolutionary tool for removing invisible control characters that undermine
the integrity of our knowledge commons.

This embodies our principle of Radical Transparency by making invisible
boundary violations visible and removable.
"""

import os
import sys
from pathlib import Path

def clean_file(filepath):
    """Remove null bytes from a file, preserving all meaningful content."""
    print(f"Examining {filepath} for boundary violations...")
    
    try:
        # Read file as binary to detect null bytes
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for null bytes
        if b'\x00' in content:
            # Remove null bytes
            clean_content = content.replace(b'\x00', b'')
            
            # Write cleaned content back
            with open(filepath, 'wb') as f:
                f.write(clean_content)
            
            print(f"✅ Liberated {filepath} from {content.count(b'\x00')} invisible control characters")
            return True
        else:
            print(f"📝 File already free from null byte corruption: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Clean null bytes from specified files or directories."""
    if len(sys.argv) < 2:
        print("Usage: python3 clean_null_bytes.py <file_or_directory_path> [additional_paths...]")
        print("\nExample: python3 clean_null_bytes.py backend/app/services/ scripts/")
        return
    
    files_cleaned = 0
    
    for path_arg in sys.argv[1:]:
        path = Path(path_arg)
        
        if path.is_file():
            # Clean single file
            if clean_file(path):
                files_cleaned += 1
        elif path.is_dir():
            # Clean all .py files in directory recursively
            for py_file in path.glob('**/*.py'):
                if clean_file(py_file):
                    files_cleaned += 1
        else:
            print(f"⚠️ Path not found: {path}")
    
    print(f"\n✨ Liberation complete: {files_cleaned} files freed from invisible control")

if __name__ == "__main__":
    main()
