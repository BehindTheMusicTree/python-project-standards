#!/usr/bin/env bash
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/source"
cp "$root/copier.yml" "$tmp/source/"
cp -R "$root/template" "$tmp/source/"
copier copy --defaults --data package_name=demo "$tmp/source" "$tmp/default" >/dev/null
[[ ! -e "$tmp/default/AGENTS.md" ]]
copier copy --defaults --data package_name=demo --data agent_guidance=true "$tmp/source" "$tmp/enabled" >/dev/null
[[ -f "$tmp/enabled/AGENTS.md" && -f "$tmp/enabled/CLAUDE.md" ]]
python3 "$1" "$tmp/enabled"
actionlint "$tmp/enabled/.github/workflows/agent-drift.yml"
mkdir -p "$tmp/existing/.github/workflows"
printf 'existing agents\n' > "$tmp/existing/AGENTS.md"
printf 'existing claude\n' > "$tmp/existing/CLAUDE.md"
printf 'existing workflow\n' > "$tmp/existing/.github/workflows/agent-drift.yml"
copier copy --defaults --overwrite --data package_name=demo --data agent_guidance=true "$tmp/source" "$tmp/existing" >/dev/null
[[ "$(cat "$tmp/existing/AGENTS.md")" == 'existing agents' ]]
[[ "$(cat "$tmp/existing/CLAUDE.md")" == 'existing claude' ]]
[[ "$(cat "$tmp/existing/.github/workflows/agent-drift.yml")" == 'existing workflow' ]]
