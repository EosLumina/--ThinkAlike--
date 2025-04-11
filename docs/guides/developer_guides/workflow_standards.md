# GitHub Actions Workflow Standards

When working with GitHub Actions workflows in ThinkAlike, follow these best practices:

1. **External Scripts**: Place Python code in separate script files under `.github/scripts/` rather than embedding directly in YAML.

2. **Required Structure**: Ensure every workflow has:
   - A descriptive `name`
   - An `on` section defining triggers (push, pull_request, etc.)
   - At least one `job` with a `runs-on` specification

3. **Validation**: Always validate workflow files before committing:
   ```bash
   python .github/scripts/validate_workflows.py
   ```

4. **Repository References**: Always use `EosLumina/--ThinkAlike--` (with double dashes) for repository references.

Following these standards prevents CI/CD pipeline failures and ensures consistent workflow behavior.

## Common Issues and Solutions

1. **Missing Trigger Definition**: Always include an `on` section:
   ```yaml
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
     workflow_dispatch:  # Enable manual triggers
   ```

2. **Multi-line Python Scripts**: Always extract to external script files in `.github/scripts/` folder rather than embedding in YAML.

3. **Validation Best Practice**: Run the validator before committing:
   ```bash
   python .github/scripts/validate_workflows.py
   ```
