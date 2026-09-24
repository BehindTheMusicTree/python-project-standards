---
applyTo: "**"
---

# Copilot code review: python-project-standards

This repository is an **organization-wide standards and template bundle** for Python projects. It is **not** an installable application: there is **no root `pyproject.toml`**. Consumer repositories render the **Copier template** (`copier.yml`, `template/`) and may call **reusable workflows** published from `.github/workflows/`.

## What reviewers should prioritize

- **Pinning and versioning:** Callable workflow `uses:` lines and documented examples should prefer **release tags** (`@vX.Y.Z`) or commit SHAs, not long-lived `@main`. Consumers track the adopted release as `_commit` in `.copier-answers.yml` (see `docs/versioning.md` and `README.md`).
- **Accurate consumer guidance:** Changes to `template/` (`pyproject`, pre-commit, workflows) should remain consistent with **`docs/development.md`**, **`docs/reusable-workflows.md`**, and **`README.md`** so adopters are not given conflicting commands or pins.
- **Reusable workflow contract:** Edits to `.github/workflows/reusable-pre-commit.yml` are a **public API** for other repositories. Treat input renames, default changes, or step removals as **breaking** unless clearly backward compatible and documented in **`CHANGELOG.md`**.

## Quick validation (this repo)

Render the template from the working tree and run its hooks:

`copier copy --vcs-ref HEAD . /tmp/demo --defaults --data package_name=demo && cd /tmp/demo && git init -q && git add -A && pre-commit run --all-files`

## Policy pointers for Python-related feedback

When reviews touch **documented** Python style or tooling expectations, align with **`docs/string-enums.md`** (`StrEnum`, not `(str, Enum)`) and the baselines (**`template/baselines/ruff.toml`** includes **`UP`** in **`select`**; **`template/pyproject.toml.jinja`** for strict **`mypy`** + pytest-cov in dev extras). Prefer **pinned** tool versions in templates and pre-commit **`rev:`** fields.

## Trust these instructions first

Use repository files (especially `README.md` and `docs/development.md`) as the source of truth. Search the tree only when something here is incomplete or appears wrong after a change.
