# Organization Python development baseline

This document is the **entry point** for cross-repository Python standards maintained in [python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards). Consumer repositories (libraries, APIs, services) should link here for shared policy; **framework-specific** or **product-specific** guides (for example Django patterns in an API repo) stay in each project’s own `DEVELOPMENT.md` or `CONTRIBUTING.md`.

## Table of Contents

- [What lives in python-project-standards](#what-lives-in-python-project-standards)
- [Python style (shared)](#python-style-shared)
- [Tooling and layout](#tooling-and-layout)
- [Portable agent guidance](#portable-agent-guidance)

## What lives in python-project-standards

- **Repository overview** — purpose, adoption tiers (library vs service/API), quick start: [README](../README.md).
- **Adopting the baseline in an existing repo** — Copier template vs callable workflows, `copier copy` / `copier update`: [migration-guide.md](migration-guide.md).
- **Versioning and releases** — SemVer tags, pinning `@v…` vs SHA, consumer bumps: [versioning.md](versioning.md).
- **Reusable GitHub Actions** — `reusable-pre-commit.yml`, inputs and examples: [reusable-workflows.md](reusable-workflows.md).

## Python style (shared)

- **String enumerations** — use `StrEnum`, not `(str, Enum)`: [string-enums.md](string-enums.md).

Further style rules may be added under `docs/` over time; this page will link them.

## Tooling and layout

Baseline **pre-commit**, **`pyproject.toml`** tooling sections and **`baselines/ruff.toml`** ship as a **Copier template** ([`template/`](../template/), [`copier.yml`](../copier.yml)), described in the [README](../README.md) (**Repository layout**, **What Is Standardized**, **Quick Start**) and [migration-guide.md](migration-guide.md).

## Portable agent guidance

Projects may opt in to the Copier `agent_guidance` question to bootstrap `AGENTS.md`, its Claude import, and a drift-check workflow pinned to github-workflows `v4.8.0`. These are project-owned bootstrap files: existing files are preserved, and teams maintain them after creation. If existing instructions are present, reconcile them with the [agent-config project contract](https://github.com/BehindTheMusicTree/agent-config) before enabling the check. Shared Python style stays in these standards; architecture and operational commands stay in the consuming repository.
