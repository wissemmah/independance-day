"""
Classes des projectiles du joueur
"""
import pygame
import math
from constantes import *
from utils import charger_image_transparente


class Balle(pygame.sprite.Sprite):
    """Balle standard du joueur"""

    def __init__(self, x, y, angle=0, niveau=1):
        super().__init__()

        # Niveaux 3 et 4 : utiliser balle.png
        if niveau >= 3:
            try:
                self.image = charger_image_transparente("balle.png", (40, 60))
            except:
                self.image = pygame.Surface([10, 20], pygame.SRCALPHA)
                pygame.draw.circle(self.image, (255, 200, 0), (5, 10), 5)
        else:
            # Niveaux 1 et 2 : utiliser bullet.png
            try:
                self.image = charger_image_transparente("bullet.png", (40, 60))
            except:
                self.image = pygame.Surface([10, 20], pygame.SRCALPHA)
                pygame.draw.rect(self.image, JAUNE, [0, 0, 10, 20], border_radius=3)

        if angle:
            self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=(x, y))
        rad = math.radians(angle)
        self.vx = 15 * math.sin(rad)
        self.vy = -15 * math.cos(rad)

    def update(self):
        """Met à jour la position de la balle"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    """Laser continu - traverse tout l'écran"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([8, HAUTEUR_JEU], pygame.SRCALPHA)
        # Dessiner un laser cyan brillant
        pygame.draw.rect(self.image, CYAN, [2, 0, 4, HAUTEUR_JEU])
        pygame.draw.rect(self.image, BLANC, [3, 0, 2, HAUTEUR_JEU])

        self.rect = self.image.get_rect(centerx=x, top=0)
        self.vie = 3  # Le laser dure quelques frames

    def update(self):
        """Met à jour le laser"""
        self.vie -= 1
        if self.vie <= 0:
            self.kill()