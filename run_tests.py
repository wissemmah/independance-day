"""Script de tests runtime automatisés
Vérifie : démarrage, spawn d'ennemis, tir auto, nuke, achat boutique, condition victoire.
"""
import time
import pygame
from constantes import *
from classes.jeu import Jeu
from classes.gestion_entrees import gerer_entrees_jeu, clic_boutique, executer_action_menu
from classes.update_jeu import update_jeu
from classes.rendu import dessiner_jeu, charger_polices_bebas

print('--- RUN TESTS ---')
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

screen = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
font, petite_font, moyenne_font, grosse_font = charger_polices_bebas()

j = Jeu()
print('Jeu initialisé. etat=', j.etat)

# 1) Lancer la partie via l'action de menu
print('\n[TEST] Lancer jeu via action menu')
executer_action_menu(j, 'LANCER_JEU')
print('Etat après LANCER_JEU:', j.etat)

# 2) Faire tourner la loop de mise à jour pendant ~3.5s pour permettre le spawn
print('\n[TEST] Update loop 3.5s (attendre spawn ennemis et tir auto)')
start = pygame.time.get_ticks()
last_mobs = 0
last_balles = 0
while pygame.time.get_ticks() - start < 3500:
    update_jeu(j)
    dessiner_jeu(j, screen, font, petite_font, grosse_font, moyenne_font)
    # Petit délai pour ne pas saturer le CPU
    pygame.time.delay(50)
    if len(j.mobs) != last_mobs or len(j.balles) != last_balles:
        print(f'  -> mobs={len(j.mobs)}, balles={len(j.balles)}, score={j.score_total}, argent={j.argent}, vies={j.vies}')
        last_mobs = len(j.mobs)
        last_balles = len(j.balles)

print('Bilan après boucle : mobs=', len(j.mobs), 'balles=', len(j.balles))

# 3) Test Nuke (donner une nuke et simuler appui sur B)
print('\n[TEST] Nuke')
j.joueur.nukes = 1
print('  nukes avant:', j.joueur.nukes)
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_b}))
gerer_entrees_jeu(j)
print('  nukes après:', j.joueur.nukes, 'mobs après nuke:', len(j.mobs), 'argent=', j.argent, 'score=', j.score_total)

# 4) Test Boutique d'achat
print('\n[TEST] Boutique / achat Tir Double')
j.etat = 'PAUSE'
j.argent = 1000
cx = LARGEUR_JEU // 2
shop_y = 100
# Clic approximatif dans la première item
clic_x = cx - 200
clic_y = shop_y + 140 + 35
print('  avant achat : niveau_tir=', j.joueur.niveau_tir, 'argent=', j.argent)
clic_boutique(j, clic_x, clic_y)
print('  après achat : niveau_tir=', j.joueur.niveau_tir, 'argent=', j.argent)

# 5) Test condition victoire (simuler fin de niveau en niveau 3)
print('\n[TEST] Condition victoire')
j.niveau = 3
# Forcer le temps de début pour que le timer soit dépassé
j.debut_niveau = pygame.time.get_ticks() - (j.temps_niveau * 1000) - 100
update_jeu(j)
print('  etat après update (doit être VICTOIRE):', j.etat)

print('\n--- TESTS TERMINÉS ---')
pygame.quit()
