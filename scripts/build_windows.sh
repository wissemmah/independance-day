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

# Zip via Python (chemins bash/Git Bash + PowerShell OK)
python - <<'PY'
import zipfile
from pathlib import Path

root = Path("dist") / "IndependenceDay"
out = Path("dist") / "IndependenceDay-Windows.zip"
if out.exists():
    out.unlink()
with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in root.rglob("*"):
        if path.is_file():
            zf.write(path, path.relative_to(root).as_posix())
print(f"OK — ZIP: {out.resolve()} ({out.stat().st_size // (1024*1024)} Mo)")
PY
