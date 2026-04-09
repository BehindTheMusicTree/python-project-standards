# python-project-standards

Organization-wide baseline standards for Python repositories: pinned tooling, pre-commit, CI, and contributor workflows.

## Table of Contents

- [Purpose](#purpose)
- [What Is Standardized](#what-is-standardized)
- [Repository Layout](#repository-layout)
- [Usage Model](#usage-model)
- [Design Principles](#design-principles)
- [Quick Start (Consumer Repo)](#quick-start-consumer-repo)
- [Reusable GitHub Actions](#reusable-github-actions)
- [Status](#status)

## Purpose

This repository provides a shared baseline for Python projects so teams can:

- keep lint, format, and type checks consistent across repositories;
- reduce CI/local drift;
- document process expectations in one place;
- allow project-specific exceptions without forking standards.

## What Is Standardized

- `pyproject.toml` tooling sections (`ruff`, `mypy`, `pytest`);
- `.pre-commit-config.yaml` with pinned hook revisions;
- CI workflow baseline for `pre-commit` and tests;
- Cursor rules baseline for process conventions;
- migration and versioning guidance.

## Repository Layout

- `templates/pyproject/`: baseline `pyproject.toml` sections and examples.
- `templates/pre-commit/`: baseline `.pre-commit-config.yaml`.
- `templates/github-workflows/`: copy-paste workflow examples for consumer repos.
- `.github/workflows/reusable-*.yml`: **callable** workflows (central lint/test matrix) for repos that reference this repository instead of duplicating YAML.
- `templates/cursor-rules/`: baseline `.cursor/rules/*.mdc` files.
- `docs/`: migration guide and standards versioning model.
- `scripts/`: validation helpers for standards adoption.

## Usage Model

1. Start from these templates when creating a new Python repository.
2. Copy the baseline into an existing repository.
3. Add explicit, documented project-level overrides.
4. Keep a `STANDARDS_VERSION` file in each consumer repository.

## Design Principles

- Tooling config is the primary enforcement mechanism.
- Exact version pinning for reproducibility.
- Baseline plus local overrides.
- Minimize duplicated policy text between tools, CI, and AI rules.

## Quick Start (Consumer Repo)

```bash
cp templates/pre-commit/.pre-commit-config.yaml /path/to/repo/.pre-commit-config.yaml
cp templates/github-workflows/lint.yml /path/to/repo/.github/workflows/lint.yml
cp templates/pyproject/pyproject.toml /path/to/repo/pyproject.toml
```

Then adjust package metadata and local exceptions.

## Reusable GitHub Actions

For orgs that keep this repo as the single source of truth, consumer workflows can call:

- `.github/workflows/reusable-lint.yml` — pre-commit on one runner.
- `.github/workflows/reusable-test-matrix.yml` — OS × Python matrix, optional unit/integration/e2e/coverage commands.

See [docs/reusable-workflows.md](docs/reusable-workflows.md) for caller examples and the full input list.

## Status

Initial baseline scaffold. Evolve this repository with versioned, documented changes.
