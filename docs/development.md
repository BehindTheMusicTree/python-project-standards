# Organization Python development baseline

This document is the **entry point** for cross-repository Python standards maintained in [python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards). Consumer repositories (libraries, APIs, services) should link here for shared policy; **framework-specific** or **product-specific** guides (for example Django patterns in an API repo) stay in each project’s own `DEVELOPMENT.md` or `CONTRIBUTING.md`.

## Table of Contents

- [What lives in python-project-standards](#what-lives-in-python-project-standards)
- [Python style (shared)](#python-style-shared)
- [Tooling and layout](#tooling-and-layout)
- [Cursor / AI assistant rules (`.cursor/rules`)](#cursor--ai-assistant-rules-cursorrules)

## What lives in python-project-standards

- **Repository overview** — purpose, adoption tiers (library vs service/API), quick start: [README](../README.md).
- **Adopting the baseline in an existing repo** — templates vs callable workflows, copying files, `STANDARDS_VERSION`: [migration-guide.md](migration-guide.md).
- **Versioning and releases** — SemVer tags, pinning `@v…` vs SHA, consumer bumps: [versioning.md](versioning.md).
- **Reusable GitHub Actions** — `reusable-pre-commit.yml`, inputs and examples: [reusable-workflows.md](reusable-workflows.md).

## Python style (shared)

- **String enumerations** — use `StrEnum`, not `(str, Enum)`: [string-enums.md](string-enums.md).

Further style rules may be added under `docs/` over time; this page will link them.

## Tooling and layout

Baseline **pre-commit**, **`pyproject.toml`** tooling sections, vendored **`baselines/`** (Ruff rules + digest, Mypy expectation JSON), **templates**, and optional **Cursor** rules are described in the [README](../README.md) (**Repository layout**, **What Is Standardized**, **Quick Start**). Repositories run **`scripts/verify-standards.sh`** (from templates) via the **`verify-python-project-standards`** hook where applicable; that script invokes **`scripts/check_lint_baseline.py`** unless **`VERIFY_STANDARDS_SKIP_LINT_BASELINE=1`** (see [migration-guide.md](migration-guide.md)).

## Cursor / AI assistant rules (`.cursor/rules`)

**`templates/cursor-rules/*.mdc`** are **optional copies** for consumer repositories. They are not fetched automatically: each repo should **`cp`** (or merge) the baseline files it wants into **`.cursor/rules/`**, alongside **project-specific** rules (Django conventions, test layout, etc.).

- **Do copy** org baselines you adopt (dependency pinning, `StrEnum`, commit messages, changelog alignment for agents, etc.) so editors and agents match the same policy as CI.
- **Do not** treat the template directory as a submodule; **re-copy or diff** when you bump **`STANDARDS_VERSION`** so local rules stay aligned.
- **python-project-standards** keeps **`.cursor/rules/`** in lockstep with **`templates/cursor-rules/*.mdc`** (same rules for maintainers; templates use absolute GitHub links where useful for copy-paste consumers, while **`.cursor/rules/strenum-string-enums.mdc`** points at **`docs/`** with repo-relative paths). String enums policy is also in **[string-enums.md](string-enums.md)**.
