#!/usr/bin/env bash
# Runs the Budget Buddy test suite with a coverage report.
set -euo pipefail

if [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="python"
fi

"$PYTHON" -m pytest --cov=. --cov-report=term-missing
