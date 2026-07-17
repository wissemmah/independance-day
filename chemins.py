"""
Résolution des chemins (dev + binaire PyInstaller).
"""
import os
import sys


def resource_root():
    """Racine des assets (dossier projet ou _MEIPASS si gelé)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def asset_path(*parts):
    """Chemin vers un fichier sous assets/."""
    return os.path.join(resource_root(), "assets", *parts)


def writable_data_dir():
    """Dossier writable pour high score (hors bundle en mode gelé)."""
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            base = os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Application Support",
                "IndependenceDay",
            )
        elif os.name == "nt":
            base = os.path.join(
                os.environ.get("APPDATA", os.path.expanduser("~")),
                "IndependenceDay",
            )
        else:
            base = os.path.join(os.path.expanduser("~"), ".independence_day")
        os.makedirs(base, exist_ok=True)
        return base
    path = os.path.join(resource_root(), "data")
    os.makedirs(path, exist_ok=True)
    return path


def is_frozen():
    return bool(getattr(sys, "frozen", False))
