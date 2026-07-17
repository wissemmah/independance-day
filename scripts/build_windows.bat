@echo off
REM Build Windows folder + zip (a lancer sur Windows)
setlocal
cd /d "%~dp0\.."

set NAME=IndependenceDay
set DIST=dist

python -m pip install -q -r requirements.txt -r requirements-build.txt
python -m PyInstaller --noconfirm --clean IndependenceDay.spec

if not exist "%DIST%\%NAME%\%NAME%.exe" (
  echo Erreur: exe introuvable
  exit /b 1
)

powershell -Command "Compress-Archive -Path '%DIST%\%NAME%\*' -DestinationPath '%DIST%\%NAME%-Windows.zip' -Force"
echo.
echo OK — ZIP: %DIST%\%NAME%-Windows.zip
dir "%DIST%\%NAME%-Windows.zip"
endlocal
