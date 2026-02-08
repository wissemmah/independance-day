"""
Classes des items ramassables
"""
import pygame
from constantes import *
from utils import charger_image_transparente


class ItemVie(pygame.sprite.Sprite):
    """Vache qui tombe et donne une vie"""

    def __init__(self, x, y):
        super().__init__()
        self.image = charger_image_transparente("vie.png", (60, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse_y = 3

    def update(self):
        """Met à jour la position de l'item"""
        self.rect.y += self.vitesse_y
        if self.rect.top > HAUTEUR_JEU:
            self.kill()


class ItemCle(pygame.sprite.Sprite):
    """Clé secrète pour débloquer le niveau infini"""

    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = charger_image_transparente("cle.png", (50, 50))
        except:
            # Image par défaut si cle.png n'existe pas
            self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
            # Dessiner une clé simple
            pygame.draw.rect(self.image, (255, 215, 0), [15, 5, 10, 30])  # Tige
            pygame.draw.circle(self.image, (255, 215, 0), (20, 40), 8)  # Tête
            pygame.draw.circle(self.image, (0, 0, 0), (20, 40), 4)  # Trou

        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse_y = 2  # Tombe lentement

    def update(self):
        """Fait tomber la clé"""
        self.rect.y += self.vitesse_y
        # Supprimer si hors écran
        if self.rect.top > HAUTEUR_JEU:
            self.kill()