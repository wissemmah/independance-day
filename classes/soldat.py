"""
Classe du joueur (Soldat/Avion)
"""
import pygame
import os
from constantes import *
from utils import charger_image_transparente

# Racine du projet
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Soldat(pygame.sprite.Sprite):
    """Le joueur - Soldat (niveau 1) ou Avion (niveaux 2+)"""

    def __init__(self, niveau):
        super().__init__()
        self.niveau = niveau

        # NIVEAU 1 : Soldat / NIVEAU 2 : Avion / NIVEAUX 3 et 4 : Fusée
        if niveau == 1:
            # Charger l'animation du soldat
            self.animation_frames = []
            self.current_frame = 0
            self.frame_timer = 0
            self.animation_speed = 5  # Frames avant de changer d'image
            
            try:
                # Charger la strip d'animation (4 frames)
                strip_path = os.path.join(PROJ_ROOT, "assets", "images", "SMS_Soldier_RUN_NORTH_strip4.png")
                if os.path.exists(strip_path):
                    strip_image = pygame.image.load(strip_path).convert_alpha()
                    # Diviser la strip en 4 frames
                    strip_width = strip_image.get_width()
                    frame_width = strip_width // 4
                    frame_height = strip_image.get_height()
                    
                    for i in range(4):
                        frame = strip_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                        frame = pygame.transform.scale(frame, (50, 60))
                        self.animation_frames.append(frame)
                    
                    print(f"[INFO] Animation soldat chargée: {strip_path}")
                else:
                    raise FileNotFoundError(f"Strip animation non trouvée: {strip_path}")
            except Exception as e:
                print(f"[WARN] Erreur chargement animation soldat: {e}")
                # Fallback : utiliser l'image statique
                try:
                    self.image = charger_image_transparente("soldier.png", (50, 60))
                except:
                    self.image = pygame.Surface([50, 60], pygame.SRCALPHA)
                    self.image.fill(VERT_MILITAIRE)
                    pygame.draw.rect(self.image, (30, 90, 55), [20, 0, 10, 20])
                self.animation_frames = None
            
            # Définir l'image initiale
            if self.animation_frames:
                self.image = self.animation_frames[0]
            
        elif niveau == 2:
            try:
                self.image = charger_image_transparente("plane.png", (100, 120))
            except:
                self.image = pygame.Surface([80, 60], pygame.SRCALPHA)
                # Dessin d'un avion simple
                pygame.draw.polygon(self.image, GRIS_FONCE, [(40, 0), (60, 60), (40, 50), (20, 60)])
                pygame.draw.rect(self.image, BLEU_BOUCLIER, [35, 20, 10, 30])
        else:  # niveaux 3 et 4
            try:
                self.image = charger_image_transparente("fusee.png", (100, 120))
            except:
                self.image = pygame.Surface([100, 120], pygame.SRCALPHA)
                # Dessin d'une fusée simple
                pygame.draw.polygon(self.image, (200, 200, 200), [(50, 0), (70, 30), (50, 120), (30, 30)])
                pygame.draw.rect(self.image, (255, 100, 0), [45, 90, 10, 30])

        self.rect = self.image.get_rect(centerx=LARGEUR_JEU // 2, bottom=HAUTEUR_JEU - 20)

        # Stats et Améliorations
        self.niveau_tir = 1  # 1, 2, 3
        self.niveau_cadence = 1
        self.cadence_base = 350
        self.a_laser = False  # Possession du laser
        self.max_vies = 3  # Maximum de vies (peut être augmenté à 4 puis 5)

        self.invincible = False
        self.fin_invincibilite = 0
        self.nukes = 0
        self.dernier_tir = 0

    def update(self):
        """Met à jour la position du joueur et l'animation"""
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(pygame.Rect(0, 0, LARGEUR_JEU, HAUTEUR_JEU))
        if self.invincible and pygame.time.get_ticks() > self.fin_invincibilite:
            self.invincible = False
        
        # Animer le soldat (niveau 1)
        if self.niveau == 1 and self.animation_frames:
            self.frame_timer += 1
            if self.frame_timer >= self.animation_speed:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame]

    def verifier_tir_auto(self):
        """Vérifie et effectue le tir automatique"""
        from classes.projectiles import Balle, Laser

        maintenant = pygame.time.get_ticks()
        delai = max(50, self.cadence_base - (self.niveau_cadence * 40))

        if maintenant - self.dernier_tir > delai:
            self.dernier_tir = maintenant
            balles = []
            x, y = self.rect.centerx + 15, self.rect.top


            # TIR NORMAL (toujours actif) - passer le niveau à la balle
            if self.niveau_tir == 1:
                balles.append(Balle(x, y, niveau=self.niveau))
            elif self.niveau_tir == 2:
                balles.append(Balle(x - 10, y, -5, niveau=self.niveau))
                balles.append(Balle(x + 10, y, 5, niveau=self.niveau))
            elif self.niveau_tir >= 3:
                for angle in [-15, -5, 5, 15]:
                    balles.append(Balle(x, y, angle, niveau=self.niveau))

            # TIR LASER : s'ajoute AUX balles si on a le laser
            if self.a_laser:
                balles.append(Laser(x, y))

            return balles
        return []