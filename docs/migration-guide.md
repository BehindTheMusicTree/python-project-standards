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
uses: BehindTheMusicTree/python-project-standards/.github/workflows/reusable-pre-commit.yml@v2.1.0
```

Match the tag in the consumer’s `STANDARDS_VERSION` file. See [versioning.md](versioning.md).

## 1. Copy baseline files

- Copy `templates/pre-commit/.pre-commit-config.yaml` to repository root.
- Copy `templates/scripts/verify-standards.sh` to `scripts/verify-standards.sh` and `chmod +x` it (the template pre-commit includes **`verify-python-project-standards`**, which runs this script).
- Copy `templates/github-workflows/lint.yml` to `.github/workflows/lint.yml` — it **delegates** to [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) (`uses:` … `@v…`; bump the tag with `STANDARDS_VERSION`). For tests, prefer a caller to [reusable-test-matrix.yml](../.github/workflows/reusable-test-matrix.yml) (see [reusable-workflows.md](reusable-workflows.md)) instead of inlining `pytest` steps.
- Merge relevant sections from `templates/pyproject/pyproject.toml`.
- Copy needed **`templates/cursor-rules/*.mdc`** files into **`.cursor/rules/`** (org baselines are optional copies; merge with repo-specific rules). Include **`strenum-string-enums.mdc`** if you enforce [string enums](string-enums.md).

## 2. Install and validate

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

The **`verify-python-project-standards`** hook checks that CI references **`pre-commit run`** and/or org **`python-project-standards`** reusables (delegated **Tier A** `lint.yml` satisfies the latter), ruff/mypy in pre-commit (remote mirrors **or** local `language: system` hooks), and `STANDARDS_VERSION` vs `@v…` pins when workflows use this org’s reusables. Set **`VERIFY_STANDARDS_SKIP_PIN_CHECK=1`** if you legitimately pin callables to a **SHA** instead of `@vX.Y.Z`.

## 3. Add project-specific overrides

- Follow shared Python style notes in this repo’s `docs/` where applicable (e.g. [string enumerations (`StrEnum`)](string-enums.md)).
- Add `ruff` per-file ignores only when needed.
- Add `mypy` overrides for tests only when needed.
- Add local hooks for custom checks only when needed.

## 4. Track adopted version

Create a `STANDARDS_VERSION` file in the consumer repository:

```text
2.1.0
```

## 5. CI alignment check

With the default **`lint.yml`** template, **pre-commit runs inside** [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) (install dev deps + `pre-commit run --all-files`). For tests, add a thin caller to [reusable-test-matrix.yml](../.github/workflows/reusable-test-matrix.yml) rather than duplicating install/pytest steps (see [reusable-workflows.md](reusable-workflows.md)).

## 6. Tier B (API / service)

Keep Docker, databases, and secrets in local workflows; call [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) for shared pre-commit in CI only.
