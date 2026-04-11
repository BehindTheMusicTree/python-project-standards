---
applyTo: "docs/**/*.md,README.md,CHANGELOG.md"
---

# Copilot code review: Markdown documentation

## Hub and cross-links

- **`docs/development.md`** is the **policy hub**: new org-wide topics should be linked from there (and implemented in templates or workflows as needed). Avoid orphan docs that duplicate README sections without a single source of truth.
- Prefer **stable, relative** links between files in this repository (e.g. `docs/reusable-workflows.md`). Use absolute GitHub URLs only where the text is explicitly meant for **copy-paste into consumer repos**.

## Table of contents

For substantial Markdown (`README.md`, `docs/**/*.md`, `CHANGELOG.md` when it uses multiple `##` sections), follow the same TOC discipline as **`templates/cursor-rules/documentation-toc.mdc`**:

1. Add **`## Table of Contents`** after the title (and short intro if present).
2. List every navigable **`##`** section in order with GitHub-style anchor links; update the TOC in the **same change** as heading edits.
3. Skip linking the TOC section itself. For trivial one-section files, a TOC is optional.

## Changelog and releases

- **`CHANGELOG.md`** entries should match the **semver** story in **`docs/versioning.md`** and tag/release practice described in **`README.md`**.

## Tone and scope

- Write for **maintainers and consumers** adopting the baseline: concrete file paths, commands, and pinning guidance. Avoid vague “best practice” filler that is not actionable in this repo.
