---
applyTo: "templates/**/*"
---

# Copilot code review: `templates/` bundle

These files are **copied into consumer repositories**. Drift between templates and what maintainers run locally in this repo causes adoption pain.

## Required consistency

- **`templates/scripts/verify-standards.sh`** must match **`scripts/verify-standards.sh`** at the repository root (see `README.md` **Quick Start**).
- **`templates/scripts/check_lint_baseline.py`** must match **`scripts/check_lint_baseline.py`** at the repository root.
- **`templates/cursor-rules/*.mdc`** should stay aligned with **`.cursor/rules/*.mdc`** for the same policy topics (paths inside rules may differ: templates sometimes use absolute GitHub links for copy-paste consumers).

## `templates/baselines/`

- **`ruff.toml`** is the canonical org Ruff rule set; **`DIGESTS`** must list the correct SHA-256 for **`baselines/ruff.toml`** (repo-root path as copied by consumers).
- **`expected-mypy.json`** must match the required **`[tool.mypy]`** keys in **`templates/pyproject/pyproject.toml`**.

## `templates/pyproject/pyproject.toml`

- Keep **`requires-python`**, **`baselines/ruff.toml` `target-version`**, and **`[tool.mypy]` `python_version`** coherent (baseline targets **3.12** in the current template).
- **`[tool.ruff]`** should remain a thin overlay: **`extend = "baselines/ruff.toml"`** only, unless documented overlay keys are intentionally expanded in **`docs/migration-guide.md`** and **`scripts/check_lint_baseline.py`**.
- **Dev dependencies** should remain **exactly pinned** (this org favors reproducibility). Include **`pytest-cov`** in dev extras as documented in the README.
- **`[lint] select`** in **`templates/baselines/ruff.toml`** should keep **`UP`** so **`UP042`** / `StrEnum` guidance in `docs/string-enums.md` matches enforcement.

## `templates/pre-commit/.pre-commit-config.yaml`

- Hook **`rev:`** values should match the versions implied by **`templates/pyproject/pyproject.toml`** where applicable (ruff, mypy, pre-commit).
- Preserve the **`verify-python-project-standards`** local hook pointing at **`bash scripts/verify-standards.sh`** with **`pass_filenames: false`** and **`always_run: true`** unless the migration guide is updated to a new contract.
- **`fail_fast: true`** is intentional baseline behavior unless policy changes.

## `templates/github-workflows/`

See **`github-actions.instructions.md`** for reusable vs template caller expectations and pinning.

## Cursor rule templates (`templates/cursor-rules/`)

- Treat edits as **org policy**: clear, actionable bullets; frontmatter (`description`, `globs`, `alwaysApply`) must remain valid for Cursor.
- Avoid contradicting **`docs/`** pages that are linked from **`docs/development.md`**.
