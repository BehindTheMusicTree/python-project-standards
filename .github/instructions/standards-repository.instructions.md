---
applyTo: "**"
---

# Copilot code review: python-project-standards

This repository is an **organization-wide standards and template bundle** for Python projects. It is **not** an installable application: there is **no root `pyproject.toml`**. Consumer repositories copy files from `templates/` and may call **reusable workflows** published from `.github/workflows/`.

## What reviewers should prioritize

- **Pinning and versioning:** Callable workflow `uses:` lines and documented examples should prefer **release tags** (`@vX.Y.Z`) or commit SHAs, not long-lived `@main`. When workflows reference this org repo, **`STANDARDS_VERSION`** in consumer repos should align with that pin (see `docs/versioning.md` and `README.md`).
- **Template parity:** `scripts/verify-standards.sh` and `templates/scripts/verify-standards.sh` must stay **identical** (or regenerated from one canonical copy). The same applies to **`.cursor/rules/*.mdc`** and **`templates/cursor-rules/*.mdc`** when both exist for the same policy.
- **Accurate consumer guidance:** Changes to templates (`pyproject`, pre-commit, workflows) should remain consistent with **`docs/development.md`**, **`docs/reusable-workflows.md`**, and **`README.md`** so adopters are not given conflicting commands or pins.
- **Reusable workflow contract:** Edits to `.github/workflows/reusable-pre-commit.yml` are a **public API** for other repositories. Treat input renames, default changes, or step removals as **breaking** unless clearly backward compatible and documented in **`CHANGELOG.md`**.

## Quick validation (this repo)

From the repository root, run:

`bash scripts/verify-standards.sh`

For **this** repository it exits **0** early with a message that verification is skipped (no root `pyproject.toml`). That is expected. After substantive edits to the verify script or templates, confirm behavior still matches the README and `templates/pre-commit` expectations.

## Policy pointers for Python-related feedback

When reviews touch **documented** Python style or tooling expectations, align with **`docs/string-enums.md`** (`StrEnum`, not `(str, Enum)`) and the baseline **`templates/pyproject/pyproject.toml`** (ruff `select` includes **`UP`**, strict mypy, pytest-cov in dev extras). Prefer **pinned** tool versions in templates and pre-commit **`rev:`** fields.

## Trust these instructions first

Use repository files (especially `README.md` and `docs/development.md`) as the source of truth. Search the tree only when something here is incomplete or appears wrong after a change.
