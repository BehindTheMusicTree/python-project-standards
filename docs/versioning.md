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

Prepare a release on a clean task branch created from current `main`. Keep the coordinated pins managed by `.bumpversion.toml`; `STANDARDS_VERSION` remains the canonical version.

### Automated bump (recommended)

1. Commit meaningful release notes under `## [Unreleased]` in `CHANGELOG.md` on the task branch.
2. Run `bash scripts/standards_release_bump.sh patch` (or `minor` / `major`). It updates the version, configured example pins, and changelog together. `--commit` stages only modified release paths and creates the preparation commit. Set `CHANGELOG_DATE=YYYY-MM-DD` to override the release date.
3. Review the diff, including the updated changelog TOC. Commit the preparation and open a pull request against `main`.
4. After merge, CI validates the version, mirror, nonempty changelog section and main ancestry, then creates an annotated tag on that exact commit. The tag workflow publishes the GitHub release from those notes. Rerun the failed workflow to recover; an existing release is retained.

`--dry-run` runs the coordinated bump simulation without finalizing the changelog or committing. Only `--dry-run`, `--verbose` and `-v` are forwarded; configuration overrides and tagging options are refused. Empty changelog sections are refused before the bump. The script also refuses `main`, `develop`, detached HEADs, and dirty trees.

**Tooling:** Prefer `uv run --with bump-my-version==1.3.0 …`; otherwise install `bump-my-version==1.3.0` on `PATH`. If the tool crashes on macOS, set `BUMP_MY_VERSION_PYTHON=3.12` (see troubleshooting below).

### Manual checklist

1. On the task branch, set `STANDARDS_VERSION`, `.bumpversion.toml` `current_version`, and every pin listed in that configuration to the same new version.
2. Move release notes into the unique matching `## [X.Y.Z] - YYYY-MM-DD` changelog section, retaining an empty `Unreleased` section and updating the TOC.
3. Commit, open a pull request against `main`, and let CI create the tag and release after merge. Do not tag or publish locally. `scripts/publish_github_release.py --dry-run` remains available to preview notes; local publication is refused once the release policy is present.

Initial adoption keeps version v5.2.0 and creates no tag. App access and tag protections are activated separately through `github-config` before a subsequent release is prepared.

**Frequency:** Cut a release when there is something adopters should **intentionally** pick up—not necessarily for every doc typo. Batch small doc fixes into the next **PATCH** or **MINOR** as appropriate.

### Troubleshooting: bump-my-version on macOS

If **`bash scripts/standards_release_bump.sh …`** dies with **`Segmentation fault: 11`** (sometimes after a **CoreFoundation** / **“process has forked … YOU MUST exec()”** message), typical causes are:

1. **Very new CPython** (for example **3.14** as the default **`python3`**) plus **`bump-my-version`**’s stack (**`pydantic-core`**, **`httpx`**, etc.). Wheels and extension modules may still be catching up; a **native** bug often shows up as **SIGSEGV** rather than a clean Python traceback.
2. **`uv run`** on **macOS** in a **sandboxed** or unusual environment (some IDE terminals, security tools, or **`sandbox-exec`** policies) stressing **SystemConfiguration** / network stacks; see upstream discussion around **`uv`** and macOS sandboxes ([astral-sh/uv#17799](https://github.com/astral-sh/uv/issues/17799) and linked issues).

**What to try (in order):**

- **Pin the interpreter for the bump only:**  
  **`BUMP_MY_VERSION_PYTHON=3.12 bash scripts/standards_release_bump.sh patch`**  
  When **`uv`** is on **`PATH`**, the script passes that value to **`uv run --python …`** so **`bump-my-version==1.3.0`** runs on a stable runtime (**`uv`** can install a managed **3.12** if needed). Without **`uv`**, install **`bump-my-version==1.3.0`** on a **3.11–3.12** environment and ensure **`bump-my-version`** on **`PATH`** uses that same interpreter.
- **Skip `uv`:** install **`bump-my-version==1.3.0`** into a **venv** with **3.12**, activate it, run **`bump-my-version bump …`** by hand, then **`python3 scripts/finalize_standards_changelog.py`** from the repo root (see the automated bump steps above).
- **Last resort (not recommended long-term):** some macOS **fork-safety** warnings go away with **`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`**; treat this as a diagnostic knob, not a fix for a segfaulting native extension.

If **`bump-my-version bump --dry-run`** succeeds but a real bump crashes, the failure is likely in a code path that edits files or runs **git**—still try an older **Python** first.

## History

- **Git** keeps full commit history; **tags** are immutable pointers to released commits.  
- **CHANGELOG.md** is the human-facing summary; it does not replace `git log`.
