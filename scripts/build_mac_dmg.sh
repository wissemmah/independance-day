#!/usr/bin/env bash
# Build Mac .app + .dmg (à lancer sur macOS)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

NAME="IndependenceDay"
DIST="$ROOT/dist"
BUILD="$ROOT/build"
DMG_PATH="$DIST/${NAME}-macOS.dmg"
STAGE="$DIST/dmg_stage"

python3 -m pip install -q -r requirements.txt -r requirements-build.txt
python3 -m PyInstaller --noconfirm --clean IndependenceDay.spec

APP="$DIST/${NAME}.app"
if [[ ! -d "$APP" ]]; then
  echo "Erreur: $APP introuvable"
  exit 1
fi

rm -rf "$STAGE" "$DMG_PATH"
mkdir -p "$STAGE"
cp -R "$APP" "$STAGE/"
ln -s /Applications "$STAGE/Applications"

hdiutil create \
  -volname "Independence Day" \
  -srcfolder "$STAGE" \
  -ov -format UDZO \
  "$DMG_PATH"

rm -rf "$STAGE"
echo ""
echo "OK — DMG: $DMG_PATH"
ls -lh "$DMG_PATH"
