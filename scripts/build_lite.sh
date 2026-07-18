#!/usr/bin/env bash
# Build lite (sans videos) — Mac DMG
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export ID_LITE=1
bash scripts/build_mac_dmg.sh
# Renomme le dmg
if [[ -f dist/IndependenceDay-macOS.dmg ]]; then
  mv -f dist/IndependenceDay-macOS.dmg dist/IndependenceDay-Lite-macOS.dmg
  echo "OK — $ROOT/dist/IndependenceDay-Lite-macOS.dmg"
fi
