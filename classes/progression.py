"""
Persistance progression (high score, clés).
"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HIGHSCORE_PATH = os.path.join(DATA_DIR, "highscore.json")


def _assurer_dossier():
    os.makedirs(DATA_DIR, exist_ok=True)


def charger_progression():
    """Charge high score et clés débloquées. Retourne un dict sûr."""
    _assurer_dossier()
    defaut = {"high_score": 0, "cles": [], "niveau_infini_debloque": False}
    if not os.path.exists(HIGHSCORE_PATH):
        return defaut
    try:
        with open(HIGHSCORE_PATH, "r", encoding="utf-8") as f:
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
    _assurer_dossier()
    payload = {
        "high_score": int(high_score),
        "cles": sorted(int(c) for c in cles),
        "niveau_infini_debloque": bool(niveau_infini_debloque),
    }
    with open(HIGHSCORE_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
