#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 launch.py
elif command -v python >/dev/null 2>&1; then
  exec python launch.py
else
  echo 'Python 3.10+ is required. Install Python and retry.' >&2
  exit 1
fi
