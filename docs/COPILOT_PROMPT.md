# ThinkAlike Project Workflow Integration: Instructions for Copilot

## Project Context

I'm working on ThinkAlike, an ethical tech platform focused on authentic connection through transparent, user-empowered
technology. The project has strict ethical guidelines and emphasizes data transparency, user sovereignty, and radical
transparency.

## Current Workflow Issues I'm Facing

1. **CI/CD Pipeline Failures**:

    * Seeing errors with pip installation commands in GitHub workflows
  * Error: `pip install is not a valid editable requirement. It should either be a path to a local project or a VCS URL`
  * Need to scan all workflow files for this pattern and fix

1. **Documentation Formatting**:

    * Hundreds of markdown linting issues across docs
  * Created a fix-markdown-linting.js script but it still needs improvement
  * Primary issues: line length, headings without blank lines, list formatting, inconsistent list markers

1. **Feature Integration**:

    * Working on integrating ethical compliance validation and workflow diagnostic tools
  * Need to ensure phone number pattern detection in ethical_compliance.py works correctly
  * Created diagnostic tools (diagnose_workflows.py, fix_requirements.py) that need proper integration

## Note for Non-Developers

If you are encountering issues and are not a developer, the complexity of these files can be confusing. Many scripts (`fix_*.py`, `fix_*.sh`) are designed to automatically repair common problems, especially with GitHub Actions workflows (files in `.github/workflows/`).

A potential first step to resolve issues is to run the emergency workflow fix script from your terminal in the project's main directory:

```bash
python scripts/emergency_workflow_fix.py
```

This script attempts to reset the workflow files to a known good state. If problems persist, please consult with a developer on the project.

## Work Completed So Far

1. Created integration-temp branch based on remote/main
2. Added workflow diagnostic and markdown fixing scripts
3. Fixed ethical compliance validation for phone numbers
4. Created PR but still need to resolve integration issues

## Requested Assistance

As I work, I need help with:

1. **Finding problematic patterns** in workflow YAML files, especially invalid pip installation commands
2. **Enhancing the markdown linting script** to better handle:

    * Standardizing list markers (asterisks vs dashes)
  * Fixing heading spacing
  * Properly handling document details sections
  * Normalizing ordered list numbering

1. **Ensuring ethical validation patterns** are robust:

    * Phone number pattern needs to detect multiple formats
  * Pattern should be part of the Ethical Compliance Validation system

1. **Creating workflow integration commands** that reliably:

    * Move changes from main to integration-temp branch
  * Properly handle merge conflicts
  * Push to the fix/integrated-workflow-fixes branch

When suggesting code changes, please prioritize clarity, stability, and maintainability aligned with ThinkAlike's
ethical principles of transparency and user agency.
