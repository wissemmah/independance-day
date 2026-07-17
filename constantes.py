"""
Constantes du jeu Independence Day
"""

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

# --- Gameplay / équilibrage ---
DUREE_NIVEAU_SEC = 60
COMBO_FENETRE_MS = 1800

# Objectif de kills pour terminer un niveau avant la fin du timer (niveaux 1-3)
OBJECTIFS_KILLS = {
    1: 12,
    2: 15,
    3: 10,
}

# Spawn par niveau : max ennemis simultanés + délai entre spawns (ms)
SPAWN_CONFIG = {
    1: {"max": 3, "delay": 900},
    2: {"max": 3, "delay": 800},
    3: {"max": 4, "delay": 1100},
}
