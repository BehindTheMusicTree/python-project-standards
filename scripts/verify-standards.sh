#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /absolute/path/to/consumer-repo"
  exit 2
fi

repo_path="$1"

if [[ ! -d "$repo_path" ]]; then
  echo "Error: repo path not found: $repo_path"
  exit 2
fi

required_paths=(
  ".pre-commit-config.yaml"
  ".github/workflows/lint.yml"
  "pyproject.toml"
)

missing=0
for rel in "${required_paths[@]}"; do
  if [[ ! -f "$repo_path/$rel" ]]; then
    echo "Missing required file: $rel"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Standards verification failed."
  exit 1
fi

contains_or_fail() {
  local file="$1"
  local pattern="$2"
  local label="$3"

  if ! rg --quiet --fixed-strings "$pattern" "$file"; then
    echo "Missing required snippet in $label: $pattern"
    return 1
  fi
}

snippet_fail=0

contains_or_fail "$repo_path/.pre-commit-config.yaml" "https://github.com/pre-commit/pre-commit-hooks" ".pre-commit-config.yaml" || snippet_fail=1
contains_or_fail "$repo_path/.pre-commit-config.yaml" "https://github.com/astral-sh/ruff-pre-commit" ".pre-commit-config.yaml" || snippet_fail=1
contains_or_fail "$repo_path/.pre-commit-config.yaml" "https://github.com/pre-commit/mirrors-mypy" ".pre-commit-config.yaml" || snippet_fail=1

contains_or_fail "$repo_path/pyproject.toml" "[tool.ruff]" "pyproject.toml" || snippet_fail=1
contains_or_fail "$repo_path/pyproject.toml" "[tool.mypy]" "pyproject.toml" || snippet_fail=1
contains_or_fail "$repo_path/pyproject.toml" "[tool.pytest.ini_options]" "pyproject.toml" || snippet_fail=1

contains_or_fail "$repo_path/.github/workflows/lint.yml" "pre-commit run --all-files" ".github/workflows/lint.yml" || snippet_fail=1

if [[ $snippet_fail -ne 0 ]]; then
  echo "Standards verification failed due to missing required snippets."
  exit 1
fi

if [[ ! -f "$repo_path/STANDARDS_VERSION" ]]; then
  echo "Missing recommended file: STANDARDS_VERSION"
else
  echo "Found STANDARDS_VERSION: $(<"$repo_path/STANDARDS_VERSION")"
fi

echo "Standards verification passed."
