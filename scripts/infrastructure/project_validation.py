#!/usr/bin/env python3
"""
Validate all aspects of the ThinkAlike project.
"""
import os
import sys
import subprocess

def validate_workflow_files():
    """Check if all workflow files are valid."""
    print("Validating workflow files...")
    try:
        result = subprocess.run(
            [sys.executable, ".github/scripts/validate_workflows.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ All workflow files are valid")
            return True
        else:
            print(f"❌ Workflow validation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error validating workflows: {e}")
        return False

def validate_dependencies():
    """Check if all required dependencies are installed."""
    print("Validating dependencies...")
    required_packages = ["markdown", "jinja2", "uvicorn", "fastapi"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        return False
    else:
        print("✅ All required dependencies are installed")
        return True

def validate_backend_services():
    """Check if backend services initialize correctly."""
    print("Validating backend services...")
    try:
        # Try importing a few key modules to ensure they load correctly
        from backend.app.services.documentation_service import DocumentationService
        print("✅ Documentation service imports correctly")
        return True
    except Exception as e:
        print(f"❌ Error initializing backend services: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🔍 Running ThinkAlike project validation\n")
    
    validations = [
        validate_workflow_files,
        validate_dependencies,
        validate_backend_services
    ]
    
    results = []
    for validation in validations:
        results.append(validation())
        print()
    
    if all(results):
        print("✅ All validation checks passed! The project is ready.")
        return 0
    else:
        print("❌ Some validation checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
