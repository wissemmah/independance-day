"""
Classe du Boss final du niveau 3
"""
import pygame
import random
import os
from constantes import *


class Boss(pygame.sprite.Sprite):
    """Boss final du niveau 3 - Très puissant avec laser"""

    def __init__(self):
        super().__init__()

        # Taille du boss (énorme !)
        self.largeur = 300
        self.hauteur = 300

        # Position de départ (en haut au centre)
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)
        self.rect.centerx = LARGEUR_JEU // 2
        self.rect.y = -self.hauteur

        # Mouvement
        self.vx = 2
        self.vy = 1  # Descend lentement
        self.phase = "entree"  # entree, combat
        self.position_combat_y = 100  # Position finale en haut de l'écran

        # Stats ÉNORMES
        self.pv = 1000  # 1000 points de vie !!! (au lieu de 500)
        self.max_pv = 1000
        self.valeur = 2000  # Énorme récompense

        # Laser
        self.laser_actif = False
        self.laser_cooldown = 0
        self.laser_duree = 0
        self.laser_charge = 0
        self.laser_x = 0  # Position X du laser

        # Nouveaux pouvoirs
        self.peut_tirer_projectiles = True
        self.dernier_tir_projectile = 0
        self.projectiles = []  # Liste des projectiles du boss

        # Animation : charger 2 frames
        self.frames = []
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        for nom in ["boss1.png", "boss2.png"]:
            chemin = os.path.join(dossier, "assets", "images", nom)
            try:
                img = pygame.transform.smoothscale(
                    pygame.image.load(chemin).convert_alpha(),
                    (self.largeur, self.hauteur)
                )
                self.frames.append(img)
            except:
                # Image par défaut si boss.png n'existe pas
                s = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
                # Dessiner un boss monstrueux
                pygame.draw.circle(s, (150, 0, 0), (self.largeur // 2, self.hauteur // 2), self.largeur // 2)
                pygame.draw.circle(s, (255, 0, 0), (self.largeur // 3, self.hauteur // 3), 30)  # Œil
                pygame.draw.circle(s, (255, 0, 0), (2 * self.largeur // 3, self.hauteur // 3), 30)  # Œil
                pygame.draw.rect(s, (100, 0, 0),
                                 (self.largeur // 3, 2 * self.hauteur // 3, self.largeur // 3, 20))  # Bouche
                self.frames.append(s)

        self.index_frame = 0
        self.image = self.frames[self.index_frame] if self.frames else pygame.Surface([self.largeur, self.hauteur])
        self.dernier_anim = pygame.time.get_ticks()
        self.vitesse_anim = 200  # Animation plus lente

        self.rect.size = self.image.get_size()

    def update(self):
        """Met à jour le boss"""
        maintenant = pygame.time.get_ticks()

        # Animation
        if maintenant - self.dernier_anim > self.vitesse_anim:
            self.dernier_anim = maintenant
            if self.frames:
                self.index_frame = (self.index_frame + 1) % len(self.frames)
                self.image = self.frames[self.index_frame]

        # Phase d'entrée
        if self.phase == "entree":
            self.rect.y += self.vy
            if self.rect.y >= self.position_combat_y:
                self.rect.y = self.position_combat_y
                self.phase = "combat"

        # Phase de combat
        elif self.phase == "combat":
            # Mouvement horizontal
            self.rect.x += self.vx

            # Rebond sur les bords
            if self.rect.left <= 0:
                self.rect.left = 0
                self.vx = abs(self.vx)
            elif self.rect.right >= LARGEUR_JEU:
                self.rect.right = LARGEUR_JEU
                self.vx = -abs(self.vx)

            # Gestion du laser
            if not self.laser_actif:
                self.laser_cooldown -= 1
                if self.laser_cooldown <= 0:
                    # Charger le laser
                    self.laser_charge += 1
                    if self.laser_charge >= 60:  # 1 seconde de charge
                        self.activer_laser()
                        self.laser_charge = 0
            else:
                # Laser actif
                self.laser_duree -= 1
                if self.laser_duree <= 0:
                    self.desactiver_laser()
                    self.laser_cooldown = random.randint(120, 180)  # 2-3 secondes avant prochain laser

            # Tir de projectiles
            maintenant = pygame.time.get_ticks()
            if maintenant - self.dernier_tir_projectile > 2000:  # Tire toutes les 2 secondes
                self.tirer_projectiles()
                self.dernier_tir_projectile = maintenant

    def activer_laser(self):
        """Active le laser depuis la bouche du boss"""
        self.laser_actif = True
        self.laser_duree = 90  # 1.5 secondes de laser
        self.laser_x = self.rect.centerx

    def desactiver_laser(self):
        """Désactive le laser"""
        self.laser_actif = False

    def tirer_projectiles(self):
        """Le boss tire 3 projectiles en éventail"""
        # Tirer 3 projectiles à partir du centre du boss
        angles = [-30, 0, 30]  # 3 directions
        for angle in angles:
            projectile = ProjectileBoss(self.rect.centerx, self.rect.bottom, angle)
            self.projectiles.append(projectile)

    def get_laser_rect(self):
        """Retourne le rectangle du laser pour les collisions"""
        if self.laser_actif:
            # Le laser part de la bouche (bas du boss) jusqu'en bas de l'écran
            laser_largeur = 60  # Laser épais
            laser_x = self.laser_x - laser_largeur // 2
            laser_y = self.rect.bottom
            laser_hauteur = HAUTEUR_JEU - laser_y
            return pygame.Rect(laser_x, laser_y, laser_largeur, laser_hauteur)
        return None

    def dessiner_laser(self, surface):
        """Dessine le laser du boss"""
        if self.laser_actif:
            laser_rect = self.get_laser_rect()
            if laser_rect:
                # Effet de charge
                if self.laser_charge > 0:
                    # Cercle de charge à la bouche
                    charge_ratio = self.laser_charge / 60
                    rayon = int(30 * charge_ratio)
                    pygame.draw.circle(surface, (255, 255, 0), (self.rect.centerx, self.rect.bottom), rayon)

                # Laser principal (rouge brillant)
                pygame.draw.rect(surface, (255, 0, 0), laser_rect)
                # Centre du laser (blanc brillant)
                centre_rect = pygame.Rect(laser_rect.x + 15, laser_rect.y, 30, laser_rect.height)
                pygame.draw.rect(surface, (255, 255, 255), centre_rect)
                # Bords du laser (orange)
                pygame.draw.rect(surface, (255, 100, 0), laser_rect, 5)

        # Effet de charge avant le laser
        elif self.laser_charge > 0:
            charge_ratio = self.laser_charge / 60
            rayon = int(30 * charge_ratio)
            # Cercle de charge qui grandit
            pygame.draw.circle(surface, (255, 255, 0, 150), (self.rect.centerx, self.rect.bottom), rayon)
            pygame.draw.circle(surface, (255, 0, 0), (self.rect.centerx, self.rect.bottom), rayon, 3)


class LaserBoss(pygame.sprite.Sprite):
    """Sprite pour le laser du boss (pour les collisions)"""

    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        laser_rect = boss.get_laser_rect()
        if laser_rect:
            self.image = pygame.Surface([laser_rect.width, laser_rect.height], pygame.SRCALPHA)
            self.image.fill((255, 0, 0, 100))
            self.rect = laser_rect
        else:
            self.image = pygame.Surface([1, 1], pygame.SRCALPHA)
            self.rect = self.image.get_rect()

    def update(self):
        """Met à jour la position du laser"""
        laser_rect = self.boss.get_laser_rect()
        if laser_rect:
            self.rect = laser_rect
        else:
            self.kill()


class ProjectileBoss(pygame.sprite.Sprite):
    """Projectile tiré par le boss"""

    def __init__(self, x, y, angle):
        super().__init__()

        # Créer un projectile rouge menaçant
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 100, 0), (10, 10), 6)

        self.rect = self.image.get_rect(center=(x, y))

        # Vitesse selon l'angle
        import math
        rad = math.radians(angle)
        vitesse = 8
        self.vx = vitesse * math.sin(rad)
        self.vy = vitesse * math.cos(rad)

    def update(self):
        """Met à jour la position du projectile"""
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Supprimer si hors écran
        if (self.rect.bottom < 0 or self.rect.top > HAUTEUR_JEU or
                self.rect.right < 0 or self.rect.left > LARGEUR_JEU):
            self.kill()