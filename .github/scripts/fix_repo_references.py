import os
import re
import sys

OLD_REPO_PATTERNS = [
    "EosLumina/ThinkAlike", # Incorrect format
    "EosLumina/-ThinkAlike-", # Incorrect format
    # Add EosLumina/--ThinkAlike-- only if you are *sure* it shouldn't appear anywhere
    # "EosLumina/--ThinkAlike--",
]
CORRECT_REPO = "EosLumina/--ThinkAlike--" # Keep the current correct name

def fix_references_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: # Ignore decoding errors
            content = f.read()
    except Exception as e:
        # Ignore files that can't be read (e.g., binary or permission issues)
        # print(f"Could not read {file_path}: {e}") # Optional: for debugging
        return False

    original_content = content
    fixed = False
    found_patterns = []

    # Check for potential incorrect references if they point to the *wrong* repo name format
    for pattern in OLD_REPO_PATTERNS:
         # Basic string check
         if pattern in content:
              found_patterns.append(pattern)
              # Automatic replacement is risky, just report for now
              # content = content.replace(pattern, CORRECT_REPO)
              # fixed = True

    if found_patterns:
        print(f"Found potential incorrect reference(s) {found_patterns} in {file_path}. Manual review recommended.")
        # If you decide to enable auto-fixing later, uncomment the replace logic above


    # Example: Fix workflow badge URLs specifically if needed
    # Regex to find markdown image links pointing to GitHub workflow badges
    # It captures the badge text, the github base url, and the workflow path + badge.svg part
    badge_pattern = r'!\[(.*?)\]\((https://github.com/)EosLumina/(?:ThinkAlike|-ThinkAlike-)(/workflows/[^/]+/badge\.svg.*?)\)'
    def replace_badge(match):
        badge_text = match.group(1)
        prefix = match.group(2)
        suffix = match.group(3)
        new_url = f'{prefix}{CORRECT_REPO}{suffix}'
        print(f"  Updating badge URL in {file_path} to {new_url}")
        return f'![{badge_text}]({new_url})'

    new_content_badges, num_badge_subs = re.subn(badge_pattern, replace_badge, content)
    if num_badge_subs > 0:
         content = new_content_badges
         fixed = True


    if fixed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Automatically fixed badge URLs in: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing fixed file {file_path}: {e}")
            # Revert content in memory if write fails? Maybe not necessary for this script.
            return False
    return False # Return False if only found patterns were detected but not auto-fixed

def main(directory="."):
    print(f"Scanning for potential incorrect repo references/badges in '{directory}'...")
    count = 0
    target_extensions = ('.yml', '.yaml', '.md', '.py', '.js', '.ts', '.html', '.json') # Added more common types
    ignore_dirs = {'.git', '.vscode', 'node_modules', '__pycache__', 'venv', '.env', 'dist', 'build'} # Directories to skip

    for root, dirs, files in os.walk(directory, topdown=True):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]

        for file in files:
            if file.endswith(target_extensions):
                file_path = os.path.join(root, file)
                try:
                    if fix_references_in_file(file_path):
                        count += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    print(f"Scan complete. Automatically fixed badge URLs in {count} files. Found potential incorrect references (manual review needed).")

if __name__ == "__main__":
    # Default to current directory if no argument provided
    scan_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    # Ensure the path exists
    if not os.path.isdir(scan_dir):
        print(f"Error: Directory '{scan_dir}' not found.")
        sys.exit(1)
    main(scan_dir)
