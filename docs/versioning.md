# Standards versioning and releases

This repository is versioned **independently** from consumer repositories. Versions communicate **compatibility and migration effort**, not a shipped Python package.

## Table of Contents

- [Semantic versioning (SemVer)](#semantic-versioning-semver)
- [What consumers should pin](#what-consumers-should-pin)
- [Release notes (what to include)](#release-notes-what-to-include)
- [Releasing (maintainers)](#releasing-maintainers)
- [History](#history)

## Semantic versioning (SemVer)

| Bump | When |
|------|------|
| **MAJOR** | Breaking changes consumers must react to: removed/renamed workflow inputs or files, changed contracts for reusable workflows, template moves that invalidate copies without migration. |
| **MINOR** | Backward-compatible additions: new optional workflow inputs, new templates, new docs, new reusable entry points. Existing callers keep working without changes. |
| **PATCH** | Fixes, clarifications, typo-only or docs-only corrections; no intended behavior change for callers. |

`STANDARDS_VERSION` in this repo uses **`MAJOR.MINOR.PATCH`** without a `v` prefix. Git tags use the **`v` prefix** (for example `v2.0.0`) so they are clearly distinguished from branch names.

## What consumers should pin

| Pin style | Use when |
|-----------|----------|
| **Version tag** (`@v1.2.3`) | Default for org repos: readable upgrades, matches the `_commit` tag in `.copier-answers.yml`. |
| **Commit SHA** | Strongest reproducibility and supply-chain hygiene; use for high-assurance CI or temporary pins while validating a fix on `main`. |

Avoid long-lived **`@main`** (or other branch refs) in production workflows: standards evolve; branch heads change without a version signal.

After each **standards** release, consumer maintainers should:

1. Run **`copier update`** (records the new tag as `_commit` in **`.copier-answers.yml`** and bumps the template `lint.yml` pin).
2. Update any other **`uses: …/workflow.yml@v…`** to the **same** tag (or chosen SHA).
3. Read **CHANGELOG.md** and **docs/migration-guide.md** for this repo before bumping **major** versions.

## Release notes (what to include)

Each GitHub Release (and matching `CHANGELOG.md` section) should make adoption safe:

- **Changed templates or workflow paths** — what moved or was renamed.
- **Callable workflow inputs/outputs** — added, removed, deprecated, default changes.
- **Migration impact** — “no action”, “optional”, or “required steps”.
- **Related docs** — links to `docs/migration-guide.md` sections when relevant.

## Releasing (maintainers)

`STANDARDS_VERSION` is the canonical version. Release Please (`release-please-config.json`, `.release-please-manifest.json`, job `release-please` in `.github/workflows/release-tag.yml`) maintains a release PR from conventional PR titles; never bump, tag or publish by hand.

1. Merge PRs titled `feat:`/`fix:` (and `!` for breaking changes); `ci:`, `docs:`, `chore:` and similar titles do not open a release.
2. Release Please updates `STANDARDS_VERSION`, every pin marked `x-release-please-version` and `CHANGELOG.md` in its release PR. `scripts/tests/test_release_version_sync.py` fails if a marked pin differs or a current-version pin lacks its marker.
3. CI auto-merges the release PR once the required checks pass, then creates the tag and publishes the GitHub Release from the generated notes. Rerun a failed workflow to recover; an existing release is retained.

**Version markers:** the Release Please Generic updater replaces the first SemVer of each marked line. Mark only the line holding the standards pin: `<!-- x-release-please-version -->` at the end of a prose line, ` # x-release-please-version` on a pin or `copier copy --vcs-ref` line in a copyable YAML or shell example, and `{# x-release-please-version #}` directly after the template pin so the rendered workflow carries no comment or trailing space.

**Frequency:** Every merged `feat:`/`fix:` PR releases; title doc-only fixes `docs:` so they ride the next release.

## History

- **Git** keeps full commit history; **tags** are immutable pointers to released commits.  
- **CHANGELOG.md** is the human-facing summary; it does not replace `git log`.
