# GitHub Actions Database Setup Guide

This guide will help you easily configure database credentials for GitHub Actions workflows without needing to manually create complex connection strings.

## Understanding Database Connection Strings

A database connection string contains the information needed to connect to a database:
- Database type (PostgreSQL, MySQL, etc.)
- Host address (where the database is located)
- Port number
- Database name
- Username
- Password
- Additional parameters

## Quick Setup Method

For ThinkAlike's CI/CD workflows, we've created a simple script that generates and tests database credentials automatically.

### Option 1: Use Our Automated Setup Script

1. In your terminal, run:

```bash
python scripts/setup_ci_credentials.py
```

2. The script will:
   - Generate appropriate database credentials for testing
   - Test the connection
   - Output the correct values to use for GitHub Actions secrets
   - Provide commands to set these secrets via GitHub CLI (if installed)

3. Follow the on-screen instructions to add the secrets to your GitHub repository

### Option 2: Use Default Testing Credentials

If you're just getting started and want a quick solution for CI workflows, you can use these standard testing values:

1. Go to your repository's Settings → Secrets and variables → Actions
2. Add the following secrets:

| Secret Name | Value for Testing |
|-------------|-------------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/thinkalike_test` |
| `SECRET_KEY` | `thinkaliketestsecretkey123456789` |

**Note:** These values are for CI testing environments only and are not meant for production use.

## Manual Setup (For Custom Database Configuration)

If you need to configure a custom database connection:

### PostgreSQL Connection String Format
