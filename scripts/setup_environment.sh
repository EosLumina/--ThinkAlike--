#!/bin/bash
# ThinkAlike development environment setup script

set -e # Exit on error

echo "🚀 Setting up ThinkAlike development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "📦 Creating Python virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || {
  echo "❌ Failed to activate virtual environment. Please check your Python installation."
  exit 1
}

# Install core dependencies
echo "📦 Installing core dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt || {
  echo "⚠️ Core requirements installation failed. Creating minimal requirements file..."
  cat > requirements.txt << EOL
fastapi>=0.95.0
uvicorn>=0.21.1
sqlalchemy>=2.0.9
alembic>=1.10.3
python-dotenv>=1.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pydantic>=1.10.7
psycopg2-binary>=2.9.6
python-multipart>=0.0.6
pytest>=7.3.1
pytest-cov>=4.1.0
PyYAML>=6.0
EOL
  echo "📦 Retrying installation with minimal requirements..."
  pip install -r requirements.txt
}

# Install development and testing dependencies
echo "📦 Installing development and testing dependencies..."
if [ -f "requirements-test.txt" ]; then
  pip install -r requirements-test.txt || echo "⚠️ Test dependencies installation had some issues. Continuing..."
fi

# Install documentation dependencies
echo "📦 Installing documentation dependencies..."
if [ -f "requirements-docs.txt" ]; then
  pip install -r requirements-docs.txt || {
    echo "⚠️ Documentation dependencies installation failed. Creating minimal docs requirements..."
    cat > requirements-docs.txt << EOL
mkdocs>=1.5.0
mkdocs-material>=9.0.0
pymdown-extensions>=10.0.0
EOL
    pip install -r requirements-docs.txt
  }
fi

# Clean null bytes from files
echo "🧹 Cleaning up project files..."
if [ -f "scripts/clean_files.py" ]; then
  python scripts/clean_files.py
else
  echo "⚠️ clean_files.py not found. Skipping file cleanup."
fi

# Create necessary directories
echo "📂 Ensuring project directory structure..."
mkdir -p backend/tests
mkdir -p frontend/src
mkdir -p docs/guides docs/core

# Initialize database if needed
if [ -f "init_db.py" ]; then
  echo "🗃️ Initializing database..."
  python init_db.py || echo "⚠️ Database initialization failed. You may need to run this manually."
fi

# Create a .env file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo "📄 Creating .env file from example..."
  cp .env.example .env
  echo "⚠️ Please update the .env file with your actual settings."
fi

echo "✅ ThinkAlike development environment setup complete!"
echo ""
echo "🔍 Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run backend: uvicorn backend.main:app --reload"
echo "  3. Run tests: pytest backend/tests/"
echo "  4. Build docs: mkdocs build"
echo ""
echo "For more information, see the project documentation."
