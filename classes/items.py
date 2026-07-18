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
        self.rect.y += self.vitesse_y
        if self.rect.top > HAUTEUR_JEU:
            self.kill()


class ItemCle(pygame.sprite.Sprite):
    """Clé secrète pour débloquer le niveau infini"""

    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = charger_image_transparente("cle.png", (50, 50))
        except Exception:
            self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 215, 0), [15, 5, 10, 30])
            pygame.draw.circle(self.image, (255, 215, 0), (20, 40), 8)
            pygame.draw.circle(self.image, (0, 0, 0), (20, 40), 4)

        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse_y = 2

    def update(self):
        self.rect.y += self.vitesse_y
        if self.rect.top > HAUTEUR_JEU:
            self.kill()


class ItemPowerUp(pygame.sprite.Sprite):
    """Bonus temporaire ramassable en run."""

    TYPES = {
        "bouclier": {"couleur": BLEU_BOUCLIER, "label": "B"},
        "spread": {"couleur": ORANGE, "label": "S"},
        "ralentir": {"couleur": VIOLET, "label": "R"},
    }

    def __init__(self, x, y, kind):
        super().__init__()
        self.kind = kind if kind in self.TYPES else "bouclier"
        meta = self.TYPES[self.kind]
        self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.circle(self.image, meta["couleur"], (22, 22), 20)
        pygame.draw.circle(self.image, BLANC, (22, 22), 20, 2)
        font = pygame.font.Font(None, 28)
        txt = font.render(meta["label"], True, BLANC)
        self.image.blit(txt, txt.get_rect(center=(22, 22)))
        self.rect = self.image.get_rect(center=(x, y))
        self.vitesse_y = 2.5

    def update(self):
        self.rect.y += self.vitesse_y
        if self.rect.top > HAUTEUR_JEU:
            self.kill()
