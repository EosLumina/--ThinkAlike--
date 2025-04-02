import os
import shutil

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created: {path}")

def move_files(source_glob, destination_dir):
    """Move files matching glob pattern to destination directory"""
    import glob
    files = glob.glob(source_glob)
    for file in files:
        if os.path.isfile(file):
            filename = os.path.basename(file)
            dest_path = os.path.join(destination_dir, filename)
            shutil.copy2(file, dest_path)
            print(f"Copied: {file} -> {dest_path}")

# Create main directories
project_root = "/workspaces/--ThinkAlike--"
directories = [
    "backend/api",
    "backend/models",
    "backend/services",
    "backend/utils",
    "backend/database",
    "frontend/src/components/profile",
    "frontend/src/components/community",
    "frontend/src/components/matching",
    "frontend/src/components/auth",
    "frontend/src/contexts",
    "docs/architecture",
    "docs/user_guides",
    "tests/backend",
    "tests/frontend"
]

for directory in directories:
    create_directory(os.path.join(project_root, directory))

# Move files to appropriate locations
mappings = [
    # API files
    ("/workspaces/--ThinkAlike--/api/*.py", "/workspaces/--ThinkAlike--/backend/api/"),
    
    # Database models
    ("/workspaces/--ThinkAlike--/backend_utils/models.py", "/workspaces/--ThinkAlike--/backend/models/"),
    
    # Frontend contexts
    ("/workspaces/--ThinkAlike--/frontend/src/contexts/*.jsx", "/workspaces/--ThinkAlike--/frontend/src/contexts/"),
]

for source, destination in mappings:
    move_files(source, destination)

print("Project structure reorganization completed!")