---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml,templates/github-workflows/**/*.yml"
---

# Copilot code review: GitHub Actions

## Callable workflows (this repository)

- Files under **`.github/workflows/`** that define **`on: workflow_call`** are **reusable entry points**. This repo uses the **`reusable-` filename prefix** as an org convention for discoverability (see `docs/reusable-workflows.md`). Renaming a published reusable file is a **breaking change** for every consumer `uses:` path.
- **`release-on-tag.yml`** is **not** callable: it runs on **`push`** of SemVer tags and publishes a GitHub Release via **`scripts/publish_github_release.py`**. It needs **`permissions: contents: write`**; keep the tag glob aligned with **`docs/versioning.md`**.
- **`reusable-pre-commit.yml`** should remain a thin, predictable pipeline: checkout → setup Python (with pip cache) → optional pre-install → install → `pre-commit run --all-files` (or overridden command). Avoid surprising side effects in defaults; document new **`inputs`** in `docs/reusable-workflows.md` and **`CHANGELOG.md`** when behavior or contract changes.

## Template caller workflows (`templates/github-workflows/`)

- **`lint.yml`** is the **Tier A** pattern: a single job that **`uses:`** the org reusable workflow with a **pinned ref** (example in tree: `@v4.3.2`). When updating the example pin, consider whether **`STANDARDS_VERSION`**, **`CHANGELOG.md`**, and docs examples need the same bump for consistency.
- **`test.yml`** is a **starter only** for consumer repos. This standards repo does **not** ship a reusable test matrix. Reviews should resist moving project-specific test logic here unless the README and docs explicitly expand that scope.

## Review checklist

- **Action versions:** Prefer pinned major versions consistent with the rest of the file (avoid mixing very old and very new without reason).
- **Security and secrets:** Do not introduce secret logging; use GitHub‑supported patterns for credentials.
- **Inputs:** New `workflow_call` inputs need defaults or `required: true` as appropriate; document them for callers.
