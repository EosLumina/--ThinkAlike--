#!/bin/bash
# Emergency clean server start
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
export PYTHONUNBUFFERED=1
echo "Starting uvicorn server..."
exec python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
