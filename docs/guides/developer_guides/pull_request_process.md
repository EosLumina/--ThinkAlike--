# Pull Request Process Guide

* --

## 1. Introduction

This document outlines the standard process for submitting Pull Requests (PRs) to the ThinkAlike project. Following
these guidelines ensures code quality, consistency, and clear communication between contributors and maintainers.
Whether you're a core team member or an external contributor, this process applies to all code changes.

* --

## 2. Before Creating a Pull Request

### 2.1 Preparation

1. **Create an Issue First** (if one doesn't exist):

    * All code changes should be tied to an issue in the GitHub tracker
  * Follow the [Issue Labels Guide](./issue_labels_guide.md) for proper categorization
  * Get feedback on your proposed approach before writing code

1. **Fork and Branch:**

    * Fork the repository if you're an external contributor
  * Create a feature branch from `main` with a descriptive name:

     ```bash

     git checkout -b feature/add-user-preferences
     # or
     git checkout -b fix/login-validation-error
     ```

    * Use prefixes like `feature/`, `fix/`, `docs/`, `refactor/`, etc.

1. **Keep Changes Focused:**

    * Each PR should address a single issue or feature
  * Avoid combining unrelated changes in a single PR
  * For large features, consider breaking them into smaller PRs

### 2.2 Development Standards

1. **Follow Code Style:**

    * Adhere to the project's coding standards for:
    * Python (backend): Follow PEP 8
    * TypeScript/JavaScript (frontend): Follow ESLint/Prettier config
  * Run linters before committing:

     ```bash

     # Backend
     flake8 app/
     black app/

     # Frontend
     npm run lint
     ```

1. **Write Tests:**

    * Include appropriate tests for your changes:
    * Unit tests for core logic
    * Integration tests for API endpoints
    * E2E tests for critical user flows
  * Aim for at least 80% test coverage for new code
  * Ensure all existing tests pass

1. **Document Your Changes:**

    * Update relevant documentation
  * Add comments for complex logic
  * Include docstrings for new functions/methods

* --

## 3. Creating the Pull Request

### 3.1 Commit Guidelines

1. **Write Meaningful Commit Messages:**

    * Use the imperative mood: "Add feature" not "Added feature"
  * Format: `[TYPE]: Short summary (50 chars or less)`
  * Examples:

     ```

     feat: add user preference settings
     fix: resolve authentication token expiration bug
     docs: update API documentation
     refactor: simplify matching algorithm
     ```

    * For larger changes, include a body that explains what and why (not how)

1. **Organize Commits:**

    * Make logical, atomic commits
  * Consider squashing fixup commits before creating PR
  * Rebase to keep a clean history:

     ```bash

     git fetch origin
     git rebase origin/main
     ```

### 3.2 PR Submission

1. **Create the PR on GitHub:**

    * Go to the repository on GitHub
  * Click "New pull request"
  * Select your branch
  * Fill in the PR template completely

1. **PR Template Contents:**

    * Link to the related issue(s)
  * Clear description of changes
  * Screenshots/videos for UI changes
  * Checklist of completed items
  * Notes on testing methodology
  * Any deployment considerations

1. **Mark as Draft if needed:**

    * Use GitHub's "Draft PR" feature if work is still in progress
  * Convert to ready when you want review

* --

## 4. PR Review Process

### 4.1 Request Reviews

1. **Assign Reviewers:**

    * Request reviews from appropriate team members
  * At least one core maintainer should review each PR
  * Consider requesting specialist reviews for complex areas

1. **Respond to Feedback:**

    * Address all comments and suggestions
  * Explain your reasoning if you disagree with feedback
  * Make requested changes promptly
  * Mark conversations as resolved after addressing them

### 4.2 CI/CD Checks

1. **Verify Automated Checks:**

    * Ensure all CI pipelines pass:
    * Tests (unit, integration, E2E)
    * Linting
    * Type checking
    * Security scans
  * Fix any failing checks before requesting re-review

1. **Update Based on Feedback:**

    * Push new commits to address review comments
  * Consider using `git commit --fixup` for small changes
  * Rebase and squash fixups when ready for final review:

     ```bash

     git rebase -i --autosquash origin/main
     ```

* --

## 5. Merging

1. **Merge Requirements:**

    * At least one approval from a core maintainer
  * All CI checks pass
  * All discussions resolved
  * PR is up-to-date with the main branch

1. **Merge Responsibility:**

    * Core team members typically handle the actual merge
  * Use the appropriate merge strategy:
    * **Squash and merge:** For most feature PRs (creates a single commit)
    * **Rebase and merge:** For PRs with well-structured commits worth preserving
    * **Merge commit:** Rarely used, only for major features with extensive history

1. **After Merging:**

    * Delete the feature branch
  * Close the associated issue or update its status
  * Deploy if required (following the deployment process)

* --

## 6. Special Cases

### 6.1 Hotfixes

For urgent production issues:

1. Create branch directly from the production tag: `hotfix/critical-auth-issue`
2. Follow an expedited review process
3. Merge to both `main` and the appropriate release branch
4. Deploy as soon as possible following approval

### 6.2 Long-Running Feature Branches

For major features that take weeks to develop:

1. Rebase regularly against `main` to prevent major conflicts
2. Consider creating intermediate PRs for reviewable chunks
3. Use feature flags to merge code that isn't ready for activation

* --

## 7. Tips for Successful PRs

* **Keep PRs Small:** Aim for <500 lines changed when possible
* **Communicate:** Use PR comments to explain decisions and ask questions
* **Be Patient:** Understand that review takes time, especially for complex changes
* **Be Responsive:** Address feedback promptly to keep the PR moving
* **Learn from Feedback:** Use review comments as learning opportunities

* --

By following this pull request process, we maintain high code quality while allowing for efficient collaboration among
all ThinkAlike contributors.

* --

## Document Details

* Title: Pull Request Process Guide

* Type: Developer Guide

* Version: 1.0.0

## - Last Updated: 2025-04-05

## End of Pull Request Process Guide
