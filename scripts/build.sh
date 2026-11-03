#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -n "${CV_PYTHON:-}" ]]; then
  PYTHON_BIN="$CV_PYTHON"
elif [[ -x "$WORKFLOW_ROOT/.venv/bin/python" ]]; then
  PYTHON_BIN="$WORKFLOW_ROOT/.venv/bin/python"
elif [[ -x "$WORKFLOW_ROOT/venv/bin/python" ]]; then
  PYTHON_BIN="$WORKFLOW_ROOT/venv/bin/python"
elif [[ -x "$WORKFLOW_ROOT/../venv/bin/python" ]]; then
  PYTHON_BIN="$WORKFLOW_ROOT/../venv/bin/python"
else
  PYTHON_BIN="python3"
fi

usage() {
  cat <<'EOF'
Usage:
  ./scripts/build.sh <target> [--public-header] [--publish]
  ./scripts/build.sh --list
  ./scripts/build.sh --help

Common targets:
  baseline               Build the single universal CV baseline (versions/cv/baseline/resume-baseline.tex)
  resume-base            Build the base demo resume (versions/cv/base/resume-base.tex)
  letter-placeholder     Build the 5-paragraph placeholder cover letter
  resume:<id|slug>       Build a targeted resume registered in targets/<slug>/metadata.yaml
  letter:<id|slug>       Build a targeted cover letter registered in targets/<slug>/metadata.yaml

Flags:
  --public-header        Compile in a temporary staging tree using header.template.tex
  --publish              Publish verified PDF to output/cv/ or output/cover-letters/pdf/ (refuses to overwrite targeted snapshots)
EOF
}

if [[ $# -eq 0 ]]; then
  usage >&2
  "$PYTHON_BIN" "$WORKFLOW_ROOT/scripts/workspace.py" list >&2
  exit 1
fi

case "$1" in
  -h|--help)
    usage
    exit 0
    ;;
  -l|--list)
    exec "$PYTHON_BIN" "$WORKFLOW_ROOT/scripts/workspace.py" list
    ;;
  *)
    exec "$PYTHON_BIN" "$WORKFLOW_ROOT/scripts/workspace.py" build "$@"
    ;;
esac
