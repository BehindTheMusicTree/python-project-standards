# Changelog

All notable changes to this standards repository will be documented in this file.

The format is inspired by Keep a Changelog and follows semantic-style versioning for standards releases.

## [Unreleased]

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
