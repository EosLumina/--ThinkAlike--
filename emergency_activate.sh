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
