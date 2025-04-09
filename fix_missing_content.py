import os
import subprocess
import re
import sys

def find_files_with_placeholder(start_dir='.'):
    """Find all files containing the '...existing content...' placeholder"""
    affected_files = []

    # Skip the script itself to avoid false positives
    this_script_path = os.path.abspath(__file__)

    # Walk through all directories
    for root, dirs, files in os.walk(start_dir):
        # Skip directories we don't want to check
        if any(skip_dir in root for skip_dir in ['.git', 'venv', 'node_modules', '__pycache__']):
            continue

        # Check each file
        for file in files:
            if file.endswith(('.md', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css')):
                file_path = os.path.join(root, file)

                # Skip this script itself
                if os.path.abspath(file_path) == this_script_path:
                    continue

                try:
                    # Try with utf-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '...existing content...' in content:
                            affected_files.append(file_path)
                            print(f"Found placeholder in: {file_path}")
                except UnicodeDecodeError:
                    # Try with latin-1 encoding
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                            if '...existing content...' in content:
                                affected_files.append(file_path)
                                print(f"Found placeholder in: {file_path} (using latin-1)")
                    except Exception as e:
                        print(f"Skipping {file_path}: {str(e)}")
                except Exception as e:
                    print(f"Skipping {file_path}: {str(e)}")

    return affected_files

def restore_file_from_branch(file_path, branch_name='revert-8-update-docs'):
    """Restore a file from the specified branch"""
    try:
        # Make sure the path is relative to git root
        git_path = file_path.replace('\\', '/')
        if git_path.startswith('./'):
            git_path = git_path[2:]

        # Get file content from the branch
        process = subprocess.run(
            ['git', 'show', f'{branch_name}:{git_path}'],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            print(f"⚠️ Error retrieving {file_path} from branch {branch_name}: {process.stderr}")
            return False

        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(process.stdout)

        print(f"✅ Restored {file_path} from branch {branch_name}")
        return True
    except Exception as e:
        print(f"⚠️ Error restoring {file_path}: {e}")
        return False

def main():
    print("=== ThinkAlike Missing Content Restore Tool ===\n")

    # First check if the branch exists
    branch_exists = subprocess.run(
        ['git', 'rev-parse', '--verify', 'revert-8-update-docs'],
        capture_output=True
    ).returncode == 0

    # If branch doesn't exist, try to fetch it
    if not branch_exists:
        print("Branch 'revert-8-update-docs' not found. Trying to fetch it...")
        fetch_result = subprocess.run(
            ['git', 'fetch', 'origin', 'revert-8-update-docs:revert-8-update-docs'],
            capture_output=True
        )

        if fetch_result.returncode != 0:
            print("Error fetching branch. Make sure the branch exists on the remote repository.")
            print("Error details:")
            print(fetch_result.stderr.decode('utf-8'))
            print("\nPlease run the following command manually:")
            print("  git fetch origin revert-8-update-docs:revert-8-update-docs")
            return
        else:
            print("Successfully fetched branch!\n")

    print("Scanning for files with missing content...")
    affected_files = find_files_with_placeholder()

    print(f"\nFound {len(affected_files)} files with placeholder content.")

    # Check again if branch exists (it should now)
    branch_exists = subprocess.run(
        ['git', 'rev-parse', '--verify', 'revert-8-update-docs'],
        capture_output=True
    ).returncode == 0

    if not branch_exists:
        print("\nError: Branch 'revert-8-update-docs' still not available.")
        print("Please create the branch manually or check the remote repository.")
        return

    # Ask for confirmation
    if affected_files:
        confirm = input(f"\nReady to restore {len(affected_files)} files. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    # Restore each file
    print("\nRestoring files from branch 'revert-8-update-docs'...")
    restored_count = 0
    for file in affected_files:
        if restore_file_from_branch(file):
            restored_count += 1

    print(f"\nRestored {restored_count} out of {len(affected_files)} files.")
    print("Complete! You can now commit the restored files.")

if __name__ == "__main__":
    main()
