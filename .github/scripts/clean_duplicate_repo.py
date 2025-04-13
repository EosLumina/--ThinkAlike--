#!/usr/bin/env python3
"""
Safely remove duplicate repository directories.
"""

import os
import shutil
import argparse


def check_is_duplicate(repo_dir):
    """Check if the directory appears to be a duplicate repository."""
    # Check for typical Git repository indicators
    git_dir = os.path.join(repo_dir, '.git')
    readme = os.path.join(repo_dir, 'README.md')

    # If it has a .git directory and README.md, it's likely a repository
    return os.path.exists(git_dir) and os.path.exists(readme)


def safely_remove_duplicate(repo_dir, force=False):
    """Safely remove a duplicate repository directory."""
    if not os.path.exists(repo_dir):
        print(f"Directory {repo_dir} does not exist.")
        return False

    if not check_is_duplicate(repo_dir):
        print(f"Warning: {repo_dir} does not appear to be a Git repository.")
        if not force:
            print("Use --force to remove it anyway.")
            return False

    try:
        # Try to remove the directory
        shutil.rmtree(repo_dir)
        print(f"Successfully removed duplicate repository: {repo_dir}")
        return True
    except Exception as e:
        print(f"Error removing directory {repo_dir}: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='Safely remove duplicate repository directories.'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='--ThinkAlike--',
        help='The duplicate repository directory to remove (default: --ThinkAlike--)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force removal even if directory does not appear to be a repository'
    )

    args = parser.parse_args()

    # Confirm before removal
    if not args.force:
        answer = input(f"Are you sure you want to remove {args.directory}? [y/N] ")
        if answer.lower() != 'y':
            print("Operation cancelled.")
            return

    safely_remove_duplicate(args.directory, args.force)


if __name__ == "__main__":
    main()
