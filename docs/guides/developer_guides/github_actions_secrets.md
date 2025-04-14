# GitHub Actions Secrets Guide

## Introduction

GitHub Actions secrets are encrypted environment variables that allow you to store sensitive information securely in your repository. These secrets can be used in your workflow files without exposing them in your code.

## Adding a New Secret

1. Navigate to your GitHub repository (`EosLumina/--ThinkAlike--`)
2. Click on the **Settings** tab near the top of the page
3. In the left sidebar, click on **Secrets and variables** → **Actions**
4. Click on the **New repository secret** button
5. Fill in the form:
   - **Name**: Enter your secret name (e.g., `DEPLOYMENT_TOKEN`)
     - Use UPPERCASE with underscores
     - Make names descriptive of their purpose
   - **Secret**: Enter the secret value
     - Be careful - you won't be able to view this value again, only replace it
6. Click **Add secret**

## Using Secrets in Workflows

Reference secrets in your workflow files using the following syntax:

```yaml
${{ secrets.YOUR_SECRET_NAME }}
```

Example usage in a workflow file:

```yaml
jobs:
  deploy:
    steps:
      - name: Deploy to production
        env:
          API_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
        run: |
          ./deploy-script.sh
```

## Security Best Practices

- Never log or print secret values in workflow runs
- Limit access to repository settings to trusted contributors
- Rotate secrets periodically (especially access tokens)
- Use the minimum required permissions for tokens and credentials

## Secret Naming Conventions for ThinkAlike

For consistency in the ThinkAlike project, use these naming conventions:

| Type of Secret | Naming Pattern | Example |
|----------------|----------------|---------|
| API Keys | `SERVICE_API_KEY` | `SENDGRID_API_KEY` |
| Access Tokens | `SERVICE_TOKEN` | `GITHUB_TOKEN` |
| Credentials | `SERVICE_CREDENTIALS` | `AWS_CREDENTIALS` |
| Environment URLs | `ENV_URL` | `STAGING_URL` |

## Updating or Deleting Secrets

To update a secret, follow the same process as adding a new one, but use the same name. The new value will replace the old one.

To delete a secret:
1. Go to the repository secrets page
2. Find the secret you want to delete
3. Click the Delete button (trash icon) next to it

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [ThinkAlike CI/CD Workflow Guide](./ci_cd_workflow_guide.md)
- [Deployment Troubleshooting](../architecture/deployment_troubleshooting.md)

---

## Document Details

- Title: GitHub Actions Secrets Guide
- Type: Developer Guide
- Version: 1.0.0
- Last Updated: 2025-08-18
