# Migration Guide

For a map of all org Python standards docs, start with **[development.md](development.md)**.

Use this guide to adopt the baseline in an existing repository.

## Templates versus reusable workflows

| Artifact | What it is | When to use |
|----------|------------|-------------|
| `templates/github-workflows/*.yml` | **Copy-paste** starters (e.g. `lint.yml` delegates via `uses:` to org reusables) | New repos; `lint.yml` stays a thin caller pinned to `@v…` |
| `.github/workflows/reusable-*.yml` | **Callable** workflows in `python-project-standards` | Repos that call `uses: org/python-project-standards/.github/workflows/....yml@ref` and pass `with:` inputs |

Reusable workflows are resolved **at CI runtime** from this repository. Templates are **static copies** you own and drift unless you sync manually.

## Pinning callee refs

Prefer a **release tag** or **commit SHA**, not `main`:

```yaml
uses: BehindTheMusicTree/python-project-standards/.github/workflows/reusable-pre-commit.yml@v4.3.2
```

Match the tag in the consumer’s `STANDARDS_VERSION` file. See [versioning.md](versioning.md).

## 1. Copy baseline files

- Copy `templates/pre-commit/.pre-commit-config.yaml` to repository root.
- Copy `templates/scripts/verify-standards.sh` and **`templates/scripts/check_lint_baseline.py`** to **`scripts/`** and `chmod +x` **`scripts/verify-standards.sh`** (the template pre-commit includes **`verify-python-project-standards`**, which runs **`verify-standards.sh`**; that script runs the Python checker unless skipped).
- Copy **`templates/baselines/`** to **`baselines/`** at the repository root (`ruff.toml`, **`DIGESTS`**, **`expected-mypy.json`**). Ruff’s shared **`select`** / **`ignore`** / line length live only in **`baselines/ruff.toml`**; **`pyproject.toml`** must keep **`[tool.ruff] extend = "baselines/ruff.toml"`** exactly.
- Copy `templates/github-workflows/lint.yml` to `.github/workflows/lint.yml` — it **delegates** to [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) (`uses:` … `@v…`; bump the tag with `STANDARDS_VERSION`). For tests, copy [`templates/github-workflows/test.yml`](../templates/github-workflows/test.yml) to `.github/workflows/test.yml` and extend it (matrix, coverage, services) in the consumer repo; there is no org reusable test workflow (see [reusable-workflows.md](reusable-workflows.md)).
- Merge relevant sections from `templates/pyproject/pyproject.toml` (metadata, dependencies, **`[tool.mypy]`**, pytest); do not move org Ruff rule settings into **`pyproject.toml`** except the thin **`[tool.ruff]`** overlay described below.
- Copy needed **`templates/cursor-rules/*.mdc`** files into **`.cursor/rules/`** (org baselines are optional copies; merge with repo-specific rules). Include **`strenum-string-enums.mdc`** if you enforce [string enums](string-enums.md).

## 2. Install and validate

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

The **`verify-python-project-standards`** hook checks that CI references **`pre-commit run`** and/or org **`python-project-standards`** reusables (delegated **Tier A** `lint.yml` satisfies the latter), ruff/mypy in pre-commit (remote mirrors **or** local `language: system` hooks), **no isort in pre-commit** (**`mirrors-isort`**, **`PyCQA/isort`**, or hook **`id: isort`**) so **`ruff format`** and Ruff’s import rules stay the single authority, **`STANDARDS_VERSION`** vs **`@v…`** pins when workflows use this org’s reusables, and (unless skipped) **lint baseline integrity**: **`baselines/DIGESTS`** lists **`baselines/ruff.toml`** and **`baselines/expected-mypy.json`** (required entries) and each listed file’s SHA-256 matches the file on disk, **`[tool.ruff]`** in **`pyproject.toml`** is only the allowed overlay on top of **`extend = "baselines/ruff.toml"`**, and **`[tool.mypy]`** matches **`baselines/expected-mypy.json`** aside from optional **`[[tool.mypy.overrides]]`**. Set **`VERIFY_STANDARDS_SKIP_PIN_CHECK=1`** if you legitimately pin callables to a **SHA** instead of **`@vX.Y.Z`**. Set **`VERIFY_STANDARDS_SKIP_LINT_BASELINE=1`** only as a temporary escape hatch (for example while rebasing a large standards bump); it disables the digest and overlay checks. Set **`VERIFY_STANDARDS_ALLOW_ISORT=1`** only briefly if you must keep an isort hook until you can remove it.

## 3. Add project-specific overrides

- Follow shared Python style notes in this repo’s `docs/` where applicable (e.g. [string enumerations (`StrEnum`)](string-enums.md)).
- **Ruff:** In **`pyproject.toml`**, only **`exclude`**, **`extend-exclude`**, and **`[tool.ruff.lint]`** keys **`per-file-ignores`** / **`extend-per-file-ignores`** may be added on top of **`extend`**. Do **not** set **`lint.select`**, **`lint.ignore`**, **`line-length`**, or **`[tool.ruff.format]`** in **`pyproject.toml`**—Ruff would override the extended baseline and **`check_lint_baseline.py`** will fail. Change shared rules by updating **`baselines/ruff.toml`** from a new template release and refreshing **`DIGESTS`**.
- **Mypy:** Match every key in **`baselines/expected-mypy.json`** in **`[tool.mypy]`**; add **`[[tool.mypy.overrides]]`** only when needed (for example tests).
- Add local hooks for custom checks only when needed.

## 4. Track adopted version

Create a `STANDARDS_VERSION` file in the consumer repository:

```text
4.3.2
```

## 5. CI alignment check

With the default **`lint.yml`** template, **pre-commit runs inside** [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) (install dev deps + `pre-commit run --all-files`). For tests, maintain a workflow in the consumer repository (start from [`templates/github-workflows/test.yml`](../templates/github-workflows/test.yml)); see [reusable-workflows.md](reusable-workflows.md).

## 6. Migrating off `reusable-test-matrix.yml` (standards v2.x → v3+)

**`reusable-test-matrix.yml` was removed in v3.0.0.** Consumers that called it should either:

- Stay on **`@v2.3.0`** (or another **v2.x** tag) until they replace the call, or
- Remove the `uses: …/reusable-test-matrix.yml@…` job and implement tests locally (copy [`templates/github-workflows/test.yml`](../templates/github-workflows/test.yml), add `strategy.matrix`, `pytest --cov`, etc., as needed).

Pin **`reusable-pre-commit.yml`** to a current release tag (e.g. **`@v4.3.2`**) when adopting **v4+**; it is unrelated to the removed matrix but should match **`STANDARDS_VERSION`** for org consistency.

## 7. Tier B (API / service)

Keep Docker, databases, and secrets in local workflows; call [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) for shared pre-commit in CI only.
