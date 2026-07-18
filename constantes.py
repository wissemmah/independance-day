"""
Constantes du jeu Independence Day
"""
import pygame

# --- Dimensions (Format 16:9) ---
LARGEUR_JEU = 1280
HAUTEUR_JEU = 720
FPS = 60

# --- Couleurs ---
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
VERT_MILITAIRE = (46, 139, 87)
GRIS_FONCE = (50, 50, 50)
GRIS_TORNADE_PETITE = (180, 180, 180)
GRIS_TORNADE_MOYENNE = (120, 100, 100)
GRIS_TORNADE_GROSSE = (80, 50, 50)
JAUNE = (255, 255, 0)
ROUGE = (255, 0, 0)
ROUGE_SANG = (180, 0, 0)
ORANGE = (255, 165, 0)
OR = (255, 215, 0)
BLEU_NUIT = (20, 20, 60)
BLEU_BOUCLIER = (0, 191, 255)
BLEU = (15, 32, 74)
BLEU_FONCE = (10, 20, 50)
CYAN = (0, 255, 255)
VIOLET = (180, 80, 255)

# --- Gameplay / équilibrage ---
DUREE_NIVEAU_SEC = 75
COMBO_FENETRE_MS = 1800
HITSTOP_FRAMES_KILL = 3
HITSTOP_FRAMES_BOSS_HIT = 2
FLASH_KILL_ALPHA = 90

OBJECTIFS_KILLS = {
    1: 14,
    2: 16,
    3: 12,
}

SPAWN_CONFIG = {
    1: {"max": 3, "delay": 950},
    2: {"max": 3, "delay": 850},
    3: {"max": 4, "delay": 1050},
}

POWERUP_DROP_CHANCE = 0.12
POWERUP_DUREE_MS = 8000
BOSS_PV = 900

# Controles par defaut (remappables)
CONTROLES_DEFAUT = {
    "gauche": pygame.K_LEFT,
    "droite": pygame.K_RIGHT,
    "pause": pygame.K_ESCAPE,
    "nuke": pygame.K_b,
    "restart": pygame.K_r,
    "valider": pygame.K_SPACE,
}

ACHIEVEMENTS = {
    "cles_4": {"titre": "Collectionneur", "desc": "Recuperer les 4 cles"},
    "combo_10": {"titre": "Combo x10", "desc": "Atteindre un combo de 10"},
    "boss_sans_nuke": {"titre": "Puriste", "desc": "Battre le boss sans utiliser de nuke"},
    "score_5k": {"titre": "As du score", "desc": "Atteindre 5000 points"},
    "infini_5min": {"titre": "Survivant", "desc": "Survivre 5 min en mode infini"},
}
