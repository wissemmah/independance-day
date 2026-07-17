#!/usr/bin/env bash
# Build Windows onedir + zip (GitHub Actions / Windows shell)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

NAME="IndependenceDay"
DIST="$ROOT/dist"

python -m pip install -q -r requirements.txt -r requirements-build.txt
python -m PyInstaller --noconfirm --clean IndependenceDay.spec

EXE="$DIST/${NAME}/${NAME}.exe"
if [[ ! -f "$EXE" ]]; then
  echo "Erreur: $EXE introuvable"
  exit 1
fi

# Prefer PowerShell Compress-Archive on Windows runners
if command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -Command "Compress-Archive -Path '${DIST}/${NAME}/*' -DestinationPath '${DIST}/${NAME}-Windows.zip' -Force"
elif command -v zip >/dev/null 2>&1; then
  (cd "$DIST/$NAME" && zip -r "../${NAME}-Windows.zip" .)
else
  echo "Aucun outil zip trouvé"
  exit 1
fi

echo "OK — ZIP: $DIST/${NAME}-Windows.zip"
ls -lh "$DIST/${NAME}-Windows.zip"
