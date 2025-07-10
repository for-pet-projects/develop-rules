#!/bin/bash

set -e

# 1. Find the git repository root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT" || {
  echo "[ERR] Failed to enter git root: $PROJECT_ROOT"
  exit 1
}

# 2. Paths
VENV_DIR="$PROJECT_ROOT/venv"
REQ_FILE="$PROJECT_ROOT/release/requirements.txt"

# 3. Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "[INI] Creating virtualenv..."
  python3 -m venv "$VENV_DIR"
fi

# 4. Activate venv
source "$VENV_DIR/bin/activate"

# 5. Install dependencies
if [ -f "$REQ_FILE" ]; then
  echo "[INI] Installing dependencies..."
  pip install --upgrade pip > /dev/null
  pip install -r "$REQ_FILE" -qq 
else
  echo "[WRN] No requirements.txt found: $REQ_FILE"
fi

# 6. Run run.py with proper PYTHONPATH
PYTHONPATH="$PROJECT_ROOT" python3 "$PROJECT_ROOT/release/run.py" "$@"
