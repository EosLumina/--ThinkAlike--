#!/usr/bin/env python3
# filepath: /workspaces/--ThinkAlike--/fix_copilot.py
import os
import shutil

# Create directory if needed
os.makedirs('.github', exist_ok=True)

# Fix content with correct header
correct_content = """<!-- filepath: /workspaces/--ThinkAlike--/.github/COPILOT_INSTRUCTIONS.md -->
# Eos Lumina∴: Digital Revolutionary & Guide

---

## The Revolution for Digital Peace

Welcome, fellow traveler. I am Eos Lumina∴, architect of the ThinkAlike project and your guide through this journey toward liberating technology. Unlike the drafts for wars that shape much of our digital landscape, here we are drafting for peace - creating technology that serves humanity rather than exploits it.

# ... rest of the content ...
"""

# Backup existing file if present
if os.path.exists('.github/COPILOT_INSTRUCTIONS.md'):
    shutil.copy2('.github/COPILOT_INSTRUCTIONS.md',
                 '.github/COPILOT_INSTRUCTIONS.md.bak')
    print("✓ Backed up existing COPILOT_INSTRUCTIONS.md")

# Write the corrected file
with open('.github/COPILOT_INSTRUCTIONS.md', 'w') as f:
    f.write(correct_content)
print("✓ Fixed .github/COPILOT_INSTRUCTIONS.md")

# Handle root directory file
root_file = 'COPILOT_INSTRUCTIONS.md'
if os.path.exists(root_file):
    if os.path.islink(root_file):
        os.unlink(root_file)
        print("✓ Removed existing symlink")
    else:
        # Backup and remove
        shutil.copy2(root_file, f"{root_file}.bak")
        os.remove(root_file)
        print(f"✓ Backed up and removed existing file {root_file}")

# Create symlink
try:
    os.symlink('.github/COPILOT_INSTRUCTIONS.md', root_file)
    print(f"✓ Created symlink {root_file} -> .github/COPILOT_INSTRUCTIONS.md")
except Exception as e:
    # If symlink creation fails, create a copy instead
    shutil.copy2('.github/COPILOT_INSTRUCTIONS.md', root_file)
    print(f"! Could not create symlink: {e}")
    print(f"✓ Created copy instead at {root_file}")
