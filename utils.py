"""
Fonctions utilitaires pour le jeu
"""
import pygame
import os
import math
from constantes import *


def charger_image_transparente(nom_fichier, taille):
    """Charge une image avec transparence depuis le dossier assets/images"""
    # MODIFIER CE CHEMIN :
    chemin = os.path.join(os.path.dirname(__file__), "assets", "images", nom_fichier)
    try:
        img = pygame.image.load(chemin).convert_alpha()
        return pygame.transform.smoothscale(img, taille)
    except:
        surface = pygame.Surface(taille, pygame.SRCALPHA)
        pygame.draw.circle(surface, ROUGE, (taille[0] // 2, taille[1] // 2), taille[0] // 2 - 5)
        return surface

def charger_polices():
    """Charge les polices Bebas Neues si disponibles"""
    dossier = os.path.dirname(__file__)
    chemin_font = os.path.join(dossier, "assets", "fonts", "BebasNeue-Regular.ttf")

    if os.path.exists(chemin_font):
        try:
            return {
                'titre': pygame.font.Font(chemin_font, 110),
                'bouton': pygame.font.Font(chemin_font, 36),
                'subtitre': pygame.font.Font(chemin_font, 48),
                'shop': pygame.font.Font(chemin_font, 32)
            }
        except:
            pass

    # Polices par défaut si BebasNeue n'est pas disponible
    return {
        'titre': pygame.font.Font(None, 110),
        'bouton': pygame.font.Font(None, 36),
        'subtitre': pygame.font.Font(None, 48),
        'shop': pygame.font.Font(None, 32)
    }


def render_text_usa_surface(font_obj, text):
    """Rend un texte avec effet drapeau américain (rouge/blanc/bleu)"""
    surf_r = font_obj.render(text, True, ROUGE)
    surf_w = font_obj.render(text, True, BLANC)
    surf_b = font_obj.render(text, True, BLEU)

    w, h = surf_w.get_size()
    surface = pygame.Surface((w + 12, h), pygame.SRCALPHA)
    surface.blit(surf_b, (0, 0))
    surface.blit(surf_w, (6, 0))
    surface.blit(surf_r, (12, 0))
    return surface


def draw_waving_text(ecran, surface, x, y, temps):
    """Dessine un texte avec effet d'ondulation"""
    largeur, hauteur = surface.get_size()
    amplitude = 10
    longueur = 140
    vitesse = 0.004
    pas = 2

    for i in range(0, largeur, pas):
        offset = int(math.sin((i / longueur) + temps * vitesse) * amplitude)
        col_width = min(pas, largeur - i)
        colonne = surface.subsurface((i, 0, col_width, hauteur))
        ecran.blit(colonne, (x + i, y + offset))


# ---------------------------------------------------
# GÉNÉRATEURS DE PLACEHOLDERS D'IMAGES
# ---------------------------------------------------
def _generer_image_simple(fullpath, taille, couleur_fond=(50, 50, 70), texte=None, text_color=(255,255,255)):
    """Génère une image simple et la sauvegarde sur disque."""
    dossier = os.path.dirname(fullpath)
    os.makedirs(dossier, exist_ok=True)
    surf = pygame.Surface(taille, pygame.SRCALPHA)
    surf.fill(couleur_fond)

    # Dessin simple selon la taille
    w, h = taille
    if w >= 30 and h >= 30:
        pygame.draw.rect(surf, (20, 20, 20), (4, 4, w-8, h-8), border_radius=min(8, w//10))
    # Texte centré si fourni
    if texte:
        try:
            f = pygame.font.Font(None, max(12, min(w//6, 48)))
            t = f.render(texte, True, text_color)
            surf.blit(t, t.get_rect(center=(w//2, h//2)))
        except Exception:
            pass

    try:
        pygame.image.save(surf, fullpath)
    except Exception:
        # Fallback silent
        pass


def assurer_images_assets():
    """S'assure que les images essentielles existent; crée des placeholders sinon."""
    base = os.path.join(os.path.dirname(__file__), "assets", "images")

    images_a_creer = [
        (os.path.join(base, "soldier.png"), (50, 60), (80, 120, 80), "S"),
        (os.path.join(base, "plane.png"), (80, 60), (100, 100, 140), "P"),
        (os.path.join(base, "bullet.png"), (40, 60), (200, 180, 60), "B"),
        (os.path.join(base, "vie.png"), (60, 60), (180, 30, 30), "♥"),
        (os.path.join(base, "logo-trump.png"), (90, 80), (200, 80, 80), "LOGO"),
        (os.path.join(base, "falling.webp"), (60, 45), (180, 180, 200), "F"),
        (os.path.join(base, "fond.png"), (LARGEUR_JEU, HAUTEUR_JEU), (20, 40, 90), None),
        (os.path.join(base, "ciel.png"), (LARGEUR_JEU, HAUTEUR_JEU), (100, 160, 220), None),
        (os.path.join(base, "espace.png"), (LARGEUR_JEU, HAUTEUR_JEU), (5, 5, 20), None),
        (os.path.join(base, "fond_usa.png"), (LARGEUR_JEU, HAUTEUR_JEU), (10, 30, 60), None),
        (os.path.join(base, "bouton-jouer.png"), (350, 250), (30, 60, 120), "JOUER"),
        (os.path.join(base, "bouton-options.png"), (350, 250), (30, 60, 120), "OPTIONS"),
        (os.path.join(base, "bouton-quitter.png"), (350, 250), (30, 60, 120), "QUITTER"),
    ]

    # GIF frames
    gif_dir = os.path.join(base, "gif_trump")
    for i in range(12):
        images_a_creer.append((os.path.join(gif_dir, f"frame_{i}.png"), (300, 300), (120, 40, 40), f"G{i}"))

    for path, taille, couleur, txt in images_a_creer:
        if not os.path.exists(path):
            _generer_image_simple(path, taille, couleur, texte=txt)

