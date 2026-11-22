#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 -m unittest -v
elif command -v python >/dev/null 2>&1; then
  exec python -m unittest -v
else
  echo 'Python 3.10+ is required.' >&2
  exit 1
fi
