# python-project-standards

Organization-wide baseline standards for Python repositories: pinned tooling, pre-commit, CI, and contributor workflows.

## Table of Contents

- [Purpose](#purpose)
- [Development documentation](#development-documentation)
- [What Is Standardized](#what-is-standardized)
- [Repository Layout](#repository-layout)
- [Usage Model](#usage-model)
- [Design Principles](#design-principles)
- [Quick Start (Consumer Repo)](#quick-start-consumer-repo)
- [Adoption tiers](#adoption-tiers)
- [Reusable GitHub Actions](#reusable-github-actions)
- [Status](#status)

## Purpose

This repository provides a shared baseline for Python projects so teams can:

- keep lint, format, and type checks consistent across repositories;
- reduce CI/local drift;
- document process expectations in one place;
- allow project-specific exceptions without forking standards.

## Development documentation

**[docs/development.md](docs/development.md)** is the hub for organization-wide Python development policy (links to migration, versioning, CI reusables, and style notes such as [string enums](docs/string-enums.md)). Point consumer `DEVELOPMENT.md` / contributor docs at that page for shared baselines.

## What Is Standardized

- Shared policy and doc index in **[docs/development.md](docs/development.md)** (includes links to style pages under `docs/`);
- `pyproject.toml` tooling sections (`ruff`, `mypy`, `pytest`, **`pytest-cov`** in template dev extras for `pytest --cov=…`);
- `.pre-commit-config.yaml` with pinned hook revisions;
- CI workflow baseline: **Tier A** `lint.yml` delegates to org **`reusable-pre-commit.yml`** (pin `@v…`); tests live in the consumer repo (start from **`templates/github-workflows/test.yml`**);
- Cursor rules baseline for process conventions;
- migration and versioning guidance.

## Repository Layout

- `templates/pyproject/`: baseline `pyproject.toml` sections and examples.
- `templates/pre-commit/`: baseline `.pre-commit-config.yaml` (includes **`verify-python-project-standards`** hook).
- `templates/scripts/`: `verify-standards.sh` — copy into consumer `scripts/` next to the pre-commit hook.
- `templates/github-workflows/`: copy-paste workflow examples for consumer repos.
- `.github/workflows/reusable-*.yml`: **callable** workflows (shared pre-commit) for repos that reference this repository instead of duplicating lint YAML. The **`reusable-` filename prefix** is an org convention for discoverability, not a GitHub requirement — see the **Naming** section in [docs/reusable-workflows.md](docs/reusable-workflows.md).
- `templates/cursor-rules/`: baseline `.cursor/rules/*.mdc` files (dependency pinning, commit messages, PR workflow, documentation TOC, **string enums / `StrEnum`**). **Consumers copy** the ones they need into their own `.cursor/rules/` — not installed automatically; see [docs/development.md](docs/development.md) (**Cursor / AI assistant rules**).
- `docs/`: **[development.md](docs/development.md)** (hub), migration guide, versioning, reusable workflows, and style notes (e.g. [`string-enums.md`](docs/string-enums.md)).
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

Then copy **`templates/scripts/verify-standards.sh`** to **`scripts/verify-standards.sh`** in the consumer repo (the pre-commit template runs it). Adjust package metadata and local exceptions.

When publishing updates to this script, keep **`scripts/verify-standards.sh`** and **`templates/scripts/verify-standards.sh`** identical (or regenerate the template copy from the canonical script).

## Adoption tiers

Not every Python repo should use the same CI shape. Use these tiers:

| Tier | Typical repo | Use from this repo | Keep local |
|------|----------------|-------------------|------------|
| **A — Library** | Packaged library, multi-OS/Python matrix, `pyproject.toml` dev extras | **Delegated** [`reusable-pre-commit.yml`](.github/workflows/reusable-pre-commit.yml) for lint; **owned** `test.yml` (see [`templates/github-workflows/test.yml`](templates/github-workflows/test.yml) + local matrix/coverage) | Thin `lint.yml` caller; full control over test CI |
| **B — Service / API** | Django/FastAPI apps, Docker, DB, secrets, long integration jobs | [`reusable-pre-commit.yml`](.github/workflows/reusable-pre-commit.yml), pre-commit + policy templates | Full test / deploy workflows in the app repository |

**Pinning:** Consumer workflows should reference a **release tag** such as **`@v3.1.0`** (or a commit SHA), not **`@main`**, and set [`STANDARDS_VERSION`](STANDARDS_VERSION) in the consumer repo to match. See [docs/versioning.md](docs/versioning.md).

**Example Tier B:** [hear-the-music-tree-api](https://github.com/BehindTheMusicTree/hear-the-music-tree-api) keeps database and containerized pytest in its own workflow and may call **reusable pre-commit** only. See that repo’s `docs/ci/python-project-standards.md`.

## Reusable GitHub Actions

For orgs that keep this repo as the single source of truth, consumer workflows can call:

- `.github/workflows/reusable-pre-commit.yml` — checkout, install, run `pre-commit` (Tier A and Tier B).

There is **no** reusable test matrix; use [`templates/github-workflows/test.yml`](templates/github-workflows/test.yml) in the consumer repo and extend it as needed.

See [docs/reusable-workflows.md](docs/reusable-workflows.md) for caller examples and the full input list.

## Releases

Versions are **SemVer** (`v1.2.3` tags, `STANDARDS_VERSION` without `v`). Maintainers document changes in **`CHANGELOG.md`**, tag **`vX.Y.Z`**, and publish a **GitHub Release** with the same notes. Consumers pin callable workflows to that tag (or a commit SHA), not to `main` long term.

See **[docs/versioning.md](docs/versioning.md)** for bump rules, pinning guidance, and step-by-step release instructions.

## Status

Baseline is **versioned**; evolve via tagged releases and migration notes, not only through `main`.
