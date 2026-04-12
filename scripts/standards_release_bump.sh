#!/usr/bin/env bash
# Bump STANDARDS_VERSION + example pins (bump-my-version), then fold CHANGELOG [Unreleased].
set -euo pipefail

usage() {
  echo "usage: $0 patch|minor|major [bump-my-version args...]" >&2
  echo "Optional env: CHANGELOG_DATE=YYYY-MM-DD, CHANGELOG_ALLOW_EMPTY=1 (passed to finalize script)." >&2
}

[[ "${1:-}" == patch || "${1:-}" == minor || "${1:-}" == major ]] || {
  usage
  exit 1
}
part="$1"
shift

root="$(git rev-parse --show-toplevel)"
cd "$root"

if command -v uv >/dev/null 2>&1; then
  uv run --with bump-my-version==1.3.0 bump-my-version bump "$part" "$@"
else
  bump-my-version bump "$part" "$@"
fi

py=(python3 "$root/scripts/finalize_standards_changelog.py")
[[ -n "${CHANGELOG_DATE:-}" ]] && py+=(--date "$CHANGELOG_DATE")
[[ -n "${CHANGELOG_ALLOW_EMPTY:-}" ]] && py+=(--allow-empty)
"${py[@]}"

ver="$(tr -d '[:space:]' <"$root/STANDARDS_VERSION")"
printf '%s\n' "Next: review diff, then git add -A && git commit -m \"chore(release): v${ver}\" && git tag -a \"v${ver}\" -m \"v${ver}\" && git push origin main && git push origin \"v${ver}\""
