# Reusable GitHub Actions workflows

This repository publishes **callable** workflows under `.github/workflows/`. Consumer repositories run them with `jobs.<job_id>.uses` so lint logic stays centralized.

## Naming: `reusable-` prefix

**GitHub does not require any filename pattern.** A workflow is reusable because its `on:` block includes `workflow_call`, not because of its name.

This repository uses the **`reusable-` prefix** as an **organizational convention**:

- **Clarity:** In `.github/workflows/`, it is obvious which files exist only to be **`uses:`’d** by other repos (or by thin caller workflows here) versus workflows that **trigger on `push` / `pull_request`**.
- **Discovery:** Contributors and reviewers can grep for `reusable-` when looking for callable entry points.

**Alternatives** that are equally valid elsewhere: no prefix with a subfolder (e.g. `.github/workflows/callable/lint.yml`), or another consistent scheme. Pick one convention per repository and stick with it.

**Renaming** a published reusable file is a **breaking change** for every consumer `uses:` path; treat renames like API changes (semver major or migration notes).

## Requirements

- The consumer repo must be allowed to use workflows from this repository (typically same GitHub organization and org settings that permit reusable workflows).
- Pin the callee ref (**prefer `@v3.0.0` or a commit SHA**). Avoid `@main` in production CI so standards updates do not surprise you.

## Reference workflows

| File | Purpose |
|------|---------|
| [`reusable-pre-commit.yml`](../.github/workflows/reusable-pre-commit.yml) | Checkout, install, run `pre-commit` (Tier A and Tier B). |

**Tests:** this repository does **not** ship a reusable test matrix. Use [`templates/github-workflows/test.yml`](../templates/github-workflows/test.yml) as a starting point in the consumer repo and add `strategy.matrix`, coverage, or service containers locally.

## Example: pre-commit only (Tier B)

```yaml
jobs:
  pre-commit:
    uses: YOUR_ORG/python-project-standards/.github/workflows/reusable-pre-commit.yml@v3.0.0
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
    uses: YOUR_ORG/python-project-standards/.github/workflows/reusable-pre-commit.yml@v3.0.0
```

Override inputs only when needed (see table below).

## Inputs: `reusable-pre-commit.yml`

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `runs-on` | string | `ubuntu-latest` | Runner label for the job. |
| `python-version` | string | `3.12` | Python version for `setup-python`. |
| `pre-install-command` | string | `""` | Optional shell command before install (skipped if empty). |
| `install-command` | string | `pip`-based editable dev install | Multi-line install script. |
| `pre-commit-command` | string | `pre-commit run --all-files` | Command to run after install. |
