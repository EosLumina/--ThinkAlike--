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
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        # Ignore files that can't be read (e.g., binary)
        return False

    original_content = content
    fixed = False

    # Fix potential incorrect references if they point to the *wrong* repo name format
    for pattern in OLD_REPO_PATTERNS:
         # Basic string replace might be safer than regex here unless needed
         if pattern in content:
              print(f"Found potential incorrect reference '{pattern}' in {file_path}. Replacing is complex, manual review recommended.")
              # content = content.replace(pattern, CORRECT_REPO) # Use with caution
              # fixed = True


    # Example: Fix workflow badge URLs specifically if needed
    badge_pattern = r'!\[(.*?)\]\((https://github.com/)[^/]+/[^/]+(/workflows/[^/]+/badge\.svg.*?)\)'
    def replace_badge(match):
        badge_text = match.group(1)
        prefix = match.group(2)
        suffix = match.group(3)
        return f'![{badge_text}]({prefix}{CORRECT_REPO}{suffix})'

    new_content_badges = re.sub(badge_pattern, replace_badge, content)
    if new_content_badges != content:
         content = new_content_badges
         fixed = True


    if fixed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Potentially fixed references/badges in: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing fixed file {file_path}: {e}")
            return False
    return False

def main(directory="."):
    print(f"Scanning for potential incorrect repo references/badges in '{directory}'...")
    count = 0
    target_extensions = ('.yml', '.yaml', '.md', '.py', '.js', '.html') # Add others if needed
    for root, _, files in os.walk(directory):
        if ".git" in root.split(os.path.sep): # Skip .git dir
            continue
        for file in files:
            if file.endswith(target_extensions):
                file_path = os.path.join(root, file)
                if fix_references_in_file(file_path):
                    count += 1
    print(f"Scan complete. Potentially fixed {count} files.")

if __name__ == "__main__":
    scan_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    main(scan_dir)
