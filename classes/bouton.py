"""
Classes pour les boutons du jeu
"""
import pygame
from constantes import *


class Bouton:
    """Bouton textuel standard"""
    
    def __init__(self, cx, cy, w, h, texte, action=None):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (cx, cy)
        self.texte = texte
        self.action = action
        self.couleur_base = GRIS_FONCE
        self.couleur_survol = ORANGE
        self.est_survole = False

    def dessiner(self, surface):
        """Dessine le bouton"""
        couleur = self.couleur_survol if self.est_survole else self.couleur_base
        pygame.draw.rect(surface, couleur, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=10)
        
        font = pygame.font.Font(None, 36)
        txt_surf = font.render(self.texte, True, BLANC)
        surface.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def verifier_survol(self, pos_souris):
        """Vérifie si la souris survole le bouton"""
        self.est_survole = self.rect.collidepoint(pos_souris)

    def verifier_clic(self, pos_souris):
        """Vérifie si le bouton est cliqué et exécute l'action"""
        if self.rect.collidepoint(pos_souris) and self.action:
            return self.action()
        return None


class BoutonImage:
    """Bouton avec image et effet de zoom au survol"""
    
    def __init__(self, image, centre_x, y, action):
        self.image_base = image.convert_alpha() if image else None
        self.image = self.image_base
        
        if self.image:
            self.rect = self.image.get_rect()
            self.rect.centerx = centre_x
            self.rect.y = y
        else:
            self.rect = pygame.Rect(centre_x - 150, y, 300, 60)
        
        self.action = action
        self.scale_hover = 1.1
        self.current_scale = 1.0
        self.scale_speed = 0.1
        self.orig_center = self.rect.center

    def update(self, souris_pos):
        """Met à jour l'état du bouton (effet hover)"""
        hovering = False
        target_scale = 1.0

        if self.image_base:
            # Vérifie d'abord collision rectangle
            if self.rect.collidepoint(souris_pos):
                local_x = souris_pos[0] - self.rect.left
                local_y = souris_pos[1] - self.rect.top
                if 0 <= local_x < self.image.get_width() and 0 <= local_y < self.image.get_height():
                    if self.image.get_at((local_x, local_y)).a > 0:
                        hovering = True
                        target_scale = self.scale_hover

            # Interpolation linéaire pour zoom fluide
            self.current_scale += (target_scale - self.current_scale) * self.scale_speed

            # Redimension de l'image
            w, h = self.image_base.get_size()
            new_w, new_h = int(w * self.current_scale), int(h * self.current_scale)
            self.image = pygame.transform.smoothscale(self.image_base, (new_w, new_h))
            self.rect = self.image.get_rect()
            self.rect.center = self.orig_center

    def draw(self, ecran):
        """Dessine le bouton"""
        if self.image:
            ecran.blit(self.image, self.rect.topleft)

    def clic(self, pos):
        """Vérifie si le bouton est cliqué"""
        if self.image_base:
            # Même vérification alpha pour le clic
            if self.rect.collidepoint(pos):
                local_x = pos[0] - self.rect.left
                local_y = pos[1] - self.rect.top
                if 0 <= local_x < self.image.get_width() and 0 <= local_y < self.image.get_height():
                    if self.image.get_at((local_x, local_y)).a > 0:
                        return True
        else:
            return self.rect.collidepoint(pos)
        return False
