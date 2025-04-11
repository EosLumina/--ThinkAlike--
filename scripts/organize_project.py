import os
import shutil
import glob

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created: {path}")
    else:
        print(f"Directory already exists: {path}")

def move_files(source_glob, destination_dir):
    """Move files matching glob pattern to destination directory"""
    import glob
    files = glob.glob(source_glob)
    
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        
    for file in files:
        if os.path.isfile(file):
            filename = os.path.basename(file)
            dest_path = os.path.join(destination_dir, filename)
            
            # Don't overwrite existing files
            if os.path.exists(dest_path):
                print(f"Skipping (file exists at destination): {file}")
                continue
                
            shutil.copy2(file, dest_path)
            print(f"Copied: {file} -> {dest_path}")

# Create main directories
project_root = "/workspaces/--ThinkAlike--"

# Backend structure following FastAPI best practices
backend_dirs = [
    "backend/app",
    "backend/app/api",
    "backend/app/api/routes",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/core",
    "backend/app/services",
    "backend/app/db",
    "backend/tests"
]

# Frontend structure following React best practices
frontend_dirs = [
    "frontend/src/components/common",
    "frontend/src/components/profile",
    "frontend/src/components/community",
    "frontend/src/components/matching",
    "frontend/src/components/auth",
    "frontend/src/components/validation",
    "frontend/src/pages",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/contexts",
    "frontend/src/services",
    "frontend/public"
]

# Create directories preserving existing ones
print("Creating directory structure...")
for directory in backend_dirs + frontend_dirs:
    create_directory(os.path.join(project_root, directory))

# Check if validation component files exist, create if they don't
validation_components = [
    "DataTraceability.jsx",
    "APIValidator.jsx",
    "CoreValuesValidator.jsx"
]

validation_dir = os.path.join(project_root, "frontend/src/components/validation")
for component in validation_components:
    component_path = os.path.join(validation_dir, component)
    old_component_path = os.path.join(project_root, "frontend/src/components", component)
    
    # Check if component exists in old location
    if os.path.exists(old_component_path):
        if not os.path.exists(component_path):
            print(f"Moving {component} to validation directory...")
            shutil.copy2(old_component_path, component_path)
            os.remove(old_component_path)
        else:
            print(f"Component exists in both locations: {component}")
    elif not os.path.exists(component_path):
        # Create empty component file with basic React structure
        with open(component_path, 'w') as f:
            component_name = os.path.splitext(component)[0]
            f.write(f"""import React from 'react';

/**
 * {component_name} - UI validation component
 * 
 * Part of ThinkAlike's UI as Validation Framework
 */
const {component_name} = (props) => {{
    return (
        <div className="{component_name.lower()}-component">
            <h3>{component_name}</h3>
            <p>Implementation pending...</p>
        </div>
    );
}};

export default {component_name};
""")
        print(f"Created validation component: {component_path}")

# Create starter FastAPI main file if it doesn't exist
main_py_path = os.path.join(project_root, "backend/main.py")
if not os.path.exists(main_py_path):
    print("Creating FastAPI main.py...")
    with open(main_py_path, 'w') as f:
        f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ThinkAlike API",
    description="API for the ThinkAlike platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to ThinkAlike API. See /docs for API documentation."}

# Import and include API routers here as they are developed
# from app.api.routes import users, profiles, narratives
# app.include_router(users.router)
# app.include_router(profiles.router)
# app.include_router(narratives.router)
""")

print("Project structure reorganization completed!")
print("\nNext steps:")
print("1. Create a .env file in the project root (see installation guide)")
print("2. Set up the database using init_db.py")
print("3. Start the backend server with 'uvicorn backend.main:app --reload'")
print("4. Start the frontend with 'cd frontend && npm start'")