---
applyTo: "template/**/*,copier.yml"
---

# Copilot code review: Copier template (`template/`, `copier.yml`)

These files are **rendered into consumer repositories** by `copier copy` and merged by `copier update`. Every change reaches adopters on their next update.

## `copier.yml`

- `_skip_if_exists` lists **bootstrap-only** files (`pyproject.toml`, `.github/workflows/test.yml`); everything else under `template/` is updated on `copier update`. `_skip_if_exists` only protects files that exist: a file a consumer deletes is re-created on update, so optional files use a question-gated filename (`reusable_lint`, `test_workflow`).
- Renaming or removing a question is **breaking** for existing `.copier-answers.yml` files; document it in **`CHANGELOG.md`** and **`docs/migration-guide.md`**.

## `template/baselines/ruff.toml`

- Canonical org Ruff rule set. **`[lint] select`** should keep **`UP`** so **`UP042`** / `StrEnum` guidance in `docs/string-enums.md` matches enforcement.

## `template/pyproject.toml.jinja`

- Keep **`requires-python`**, **`baselines/ruff.toml` `target-version`**, and **`[tool.mypy]` `python_version`** coherent (baseline targets **3.12**).
- **`[tool.ruff]`** should remain a thin overlay: **`extend = "baselines/ruff.toml"`** only.
- **Dev dependencies** should remain **exactly pinned**. Include **`pytest-cov`** in dev extras as documented in the README.

## `template/.pre-commit-config.yaml`

- Hook **`rev:`** values should match the versions pinned in **`template/pyproject.toml.jinja`** where applicable (ruff, mypy, pre-commit).
- **`fail_fast: true`** is intentional baseline behavior unless policy changes.

## `template/.github/workflows/`

See **`github-actions.instructions.md`** for reusable vs template caller expectations and pinning.
