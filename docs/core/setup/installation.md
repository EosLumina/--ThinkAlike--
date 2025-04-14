# Installation Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 18.x or higher
- Git

## Quick Start

```bash
# Clone repository
git clone https://github.com/EosLumina/--ThinkAlike--.git
cd --ThinkAlike--

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
cd ..

# Initialize database
python init_db.py
```

For detailed setup instructions, see [Developer Workflow](../../guides/developer_guides/developer_workflow.md).
