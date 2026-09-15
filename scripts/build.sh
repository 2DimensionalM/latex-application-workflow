#!/usr/bin/env bash
set -euo pipefail
WORKFLOW_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKFLOW_PYTHON="${WORKFLOW_PYTHON:-python3}"
exec "$WORKFLOW_PYTHON" "$WORKFLOW_ROOT/scripts/workspace.py" build "$@"

