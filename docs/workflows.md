# Workflows Guide

## Overview

### `Run Lint` Workflow

Uses `ruff` to check code style and linting issues across the codebase. It runs on pushes, pull requests to the `main` branch and can be called from another workflow.

![lint workflow](./images/lint-workflow.png)

### `Run Tests` Workflow

Uses `pytest` to run the test suite, ensuring that all tests pass before code is merged. It runs on pushes, pull requests to the `main` branch and can be called from another workflow.

![test workflow](./images/test-workflow.png)

### `Check PR Title` Workflow

Validates that pull request titles follow the conventional commit format. It runs on pull requests to the `main` branch and every time a PR is opened or updated.

Uses `amannn/action-semantic-pull-request` GitHub Action to enforce the commit message standards. The accepted types are: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, and `ci`.

![pr title workflow](./images/pr-title-workflow.png)

### `Release` Workflow

Automates the release process by creating a tag and new release on GitHub and building a Docker image. It runs manually via the GitHub Actions interface.

Uses `Run Lint` and `Run Tests` workflows to ensure code quality before proceeding with the release. The release version is determined based on the conventional commit messages since the last release using `googleapis/release-please-action`.

**Important:** uses semantic versioning and updates the version based on the commit types:

- `feat`: minor version bump
- `fix`: patch version bump
- `BREAKING CHANGE` or `feat!`: major version bump

## Pull Request Workflows

The `Run Lint`, `Run Tests`, and `Check PR Title` workflows are configured to run automatically on pull requests to the `main` branch. This ensures that code quality checks and tests are performed before any changes are merged.

![PR workflows](./images/pr-workflows.png)

## Creating Releases

*To be updated...*
