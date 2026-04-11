---
applyTo: "scripts/**/*.sh,templates/scripts/**/*.sh,scripts/**/*.py,templates/scripts/**/*.py"
---

# Copilot code review: shell scripts

- Prefer **`#!/usr/bin/env bash`** with **`set -euo pipefail`** for new or heavily edited scripts (match `scripts/verify-standards.sh`).
- **`scripts/verify-standards.sh`** and **`templates/scripts/verify-standards.sh`** must remain **byte-for-byte aligned** with the same behavior; this repository relies on that for consumer pre-commit.
- **`scripts/check_lint_baseline.py`** and **`templates/scripts/check_lint_baseline.py`** must remain **byte-for-byte aligned**.
- **`scripts/publish_github_release.py`** is maintainer-only (not copied to **`templates/`**): keep it working with **`CHANGELOG.md`** section headers **`## [X.Y.Z]`** and **`gh release create`**.
- Keep the **early exit** path for **python-project-standards** itself (no root `pyproject.toml` but `templates/pyproject` exists): consumers must not break, and this repo’s own CI or hooks must not falsely fail.
- Use portable patterns where reasonable; the script already branches on **`rg`** vs **`grep`**. Avoid introducing dependencies on nonstandard tools without documenting them.
- When changing verification rules, update **`README.md`**, **`docs/migration-guide.md`** (if adopters must change layout), and **`templates/pre-commit`** comments if the hook contract changes.
