# GitHub Actions Workflow Format Guide

## Required Format for GitHub Actions Workflows

For workflows to pass validation in the ThinkAlike project, they must follow this specific format for the trigger section:

```yaml
name: Workflow Name

'on':  # Note the single quotes around 'on'
  push:
    branches:
    - main  # Note the dash format for list items
  pull_request:
    branches:
    - main
  workflow_dispatch: {}  # Empty object syntax
```

### Key Format Requirements

1. **Single Quotes Around 'on'**: The trigger keyword must be in single quotes: `'on':`
2. **List Format**: Use dashes for list items (`- main`) rather than brackets `[main]`
3. **Empty Objects**: Use `{}` for empty objects like `workflow_dispatch: {}`
4. **Indentation**: Use consistent indentation (2 spaces recommended)

## Creating New Workflows

To create new workflow files that pass validation:

1. Copy the template from `.github/workflow_templates/standard_workflow.yml`
2. Customize the name, triggers, and jobs as needed
3. Run validation before committing: `python .github/scripts/simple_workflow_validator.py`

## Common Issues and Solutions

| Issue                                      | Solution                                                               |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| "Workflow missing 'on' trigger definition" | Ensure the 'on' keyword has single quotes: `'on':`                     |
| Empty validation results                   | Check file extensions (.yml not .yaml) and line endings (LF preferred) |
| Workflow doesn't run                       | Check branch name and path filters match your repository structure     |

## In Case of Validation Failures

If you encounter workflow validation errors, run:

```bash
bash .github/scripts/nuclear_fix_workflows.sh
```

This will regenerate all problematic workflow files with the correct format.
