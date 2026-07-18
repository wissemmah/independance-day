"""
Boss final — phases de combat
"""
import math
import os
import random
import pygame
from constantes import *
from chemins import resource_root


class Boss(pygame.sprite.Sprite):
    """Boss final niveau 4 — 3 phases selon les PV."""

    def __init__(self):
        super().__init__()
        self.largeur = 300
        self.hauteur = 300
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)
        self.rect.centerx = LARGEUR_JEU // 2
        self.rect.y = -self.hauteur

        self.vx = 2
        self.vy = 1
        self.phase = "entree"
        self.phase_combat = 1  # 1, 2, 3 selon PV
        self.position_combat_y = 100

        self.pv = BOSS_PV
        self.max_pv = BOSS_PV
        self.valeur = 2000

        self.laser_actif = False
        self.laser_cooldown = 90
        self.laser_duree = 0
        self.laser_charge = 0
        self.laser_x = 0

        self.peut_tirer_projectiles = True
        self.dernier_tir_projectile = 0
        self.projectiles = []
        self.charge_active = False
        self.charge_timer = 0
        self.charge_cooldown = 180

        self.frames = []
        dossier = resource_root()
        for nom in ["boss1.png", "boss2.png"]:
            chemin = os.path.join(dossier, "assets", "images", nom)
            try:
                img = pygame.transform.smoothscale(
                    pygame.image.load(chemin).convert_alpha(),
                    (self.largeur, self.hauteur),
                )
                self.frames.append(img)
            except Exception:
                s = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
                pygame.draw.circle(s, (150, 0, 0), (self.largeur // 2, self.hauteur // 2), self.largeur // 2)
                pygame.draw.circle(s, (255, 0, 0), (self.largeur // 3, self.hauteur // 3), 30)
                pygame.draw.circle(s, (255, 0, 0), (2 * self.largeur // 3, self.hauteur // 3), 30)
                self.frames.append(s)

        self.index_frame = 0
        self.image = self.frames[0]
        self.dernier_anim = pygame.time.get_ticks()
        self.vitesse_anim = 200
        self.rect.size = self.image.get_size()

    def _maj_phase_combat(self):
        ratio = self.pv / self.max_pv
        if ratio > 0.66:
            self.phase_combat = 1
            self.vx = 2 if self.vx >= 0 else -2
            self.vitesse_anim = 200
        elif ratio > 0.33:
            self.phase_combat = 2
            self.vx = 3.5 if self.vx >= 0 else -3.5
            self.vitesse_anim = 140
        else:
            self.phase_combat = 3
            self.vx = 5 if self.vx >= 0 else -5
            self.vitesse_anim = 90

    def update(self):
        maintenant = pygame.time.get_ticks()
        if maintenant - self.dernier_anim > self.vitesse_anim:
            self.dernier_anim = maintenant
            self.index_frame = (self.index_frame + 1) % len(self.frames)
            self.image = self.frames[self.index_frame]

        if self.phase == "entree":
            self.rect.y += self.vy
            if self.rect.y >= self.position_combat_y:
                self.rect.y = self.position_combat_y
                self.phase = "combat"
            return

        self._maj_phase_combat()

        if self.charge_active:
            self.rect.y += 10
            self.charge_timer -= 1
            if self.rect.bottom >= HAUTEUR_JEU - 40 or self.charge_timer <= 0:
                self.charge_active = False
                self.rect.y = self.position_combat_y
                self.charge_cooldown = random.randint(150, 220)
            return

        self.rect.x += int(self.vx)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        elif self.rect.right >= LARGEUR_JEU:
            self.rect.right = LARGEUR_JEU
            self.vx = -abs(self.vx)

        # Laser
        if not self.laser_actif:
            self.laser_cooldown -= 1
            if self.laser_cooldown <= 0:
                self.laser_charge += 1
                charge_max = 45 if self.phase_combat >= 2 else 60
                if self.laser_charge >= charge_max:
                    self.activer_laser()
                    self.laser_charge = 0
        else:
            self.laser_duree -= 1
            if self.laser_duree <= 0:
                self.desactiver_laser()
                cd = {1: (140, 200), 2: (100, 150), 3: (70, 110)}[self.phase_combat]
                self.laser_cooldown = random.randint(*cd)

        # Projectiles
        intervalle = {1: 2200, 2: 1500, 3: 900}[self.phase_combat]
        if maintenant - self.dernier_tir_projectile > intervalle:
            self.tirer_projectiles()
            self.dernier_tir_projectile = maintenant

        # Charge (phase 3)
        if self.phase_combat == 3:
            self.charge_cooldown -= 1
            if self.charge_cooldown <= 0 and not self.laser_actif:
                self.charge_active = True
                self.charge_timer = 40

    def activer_laser(self):
        self.laser_actif = True
        self.laser_duree = {1: 70, 2: 90, 3: 110}[self.phase_combat]
        self.laser_x = self.rect.centerx

    def desactiver_laser(self):
        self.laser_actif = False

    def tirer_projectiles(self):
        if self.phase_combat == 1:
            angles = [-20, 0, 20]
        elif self.phase_combat == 2:
            angles = [-35, -15, 0, 15, 35]
        else:
            angles = [-45, -25, -10, 0, 10, 25, 45]
        for angle in angles:
            self.projectiles.append(ProjectileBoss(self.rect.centerx, self.rect.bottom, angle, self.phase_combat))

    def get_laser_rect(self):
        if not self.laser_actif:
            return None
        largeur = 50 + 10 * self.phase_combat
        return pygame.Rect(self.laser_x - largeur // 2, self.rect.bottom, largeur, HAUTEUR_JEU - self.rect.bottom)

    def dessiner_laser(self, surface):
        if self.laser_actif:
            laser_rect = self.get_laser_rect()
            if laser_rect:
                pygame.draw.rect(surface, (255, 0, 0), laser_rect)
                centre = pygame.Rect(laser_rect.x + laser_rect.width // 4, laser_rect.y,
                                    laser_rect.width // 2, laser_rect.height)
                pygame.draw.rect(surface, BLANC, centre)
                pygame.draw.rect(surface, ORANGE, laser_rect, 4)
        elif self.laser_charge > 0:
            charge_max = 45 if self.phase_combat >= 2 else 60
            rayon = int(30 * (self.laser_charge / charge_max))
            pygame.draw.circle(surface, JAUNE, (self.rect.centerx, self.rect.bottom), rayon)
            pygame.draw.circle(surface, ROUGE, (self.rect.centerx, self.rect.bottom), rayon, 3)


class ProjectileBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, phase=1):
        super().__init__()
        taille = 16 + phase * 2
        self.image = pygame.Surface([taille, taille], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (taille // 2, taille // 2), taille // 2)
        pygame.draw.circle(self.image, (255, 100, 0), (taille // 2, taille // 2), taille // 3)
        self.rect = self.image.get_rect(center=(x, y))
        rad = math.radians(angle)
        vitesse = 7 + phase
        self.vx = vitesse * math.sin(rad)
        self.vy = vitesse * math.cos(rad)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.bottom < 0 or self.rect.top > HAUTEUR_JEU or
                self.rect.right < 0 or self.rect.left > LARGEUR_JEU):
            self.kill()
