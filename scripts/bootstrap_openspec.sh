#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$project_root"
for command in node npm python3 git; do
  command -v "$command" >/dev/null || { echo "Нет команды: $command" >&2; exit 1; }
done
node -e 'if (+process.versions.node.split(".")[0] !== 24) { console.error("Нужен Node.js24.x"); process.exit(1); }'
python3 -c 'import sys; assert sys.version_info >= (3,9), "Нужен Python>=3.9 для проверок документов"'
export OPENSPEC_TELEMETRY=0
npm ci --ignore-scripts
npm run check
echo 'Готово. Codex: bash scripts/with-tools.sh codex'
