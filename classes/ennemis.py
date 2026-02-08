"""
Classes des ennemis du jeu
"""
import pygame
import random
import os
from constantes import *


class Tornade(pygame.sprite.Sprite):
    """Ennemi Tornade - présent dans tous les niveaux"""

    def __init__(self, niveau_jeu):
        super().__init__()
        self.niveau_jeu = niveau_jeu

        # --- TAILLE ET VITESSE SELON NIVEAU ---
        if niveau_jeu == 1:
            scale = random.randint(40, 60)
        elif niveau_jeu == 2:
            scale = random.randint(50, 80)
        else:
            scale = random.randint(60, 100)

        self.largeur = scale
        self.hauteur = int(scale * 1.5)
        self.vy = int(scale / 10) + random.randint(1, 3)

        # --- POSITION DE DEPART (TOUJOURS EN HAUT) ---
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)
        self.rect.x = random.randint(0, LARGEUR_JEU - self.largeur)
        self.rect.y = -self.hauteur

        # --- COMPORTEMENT SELON NIVEAU ---
        self.vx = 0

        if niveau_jeu == 1:
            self.pv = 1
            self.vx = 0
            self.couleur = GRIS_TORNADE_PETITE
            self.valeur = 15
        elif niveau_jeu == 2:
            self.pv = 2
            self.vx = random.choice([-2, 2])
            self.couleur = GRIS_TORNADE_MOYENNE
            self.valeur = 15
        else:
            self.pv = 3
            self.vx = random.choice([-3, 3])
            self.couleur = GRIS_TORNADE_GROSSE
            self.valeur = 15

        self.max_pv = self.pv

        # --- ANIMATION : CHARGER STRIP 4 FRAMES ---
        self.frames = []
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        strip_path = os.path.join(dossier, "assets", "images", "tornado_strip4.png")

        try:
            # Charger la strip d'animation (4 frames)
            strip_image = pygame.image.load(strip_path).convert_alpha()
            strip_width = strip_image.get_width()
            frame_width = strip_width // 4
            frame_height = strip_image.get_height()

            # Diviser la strip en 4 frames et redimensionner
            for i in range(4):
                frame = strip_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.smoothscale(frame, (self.largeur, self.hauteur))
                self.frames.append(frame)

            print(f"[INFO] Animation tornade chargée: {strip_path}")
        except Exception as e:
            print(f"[WARN] Erreur chargement animation tornade: {e}")
            # Fallback : charger les 2 frames classiques
            for nom in ["tornado.png", "tornado2.png"]:
                chemin = os.path.join(dossier, "assets", "images", nom)
                try:
                    img = pygame.transform.smoothscale(
                        pygame.image.load(chemin).convert_alpha(),
                        (self.largeur, self.hauteur)
                    )
                    self.frames.append(img)
                except:
                    s = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
                    couleur = GRIS_TORNADE_PETITE if "2" not in nom else self.couleur
                    pygame.draw.polygon(s, couleur, [(0, 0), (self.largeur, 0), (self.largeur // 2, self.hauteur)])
                    self.frames.append(s)

        self.index_frame = 0
        self.image = self.frames[self.index_frame]
        self.dernier_anim = pygame.time.get_ticks()
        self.vitesse_anim = 100

        self.rect.size = self.image.get_size()

    def update(self):
        """Met à jour la tornade"""
        # Mouvement
        self.rect.y += self.vy
        self.rect.x += self.vx

        # Rebond sur les côtés
        if self.niveau_jeu > 1:
            if self.rect.left <= 0:
                self.rect.left = 0
                self.vx *= -1
            elif self.rect.right >= LARGEUR_JEU:
                self.rect.right = LARGEUR_JEU
                self.vx *= -1

        # Animation
        maintenant = pygame.time.get_ticks()
        if maintenant - self.dernier_anim > self.vitesse_anim:
            self.dernier_anim = maintenant
            self.index_frame = (self.index_frame + 1) % len(self.frames)
            self.image = self.frames[self.index_frame]


class UFO(pygame.sprite.Sprite):
    """UFO pour le niveau 2 - rapide et zigzag"""

    def __init__(self):
        super().__init__()

        # Taille aléatoire
        scale = random.randint(50, 80)
        self.largeur = scale
        self.hauteur = int(scale * 0.6)

        # Position de départ
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)
        self.rect.x = random.randint(0, LARGEUR_JEU - self.largeur)
        self.rect.y = -self.hauteur

        # Vitesse plus rapide que les tornades
        self.vy = random.randint(4, 7)

        # Mouvement zigzag
        self.vx = random.choice([-4, -3, 3, 4])
        self.zigzag_timer = 0
        self.zigzag_interval = random.randint(20, 40)  # Changement de direction fréquent

        # Stats
        self.pv = 2
        self.max_pv = 2
        self.valeur = 20

        # Charger l'image UFO
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chemin = os.path.join(dossier, "assets", "images", "ufo.png")
        try:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(chemin).convert_alpha(),
                (self.largeur, self.hauteur)
            )
        except:
            # Image par défaut si ufo.png n'existe pas
            self.image = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
            # Dessiner une soucoupe volante simple
            pygame.draw.ellipse(self.image, (150, 150, 150), (0, self.hauteur // 3, self.largeur, self.hauteur // 2))
            pygame.draw.ellipse(self.image, (100, 100, 255),
                                (self.largeur // 4, 0, self.largeur // 2, self.hauteur // 3))

        self.rect.size = self.image.get_size()

    def update(self):
        """Met à jour l'UFO"""
        # Mouvement vertical
        self.rect.y += self.vy

        # Mouvement horizontal zigzag
        self.rect.x += self.vx

        # Changement de direction pour zigzag
        self.zigzag_timer += 1
        if self.zigzag_timer >= self.zigzag_interval:
            self.zigzag_timer = 0
            self.vx = -self.vx + random.choice([-1, 0, 1])  # Variation aléatoire
            self.zigzag_interval = random.randint(20, 40)

        # Rebond sur les bords
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        elif self.rect.right >= LARGEUR_JEU:
            self.rect.right = LARGEUR_JEU
            self.vx = -abs(self.vx)


class Meteorite(pygame.sprite.Sprite):
    """Météorite pour le niveau 3 - rapide et zigzag comme les UFO"""

    def __init__(self):
        super().__init__()

        # Taille aléatoire
        scale = random.randint(60, 100)
        self.largeur = scale
        self.hauteur = scale

        # Position de départ
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)
        self.rect.x = random.randint(0, LARGEUR_JEU - self.largeur)
        self.rect.y = -self.hauteur

        # Vitesse plus rapide
        self.vy = random.randint(5, 8)

        # Mouvement zigzag
        self.vx = random.choice([-5, -4, 4, 5])
        self.zigzag_timer = 0
        self.zigzag_interval = random.randint(15, 35)

        # Stats
        self.pv = 3
        self.max_pv = 3
        self.valeur = 25


        # Charger l'image de la météorite
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chemin = os.path.join(dossier, "assets", "images", "Meteorite.png")

        try:
            # Charger Meteorite.png
            self.image = pygame.image.load(chemin).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (self.largeur, self.hauteur))
        except:
            # Image par défaut si Meteorite.png n'existe pas
            self.image = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
            # Dessiner une météorite simple (cercle rocheux avec cratères)
            pygame.draw.circle(self.image, (100, 80, 60),
                               (self.largeur // 2, self.hauteur // 2), self.largeur // 2)
            pygame.draw.circle(self.image, (70, 50, 40),
                               (self.largeur // 2, self.hauteur // 2), self.largeur // 3)
            # Quelques cratères
            pygame.draw.circle(self.image, (50, 40, 30),
                               (self.largeur // 3, self.hauteur // 3), self.largeur // 8)
            pygame.draw.circle(self.image, (50, 40, 30),
                               (2 * self.largeur // 3, 2 * self.hauteur // 3), self.largeur // 10)

        self.rect.size = self.image.get_size()

    def update(self):
        """Met à jour la météorite"""
        # Mouvement vertical
        self.rect.y += self.vy

        # Mouvement horizontal zigzag
        self.rect.x += self.vx

        # Changement de direction pour zigzag
        self.zigzag_timer += 1
        if self.zigzag_timer >= self.zigzag_interval:
            self.zigzag_timer = 0
            self.vx = -self.vx + random.choice([-1, 0, 1])
            self.zigzag_interval = random.randint(15, 35)

        # Rebond sur les bords
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        elif self.rect.right >= LARGEUR_JEU:
            self.rect.right = LARGEUR_JEU
            self.vx = -abs(self.vx)


class Comet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Taille aléatoire RÉDUITE
        scale = random.randint(50, 80)  # Avant : 70-120
        self.largeur = scale
        self.hauteur = scale

        # Position de départ - ARRIVE SEULEMENT DU HAUT
        self.rect = pygame.Rect(0, 0, self.largeur, self.hauteur)

        # Vient du haut uniquement
        self.rect.x = random.randint(0, LARGEUR_JEU - self.largeur)
        self.rect.y = -self.hauteur
        self.vx = random.choice([-4, -3, -2, 2, 3, 4])  # Avant : -6 à 6, maintenant -4 à 4
        self.vy = random.randint(2, 4)  # Avant : 4-7, maintenant 2-4

        # Stats - Plus fortes que les UFO (2 PV) mais pas trop difficiles
        self.pv = 7  # 7 points de vie (entre UFO et l'ancienne valeur de 10)
        self.max_pv = 7
        self.valeur = 25 # Avant : 25 points

        # --- ANIMATION : CHARGER STRIP 4 FRAMES ---
        self.frames = []
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        strip_path = os.path.join(dossier, "assets", "images", "comete_strip4.png")

        try:
            # Charger la strip d'animation (4 frames)
            strip_image = pygame.image.load(strip_path).convert_alpha()
            strip_width = strip_image.get_width()
            frame_width = strip_width // 4
            frame_height = strip_image.get_height()

            # Diviser la strip en 4 frames et redimensionner
            for i in range(4):
                frame = strip_image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.smoothscale(frame, (self.largeur, self.hauteur))
                self.frames.append(frame)

            print(f"[INFO] Animation comète chargée: {strip_path}")
        except Exception as e:
            print(f"[WARN] Erreur chargement animation comète: {e}")
            # Fallback : charger l'image classique
            chemin = os.path.join(dossier, "assets", "images", "comete.png")
            try:
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.smoothscale(img, (self.largeur, self.hauteur))
                self.frames.append(img)
            except:
                # Image par défaut si comete.png n'existe pas
                s = pygame.Surface([self.largeur, self.hauteur], pygame.SRCALPHA)
                # Dessiner une comète (cercle rocheux avec queue de feu)
                pygame.draw.circle(s, (150, 100, 70),
                                   (self.largeur // 2, self.hauteur // 2), self.largeur // 2)
                pygame.draw.circle(s, (255, 100, 0),
                                   (self.largeur // 3, self.hauteur // 3), self.largeur // 4, 0)
                pygame.draw.circle(s, (255, 150, 0),
                                   (self.largeur // 4, self.hauteur // 4), self.largeur // 5, 0)
                self.frames.append(s)

        self.index_frame = 0
        self.image = self.frames[self.index_frame]
        self.dernier_anim = pygame.time.get_ticks()
        self.vitesse_anim = 100

    def update(self):
        """Met à jour la comète - rebondit sur les côtés et le haut seulement"""
        # Mouvement diagonal
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Rebond sur les bords GAUCHE et DROITE
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)  # Inverse direction X
        elif self.rect.right >= LARGEUR_JEU:
            self.rect.right = LARGEUR_JEU
            self.vx = -abs(self.vx)  # Inverse direction X

        # Rebond sur le bord HAUT uniquement (pas le bas)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)  # Inverse direction Y

        # Animation
        if self.frames and len(self.frames) > 1:
            maintenant = pygame.time.get_ticks()
            if maintenant - self.dernier_anim > self.vitesse_anim:
                self.dernier_anim = maintenant
                self.index_frame = (self.index_frame + 1) % len(self.frames)
                self.image = self.frames[self.index_frame]