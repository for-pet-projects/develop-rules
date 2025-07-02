#!/bin/bash

ROOT_DIR="release"  # можно заменить на нужную директорию
echo "Listing Python files and their contents under $ROOT_DIR"
echo "========================================"

find "$ROOT_DIR" -type f -name "*.py" | sort | while read -r file; do
  echo
  echo "===== FILE: $file ====="
  cat "$file"
done
