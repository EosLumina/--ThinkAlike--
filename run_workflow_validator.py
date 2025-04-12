#!/usr/bin/env python3
"""
Helper script to install required dependencies and run the workflow validator.
"""

import os
import sys
import subprocess

def ensure_dependencies():
    """Ensure all required dependencies are installed."""
    try:
        import yaml
        print("✅ PyYAML is already installed")
    except ImportError:
        print("⚠️ Installing PyYAML...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML"])
        print("✅ PyYAML installed successfully")

def run_validator():
    """Run the workflow validator with the provided arguments."""
    cmd = [sys.executable, "workflow_validator.py"] + sys.argv[1:]
    return subprocess.call(cmd)

if __name__ == "__main__":
    ensure_dependencies()
    sys.exit(run_validator())
