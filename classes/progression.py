"""
Persistance progression (high score, clés).
"""
import json
import os

from chemins import writable_data_dir


def _assurer_dossier():
    return writable_data_dir()


def _highscore_path():
    return os.path.join(writable_data_dir(), "highscore.json")


def charger_progression():
    """Charge high score et clés débloquées. Retourne un dict sûr."""
    path = _highscore_path()
    defaut = {"high_score": 0, "cles": [], "niveau_infini_debloque": False}
    if not os.path.exists(path):
        return defaut
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "high_score": int(data.get("high_score", 0)),
            "cles": list(data.get("cles", [])),
            "niveau_infini_debloque": bool(data.get("niveau_infini_debloque", False)),
        }
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return defaut


def sauvegarder_progression(high_score, cles, niveau_infini_debloque):
    """Écrit la progression sur disque."""
    path = _highscore_path()
    payload = {
        "high_score": int(high_score),
        "cles": sorted(int(c) for c in cles),
        "niveau_infini_debloque": bool(niveau_infini_debloque),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
