#!/usr/bin/env python3
"""Move CHANGELOG.md ## [Unreleased] body into ## [VERSION] using STANDARDS_VERSION."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_version(root: Path) -> str:
    raw = (root / "STANDARDS_VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", raw):
        print(f"STANDARDS_VERSION must be SemVer X.Y.Z (got {raw!r}).", file=sys.stderr)
        sys.exit(1)
    return raw


def _split_unreleased(lines: list[str]) -> tuple[int, int, str] | None:
    """Return (start_line_index, first_line_after_body, body_without_surrounding_blank_runs)."""
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## [Unreleased]"):
            start = i
            break
    if start is None:
        print("CHANGELOG.md: missing ## [Unreleased] section.", file=sys.stderr)
        sys.exit(1)

    j = None
    for k in range(start + 1, len(lines)):
        if lines[k].startswith("## [") and not lines[k].startswith("## [Unreleased]"):
            j = k
            break
    if j is None:
        j = len(lines)

    body_lines = lines[start + 1 : j]
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    while body_lines and body_lines[-1].strip() == "":
        body_lines.pop()

    body = "".join(body_lines).rstrip("\n")
    return start, j, body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Release date (default: today, local timezone).",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow an empty ## [Unreleased] body (creates a dated section with no subsections).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the new section only; do not write CHANGELOG.md.",
    )
    args = parser.parse_args()

    root = _repo_root()
    version = _read_version(root)
    changelog = root / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    start, j, body = _split_unreleased(lines)
    if not body.strip() and not args.allow_empty:
        print(
            "CHANGELOG.md: ## [Unreleased] has no release notes. "
            "Add bullets or pass --allow-empty.",
            file=sys.stderr,
        )
        sys.exit(1)

    header = f"## [{version}] - {args.date or date.today().isoformat()}\n"
    new_block = f"## [Unreleased]\n\n{header}\n"
    if body.strip():
        new_block += f"{body}\n\n"
    else:
        new_block += "\n"

    tail = "".join(lines[j:])
    if re.search(rf"^## \[{re.escape(version)}\]", tail, re.MULTILINE):
        print(f"CHANGELOG.md already contains ## [{version}] below [Unreleased].", file=sys.stderr)
        sys.exit(1)

    out_lines = lines[:start] + [new_block] + lines[j:]
    out = "".join(out_lines)

    if args.dry_run:
        print(new_block, end="")
        return

    changelog.write_text(out, encoding="utf-8", newline="\n")
    print(f"CHANGELOG.md: finalized [Unreleased] → [{version}].")


if __name__ == "__main__":
    main()
