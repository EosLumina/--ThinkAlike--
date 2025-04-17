#!/usr/bin/env python3
"""
Workflow Verification Script

Regularly run this to ensure all workflow files remain valid.
"""
import subprocess
import sys

def verify_workflows():
    print("Verifying GitHub workflow files...")
    result = subprocess.run(
        [sys.executable, '.github/scripts/validate_workflows.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All workflow files are valid")
        return True
    else:
        print("❌ Workflow validation failed:")
        print(result.stdout)
        print(result.stderr)
        return False

if __name__ == "__main__":
    sys.exit(0 if verify_workflows() else 1)
