# Changelog

All notable changes to this standards repository will be documented in this file.

The format is inspired by Keep a Changelog and follows semantic-style versioning for standards releases.

## [Unreleased]

### Fixed

- **`scripts/check_lint_baseline.py`** (and **`templates/scripts/check_lint_baseline.py`**): avoid reassigning the **`for`** loop variable (**`PLW2901`**) so consumers whose baseline includes **`PL`** can run **Ruff** on this script without a per-file ignore.

- **`scripts/check_lint_baseline.py`** (and **`templates/scripts/check_lint_baseline.py`**): fail if **`baselines/DIGESTS`** omits **`baselines/ruff.toml`** or **`baselines/expected-mypy.json`**, so those baselines cannot silently drop out of digest verification.

- **[`docs/migration-guide.md`](docs/migration-guide.md)**: **`verify-python-project-standards`** description notes that **`baselines/DIGESTS`** must list **`baselines/ruff.toml`** and **`baselines/expected-mypy.json`**.

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.3.2`** / **`@v4.3.2`**.

## [4.3.1] - 2026-04-12

### Changed

- **`scripts/standards_release_bump.sh`**: optional **`BUMP_MY_VERSION_PYTHON`** for **`uv run --python`** when **`uv`** is used; **[`docs/versioning.md`](docs/versioning.md)** documents macOS **`bump-my-version`** segfault / CoreFoundation fork troubleshooting.

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.3.1`** / **`@v4.3.1`**.

## [4.3.0] - 2026-04-12

### Changed

- **`scripts/verify-standards.sh`** (and **`templates/scripts/verify-standards.sh`**): reject **isort** in **`.pre-commit-config.yaml`** (**`mirrors-isort`**, **`PyCQA/isort`**, hook **`id: isort`**) with an error explaining conflict with **`ruff format`**; import sorting stays on Ruff **`I`** via **`baselines/ruff.toml`**. Escape hatch: **`VERIFY_STANDARDS_ALLOW_ISORT=1`**.

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.3.0`** / **`@v4.3.0`**.

## [4.2.0] - 2026-04-12

### Added

- **Release automation**: **`.bumpversion.toml`** for **`bump-my-version==1.3.0`** (typically **`uv run --with bump-my-version==1.3.0 …`**); **`scripts/standards_release_bump.sh`** bumps **`STANDARDS_VERSION`** and org example **`@v…`** pins, then **`scripts/finalize_standards_changelog.py`** folds **`CHANGELOG.md` `## [Unreleased]`** into **`## [X.Y.Z] - YYYY-MM-DD`** using the post-bump version (see **`docs/versioning.md`**). The script **requires a clean git tree** before **`bump-my-version`**; optional **`--commit`** stages **only** paths from **`git diff --name-only HEAD`** after bump + finalize (never **`git add -A`**), then commits **`chore(release): vX.Y.Z`**.

- **Cursor**: **`changelog-alignment.mdc`** in **`.cursor/rules/`** and **`templates/cursor-rules/`** (`alwaysApply`) requires updating **`CHANGELOG.md` `## [Unreleased]`** alongside substantive repo changes (with narrow exemptions), including a reminder to update consumer changelogs when aligning downstream repos. **[README](README.md)** lists the rule in the Cursor template bundle.

### Changed

- **`scripts/verify-standards.sh`** (and **`templates/scripts/verify-standards.sh`**): skip consumer verification when **`templates/pyproject/pyproject.toml`** exists and there is **no** root **`baselines/ruff.toml`**, so a future root **`pyproject.toml`** (for example maintainer tooling) does not require a consumer **`baselines/`** tree.

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.2.0`** / **`@v4.2.0`**.

## [4.1.1] - 2026-04-12

### Fixed

- **`templates/baselines/DIGESTS`**: list SHA-256 for **`baselines/expected-mypy.json`** alongside **`baselines/ruff.toml`** so **`check_lint_baseline.py`** digest verification catches Mypy baseline drift.

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.1.1`** / **`@v4.1.1`**.

## [4.1.0] - 2026-04-11

### Added

- **`scripts/publish_github_release.py`**: create a GitHub Release from the matching **`CHANGELOG.md`** section via **`gh release create`** (see **`docs/versioning.md`**).
- **`.github/workflows/release-on-tag.yml`**: on SemVer tag push, run that script with **`GITHUB_TOKEN`** so releases do not depend on a maintainer laptop.

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.1.0`** / **`@v4.1.0`**.

## [4.0.0] - 2026-04-11

### Added

- **`templates/baselines/`**: vendored **`ruff.toml`**, **`DIGESTS`**, and **`expected-mypy.json`** for a strict shared lint/type baseline; consumer **`pyproject.toml`** uses **`[tool.ruff] extend = "baselines/ruff.toml"`** with an allowlisted overlay only.
- **`scripts/check_lint_baseline.py`** (mirrored under **`templates/scripts/`**): verifies digest, Ruff overlay keys, and Mypy keys vs **`baselines/expected-mypy.json`** (optional **`[[tool.mypy.overrides]]`** only).

### Breaking

- Consumers that run **`verify-python-project-standards`** must adopt the new **`baselines/`** tree and scripts or set **`VERIFY_STANDARDS_SKIP_LINT_BASELINE=1`** until migrated.

### Changed

- **`scripts/verify-standards.sh`** (and template copy): after layout checks, runs **`python3 scripts/check_lint_baseline.py`** unless **`VERIFY_STANDARDS_SKIP_LINT_BASELINE=1`**. Adopters must copy **`baselines/`**, **`check_lint_baseline.py`**, and the updated **`pyproject.toml`** / **`verify-standards.sh`** from templates (see **`docs/migration-guide.md`**).
- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`4.0.0`** / **`@v4.0.0`**.

## [3.1.0] - 2026-04-11

### Added

- **GitHub Copilot**: Path-specific repository instructions under **`.github/instructions/*.instructions.md`** (`applyTo` frontmatter) for Copilot code review and cloud agent context (repository overview, Actions, templates, documentation, shell scripts).

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`.github/instructions/github-actions.instructions.md`](.github/instructions/github-actions.instructions.md), [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`3.1.0`** / **`@v3.1.0`**.

## [3.0.1] - 2026-04-13

### Fixed

- **`scripts/verify-standards.sh`** (and **`templates/scripts/verify-standards.sh`**): Local ruff detection no longer matches **`id: ruff-format`** as **`ruff`**; requires **`id: ruff`**, **`id: ruff-check`**, or **`entry: … ruff check …`**.

- **`STANDARDS_VERSION` pin check**: Scan **`.github/workflows/*.yml`** and **`*.yaml`** with a shell loop instead of **`grep -r … --include`** after the path (which some **`grep`** implementations treat as extra filenames). Same logic: any line mentioning **`python-project-standards`** must include a matching **`@v…`** pin when workflows reference the org.

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`3.0.1`** / **`@v3.0.1`**.

## [3.0.0] - 2026-04-12

### Removed

- **`reusable-test-matrix.yml`**: removed. **Breaking change** for consumers that called it — stay on **`@v2.3.0`** until you replace the job, or implement tests locally (see [`templates/github-workflows/test.yml`](templates/github-workflows/test.yml)). [docs/migration-guide.md](docs/migration-guide.md) adds a short migration section.

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`3.0.0`** / **`@v3.0.0`** for **`reusable-pre-commit.yml`**.
- **Tier A docs**: libraries delegate lint only; test CI is owned in each consumer repository.

## [2.3.0] - 2026-04-11

### Added

- **`templates/pyproject/pyproject.toml`**: **`pytest-cov==4.0.0`** in **`[project.optional-dependencies] dev`** so **`pytest --cov=…`** works out of the box for Tier A-style CI (see **`reusable-test-matrix`**); consumers may still override or drop if they use **`coverage run -m pytest`** only.

### Changed

- **`reusable-test-matrix.yml`**: **`coverage-fail-under`** defaults to **`"80"`** and runs **`coverage report --fail-under=…`** when **`coverage-command`** is empty **only if** **`unit-command`** or **`integration-command`** is non-empty or **`e2e-command`** contains **`--cov`** (so the default **`pytest -q`** matrix does not run an empty coverage step). Set **`coverage-fail-under: ''`** to disable. Documented in [reusable-workflows.md](docs/reusable-workflows.md).

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, **`templates/github-workflows/lint.yml`**, [`STANDARDS_VERSION`](STANDARDS_VERSION) → **`2.3.0`** / **`@v2.3.0`**.

## [2.2.0] - 2026-04-10

### Added

- **`reusable-test-matrix.yml`**: optional **`coverage-fail-under`** string input. When **`coverage-command`** is empty and **`coverage-fail-under`** is set (e.g. `"85"`), the coverage step runs **`coverage report --fail-under=<value>`**. Non-empty **`coverage-command`** still runs the custom command and ignores **`coverage-fail-under`** for that step. Documented in [docs/reusable-workflows.md](docs/reusable-workflows.md).

### Changed

- **Pins**: README, [migration-guide.md](docs/migration-guide.md), [reusable-workflows.md](docs/reusable-workflows.md) examples, and **`templates/github-workflows/lint.yml`** use **`@v2.2.0`**; [`STANDARDS_VERSION`](STANDARDS_VERSION) is **`2.2.0`**.

## [2.1.0] - 2026-04-09

### Changed

- **`templates/github-workflows/lint.yml`**: example **`uses:`** pin updated to **`@v2.1.0`**. README, [migration-guide.md](docs/migration-guide.md), and [reusable-workflows.md](docs/reusable-workflows.md) examples use **`@v2.1.0`** for current adoption.

### Added

- **`templates/cursor-rules/strenum-string-enums.mdc`**: Cursor baseline for `StrEnum` vs `(str, Enum)`; **`.cursor/rules/strenum-string-enums.mdc`** mirror for maintainers of this repository.

### Documentation

- **[docs/development.md](docs/development.md)**: hub for org-wide Python development policy (migration, versioning, reusables, [string-enums.md](docs/string-enums.md), README). README **Development documentation** section; **Cursor / AI assistant rules** (copy **`templates/cursor-rules/`** into consumers; diff on `STANDARDS_VERSION` bumps).
- **[docs/string-enums.md](docs/string-enums.md)**: `StrEnum` vs `(str, Enum)`; **Enforcement** recommends Ruff **UP042** when **`UP`** is selected; optional AST hook / Cursor as extras. Linked from migration guide and hub.

## [2.0.0] - 2026-04-09

### Removed

- **`reusable-lint.yml`**: removed; **`reusable-pre-commit.yml`** is the single callable for checkout → install → `pre-commit`. Consumers must replace `uses: …/reusable-lint.yml@…` with **`…/reusable-pre-commit.yml@…`** (same inputs).

### Changed

- **`templates/github-workflows/lint.yml`**: delegates to **`reusable-pre-commit.yml@v2.0.0`**. Tier A/B docs and examples updated to **`@v2.0.0`** where they describe current pinning.

### Added

- **Pre-commit**: Template includes **`verify-python-project-standards`** running `scripts/verify-standards.sh`; **`templates/scripts/verify-standards.sh`** ships the same script for copy-into-consumer. Verifier supports Tier **A/B**, local or remote ruff/mypy hooks, `pytest.ini` or `[tool.pytest.ini_options]`, optional **`STANDARDS_VERSION`** vs `@v…` pin check (`VERIFY_STANDARDS_SKIP_PIN_CHECK=1` for SHA-only pins).

### Documentation

- README / migration guide: copy `verify-standards.sh` with the pre-commit template; release checklist note to keep template script in sync.
- [docs/reusable-workflows.md](docs/reusable-workflows.md): **Naming** section documents the optional `reusable-` prefix (convention vs GitHub requirement, alternatives, rename = breaking for `uses:` paths).

## [1.0.0] - 2026-04-09

### Added

- First publishable baseline for cross-project Python standards (templates, docs, reusable workflows).
- Adoption tiers (library vs API) in README; example Tier B link to hear-the-music-tree-api.
- `reusable-pre-commit.yml` callable workflow (forwards to `reusable-lint.yml`).
- `reusable-test-matrix.yml`: inputs `fail-fast` (default `true`) and `cache-pytest` (default `false`).

### Documentation

- **[docs/versioning.md](docs/versioning.md)**: SemVer for standards, consumer pinning (tags vs SHA), maintainer release checklist, GitHub Releases.
- Migration guide: templates vs reusables, pinning `@v` refs, Tier A/B pointers.
- Reusable workflows doc: `reusable-pre-commit`, matrix inputs, examples use `@v1.0.0`.
