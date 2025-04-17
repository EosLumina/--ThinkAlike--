# Contributing to ThinkAlike

Thank you for considering contributing to ThinkAlike! We welcome contributions from everyone. By participating in this project, you agree to abide by our [Code of Conduct](./docs/core/code_of_conduct.md).

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Branching Strategy](#branching-strategy)
4. [Running Linters and Tests Locally](#running-linters-and-tests-locally)
5. [Submitting Changes](#submitting-changes)
6. [Code of Conduct](#code-of-conduct)

## Getting Started

To get started with contributing to ThinkAlike, please follow these steps:

1. **Read the [Onboarding Guide](./docs/core/onboarding_guide.md)**: This guide provides a comprehensive introduction to the project and its goals.
2. **Familiarize Yourself with the [Project Overview](./docs/core/project_overview.md)**: Understand the high-level summary of the project.
3. **Join the Community**: Connect with other contributors on [Discord](https://discord.gg/TnAcWezH) or [Matrix](https://matrix.to/#/#thinkalike:matrix.org).

## Development Environment Setup

To set up your development environment, follow these steps:

### Backend

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/EosLumina/--ThinkAlike--.git
    cd --ThinkAlike--
    ```

2. **Set Up Python Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install --upgrade pip
    pip install -r backend/requirements.txt
    pip install -r backend/requirements-dev.txt
    ```

### Frontend

1. **Navigate to Frontend Directory**:
    ```sh
    cd frontend
    ```

2. **Install Node.js Dependencies**:
    ```sh
    npm install
    ```

## Branching Strategy

We follow the GitHub Flow branching strategy:

1. **Create a Branch**: Branch from `main` for new features or bug fixes.
    ```sh
    git checkout -b feature/your-feature-name
    ```

2. **Commit Changes**: Make your changes and commit them with clear and descriptive messages.
    ```sh
    git add .
    git commit -m "Add feature: your feature description"
    ```

3. **Push to Remote**: Push your branch to the remote repository.
    ```sh
    git push origin feature/your-feature-name
    ```

4. **Create a Pull Request**: Open a pull request (PR) to merge your changes back into `main`.

## Running Linters and Tests Locally

### Backend

1. **Run Linters**:
    ```sh
    flake8 backend
    black --check backend
    isort --check-only backend
    ```

2. **Run Tests**:
    ```sh
    pytest backend/tests
    ```

### Frontend

1. **Run Linters**:
    ```sh
    npm run lint
    ```

2. **Run Tests**:
    ```sh
    npm test
    ```

## Submitting Changes

1. **Ensure All Tests Pass**: Make sure all tests pass locally before submitting your changes.
2. **Follow Code Style Guidelines**: Ensure your code follows the project's code style guidelines.
3. **Submit a Pull Request**: Open a pull request with a clear description of your changes and any relevant issue numbers.

## Code of Conduct

Please read and follow our [Code of Conduct](./docs/core/code_of_conduct.md) to ensure a welcoming and inclusive environment for everyone.

Thank you for contributing to ThinkAlike!
