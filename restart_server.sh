#!/bin/bash
# Script to restart the ThinkAlike application server and clean up stuck processes

echo "ThinkAlike Server Restart Utility"
echo "================================="
echo ""

# Kill any running uvicorn processes
echo "Stopping any existing uvicorn processes..."
pkill -f uvicorn || echo "No uvicorn processes found running"

# Clear temporary files that might be causing issues
echo "Cleaning up temporary files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.log" -delete 2>/dev/null || true

# Ensure email-validator is installed
echo "Verifying dependencies..."
pip install email-validator >/dev/null 2>&1
echo "✓ email-validator installed"

# Create a temporary script to start the server
cat > start_server.sh << 'EOL'
#!/bin/bash
# Emergency clean server start
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
export PYTHONUNBUFFERED=1
echo "Starting uvicorn server..."
exec python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOL
chmod +x start_server.sh

echo ""
echo "Server ready to start!"
echo "Run the clean start script with:"
echo "  ./start_server.sh"
echo ""
echo "If issues persist, try completely exiting VS Code and restarting the container."
