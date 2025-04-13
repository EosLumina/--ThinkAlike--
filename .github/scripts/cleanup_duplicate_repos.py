#!/usr/bin/env python3
"""
Identify and suggest cleanup for duplicate repository directories.
"""

import os
import shutil
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'='*20} {text} {'='*20}{Style.RESET_ALL}\n")

def print_warning(text):
    """Print a warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def main():
    """Identify duplicate repository directories."""
    print_header("Checking for Duplicate Repository Directories")

    # Check for nested ThinkAlike directory
    nested_repo = Path('--ThinkAlike--')

    if nested_repo.exists() and nested_repo.is_dir():
        print_warning(f"Found duplicate repository directory: {nested_repo}")
        print(f"\nThis appears to be a nested clone of the repository and may cause issues.")
        print(f"\nRecommended action: Remove the duplicate directory")
        print(f"\n    rm -rf --ThinkAlike--")
        print(f"\nWARNING: Only do this if you're sure it's a duplicate and not needed!")

        # Don't delete automatically - just suggest the command
    else:
        print("No duplicate repository directories found.")

if __name__ == "__main__":
    main()
