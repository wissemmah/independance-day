import pygame
from constantes import *
from classes.jeu import Jeu
from classes.gestion_entrees import gerer_entrees_jeu
from classes.rendu import dessiner_jeu, charger_polices_bebas

print('pygame', pygame.__version__)
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print('pygame initialized')

# Créer l'écran AVANT d'appeler les méthodes qui utilisent convert/convert_alpha
try:
    screen = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
    print('display created')
except Exception as e:
    print('display create error', e)

font, petite_font, moyenne_font, grosse_font = charger_polices_bebas()
print('fonts loaded')

try:
    j = Jeu()
    print('Jeu created, etat=', j.etat)
except Exception as e:
    import traceback
    print('Erreur pendant la création de Jeu:')
    traceback.print_exc()
    pygame.quit()
    raise

res = gerer_entrees_jeu(j)
print('gerer_entrees_jeu returned', res)

dessiner_jeu(j, screen, font, petite_font, grosse_font, moyenne_font)
print('dessiner_jeu called')

pygame.quit()
print('pygame quit')
