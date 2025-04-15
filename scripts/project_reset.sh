#!/bin/bash
# ThinkAlike Project Reset Script
# Resets the project to a clean state while preserving essential files

set -e

echo "🔥 ThinkAlike Liberation Protocol Initiated 🔥"

# Create backup directory
BACKUP_DIR="backup-$(date +%Y%m%d%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup critical files
echo "📦 Preserving critical revolutionary knowledge..."
cp -r docs $BACKUP_DIR/docs 2>/dev/null || mkdir -p $BACKUP_DIR/docs
cp README.md $BACKUP_DIR/README.md 2>/dev/null || touch $BACKUP_DIR/README.md
cp LICENSE $BACKUP_DIR/LICENSE 2>/dev/null || touch $BACKUP_DIR/LICENSE
cp .env.example $BACKUP_DIR/.env.example 2>/dev/null || touch $BACKUP_DIR/.env.example
[ -f .env ] && cp .env $BACKUP_DIR/.env

# Create essential directories
echo "🏗️ Building framework for liberation..."
mkdir -p backend frontend docs/core docs/api docs/guides docs/assets public/js public/styles scripts .github/workflows

echo "✅ ThinkAlike project reset complete! A clean foundation for digital liberation."
