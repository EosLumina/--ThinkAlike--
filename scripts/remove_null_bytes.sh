#!/bin/bash
# Remove stray null bytes recursively in given directories
for dir in backend tests; do
  if [ -d "$dir" ]; then
    find "$dir" -type f -exec sed -i 's/\x0//g' {} \;
  fi
done
echo "Null bytes removed from backend and tests directories."
