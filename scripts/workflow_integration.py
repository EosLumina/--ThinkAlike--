#!/usr/bin/env python3
"""
Script to integrate workflow fixes into a clean branch for PR submission
"""
import subprocess
import sys
import os
import argparse

def run_command(command, exit_on_error=True):
    """Run a shell command and optionally exit on error"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0 and exit_on_error:
        print(f"Error executing: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    return result

def create_integration_branch(source_branch="main", target_branch="workflow-fixes"):
    """Create or update the integration branch from source"""
    # Check if we're on the right branch
    current_branch = run_command("git branch --show-current").stdout.strip()
    if (current_branch != source_branch):
        print(f"Switching from {current_branch} to {source_branch}")
        run_command(f"git checkout {source_branch}")
    
    # Pull latest from source branch
    run_command(f"git pull origin {source_branch}")
    
    # Check if target branch exists
    branches = run_command("git branch").stdout
    
    if target_branch in branches:
        print(f"Target branch {target_branch} exists, checking out")
        run_command(f"git checkout {target_branch}")
        
        # Update with latest from source
        print(f"Updating {target_branch} with latest from {source_branch}")
        merge_result = run_command(f"git merge {source_branch}", exit_on_error=False)
        
        if merge_result.returncode != 0:
            print("Merge conflict detected. You have options:")
            print("1. Resolve conflicts manually and continue")
            print("2. Abort the merge and start over")
            choice = input("Enter choice (1/2): ")
            
            if choice == "1":
                print("Resolve conflicts manually, then run 'git add' on the resolved files")
                print("Then run 'git commit' to complete the merge")
                sys.exit(0)
            else:
                run_command("git merge --abort")
                print("Merge aborted. Starting over with fresh branch")
                run_command(f"git branch -D {target_branch}")
                run_command(f"git checkout -b {target_branch}")
    else:
        # Create the target branch
        print(f"Creating new branch {target_branch} from {source_branch}")
        run_command(f"git checkout -b {target_branch}")
    
    return True

def apply_workflow_fixes():
    """Apply workflow fixes to the current branch"""
    # Run the comprehensive workflow fixer
    run_command("python scripts/fix_all_workflows.py")
    
    # Check for changes
    status = run_command("git status --porcelain").stdout
    
    if not status.strip():
        print("No changes made by the fix scripts")
        return False
    
    # Commit changes
    run_command('git add .')
    run_command('git commit -m "fix: integrated workflow fixes for CI/CD pipeline issues"')
    return True

def push_changes(target_branch="fix/workflow-improvements"):
    """Push changes to the specified branch"""
    current_branch = run_command("git branch --show-current").stdout.strip()
    
    # Create a new branch for the PR
    run_command(f"git checkout -b {target_branch}")
    
    # Push to remote
    push_result = run_command(f"git push -u origin {target_branch}", exit_on_error=False)
    
    if push_result.returncode != 0:
        print(f"Error pushing to {target_branch}")
        print(push_result.stderr)
        
        # Ask if forced push is okay
        force_push = input("Force push? This will overwrite remote branch (y/n): ")
        if force_push.lower() == 'y':
            run_command(f"git push -f -u origin {target_branch}")
        else:
            print("Push aborted")
            return False
    
    print(f"Changes pushed to {target_branch}")
    
    # Print PR creation link
    remote_url = run_command("git remote get-url origin").stdout.strip()
    if "github.com" in remote_url:
        # Extract owner and repo
        repo_info = remote_url.split("github.com/")[1].replace(".git", "")
        print(f"\nCreate PR: https://github.com/{repo_info}/compare/main...{target_branch}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Integrate workflow fixes")
    parser.add_argument("--source", default="main", help="Source branch (default: main)")
    parser.add_argument("--temp", default="workflow-fixes-temp", help="Temporary integration branch")
    parser.add_argument("--target", default="fix/workflow-improvements", help="Target PR branch")
    parser.add_argument("--no-push", action="store_true", help="Skip pushing changes")
    
    args = parser.parse_args()
    
    # Create integration branch
    create_integration_branch(args.source, args.temp)
    
    # Apply fixes
    changes_made = apply_workflow_fixes()
    
    if not changes_made:
        print("No changes to push")
        return
    
    if not args.no_push:
        # Push changes
        push_changes(args.target)
    else:
        print("Changes applied but not pushed (--no-push flag used)")

if __name__ == "__main__":
    main()
