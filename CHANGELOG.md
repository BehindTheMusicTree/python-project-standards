# Changelog

All notable changes to this standards repository will be documented in this file.

The format is inspired by Keep a Changelog and follows semantic-style versioning for standards releases.

## [Unreleased]

### Changed

- **`templates/github-workflows/lint.yml`**: delegates to **`reusable-lint.yml@v1.0.0`** instead of inlining checkout/install/pre-commit steps (shared linting). README adoption table and migration guide updated.

### Added

- **Pre-commit**: Template includes **`verify-python-project-standards`** running `scripts/verify-standards.sh`; **`templates/scripts/verify-standards.sh`** ships the same script for copy-into-consumer. Verifier supports Tier **A/B**, local or remote ruff/mypy hooks, `pytest.ini` or `[tool.pytest.ini_options]`, optional **`STANDARDS_VERSION`** vs `@v…` pin check (`VERIFY_STANDARDS_SKIP_PIN_CHECK=1` for SHA-only pins).

### Documentation

- README / migration guide: copy `verify-standards.sh` with the pre-commit template; release checklist note to keep template script in sync.

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
