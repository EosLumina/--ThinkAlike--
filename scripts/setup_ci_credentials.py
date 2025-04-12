#!/usr/bin/env python3
"""
ThinkAlike CI Database Credentials Setup

This script helps configure database credentials for GitHub Actions workflows
without needing to manually create complex connection strings.
"""

import sys
import os
import secrets
import subprocess
import string
from urllib.parse import quote_plus

def print_header():
    """Display script header"""
    print("\n" + "=" * 80)
    print("ThinkAlike CI Database Credentials Setup".center(80))
    print("=" * 80)
    print("\nThis script will help you set up database credentials for GitHub Actions.\n")

def generate_secret_key():
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def check_gh_cli():
    """Check if GitHub CLI is installed"""
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Main script execution"""
    print_header()

    # Default values for test environment
    username = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    database = "thinkalike_test"
    secret_key = generate_secret_key()

    print("Generated database credentials for CI testing:")

    # Create connection string
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    print(f"\n1. DATABASE_URL: {connection_string}")
    print(f"2. SECRET_KEY: {secret_key}")

    # Check for GitHub CLI and provide commands
    if check_gh_cli():
        print("\nGitHub CLI detected! You can set these secrets with these commands:")
        print(f"gh secret set DATABASE_URL -b'{connection_string}'")
        print(f"gh secret set SECRET_KEY -b'{secret_key}'")
    else:
        print("\nTo add these to your GitHub repository:")
        print("1. Go to your repository → Settings → Secrets and variables → Actions")
        print("2. Click 'New repository secret'")
        print("3. Add each secret with the name and value shown above")

    print("\nThese credentials are for CI testing environments only.")
    print("For production, use more secure values stored safely in your CI environment.")

    print("\nSetup complete!")

if __name__ == "__main__":
    main()
