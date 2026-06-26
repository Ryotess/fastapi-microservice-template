#!/usr/bin/env bash
set -euo pipefail

IFS=$'\n\t'

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
scaffold_dir="$repo_root/templates/feature_scaffold"

feature_name="${1:-}"

if [[ -z "$feature_name" ]]; then
  echo "Usage: bash scripts/new_feature.sh <feature_name>"
  echo "Example: bash scripts/new_feature.sh users"
  exit 1
fi

if [[ ! "$feature_name" =~ ^[a-z][a-z0-9_]*$ ]]; then
  echo "Invalid feature name: '$feature_name'"
  echo "Use snake_case starting with a letter, e.g. users or payment_events"
  exit 1
fi

if [[ ! -d "$scaffold_dir" ]]; then
  echo "Feature scaffold directory not found: $scaffold_dir"
  exit 1
fi

target_dir="$repo_root/src/$feature_name"
if [[ -e "$target_dir" ]]; then
  echo "Target already exists: $target_dir"
  exit 1
fi

test_dir="$repo_root/tests/$feature_name"
if [[ -e "$test_dir" ]]; then
  echo "Test target already exists: $test_dir"
  exit 1
fi

mkdir -p "$target_dir" "$test_dir"
cp -R "$scaffold_dir"/. "$target_dir"/
touch "$test_dir/.gitkeep"

feature_prefix="$(printf '%s' "$feature_name" | tr '[:lower:]' '[:upper:]')_"

echo "Created feature scaffold: src/$feature_name"
echo "Created feature test scaffold: tests/$feature_name"
echo "Next steps:"
echo "  1) Implement schemas, service logic, and routes in src/$feature_name/"
echo "  2) Register the feature router in src/main.py"
echo "  3) Add tests in tests/$feature_name/"
echo "  4) Add feature env vars to root .env using a feature prefix (e.g. $feature_prefix)"
