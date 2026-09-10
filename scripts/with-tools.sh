#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
[[ -x "$project_root/node_modules/.bin/openspec" ]] || { echo 'Сначала npm ci --ignore-scripts в корне проекта' >&2; exit 1; }
[[ $# -gt 0 ]] || { echo 'Использование: bash scripts/with-tools.sh <команда> [аргументы]' >&2; exit 2; }
export PATH="$project_root/node_modules/.bin:$PATH"
export OPENSPEC_TELEMETRY=0
cd -- "$project_root"
exec "$@"
