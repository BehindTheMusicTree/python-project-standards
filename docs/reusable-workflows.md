# Reusable GitHub Actions workflows

This repository publishes **callable** workflows under `.github/workflows/`. Consumer repositories run them with `jobs.<job_id>.uses` so lint and test logic stay centralized.

## Naming: `reusable-` prefix

**GitHub does not require any filename pattern.** A workflow is reusable because its `on:` block includes `workflow_call`, not because of its name.

This repository uses the **`reusable-` prefix** as an **organizational convention**:

- **Clarity:** In `.github/workflows/`, it is obvious which files exist only to be **`uses:`’d** by other repos (or by thin caller workflows here) versus workflows that **trigger on `push` / `pull_request`**.
- **Discovery:** Contributors and reviewers can grep for `reusable-` when looking for callable entry points.

**Alternatives** that are equally valid elsewhere: no prefix with a subfolder (e.g. `.github/workflows/callable/lint.yml`), or another consistent scheme. Pick one convention per repository and stick to it.

**Renaming** a published reusable file is a **breaking change** for every consumer `uses:` path; treat renames like API changes (semver major or migration notes).

## Requirements

- The consumer repo must be allowed to use workflows from this repository (typically same GitHub organization and org settings that permit reusable workflows).
- Pin the callee ref (**prefer `@v2.1.0` or a commit SHA**). Avoid `@main` in production CI so standards updates do not surprise you.

## Reference workflows

| File | Purpose |
|------|---------|
| [`reusable-pre-commit.yml`](../.github/workflows/reusable-pre-commit.yml) | Checkout, install, run `pre-commit` (Tier A and Tier B). |
| [`reusable-test-matrix.yml`](../.github/workflows/reusable-test-matrix.yml) | Matrix of OS × Python; install; optional pytest cache, `fail-fast`, unit, integration, e2e, and coverage steps. |

## Example: pre-commit only (Tier B)

```yaml
jobs:
  pre-commit:
    uses: YOUR_ORG/python-project-standards/.github/workflows/reusable-pre-commit.yml@v2.1.0
    with:
      python-version: "3.14"
      install-command: |
        python -m pip install --upgrade pip
        pip install pre-commit==4.5.1
```

## Example: pre-commit caller (Tier A `lint.yml`)

Create `.github/workflows/lint.yml` in the consumer repository:

```yaml
name: Lint

on:
  pull_request:
  push:
    branches: [main]

jobs:
  lint:
    uses: YOUR_ORG/python-project-standards/.github/workflows/reusable-pre-commit.yml@v2.1.0
```

Override inputs only when needed (see table below).

## Example: test matrix caller

Create `.github/workflows/test.yml`:

```yaml
name: Test

on:
  pull_request:
  push:
    branches: [main]

jobs:
  tests:
    uses: YOUR_ORG/python-project-standards/.github/workflows/reusable-test-matrix.yml@v2.1.0
    with:
      os-matrix: '["ubuntu-latest", "macos-latest"]'
      python-matrix: '["3.11", "3.12"]'
```

`os-matrix` and `python-matrix` are **JSON arrays encoded as strings** (required by `workflow_call` string inputs and `fromJson` in the reusable workflow).

### Default test behavior

If you only set matrices (or use defaults), the reusable workflow runs **`e2e-command`** only for tests. Its default is `pytest -q`. **`unit-command`**, **`integration-command`**, and **`coverage-command`** default to empty and their steps are skipped.

**Windows note:** steps for **unit**, **integration**, and **coverage** are skipped when `runner.os == 'Windows'`. **e2e** runs on all matrix OS values when `e2e-command` is non-empty.

## Inputs: `reusable-pre-commit.yml`

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `runs-on` | string | `ubuntu-latest` | Runner label for the job. |
| `python-version` | string | `3.12` | Python version for `setup-python`. |
| `pre-install-command` | string | `""` | Optional shell command before install (skipped if empty). |
| `install-command` | string | `pip`-based editable dev install | Multi-line install script. |
| `pre-commit-command` | string | `pre-commit run --all-files` | Command to run after install. |

## Inputs: `reusable-test-matrix.yml`

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `os-matrix` | string (JSON array) | `["ubuntu-latest"]` | Runner OS labels for the matrix. |
| `python-matrix` | string (JSON array) | `["3.12"]` | Python versions for the matrix. |
| `install-command` | string | `pip`-based editable dev install | Run after optional pre-install steps. |
| `pre-install-ubuntu` | string | `""` | Linux-only pre-install (skipped if empty). |
| `pre-install-macos` | string | `""` | macOS-only pre-install. |
| `pre-install-windows` | string | `""` | Windows-only pre-install (runs with `pwsh`). |
| `unit-command` | string | `""` | Unit test command (skipped on Windows). |
| `integration-command` | string | `""` | Integration tests (skipped on Windows). |
| `e2e-command` | string | `pytest -q` | Main test command; runs on all matrix OS unless set empty. |
| `coverage-command` | string | `""` | e.g. coverage threshold check (skipped on Windows). |
| `fail-fast` | boolean | `true` | Matrix `fail-fast` (cancel other matrix jobs on first failure when `true`). |
| `cache-pytest` | boolean | `false` | Restore/save `.pytest_cache` keyed by OS, Python, `pyproject.toml`, `requirements.txt`. |
