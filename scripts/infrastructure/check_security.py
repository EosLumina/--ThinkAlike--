#!/usr/bin/env python3
"""
Security vulnerability checker for ThinkAlike

This script verifies that all dependencies meet minimum security requirements.
"""
import sys
import pkg_resources
import re
from pathlib import Path

REQUIRED_VERSIONS = {
    "pydantic": ">=2.5.0,<3.0.0",
    "python-jose": ">=3.3.0,<4.0.0",
    "passlib": ">=1.7.4,<1.8.0",
}

def parse_version_spec(spec):
    """Parse a version specification into min and max versions."""
    min_version = None
    max_version = None
    
    for part in spec.split(','):
        part = part.strip()
        if part.startswith('>='):
            min_version = part[2:]
        elif part.startswith('>'):
            min_version = part[1:]
        elif part.startswith('<'):
            max_version = part[1:]
    
    return min_version, max_version

def check_dependencies():
    """Check if installed dependencies meet security requirements."""
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    issues = []
    
    for package, required_version in REQUIRED_VERSIONS.items():
        if package not in installed_packages:
            issues.append(f"MISSING: {package} {required_version}")
            continue
            
        installed_version = installed_packages[package]
        min_required, max_allowed = parse_version_spec(required_version)
        
        if min_required and pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(min_required):
            issues.append(f"OUTDATED: {package} {installed_version} (required: {required_version})")
        
        if max_allowed and pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version(max_allowed):
            issues.append(f"TOO NEW: {package} {installed_version} (required: {required_version})")
    
    return issues

if __name__ == "__main__":
    print("Checking for security vulnerabilities in dependencies...")
    issues = check_dependencies()
    
    if issues:
        print("\nSecurity issues found:")
        for issue in issues:
            print(f"  • {issue}")
        print("\nRun the following to fix:")
        print('pip3 install --upgrade "pydantic>=2.5.0,<3.0.0" "python-jose>=3.3.0,<4.0.0" "passlib[bcrypt]>=1.7.4,<1.8.0"')
        sys.exit(1)
    else:
        print("✓ All dependencies meet security requirements")
        sys.exit(0)
