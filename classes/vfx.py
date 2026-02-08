"""
Système de particules et effets visuels (VFX)
"""
import pygame
import random
import math
from constantes import *


class Particule:
    """Particule individuelle pour les effets visuels"""

    def __init__(self, x, y, couleur, vitesse, taille, vie):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vx = random.uniform(-vitesse, vitesse)
        self.vy = random.uniform(-vitesse, vitesse)
        self.taille = taille
        self.vie = vie
        self.vie_max = vie

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vie -= 1
        self.taille *= 0.9

    def draw(self, surface):
        if self.vie > 0:
            alpha = int((self.vie / self.vie_max) * 255)
            s = pygame.Surface((int(self.taille * 2), int(self.taille * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.couleur, alpha), (int(self.taille), int(self.taille)), int(self.taille))
            surface.blit(s, (self.x, self.y))


class GestionnaireVFX:
    """Gestionnaire des effets visuels du jeu"""

    def __init__(self):
        self.particules = []
        self.ecran_rouge = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
        self.ecran_rouge.fill(ROUGE)
        self.flash_nuke = 0
        self.timer_degats_rouge = 0
        self.tremblement_actif = False
        self.tremblement_intensite = 0
        self.tremblement_duree = 0

    def ajouter(self, x, y, couleur, count=5):
        """Ajoute des particules à la position donnée"""
        for _ in range(count):
            self.particules.append(Particule(x, y, couleur, 3, random.randint(3, 6), 30))

    def declencher_nuke(self):
        """Déclenche l'effet visuel de la bombe nucléaire"""
        self.flash_nuke = 255
        self.tremblement_actif = True
        self.tremblement_intensite = 20  # Intensité du tremblement
        self.tremblement_duree = 30  # Durée en frames

    def declencher_degats(self):
        """Déclenche l'effet visuel de dégâts"""
        self.timer_degats_rouge = 15

    def update(self):
        """Met à jour tous les effets"""
        for p in self.particules[:]:
            p.update()
            if p.vie <= 0:
                self.particules.remove(p)
        if self.flash_nuke > 0:
            self.flash_nuke -= 5
        if self.timer_degats_rouge > 0:
            self.timer_degats_rouge -= 1

        # Mise à jour du tremblement
        if self.tremblement_actif:
            self.tremblement_duree -= 1
            # Diminuer progressivement l'intensité
            self.tremblement_intensite *= 0.9
            if self.tremblement_duree <= 0:
                self.tremblement_actif = False
                self.tremblement_intensite = 0

    def draw(self, surface):
        """Dessine les particules et le flash de nuke"""
        for p in self.particules:
            p.draw(surface)
        if self.flash_nuke > 0:
            s = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
            s.fill(BLANC)
            s.set_alpha(self.flash_nuke)
            surface.blit(s, (0, 0))

    def draw_low_hp(self, surface):
        """Dessine l'effet de vie faible (écran rouge clignotant)"""
        alpha = int(50 + math.sin(pygame.time.get_ticks() * 0.01) * 30)
        self.ecran_rouge.set_alpha(alpha)
        surface.blit(self.ecran_rouge, (0, 0), special_flags=pygame.BLEND_ADD)

    def draw_border_damage(self, surface):
        """Dessine la bordure rouge lors de dégâts"""
        if self.timer_degats_rouge > 0:
            pygame.draw.rect(surface, ROUGE, (0, 0, LARGEUR_JEU, HAUTEUR_JEU), 10)

    def get_tremblement_offset(self):
        """Retourne l'offset aléatoire pour le tremblement d'écran"""
        if self.tremblement_actif:
            offset_x = random.randint(-int(self.tremblement_intensite), int(self.tremblement_intensite))
            offset_y = random.randint(-int(self.tremblement_intensite), int(self.tremblement_intensite))
            return offset_x, offset_y
        return 0, 0