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

`STANDARDS_VERSION` in this repo (and in consumer repos) uses **`MAJOR.MINOR.PATCH`** without a `v` prefix. Git tags use the **`v` prefix** (for example `v2.0.0`) so they are clearly distinguished from branch names.

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

### Automated bump (recommended)

1. **Changelog draft** — Add release notes under **`## [Unreleased]`** in **`CHANGELOG.md`**, then **`git commit`** that draft (only the prep you want on **`main`**). **`scripts/standards_release_bump.sh`** refuses to start unless the working tree is **clean**, so **`bump-my-version`** can keep **`allow_dirty = false`** without toggling config.

2. **Bump** — From the repository root, run **`bash scripts/standards_release_bump.sh patch`** (or **`minor`** / **`major`**). Optional **`--commit`**: after **`bump-my-version`** and **`finalize_standards_changelog.py`**, the script runs **`git add --`** on exactly the paths from **`git diff --name-only HEAD`** (release-only edits: pin files, **`CHANGELOG.md`**, etc.)—never **`git add -A`**—then **`git commit -m "chore(release): vX.Y.Z"`**. Without **`--commit`**, stage those same paths yourself (again: only **`git diff --name-only`**, not the whole tree), then commit. This runs **`bump-my-version`** using **`.bumpversion.toml`**, updating **`STANDARDS_VERSION`**, **`current_version`** in that config, and every listed **`@v…`** / example pin file **except** **`CHANGELOG.md`**. The script then runs **`scripts/finalize_standards_changelog.py`**, which reads the new version from **`STANDARDS_VERSION`** and moves the **`[Unreleased]`** body into **`## [X.Y.Z] - YYYY-MM-DD`** (today’s date by default). Set **`CHANGELOG_DATE=YYYY-MM-DD`** to override the date, or **`CHANGELOG_ALLOW_EMPTY=1`** to allow an empty **`[Unreleased]`** body. Arguments other than **`--commit`** are forwarded to **`bump-my-version bump`** (for example **`--dry-run`**); **`--commit`** is not passed through.

3. **Tag / push** — Create the annotated tag and push **`main`** + tag (see the manual checklist below). If you used **`--commit`**, the script prints the suggested **`git tag`** / **`git push`** line after the commit.

4. **GitHub Release** — Same as step 6 below (tag push triggers **`release-on-tag.yml`** when applicable).

**Tooling:** Prefer **`uv run --with bump-my-version==1.3.0 …`** so no project virtualenv is required; otherwise install **`bump-my-version==1.3.0`** and ensure **`bump-my-version`** is on **`PATH`**. If **`bump-my-version`** crashes on macOS, set **`BUMP_MY_VERSION_PYTHON=3.12`** (see [Troubleshooting](#troubleshooting-bump-my-version-on-macos) below). If you truly must bump with unrelated local edits, pass **`--allow-dirty`** through to **`bump-my-version bump`** (advanced; not recommended).

### Manual checklist

1. **Changelog**  
   - Move items from `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section (or fold into the version you are cutting).  
   - Leave `## [Unreleased]` empty or remove subsection bullets until the next change.

2. **Version file**  
   - Set root **`STANDARDS_VERSION`** to **`X.Y.Z`** (no `v`), and keep **`.bumpversion.toml`** **`current_version`** in sync if you use the automated bump config.

3. **Commit**  
   - One commit for the release prep, for example: `chore(release): v2.0.0`.

4. **Tag**  
   - Create an annotated tag: `git tag -a vX.Y.Z -m "vX.Y.Z"`  
   - Light tags are acceptable if your org standardizes on them; annotated tags carry the message on `git show`.

5. **Push**  
   - `git push origin main` and `git push origin vX.Y.Z` (or push all tags).

6. **GitHub Release**  
   - **Automated (default):** pushing a SemVer tag matching **`v*.*.*`** (for example **`v4.3.1`**) runs [`.github/workflows/release-on-tag.yml`](../.github/workflows/release-on-tag.yml), which calls **`scripts/publish_github_release.py`** with **`GITHUB_REF_NAME`**. The script reads the matching **`## [X.Y.Z]`** block from **`CHANGELOG.md`** and runs **`gh release create`** with **`--verify-tag`** using the workflow token.  
   - **Local (optional):** with **`gh`** installed and **`gh auth login`**, and **`vX.Y.Z`** already on **`origin`**: **`python3 scripts/publish_github_release.py`** (uses **`STANDARDS_VERSION`** if you omit the version). Supports **`--draft`**, **`--dry-run`**.  
   - **Manual:** **Releases → Draft a new release → Choose tag `vX.Y.Z`**, paste the **`CHANGELOG.md`** section if you skip automation.

**Frequency:** Cut a release when there is something adopters should **intentionally** pick up—not necessarily for every doc typo. Batch small doc fixes into the next **PATCH** or **MINOR** as appropriate.

**Template sync:** After changing **`scripts/verify-standards.sh`**, copy it to **`templates/scripts/verify-standards.sh`** before tagging so the template bundle matches the canonical script. Do the same for **`scripts/check_lint_baseline.py`** → **`templates/scripts/check_lint_baseline.py`**.

**Lint baselines:** If you change **`templates/baselines/ruff.toml`** or **`templates/baselines/expected-mypy.json`**, recompute each file’s SHA-256 and update the matching line in **`templates/baselines/DIGESTS`** (paths are relative to the consumer repo root, e.g. **`baselines/ruff.toml`**). If org Mypy defaults change, update **`expected-mypy.json`** and the **`[tool.mypy]`** section in **`templates/pyproject/pyproject.toml`** together so **`check_lint_baseline.py`** stays consistent.

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
