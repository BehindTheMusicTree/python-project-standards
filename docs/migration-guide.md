# Migration Guide

Use this guide to adopt the baseline in an existing repository.

## Templates versus reusable workflows

| Artifact | What it is | When to use |
|----------|------------|-------------|
| `templates/github-workflows/*.yml` | **Copy-paste** starters for a consumer repo | New repos or teams that want a full workflow file in-tree without `uses:` |
| `.github/workflows/reusable-*.yml` | **Callable** workflows in `python-project-standards` | Repos that call `uses: org/python-project-standards/.github/workflows/....yml@ref` and pass `with:` inputs |

Reusable workflows are resolved **at CI runtime** from this repository. Templates are **static copies** you own and drift unless you sync manually.

## Pinning callee refs

Prefer a **release tag** or **commit SHA**, not `main`:

```yaml
uses: BehindTheMusicTree/python-project-standards/.github/workflows/reusable-lint.yml@v1.0.0
```

Match the tag in the consumer’s `STANDARDS_VERSION` file. See [versioning.md](versioning.md).

## 1. Copy baseline files

- Copy `templates/pre-commit/.pre-commit-config.yaml` to repository root.
- Copy `templates/scripts/verify-standards.sh` to `scripts/verify-standards.sh` and `chmod +x` it (the template pre-commit includes **`verify-python-project-standards`**, which runs this script).
- Copy `templates/github-workflows/lint.yml` to `.github/workflows/lint.yml` (or call the central reusable workflows; see [reusable-workflows.md](reusable-workflows.md)).
- Merge relevant sections from `templates/pyproject/pyproject.toml`.
- Copy needed `.mdc` files into `.cursor/rules/`.

## 2. Install and validate

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

The **`verify-python-project-standards`** hook checks Tier **A** (local `pre-commit run` in CI) and **B** (workflows referencing org `python-project-standards` reusables), ruff/mypy in pre-commit (remote mirrors **or** local `language: system` hooks), and `STANDARDS_VERSION` vs `@v…` pins when workflows use this org’s reusables. Set **`VERIFY_STANDARDS_SKIP_PIN_CHECK=1`** if you legitimately pin callables to a **SHA** instead of `@vX.Y.Z`.

## 3. Add project-specific overrides

- Add `ruff` per-file ignores only when needed.
- Add `mypy` overrides for tests only when needed.
- Add local hooks for custom checks only when needed.

## 4. Track adopted version

Create a `STANDARDS_VERSION` file in the consumer repository:

```text
1.0.0
```

## 5. CI alignment check

Ensure CI installs dev dependencies and runs:

```bash
pre-commit run --all-files
```

## 6. Optional: call reusable workflows instead of copying

For **Tier A (library)** repos, prefer calling [reusable-lint.yml](../.github/workflows/reusable-lint.yml) and [reusable-test-matrix.yml](../.github/workflows/reusable-test-matrix.yml) from a small caller workflow (see [reusable-workflows.md](reusable-workflows.md)).

For **Tier B (API / service)** repos, keep Docker, databases, and secrets in local workflows; optionally call [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) only.
