# Migration Guide

For a map of all org Python standards docs, start with **[development.md](development.md)**.

Use this guide to adopt the baseline in an existing repository.

## Copier template versus reusable workflows

| Artifact | What it is | When to use |
|----------|------------|-------------|
| [`template/`](../template/) + [`copier.yml`](../copier.yml) | **[Copier](https://copier.readthedocs.io/)** template: `.pre-commit-config.yaml`, `baselines/ruff.toml`, `lint.yml`, starter `pyproject.toml` / `test.yml` | Every consumer; `copier update` merges new releases into the repo while keeping local edits |
| `.github/workflows/reusable-*.yml` | **Callable** workflows in `python-project-standards` | Repos that call `uses: org/python-project-standards/.github/workflows/....yml@ref` and pass `with:` inputs |

Reusable workflows are resolved **at CI runtime** from this repository. Template files are rendered into the consumer and updated with **`copier update`** (3-way merge against the previously adopted release).

## Pinning callee refs

Prefer a **release tag** or **commit SHA**, not `main`:

```yaml
uses: BehindTheMusicTree/python-project-standards/.github/workflows/reusable-pre-commit.yml@v5.0.0
```

The template’s `lint.yml` carries this pin, so `copier update` bumps it. Repos with their own caller workflow (`reusable_lint: false`) bump the pin by hand. See [versioning.md](versioning.md).

## 1. Adopt the template

Install Copier with an exact pin (for example `uv tool install copier==9.18.2`), then from the repository root:

```bash
copier copy --vcs-ref v5.0.0 gh:BehindTheMusicTree/python-project-standards . --overwrite
git add -p   # keep repo-specific hooks and settings the template overwrote
```

Questions (`copier.yml`):

- **`package_name`** — `[project] name` in the starter `pyproject.toml`.
- **`reusable_lint`** — `true` renders `.github/workflows/lint.yml` delegating to [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml); `false` when the repo already runs pre-commit in its own workflow (e.g. Tier B services).
- **`test_workflow`** — `true` renders a starter `.github/workflows/test.yml`; `false` when tests run in a differently named workflow (otherwise `copier update` re-creates the deleted file).

`pyproject.toml` and `.github/workflows/test.yml` are **bootstrap-only** (`_skip_if_exists`): rendered for new repos, never touched in existing ones. Merge relevant sections from [`template/pyproject.toml.jinja`](../template/pyproject.toml.jinja) by hand (metadata, dependencies, **`[tool.mypy]`**, pytest). Tests stay in the consumer repo; there is no org reusable test workflow (see [reusable-workflows.md](reusable-workflows.md)).

Commit **`.copier-answers.yml`**: it records the adopted release (`_commit`) and answers so later updates know what to merge.

## 2. Install and validate

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## 3. Add project-specific overrides

- Follow shared Python style notes in this repo’s `docs/` where applicable (e.g. [string enumerations (`StrEnum`)](string-enums.md)).
- **Ruff:** keep **`[tool.ruff] extend = "baselines/ruff.toml"`** in **`pyproject.toml`** and put only **`exclude`**, **`extend-exclude`**, and **`[tool.ruff.lint]`** **`per-file-ignores`** / **`extend-per-file-ignores`** on top. Do **not** set **`lint.select`**, **`lint.ignore`**, **`line-length`**, or **`[tool.ruff.format]`** there—Ruff would override the shared baseline. Shared rule changes arrive through `copier update` on **`baselines/ruff.toml`**.
- **Mypy:** keep the strict keys from the template **`[tool.mypy]`**; add **`[[tool.mypy.overrides]]`** only when needed (for example tests).
- Add local pre-commit hooks for custom checks only when needed; `copier update` keeps them.

## 4. Update to a new release

```bash
copier update            # latest tag; or --vcs-ref vX.Y.Z
pre-commit run --all-files
```

Resolve any conflicts like a git merge and commit the result together with the updated `.copier-answers.yml`.

## 5. Migrating from v4 (copied templates) to v5 (Copier)

v5 removes the copy-and-verify machinery. In each consumer:

1. Run the adoption steps in [§1](#1-adopt-the-template).
2. Delete **`STANDARDS_VERSION`** (replaced by `_commit` in `.copier-answers.yml`), **`scripts/verify-standards.sh`**, **`scripts/check_lint_baseline.py`**, **`baselines/DIGESTS`** and **`baselines/expected-mypy.json`**.
3. Remove the **`verify-python-project-standards`** hook from `.pre-commit-config.yaml`.
4. Agent/editor rules are no longer distributed (`templates/cursor-rules/` is gone); rules each repo already copied are now owned by that repo.

## 6. Migrating off `reusable-test-matrix.yml` (standards v2.x → v3+)

**`reusable-test-matrix.yml` was removed in v3.0.0.** Consumers that called it should either:

- Stay on **`@v2.3.0`** (or another **v2.x** tag) until they replace the call, or
- Remove the `uses: …/reusable-test-matrix.yml@…` job and implement tests locally (start from [`template/.github/workflows/test.yml`](../template/.github/workflows/), add `strategy.matrix`, `pytest --cov`, etc., as needed).

## 7. Tier B (API / service)

Keep Docker, databases, and secrets in local workflows; call [reusable-pre-commit.yml](../.github/workflows/reusable-pre-commit.yml) for shared pre-commit in CI only, or answer `reusable_lint: false` and run pre-commit inline.
