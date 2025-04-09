import os
import subprocess
import re

def find_files_with_placeholder(start_dir='..'):
    """Find all files containing the '...existing content...' placeholder"""
    affected_files = []

    # Walk through all directories
    for root, dirs, files in os.walk(start_dir):
        # Skip .git directory
        if '.git' in root:
            continue

        # Check each file
        for file in files:
            if file.endswith(('.md', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '...existing content...' in content:
                            affected_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return affected_files

def restore_file_from_branch(file_path, branch_name='revert-8-update-docs'):
    """Restore a file from the specified branch"""
    try:
        # Get file content from the branch
        process = subprocess.run(
            ['git', 'show', f'{branch_name}:{file_path}'],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            print(f"Error retrieving {file_path} from branch {branch_name}: {process.stderr}")
            return False

        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(process.stdout)

        print(f"✅ Restored {file_path} from branch {branch_name}")
        return True
    except Exception as e:
        print(f"Error restoring {file_path}: {e}")
        return False

def main():
    print("Scanning for files with missing content...")
    affected_files = find_files_with_placeholder()

    print(f"Found {len(affected_files)} files with placeholder content.")

    # Check if branch exists
    branch_exists = subprocess.run(
        ['git', 'rev-parse', '--verify', 'revert-8-update-docs'],
        capture_output=True
    ).returncode == 0

    if not branch_exists:
        print("Error: Branch 'revert-8-update-docs' not found.")
        return

    # Restore each file
    restored_count = 0
    for file in affected_files:
        if restore_file_from_branch(file):
            restored_count += 1

    print(f"Restored {restored_count} out of {len(affected_files)} files.")
    print("Complete! You can now commit the restored files.")

if __name__ == "__main__":
    main()
