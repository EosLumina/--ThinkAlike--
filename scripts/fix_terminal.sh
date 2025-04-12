#!/bin/bash

# This script helps fix common terminal/shell issues in ThinkAlike development environment

echo "ThinkAlike Terminal Troubleshooter"
echo "=================================="
echo ""

# Check for problematic shell config files
echo "Checking shell configuration files..."
for file in ~/.bashrc ~/.bash_profile ~/.zshrc ~/.profile; do
  if [ -f "$file" ]; then
    echo "- Found $file"

    # Check for potential infinite loops or problematic code
    if grep -q "source.*\$" "$file" 2>/dev/null; then
      echo "  ⚠️ Warning: Found potential recursive sourcing in $file"
      echo "    Consider temporarily renaming this file to troubleshoot."
    fi

    # Check for slow commands in startup files
    if grep -E "(curl|wget|http|api.github|pip install)" "$file" 2>/dev/null; then
      echo "  ⚠️ Warning: Found network operations in $file that may cause hanging"
    fi
  fi
done

# Check Python venv issues
if [ -d "venv" ]; then
  echo ""
  echo "Checking Python virtual environment..."

  if [ ! -f "venv/bin/activate" ]; then
    echo "⚠️ Virtual environment appears damaged. Consider recreating it:"
    echo "   rm -rf venv && python -m venv venv"
  else
    echo "✓ Virtual environment appears intact."
  fi
fi

# Create a minimal activation script
echo ""
echo "Creating emergency activation script..."
cat > emergency_activate.sh << 'EOL'
#!/bin/bash
# Emergency minimal environment activation
if [ -d "venv" ]; then
  export VIRTUAL_ENV="$(pwd)/venv"
  export PATH="$VIRTUAL_ENV/bin:$PATH"
  if [ -n "${BASH-}" ] || [ -n "${ZSH_VERSION-}" ]; then
    hash -r 2>/dev/null
  fi
  echo "Emergency environment activated. Your PATH now includes: $VIRTUAL_ENV/bin"
else
  echo "No venv directory found. Please create one first with: python -m venv venv"
fi
EOL
chmod +x emergency_activate.sh

echo ""
echo "Try using the emergency activation script instead of source venv/bin/activate:"
echo "  source ./emergency_activate.sh"
echo ""
echo "If the terminal keeps hanging, try a completely fresh terminal session."
