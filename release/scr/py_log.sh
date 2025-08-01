#!/bin/bash

PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT" || {
  echo "[ERR] Failed to enter git root: $PROJECT_ROOT"
  exit 1
}

ROOT_DIR="release"
echo "Listing Python files and their contents under $ROOT_DIR"
echo "========================================"

find "$ROOT_DIR" -type f -name "*.py" | sort | while read -r file; do
  echo
  echo "===== FILE: $file ====="
  cat "$file"
done
