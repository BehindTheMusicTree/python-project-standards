# Standards versioning and releases

This repository is versioned **independently** from consumer repositories. Versions communicate **compatibility and migration effort**, not a shipped Python package.

## Semantic versioning (SemVer)

| Bump | When |
|------|------|
| **MAJOR** | Breaking changes consumers must react to: removed/renamed workflow inputs or files, changed contracts for reusable workflows, template moves that invalidate copies without migration. |
| **MINOR** | Backward-compatible additions: new optional workflow inputs, new templates, new docs, new reusable entry points. Existing callers keep working without changes. |
| **PATCH** | Fixes, clarifications, typo-only or docs-only corrections; no intended behavior change for callers. |

`STANDARDS_VERSION` in this repo (and in consumer repos) uses **`MAJOR.MINOR.PATCH`** without a `v` prefix. Git tags use the **`v` prefix** (for example `v1.0.0`) so they are clearly distinguished from branch names.

## What consumers should pin

| Pin style | Use when |
|-----------|----------|
| **Version tag** (`@v1.2.3`) | Default for org repos: readable upgrades, matches `STANDARDS_VERSION`. |
| **Commit SHA** | Strongest reproducibility and supply-chain hygiene; use for high-assurance CI or temporary pins while validating a fix on `main`. |

Avoid long-lived **`@main`** (or other branch refs) in production workflows: standards evolve; branch heads change without a version signal.

After each **standards** release, consumer maintainers should:

1. Set **`STANDARDS_VERSION`** to the new version (for example `1.1.0`).
2. Update **`uses: …/workflow.yml@v…`** to the **same** tag (or chosen SHA).
3. Read **CHANGELOG.md** and **docs/migration-guide.md** for this repo before bumping **major** versions.

## Release notes (what to include)

Each GitHub Release (and matching `CHANGELOG.md` section) should make adoption safe:

- **Changed templates or workflow paths** — what moved or was renamed.
- **Callable workflow inputs/outputs** — added, removed, deprecated, default changes.
- **Migration impact** — “no action”, “optional”, or “required steps”.
- **Related docs** — links to `docs/migration-guide.md` sections when relevant.

## Releasing (maintainers)

Do this from a clean working tree on **`main`** (or your default branch).

1. **Changelog**  
   - Move items from `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section (or fold into the version you are cutting).  
   - Leave `## [Unreleased]` empty or remove subsection bullets until the next change.

2. **Version file**  
   - Set root **`STANDARDS_VERSION`** to **`X.Y.Z`** (no `v`).

3. **Commit**  
   - One commit for the release prep, for example: `chore(release): v1.0.0`.

4. **Tag**  
   - Create an annotated tag: `git tag -a vX.Y.Z -m "vX.Y.Z"`  
   - Light tags are acceptable if your org standardizes on them; annotated tags carry the message on `git show`.

5. **Push**  
   - `git push origin main` and `git push origin vX.Y.Z` (or push all tags).

6. **GitHub Release**  
   - On GitHub: **Releases → Draft a new release → Choose tag `vX.Y.Z`**.  
   - Title: **`vX.Y.Z`**.  
   - Description: copy the **`## [X.Y.Z]`** section from `CHANGELOG.md` (or summarize).  
   - Publish the release so adopters see release notes next to the tag.

**Frequency:** Cut a release when there is something adopters should **intentionally** pick up—not necessarily for every doc typo. Batch small doc fixes into the next **PATCH** or **MINOR** as appropriate.

**Template sync:** After changing **`scripts/verify-standards.sh`**, copy it to **`templates/scripts/verify-standards.sh`** before tagging so the template bundle matches the canonical script.

## History

- **Git** keeps full commit history; **tags** are immutable pointers to released commits.  
- **CHANGELOG.md** is the human-facing summary; it does not replace `git log`.
