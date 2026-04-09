# Changelog

All notable changes to this standards repository will be documented in this file.

The format is inspired by Keep a Changelog and follows semantic-style versioning for standards releases.

## [Unreleased]

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
