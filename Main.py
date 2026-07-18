import os
import sys
import pygame

from constantes import *
from classes.jeu import Jeu
from classes.gestion_entrees import gerer_entrees_jeu
from classes.update_jeu import update_jeu
from classes.rendu import dessiner_jeu, charger_polices_bebas
from chemins import asset_path, is_frozen

# Mode lite : saute les videos lourdes
LITE_MODE = os.environ.get("ID_LITE", "").strip() in ("1", "true", "yes")

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

# Icone fenetre
try:
    icon_path = asset_path("images", "icon.png")
    if os.path.exists(icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))
except Exception:
    pass

ecran = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
pygame.display.set_caption("Independence Day : Deluxe Edition - 250th Anniversary")
clock = pygame.time.Clock()

font, petite_font, moyenne_font, grosse_font = charger_polices_bebas()


def dessiner_splash(surface, jeu):
    surface.fill(BLEU_FONCE)
    titre = grosse_font.render("INDEPENDENCE DAY", True, OR)
    surface.blit(titre, titre.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 40)))
    sub = font.render("250th Anniversary Deluxe", True, BLANC)
    surface.blit(sub, sub.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 20)))
    if LITE_MODE or getattr(jeu, "lite_mode", False):
        lite = petite_font.render("LITE BUILD", True, ORANGE)
        surface.blit(lite, lite.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 60)))


def main():
    jeu = Jeu()
    jeu.lite_mode = LITE_MODE or is_frozen() and os.environ.get("ID_LITE", "") == "1"
    pygame.mouse.set_visible(True)

    try:
        while True:
            if getattr(jeu, "splash_timer", 0) > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        jeu.splash_timer = 0
                dessiner_splash(ecran, jeu)
                pygame.display.flip()
                jeu.splash_timer -= 1
                clock.tick(FPS)
                continue

            if not gerer_entrees_jeu(jeu):
                break

            if jeu.achievement_toast_timer > 0:
                jeu.achievement_toast_timer -= 1

            # Hit-stop : freeze logique, continue le rendu
            if jeu.hitstop_frames > 0:
                jeu.hitstop_frames -= 1
            elif jeu.etat == "JEU":
                update_jeu(jeu)

            dessiner_jeu(jeu, ecran, font, petite_font, grosse_font, moyenne_font)

            speed = jeu.debug_game_speed * getattr(jeu, "game_speed_override", 1.0)
            clock.tick(max(1, int(FPS * speed)))
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
