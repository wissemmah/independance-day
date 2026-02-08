import pygame
import sys

from constantes import *
from classes.jeu import Jeu
from classes.gestion_entrees import gerer_entrees_jeu
from classes.update_jeu import update_jeu
from classes.rendu import dessiner_jeu, charger_polices_bebas

# --- Initialisation Pygame ---
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

# Écran et horloge
ecran = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
pygame.display.set_caption("Independence Day : Deluxe Edition - 250th Anniversary")
clock = pygame.time.Clock()

# Polices Bebas (si disponibles) -> renvoie (font, petite_font, moyenne_font, grosse_font)
font, petite_font, moyenne_font, grosse_font = charger_polices_bebas()


def main():
    jeu = Jeu()
    pygame.mouse.set_visible(True)

    try:
        while True:
            if not gerer_entrees_jeu(jeu):
                break

            if jeu.etat == "JEU":
                update_jeu(jeu)

            # Dessin via le module `classes.rendu`
            dessiner_jeu(jeu, ecran, font, petite_font, grosse_font, moyenne_font)
            
            # Appliquer la vitesse du debug (ralenti/accéléré)
            clock.tick(int(FPS * jeu.debug_game_speed))
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()

