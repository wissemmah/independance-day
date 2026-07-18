"""
Persistance : scores, cles, settings, achievements.
"""
import json
import os
import time

from chemins import writable_data_dir
from constantes import CONTROLES_DEFAUT, ACHIEVEMENTS


def _save_path():
    return os.path.join(writable_data_dir(), "highscore.json")


def _defaut():
    return {
        "high_score": 0,
        "leaderboard": [],
        "cles": [],
        "niveau_infini_debloque": False,
        "tutoriel_vu": False,
        "achievements": [],
        "settings": {
            "volume_musique": 0.5,
            "volume_effets": 0.7,
            "musique_active": True,
            "effets_actifs": True,
            "controles": dict(CONTROLES_DEFAUT),
        },
    }


def charger_progression():
    path = _save_path()
    data = _defaut()
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return data

    data["high_score"] = int(raw.get("high_score", 0))
    data["cles"] = list(raw.get("cles", []))
    data["niveau_infini_debloque"] = bool(raw.get("niveau_infini_debloque", False))
    data["tutoriel_vu"] = bool(raw.get("tutoriel_vu", False))
    data["achievements"] = list(raw.get("achievements", []))
    lb = raw.get("leaderboard", [])
    if isinstance(lb, list):
        data["leaderboard"] = [
            {"score": int(e.get("score", 0)), "date": str(e.get("date", ""))}
            for e in lb
            if isinstance(e, dict)
        ][:5]
    settings = raw.get("settings", {})
    if isinstance(settings, dict):
        data["settings"]["volume_musique"] = float(settings.get("volume_musique", 0.5))
        data["settings"]["volume_effets"] = float(settings.get("volume_effets", 0.7))
        data["settings"]["musique_active"] = bool(settings.get("musique_active", True))
        data["settings"]["effets_actifs"] = bool(settings.get("effets_actifs", True))
        ctrls = settings.get("controles", {})
        merged = dict(CONTROLES_DEFAUT)
        if isinstance(ctrls, dict):
            for k, v in ctrls.items():
                if k in merged:
                    try:
                        merged[k] = int(v)
                    except (TypeError, ValueError):
                        pass
        data["settings"]["controles"] = merged
    if data["high_score"] and not data["leaderboard"]:
        data["leaderboard"] = [{"score": data["high_score"], "date": ""}]
    return data


def sauvegarder_tout(etat):
    """etat = dict complet retourné/mis à jour par le jeu."""
    path = _save_path()
    payload = {
        "high_score": int(etat.get("high_score", 0)),
        "leaderboard": etat.get("leaderboard", [])[:5],
        "cles": sorted(int(c) for c in etat.get("cles", [])),
        "niveau_infini_debloque": bool(etat.get("niveau_infini_debloque", False)),
        "tutoriel_vu": bool(etat.get("tutoriel_vu", False)),
        "achievements": list(etat.get("achievements", [])),
        "settings": etat.get("settings", _defaut()["settings"]),
    }
    # serialiser controles en int
    ctrls = payload["settings"].get("controles", {})
    payload["settings"]["controles"] = {k: int(v) for k, v in ctrls.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def ajouter_score_leaderboard(leaderboard, score, top_n=5):
    entry = {"score": int(score), "date": time.strftime("%Y-%m-%d")}
    board = list(leaderboard) + [entry]
    board.sort(key=lambda e: e["score"], reverse=True)
    return board[:top_n]


def debloquer_achievement(unlocked, cle):
    if cle not in ACHIEVEMENTS:
        return unlocked, None
    if cle in unlocked:
        return unlocked, None
    nouveaux = list(unlocked) + [cle]
    return nouveaux, ACHIEVEMENTS[cle]
