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
- allow project-specific **ignores** (Ruff per-file, Mypy overrides) without forking the shared rule baseline.

## Development documentation

**[docs/development.md](docs/development.md)** is the hub for organization-wide Python development policy (links to migration, versioning, CI reusables, and style notes such as [string enums](docs/string-enums.md)). Point consumer `DEVELOPMENT.md` / contributor docs at that page for shared baselines.

## What Is Standardized

- Shared policy and doc index in **[docs/development.md](docs/development.md)** (includes links to style pages under `docs/`);
- `pyproject.toml` tooling sections (`ruff` via **`baselines/ruff.toml`** + thin overlay, strict **`mypy`** keys, `pytest`, **`pytest-cov`** in template dev extras for `pytest --cov=…`);
- `.pre-commit-config.yaml` with pinned hook revisions;
- CI workflow baseline: **Tier A** `lint.yml` delegates to org **`reusable-pre-commit.yml`** (pin `@v…`); tests live in the consumer repo (start from **`template/.github/workflows/test.yml`**);
- migration and versioning guidance.

## Repository Layout

- `copier.yml` + `template/`: **[Copier](https://copier.readthedocs.io/)** template rendered into consumer repos — `.pre-commit-config.yaml`, `baselines/ruff.toml`, optional `.github/workflows/lint.yml` (updated by `copier update`), plus bootstrap-only `pyproject.toml` and `.github/workflows/test.yml`.
- `.github/workflows/reusable-*.yml`: **callable** workflows (shared pre-commit) for repos that reference this repository instead of duplicating lint YAML. The **`reusable-` filename prefix** is an org convention for discoverability, not a GitHub requirement — see the **Naming** section in [docs/reusable-workflows.md](docs/reusable-workflows.md).
- `docs/`: **[development.md](docs/development.md)** (hub), migration guide, versioning, reusable workflows, and style notes (e.g. [`string-enums.md`](docs/string-enums.md)).
- `scripts/`: maintainer release tooling; **`standards_release_bump.sh`** + **`finalize_standards_changelog.py`** automate SemVer bumps (see [docs/versioning.md](docs/versioning.md)). **`.bumpversion.toml`** configures **`bump-my-version`** for **`STANDARDS_VERSION`** and example **`@v…`** pins (not **`CHANGELOG.md`**).

## Usage Model

1. Render the template into a new or existing repository with `copier copy`.
2. Add explicit, documented project-level overrides.
3. Pull new releases with `copier update`; the adopted release is recorded in `.copier-answers.yml`.

## Design Principles

- Tooling config is the primary enforcement mechanism.
- Exact version pinning for reproducibility.
- Baseline plus local overrides.
- Minimize duplicated policy text between tools, CI, and AI rules.

## Quick Start (Consumer Repo)

```bash
uv tool install copier==9.18.2
copier copy gh:BehindTheMusicTree/python-project-standards /path/to/repo   # new repo
copier update                                                             # later, from the repo root
```

For an existing repository, see [docs/migration-guide.md](docs/migration-guide.md). Keep **`[tool.ruff] extend = "baselines/ruff.toml"`** in `pyproject.toml`; shared rule changes arrive through `copier update`.

## Adoption tiers

Not every Python repo should use the same CI shape. Use these tiers:

| Tier | Typical repo | Use from this repo | Keep local |
|------|----------------|-------------------|------------|
| **A — Library** | Packaged library, multi-OS/Python matrix, `pyproject.toml` dev extras | **Delegated** [`reusable-pre-commit.yml`](.github/workflows/reusable-pre-commit.yml) for lint; **owned** `test.yml` (see [`template/.github/workflows/test.yml`](template/.github/workflows/) + local matrix/coverage) | Thin `lint.yml` caller; full control over test CI |
| **B — Service / API** | Django/FastAPI apps, Docker, DB, secrets, long integration jobs | [`reusable-pre-commit.yml`](.github/workflows/reusable-pre-commit.yml), pre-commit + policy templates | Full test / deploy workflows in the app repository |

**Pinning:** Consumer workflows should reference a **release tag** such as **`@v5.1.0`** (or a commit SHA), not **`@main`**; `copier update` bumps the template `lint.yml` pin. See [docs/versioning.md](docs/versioning.md).

**Example Tier B:** [hear-the-music-tree-api](https://github.com/BehindTheMusicTree/hear-the-music-tree-api) keeps database and containerized pytest in its own workflow and may call **reusable pre-commit** only. See that repo’s `docs/ci/python-project-standards.md`.

## Reusable GitHub Actions

For orgs that keep this repo as the single source of truth, consumer workflows can call:

- `.github/workflows/reusable-pre-commit.yml` — checkout, install, run `pre-commit` (Tier A and Tier B).

There is **no** reusable test matrix; use [`template/.github/workflows/test.yml`](template/.github/workflows/) in the consumer repo and extend it as needed.

See [docs/reusable-workflows.md](docs/reusable-workflows.md) for caller examples and the full input list.

## Releases

Versions are **SemVer** (`v1.2.3` tags, `STANDARDS_VERSION` without `v`). Maintainers document changes in **`CHANGELOG.md`**, tag **`vX.Y.Z`**, and publish a **GitHub Release** with the same notes. Consumers pin callable workflows to that tag (or a commit SHA), not to `main` long term.

Pushing a SemVer tag like **`v5.1.0`** triggers [`.github/workflows/release-on-tag.yml`](.github/workflows/release-on-tag.yml), which publishes the GitHub Release from the matching **`CHANGELOG.md`** section. You can still run **`python3 scripts/publish_github_release.py`** locally (see **[docs/versioning.md](docs/versioning.md)**).

## Status

Baseline is **versioned**; evolve via tagged releases and migration notes, not only through `main`.
