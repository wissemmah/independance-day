# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — Independence Day (onedir, windowed)."""
import sys
from pathlib import Path

ROOT = Path(SPECPATH).resolve()
NAME = "IndependenceDay"

datas = [
    (str(ROOT / "assets"), "assets"),
]

hiddenimports = [
    "pygame",
    "cv2",
    "chemins",
    "constantes",
    "utils",
    "classes",
    "classes.jeu",
    "classes.rendu",
    "classes.update_jeu",
    "classes.gestion_entrees",
    "classes.ennemis",
    "classes.soldat",
    "classes.boss",
    "classes.items",
    "classes.projectiles",
    "classes.vfx",
    "classes.gestionnaire_musique",
    "classes.progression",
    "classes.Niveau_infini",
    "classes.lecteur_video",
    "classes.audio_intro",
    "classes.bouton",
]

a = Analysis(
    [str(ROOT / "Main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=NAME,
)

# macOS .app bundle
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name=f"{NAME}.app",
        icon=None,
        bundle_identifier="com.wissemmah.independenceday",
        info_plist={
            "CFBundleDisplayName": "Independence Day",
            "CFBundleName": "IndependenceDay",
            "NSHighResolutionCapable": True,
            "LSBackgroundOnly": False,
        },
    )
