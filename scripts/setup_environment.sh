#!/bin/bash

# ThinkAlike Development Environment Setup Script
# This script creates a Python virtual environment and installs required dependencies

echo "===== ThinkAlike Development Environment Setup ====="

# Function to check if virtual environment is working properly
check_venv() {
    if [ -f "venv/bin/python" ] && [ -f "venv/bin/pip" ]; then
        echo "Virtual environment looks valid."
        return 0
    else
        echo "Virtual environment is incomplete or corrupted."
        return 1
    fi
}

# Create or fix virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment. Make sure Python 3 is installed."
        exit 1
    fi
    echo "Virtual environment created successfully!"
elif ! check_venv; then
    echo "Rebuilding corrupted virtual environment..."
    rm -rf venv
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error rebuilding virtual environment."
        exit 1
    fi
    echo "Virtual environment rebuilt successfully!"
else
    echo "Using existing virtual environment."
fi

# Verify virtual environment activation
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Verify pip is working
if ! command -v pip &> /dev/null; then
    echo "Error: pip command not found in virtual environment."
    echo "Attempting to fix by reinstalling virtualenv..."
    deactivate 2>/dev/null || true
    rm -rf venv
    python -m venv venv
    source venv/bin/activate
    if ! command -v pip &> /dev/null; then
        echo "Failed to fix pip installation. Please install Python virtualenv manually."
        exit 1
    fi
fi

# Update pip itself
echo "Updating pip..."
pip install --upgrade pip

# Check requirements.txt format before installing
if [ -f "requirements.txt" ] && grep -E "^pip install" requirements.txt > /dev/null; then
    echo "Error: requirements.txt contains invalid line starting with 'pip install'."
    echo "Fixing requirements.txt format..."
    grep -v "^pip install" requirements.txt > requirements_fixed.txt
    mv requirements_fixed.txt requirements.txt
    echo "requirements.txt fixed."
fi

# Create or update requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "No requirements.txt found. Creating a basic one..."
    cat > requirements.txt << EOF
fastapi>=0.104.1
uvicorn>=0.24.0
sqlalchemy>=2.0.23
pydantic>=2.4.2
pytest>=7.4.3
python-dotenv>=1.0.0
requests>=2.31.0
pytest-cov>=4.1.0
mkdocs>=1.5.3
mkdocs-material>=9.4.6
EOF
fi

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies."
    exit 1
fi
echo "Dependencies installed successfully!"

# Create basic project structure if it doesn't exist
if [ ! -d "app" ]; then
    echo "Creating basic project structure..."
    mkdir -p app/models app/routes app/services
    touch app/__init__.py app/models/__init__.py app/routes/__init__.py app/services/__init__.py
fi

if [ ! -f "main.py" ] && [ ! -f "app/main.py" ]; then
    echo "Creating main.py entry point..."
    cat > main.py << EOF
from fastapi import FastAPI

app = FastAPI(
    title="ThinkAlike API",
    description="API for ThinkAlike platform - Architecting Connection for Enlightenment 2.0",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to ThinkAlike API",
        "status": "operational",
        "docs_url": "/docs"
    }
EOF
fi

# Create a .env file for local development if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file for local development..."
    cat > .env << EOF
# Local development environment variables
DATABASE_URL=sqlite:///./thinkalike.db
SECRET_KEY=thinkalike_local_development_secret_key
DEBUG=True
EOF
    echo ".env file created."
fi

# Initialize a basic database script if it doesn't exist
if [ ! -f "init_db.py" ]; then
    echo "Creating database initialization script..."
    cat > init_db.py << EOF
"""
Database initialization script for ThinkAlike.
Handles schema creation and initial data setup.
"""
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use SQLite default
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

def init_database():
    print(f"Initializing database with connection: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)

    # Create tables
    metadata = MetaData()

    # Example table - replace with your schema
    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String, unique=True),
        Column("email", String, unique=True),
    )

    metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
EOF
fi

echo ""
echo "===== Setup Complete! ====="
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the development server:"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "ThinkAlike API will be available at: http://localhost:8000"
echo "API documentation will be available at: http://localhost:8000/docs"
echo ""
