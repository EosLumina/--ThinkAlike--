import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required Python packages."""
    print("Installing required dependencies...")
    packages = [
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "sqlalchemy>=2.0.9",
        "alembic>=1.10.3",
        "python-dotenv>=1.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic[email]>=1.10.7",
        "psycopg2-binary>=2.9.6",
        "python-multipart>=0.0.6",
    ]

    try:
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ Dependencies installed successfully!")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def create_vscode_settings():
    """Create VS Code settings to help with imports."""
    vscode_dir = Path(".vscode")
    if not vscode_dir.exists():
        vscode_dir.mkdir()

    settings_file = vscode_dir / "settings.json"
    settings_content = '''{
    "python.analysis.extraPaths": [
        "${workspaceFolder}"
    ],
    "python.linting.enabled": true,
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.typeCheckingMode": "basic"
}'''

    with open(settings_file, "w") as f:
        f.write(settings_content)

    print(f"✅ Created {settings_file}")

    # Create pyrightconfig.json
    pyright_config = Path("pyrightconfig.json")
    pyright_content = '''{
  "include": [
    "backend"
  ],
  "extraPaths": [
    "."
  ],
  "typeCheckingMode": "basic",
  "reportMissingImports": "warning",
  "reportMissingModuleSource": "warning",
  "reportOptionalMemberAccess": "information"
}'''

    with open(pyright_config, "w") as f:
        f.write(pyright_content)

    print(f"✅ Created {pyright_config}")

def main():
    print("===== Setting up ThinkAlike Project =====")

    # Create requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("""fastapi>=0.95.0
uvicorn>=0.21.1
sqlalchemy>=2.0.9
alembic>=1.10.3
python-dotenv>=1.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pydantic[email]>=1.10.7
psycopg2-binary>=2.9.6
python-multipart>=0.0.6
""")
    print("✅ Created requirements.txt")

    # Install dependencies
    if not install_dependencies():
        return

    # Create VS Code settings
    create_vscode_settings()

    print("\n===== Setup Complete =====")
    print("Next, run fix_project.py to fix code issues.")

if __name__ == "__main__":
    main()
