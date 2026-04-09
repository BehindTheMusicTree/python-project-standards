# Migration Guide

Use this guide to adopt the baseline in an existing repository.

## 1. Copy baseline files

- Copy `templates/pre-commit/.pre-commit-config.yaml` to repository root.
- Copy `templates/github-workflows/lint.yml` to `.github/workflows/lint.yml` (or call the central reusable workflows; see [reusable-workflows.md](reusable-workflows.md)).
- Merge relevant sections from `templates/pyproject/pyproject.toml`.
- Copy needed `.mdc` files into `.cursor/rules/`.

## 2. Install and validate

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## 3. Add project-specific overrides

- Add `ruff` per-file ignores only when needed.
- Add `mypy` overrides for tests only when needed.
- Add local hooks for custom checks only when needed.

## 4. Track adopted version

Create a `STANDARDS_VERSION` file in the consumer repository:

```text
1.0.0
```

## 5. CI alignment check

Ensure CI installs dev dependencies and runs:

```bash
pre-commit run --all-files
```
