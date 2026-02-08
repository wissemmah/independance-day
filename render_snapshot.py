import os
import pygame
from classes.jeu import Jeu
from classes.rendu import dessiner_jeu, charger_polices_bebas
from constantes import *

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
font, petite_font, moyenne_font, grosse_font = charger_polices_bebas()

j = Jeu()

# Snapshot MENU
j.etat = 'MENU'
dessiner_jeu(j, SCREEN, font, petite_font, grosse_font, moyenne_font)
pygame.image.save(SCREEN, 'assets/images/snapshot_menu.png')
print('Saved snapshot_menu.png')

# Snapshot JEU
j.reset_partie()
j.etat = 'JEU'
dessiner_jeu(j, SCREEN, font, petite_font, grosse_font, moyenne_font)
pygame.image.save(SCREEN, 'assets/images/snapshot_game.png')
print('Saved snapshot_game.png')

pygame.quit()
