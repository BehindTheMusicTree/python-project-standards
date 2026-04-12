#!/usr/bin/env bash
# Bump STANDARDS_VERSION + example pins (bump-my-version), then fold CHANGELOG [Unreleased].
set -euo pipefail

usage() {
  echo "usage: $0 patch|minor|major [--commit] [bump-my-version args...]" >&2
  echo "  Requires a clean git working tree (matches .bumpversion.toml allow_dirty = false)." >&2
  echo "  --commit  after bump + finalize, git add only files changed since HEAD, then commit chore(release): vX.Y.Z" >&2
  echo "Optional env: CHANGELOG_DATE=YYYY-MM-DD, CHANGELOG_ALLOW_EMPTY=1 (passed to finalize script)." >&2
}

[[ "${1:-}" == patch || "${1:-}" == minor || "${1:-}" == major ]] || {
  usage
  exit 1
}

part="$1"
shift

commit_release=false
bump_args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit)
      commit_release=true
      shift
      ;;
    *)
      bump_args+=("$1")
      shift
      ;;
  esac
done

root="$(git rev-parse --show-toplevel)"
cd "$root"

if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
  echo "error: git working tree is not clean (see git status)." >&2
  echo "  Commit or stash your edits first so bump-my-version matches allow_dirty = false." >&2
  echo "  Tip: commit your ## [Unreleased] draft, then run this script." >&2
  exit 1
fi

dry_run=false
for a in "${bump_args[@]}"; do
  if [[ "$a" == "--dry-run" ]]; then
    dry_run=true
    break
  fi
done

if command -v uv >/dev/null 2>&1; then
  uv run --with bump-my-version==1.3.0 bump-my-version bump "$part" "${bump_args[@]}"
else
  bump-my-version bump "$part" "${bump_args[@]}"
fi

py=(python3 "$root/scripts/finalize_standards_changelog.py")
[[ -n "${CHANGELOG_DATE:-}" ]] && py+=(--date "$CHANGELOG_DATE")
[[ -n "${CHANGELOG_ALLOW_EMPTY:-}" ]] && py+=(--allow-empty)
"${py[@]}"

ver="$(tr -d '[:space:]' <"$root/STANDARDS_VERSION")"

if [[ "$commit_release" == true ]]; then
  if [[ "$dry_run" == true ]]; then
    echo "Skipping --commit because bump-my-version was run with --dry-run."
  else
    changed=()
    while IFS= read -r line; do
      [[ -n "$line" ]] && changed+=("$line")
    done < <(git diff --name-only HEAD)

    if [[ ${#changed[@]} -eq 0 ]]; then
      echo "error: no modified files after bump + finalize; nothing to commit." >&2
      exit 1
    fi

    git add -- "${changed[@]}"
    git commit -m "chore(release): v${ver}"
    printf '%s\n' "Committed release-only paths: ${changed[*]}"
    printf '%s\n' "Next: git tag -a \"v${ver}\" -m \"v${ver}\" && git push origin main && git push origin \"v${ver}\""
  fi
else
  printf '%s\n' "Next: review git diff; stage only release files (paths from: git diff --name-only HEAD), then:"
  printf '%s\n' "  git commit -m \"chore(release): v${ver}\" && git tag -a \"v${ver}\" -m \"v${ver}\" && git push origin main && git push origin \"v${ver}\""
  printf '%s\n' "Tip: pass --commit on this script to create that commit automatically (same paths only, never git add -A)."
fi
