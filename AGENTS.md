# Python project standards

This repository owns the Copier template, reusable workflows and shared Python standards. Read `README.md` and `docs/development.md` for the current contract; there is no root Python package. Follow the actual Copier update and release procedures when changing templates or versions.

For substantive changes read `.agents/rules/changelog-alignment.md`. For commits read `.agents/rules/commit-message-convention.md`; for dependencies read `.agents/rules/dependency-pinning.md`; for PRs read `.agents/rules/pr-description-workflow.md`. For Python string enums read `.agents/rules/strenum-string-enums.md` and `docs/string-enums.md`.

Before changing `**/*.md`, read `.agents/rules/documentation-toc.md`.

Before changing `template/**/*` or `copier.yml`, read `.agents/rules/copier-template.md`. Before changing `.github/workflows/**/*.yml`, `.github/workflows/**/*.yaml` or `template/.github/workflows/**`, read `.agents/rules/github-actions.md`. Before changing `docs/**/*.md`, `README.md` or `CHANGELOG.md`, read `.agents/rules/markdown-documentation.md`. Before changing `scripts/**/*.sh` or `scripts/**/*.py`, read `.agents/rules/shell-scripts.md`.

If graphify is installed and a graph exists, it may help explore the repository; keep it current when relevant.

## Repository review focus

This repository is an organization-wide standards and template bundle, not an installable application: there is no root `pyproject.toml`. Consumers render the Copier template (`copier.yml`, `template/`) and call the reusable workflows in `.github/workflows/`.

- Pinning: workflow `uses:` lines and documented examples use release tags (`@vX.Y.Z`) or commit SHAs, never long-lived `@main`.
- Consumer guidance: changes to `template/` stay consistent with `docs/development.md`, `docs/reusable-workflows.md` and `README.md`.
- Reusable workflow contract: `.github/workflows/reusable-pre-commit.yml` is a public API; input renames, default changes or step removals are breaking unless documented in `CHANGELOG.md`.
- Validate: `copier copy --vcs-ref HEAD . "$TMPDIR/demo" --defaults --data package_name=demo && cd "$TMPDIR/demo" && git init -q && git add -A && pre-commit run --all-files`.
- Python policy follows `docs/string-enums.md` (`StrEnum`, not `(str, Enum)`), `template/baselines/ruff.toml` (`UP` selected) and strict mypy plus pytest-cov in `template/pyproject.toml.jinja`; tools and pre-commit `rev:` stay pinned.
- `README.md` and `docs/development.md` are the source of truth.
