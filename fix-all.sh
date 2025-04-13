#!/bin/bash

# This script fixes common issues in the ThinkAlike repository
echo "🛠️ ThinkAlike Project Fixer"
echo "=========================="

# Ensure we're in the repository root
if [ -d ".git" ]; then
  echo "✅ Already in repository root"
elif [ -d "../.git" ]; then
  echo "⚠️ Moving to repository root..."
  cd ..
else
  echo "❌ Could not locate repository root. Please run this from the repository root or a subdirectory."
  exit 1
fi

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p .github/config

# Fix workflow trigger issues
echo "🔄 Fixing workflow trigger issues..."
chmod +x .github/scripts/fix_workflow_triggers.py
python .github/scripts/fix_workflow_triggers.py

# Set up frontend type definitions
echo "📝 Setting up frontend type definitions..."
chmod +x scripts/setup-frontend-types.sh
./scripts/setup-frontend-types.sh

# Create repository settings file
echo "⚙️ Creating repository settings configuration..."
cat > .github/config/repository-settings.yml << 'EOL'
# Repository settings configuration
repository:
  name: --ThinkAlike--
  description: "Platform for enhancing human autonomy through ethical technology"
  homepage: https://github.com/EosLumina/--ThinkAlike--
  private: false
  has_issues: true
  has_projects: true
  has_wiki: true
  has_downloads: true
  default_branch: main

# Branch protection rules
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      required_status_checks:
        strict: true
      enforce_admins: false
EOL

# Create merge and push script if it doesn't exist
if [ ! -f "merge_and_push.sh" ]; then
  echo "📝 Creating merge and push script..."
  cat > merge_and_push.sh << 'EOL'
#!/bin/bash

# Check for unstaged changes first
if ! git diff-index --quiet HEAD --; then
    echo "🔎 Unstaged changes detected. Please choose how to handle them:"
    echo "1. Stash changes (retrieve later with 'git stash pop')"
    echo "2. Commit changes with temporary message"
    echo "3. Abort operation"
    read -p "Choose option (1, 2, or 3): " unstaged_choice

    case $unstaged_choice in
        1)
            echo "Stashing changes..."
            git stash save "Auto-stashed before merge/pull operation"
            ;;
        2)
            echo "Committing changes..."
            git add .
            git commit -m "temp: save changes before merge operation"
            ;;
        3)
            echo "Operation aborted. Please handle unstaged changes manually."
            exit 1
            ;;
        *)
            echo "Invalid choice. Operation aborted."
            exit 1
            ;;
    esac
fi

# Step 1: Fetch the latest changes from the remote
git fetch origin

# Step 2: Integrate remote changes with our workflow fixes
echo "Choosing integration strategy..."
echo "1. Using git pull with merge (safer, preserves exact commit history)"
echo "2. Using git pull with rebase (cleaner history, but may require conflict resolution)"

read -p "Choose option (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo "Using merge strategy..."
    git pull origin main
elif [ "$choice" = "2" ]; then
    echo "Using rebase strategy..."
    git pull --rebase origin main
else
    echo "Invalid choice. Using merge strategy as default..."
    git pull origin main
fi

# Step 3: Check for any conflicts
if [ $? -ne 0 ]; then
    echo "⚠️ Conflicts detected. Please resolve them and then run:"
    echo "git add ."
    echo "git commit -m \"fix: resolve merge conflicts\""
    echo "git push origin main"
    exit 1
fi

# Step 4: Push the integrated changes
echo "Pushing integrated changes..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Success! All workflow fixes are now pushed to GitHub."
    echo "Workflow validation status should now be green on GitHub."

    # If we stashed changes, ask if user wants to pop them back
    if [ "$unstaged_choice" = "1" ]; then
        echo ""
        read -p "Do you want to restore your stashed changes now? (y/n): " restore_stash
        if [ "$restore_stash" = "y" ] || [ "$restore_stash" = "Y" ]; then
            git stash pop
            echo "Stashed changes restored. You may need to resolve conflicts."
        else
            echo "Stashed changes remain in the stash. Use 'git stash pop' to restore them later."
        fi
    fi
else
    echo "⚠️ Push failed. Please check the error message above for details."
fi
EOL
  chmod +x merge_and_push.sh
fi

# Validate workflows
echo "🔍 Validating workflows..."
if [ -f ".github/scripts/validate_workflows.py" ]; then
  python .github/scripts/validate_workflows.py
else
  echo "⚠️ Workflow validation script not found"
fi

# Summary
echo ""
echo "✅ Setup complete! Next steps:"
echo "1. Review changes with: git status"
echo "2. Commit your changes with: git add . && git commit -m \"fix: add workflow triggers and repository configuration\""
echo "3. Push changes with: ./merge_and_push.sh"

exit 0
