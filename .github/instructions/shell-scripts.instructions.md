---
applyTo: "scripts/**/*.sh,scripts/**/*.py"
---

# Copilot code review: shell scripts

- Prefer **`#!/usr/bin/env bash`** with **`set -euo pipefail`** for new or heavily edited scripts.
- **`scripts/publish_github_release.py`** is maintainer-only: keep it working with **`CHANGELOG.md`** section headers **`## [X.Y.Z]`** and **`gh release create`**.
- Use portable patterns where reasonable. Avoid introducing dependencies on nonstandard tools without documenting them.
