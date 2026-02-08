"""
Classe principale du jeu
"""
import os
import random
import pygame
from utils import *
from classes.vfx import GestionnaireVFX
from classes.gestionnaire_musique import GestionnaireMusique
from classes.bouton import Bouton, BoutonImage
from classes.soldat import Soldat
from classes.lecteur_video import LecteurVideo
from classes.audio_intro import AudioIntro

# Racine du projet (dossier parent de 'classes')
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Jeu:
    """Classe principale gérant le jeu"""

    def __init__(self):
        self.etat = "MENU"
        self.plein_ecran = False

        try:
            assurer_images_assets()
        except Exception:
            pass

        self.musique = GestionnaireMusique()
        self.vfx = GestionnaireVFX()
        self.img_vie_ui = charger_image_transparente("vie.png", (50, 50))

        self.scroll_offset = 0
        self.scroll_dragging = False
        self.scroll_drag_start = 0

        # Menu stars animation
        self.etoiles = [
            {"x": random.randint(0, LARGEUR_JEU),
             "y": random.randint(0, HAUTEUR_JEU // 2),
             "alpha": random.randint(150, 255),
             "rayon": random.randint(2, 3)}
            for _ in range(35)
        ]

        # Falling images animation
        self.charger_falling_images()
        self.fallings = [
            {"x": random.randint(0, LARGEUR_JEU - 60),
             "y": random.randint(-600, -60),
             "vitesse": random.uniform(1, 3)}
            for _ in range(10)
        ]

        # Trump GIF animation
        self.charger_gif_trump()
        self.gif_index = 0
        self.gif_timer = 0
        self.gif_playing = False
        self.GIF_SPEED = 5

        # Trump logo
        self.charger_logo_trump()

        # Video and audio paths for intro and levels
        self.video_intro_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon film.mp4")
        self.audio_intro_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon-film.mp3")

        self.video_niveau2_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon film 1.mp4")
        self.audio_niveau2_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon-film-1.mp3")

        self.video_niveau3_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon film 2.mp4")
        self.audio_niveau3_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon-film-2.mp3")

        self.video_niveau4_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon film 3.mp4")
        self.audio_niveau4_path = os.path.join(PROJ_ROOT, "assets", "video", "Mon-film-3.mp3")

        self.video_intro = None
        self.video_frame = None
        self.video_position = 0

        self.audio_intro = AudioIntro()
        self.audio_intro.charger(self.audio_intro_path)

        self.audio_niveau2 = AudioIntro()
        self.audio_niveau2.charger(self.audio_niveau2_path)

        self.audio_niveau3 = AudioIntro()
        self.audio_niveau3.charger(self.audio_niveau3_path)

        self.audio_niveau4 = AudioIntro()
        chargement_n4 = self.audio_niveau4.charger(self.audio_niveau4_path)
        if not chargement_n4:
            print(f"[WARN] Impossible de charger audio niveau 4 depuis: {self.audio_niveau4_path}")

        self.charger_video_intro()

        self.creer_menus()
        self.reset_partie()
        self.charger_fond_niveau(1)
        self.charger_fond_menu()

        self.FONTS = charger_polices()

        # Easter egg system
        self.cles_trouvees = set()
        self.niveau_infini_debloque = False

        # DEBUG MODE
        self.debug_mode = False
        self.debug_invincible = False
        self.debug_infinite_ennemis = False
        self.debug_game_speed = 1.0  # Multiplicateur de vitesse (1.0 = normal)
        self.debug_spawner_actif = False
        self.debug_argent_infini = False  # Argent infini

        self.musique.jouer_musique_menu()

    def charger_logo_trump(self):
        """Charge le logo Trump"""
        dossier = PROJ_ROOT
        chemin = os.path.join(dossier, "assets", "images", "logo-trump.png")
        try:
            self.logo_trump = pygame.image.load(chemin).convert_alpha()
            self.logo_trump = pygame.transform.scale(self.logo_trump, (90, 80))
            self.logo_rect = self.logo_trump.get_rect()
            self.logo_rect.bottomright = (LARGEUR_JEU - 20, HAUTEUR_JEU - 20)
        except Exception as e:
            print(f"[WARN] Impossible de charger logo '{chemin}': {e}")
            self.logo_trump = pygame.Surface((90, 80), pygame.SRCALPHA)
            pygame.draw.circle(self.logo_trump, ROUGE, (45, 40), 35)
            self.logo_rect = self.logo_trump.get_rect()
            self.logo_rect.bottomright = (LARGEUR_JEU - 20, HAUTEUR_JEU - 20)

    def charger_gif_trump(self):
        """Charge les frames du GIF Trump"""
        self.gif_frames = []
        dossier = PROJ_ROOT
        for i in range(12):
            chemin = os.path.join(dossier, "assets", "images", "gif_trump", f"frame_{i}.png")
            try:
                frame = pygame.image.load(chemin).convert_alpha()
                frame = pygame.transform.scale(frame, (300, 300))
                self.gif_frames.append(frame)
            except Exception as e:
                print(f"[WARN] Impossible de charger frame GIF '{chemin}': {e}")
                frame = pygame.Surface((300, 300), pygame.SRCALPHA)
                pygame.draw.circle(frame, ROUGE, (150, 150), 100)
                self.gif_frames.append(frame)

    def charger_falling_images(self):
        """Charge l'image falling.webp"""
        dossier = PROJ_ROOT
        chemin = os.path.join(dossier, "assets", "images", "falling.webp")
        try:
            self.falling_img = pygame.image.load(chemin).convert_alpha()
            self.falling_img = pygame.transform.scale(self.falling_img, (60, 45))
            print(f"[INFO] falling image chargée depuis: {chemin}")
        except Exception as e:
            print(f"[WARN] Impossible de charger falling image '{chemin}': {e}")
            self.falling_img = pygame.Surface((60, 45), pygame.SRCALPHA)
            pygame.draw.ellipse(self.falling_img, (200, 200, 200), (0, 0, 60, 45))

    def charger_video_intro(self):
        """Prépare la vidéo d'intro (ne la lance pas tout de suite)"""
        if os.path.exists(self.video_intro_path):
            try:
                print(f"[INFO] Préparation vidéo intro: {self.video_intro_path}")
                self.video_intro_prete = True
            except Exception as e:
                print(f"[WARN] Erreur lors de la préparation vidéo: {e}")
                self.video_intro_prete = False
        else:
            print(f"[WARN] Vidéo intro introuvable: {self.video_intro_path}")
            self.video_intro_prete = False

    def lancer_video_intro(self):
        """Lance la vidéo d'intro (appelée quand l'utilisateur clique sur Jouer)"""
        if self.video_intro_prete and os.path.exists(self.video_intro_path):
            try:
                self.musique.arreter_musique()
                self.lecteur_video = LecteurVideo(self.video_intro_path, self.audio_intro_path)
                if self.lecteur_video.video:
                    self.etat = "VIDEO_INTRO"
                    self.clock_video = pygame.time.Clock()
                    print("[INFO] Vidéo intro lancée")
                else:
                    print("[WARN] Impossible de charger la vidéo intro")
                    self.demarrer_jeu()
            except Exception as e:
                print(f"[WARN] Erreur lors du lancement vidéo: {e}")
                self.demarrer_jeu()
        else:
            self.demarrer_jeu()

    def demarrer_jeu(self):
        """Lance le jeu directement (sans vidéo)"""
        self.reset_partie()
        self.etat = "JEU"
        pygame.mouse.set_visible(False)
        self.musique.jouer_musique_niveau(1)

    def charger_fond_menu(self):
        dossier = PROJ_ROOT
        chemins = [
            os.path.join(dossier, "assets", "images", "back.jpg"),
            os.path.join(dossier, "assets", "images", "fond_usa.png"),
        ]

        for chemin_fond in chemins:
            if os.path.exists(chemin_fond):
                try:
                    self.fond_menu = pygame.image.load(chemin_fond).convert()
                    self.fond_menu = pygame.transform.scale(self.fond_menu, (LARGEUR_JEU, HAUTEUR_JEU))
                    print(f"[INFO] fond_menu chargé depuis: {chemin_fond}")
                    return
                except Exception as e:
                    print(f"[WARN] Erreur en chargeant fond menu '{chemin_fond}': {e}")
                    break

        print("[WARN] Aucun fond de menu trouvé, utilisation d'un fond par défaut")
        self.fond_menu = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
        self.fond_menu.fill(BLEU_NUIT)

    def charger_fond_niveau(self, niveau):
        """Change le fond selon le niveau"""
        dossier = PROJ_ROOT
        if niveau == 2:
            nom_fichier = "Ciel.png"
        elif niveau == 3 or niveau == 4:
            nom_fichier = "espace.png"
        else:
            nom_fichier = "fond.png"

        img_path = os.path.join(dossier, "assets", "images", nom_fichier)
        if os.path.exists(img_path):
            try:
                loaded = pygame.image.load(img_path).convert()
                scale = max(LARGEUR_JEU / loaded.get_width(), HAUTEUR_JEU / loaded.get_height())
                self.image_fond = pygame.transform.smoothscale(
                    loaded,
                    (int(loaded.get_width() * scale), int(loaded.get_height() * scale))
                )
            except Exception as e:
                print(f"[WARN] Erreur en chargeant fond niveau '{img_path}': {e}")
                self.creer_fond_par_defaut()
        else:
            print(f"[WARN] fond niveau introuvable: {img_path}")
            self.creer_fond_par_defaut()

        self.fond_x = (LARGEUR_JEU - self.image_fond.get_width()) // 2
        self.hauteur_fond = self.image_fond.get_height()
        self.fond_y1, self.fond_y2 = 0, -self.hauteur_fond
        self.vitesse_fond = 1.5

    def creer_fond_par_defaut(self):
        """Crée un fond par défaut si aucune image n'est trouvée"""
        self.image_fond = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
        for i in range(HAUTEUR_JEU):
            c = int(i / HAUTEUR_JEU * 50)
            pygame.draw.line(self.image_fond, (c, c, c + 20), (0, i), (LARGEUR_JEU, i))

    # ----------------------- MISE À JOUR -----------------------
    def update_fond(self):
        """Met à jour le défilement du fond"""
        self.fond_y1 += self.vitesse_fond
        self.fond_y2 += self.vitesse_fond
        if self.fond_y1 >= self.hauteur_fond:
            self.fond_y1 = self.fond_y2 - self.hauteur_fond
        if self.fond_y2 >= self.hauteur_fond:
            self.fond_y2 = self.fond_y1 - self.hauteur_fond

    def reset_partie(self):
        """Réinitialise la partie"""
        self.joueur = Soldat(1)
        self.all_sprites = pygame.sprite.Group(self.joueur)
        self.mobs = pygame.sprite.Group()
        self.balles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.argent = 0
        self.score_total = 0
        self.niveau = 1
        self.niveau_precedent = 0
        self.vies = 3
        self.dernier_spawn = 0

        # Système de clés - NE PAS réinitialiser cles_trouvees (conservées entre parties)
        self.cle_niveau_spawned = False

        # Fermer le menu options de la boutique si ouvert
        self.options_boutique_ouvert = False

        if hasattr(self, 'boss'):
            delattr(self, 'boss')
        if hasattr(self, 'boss_apparu'):
            delattr(self, 'boss_apparu')
        if hasattr(self, 'boss_debut'):
            delattr(self, 'boss_debut')
        if hasattr(self, 'boss_temps_limite'):
            delattr(self, 'boss_temps_limite')

        self.temps_niveau = 60
        self.debut_niveau = pygame.time.get_ticks()
        self.temps_pause = 0
        self.temps_pause_debut = 0

        self.charger_fond_niveau(1)

    def creer_menus(self):
        """Crée tous les boutons des menus"""
        cx, cy = LARGEUR_JEU // 2, HAUTEUR_JEU // 2
        dossier = os.path.dirname(os.path.dirname(__file__))

        def charger_image_bouton(nom):
            chemin = os.path.join(dossier, "assets", "images", nom)
            if os.path.exists(chemin):
                img = pygame.image.load(chemin).convert_alpha()
                return pygame.transform.scale(img, (350, 250))
            return None

        btn_jouer_img = charger_image_bouton("bouton-jouer.png")
        btn_option_img = charger_image_bouton("bouton-options.png")
        btn_quitter_img = charger_image_bouton("bouton-quitter.png")

        y_start = 250
        espacement = 120

        # Bouton niveau infini (juste au-dessus du bouton Jouer avec 10px d'espacement)
        # Bouton Jouer : centre à y=250, hauteur 250px → haut à y=125
        # Bouton infini : hauteur 60px, on veut 10px d'espacement
        # Centre du bouton infini à y=115
        self.btn_niveau_infini = Bouton(cx, 115, 300, 60, "🔥 NIVEAU INFINI",
                                        lambda: "LANCER_NIVEAU_INFINI")

        self.btns_menu_img = [
            BoutonImage(btn_jouer_img, cx, y_start, lambda: "LANCER_JEU"),
            BoutonImage(btn_option_img, cx, y_start + espacement, lambda: "ALLER_OPTIONS"),
            BoutonImage(btn_quitter_img, cx, y_start + 2 * espacement, lambda: "QUITTER")
        ]

        # Boutons pause (en bas)
        btn_width = 280
        btn_spacing = 40
        total_width = (btn_width * 2) + btn_spacing
        start_x = cx - (total_width // 2) + (btn_width // 2)

        self.btns_pause = [
            Bouton(start_x, HAUTEUR_JEU - 100, btn_width, 60, "REPRENDRE", lambda: "REPRENDRE"),
            Bouton(start_x + btn_width + btn_spacing, HAUTEUR_JEU - 100, btn_width, 60, "MENU PRINCIPAL",
                   lambda: "RETOUR_MENU")
        ]

        # Bouton OPTIONS dans la boutique (en haut à droite)
        audio_btn_width = 180
        audio_x = cx + 200
        self.btn_options_boutique = Bouton(audio_x, 120, audio_btn_width, 50, "⚙️ OPTIONS",
                                           lambda: "OUVRIR_OPTIONS_BOUTIQUE")

        # Sous-menu options (initialement caché)
        self.options_boutique_ouvert = False
        self.btns_options_boutique_submenu = [
            Bouton(audio_x, 180, audio_btn_width, 50, "Musique: ON", lambda: "TOGGLE_MUSIQUE_PAUSE"),
            Bouton(audio_x, 240, audio_btn_width, 50, "Effets: ON", lambda: "TOGGLE_EFFETS_PAUSE"),
            Bouton(audio_x, 300, audio_btn_width, 50, "Plein Écran: NON", lambda: "TOGGLE_FULLSCREEN_PAUSE")
        ]

        self.btns_opt = [
            Bouton(cx, cy - 120, 400, 60, "Musique : ON", lambda: "TOGGLE_MUSIQUE"),
            Bouton(cx, cy - 40, 400, 60, "Effets : ON", lambda: "TOGGLE_EFFETS"),
            Bouton(cx, cy + 40, 400, 60, "Plein Écran : NON", lambda: "TOGGLE_FULLSCREEN"),
            Bouton(cx, cy + 140, 300, 60, "RETOUR", lambda: "RETOUR_DEPUIS_OPT")
        ]

    def draw_etoiles(self, surface):
        """Dessine les étoiles scintillantes du menu"""
        for e in self.etoiles:
            surf = pygame.Surface((e["rayon"] * 2, e["rayon"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 255, e["alpha"]),
                               (e["rayon"], e["rayon"]), e["rayon"])
            surface.blit(surf, (e["x"], e["y"]))
            e["alpha"] += random.randint(-4, 4)
            e["alpha"] = max(150, min(255, e["alpha"]))

    def draw_fallings(self, surface):
        """Dessine les images qui tombent"""
        for f in self.fallings:
            surface.blit(self.falling_img, (f["x"], f["y"]))
            f["y"] += f["vitesse"]
            if f["y"] > HAUTEUR_JEU:
                f["y"] = random.randint(-600, -60)
                f["x"] = random.randint(0, LARGEUR_JEU - 60)

    def draw_gif(self, surface):
        """Affiche le GIF Trump animé"""
        if not self.gif_playing:
            return

        self.gif_timer += 1
        if self.gif_timer >= self.GIF_SPEED:
            self.gif_timer = 0
            self.gif_index += 1
            if self.gif_index >= len(self.gif_frames):
                self.gif_index = 0

        frame = self.gif_frames[self.gif_index]
        rect = frame.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2))
        surface.blit(frame, rect)

    def afficher_titre(self, surface, temps, texte=None, couleur=None):
        """Affiche le titre animé du menu"""
        if texte is None:
            texte = "Independence Day"
        if couleur is None:
            couleur = OR

        texte_surface = render_text_usa_surface(self.FONTS['titre'], texte)
        x = LARGEUR_JEU // 2 - texte_surface.get_width() // 2
        y = 30

        # Ombre
        ombre = texte_surface.copy()
        ombre.fill((0, 0, 0, 140), special_flags=pygame.BLEND_RGBA_MULT)
        draw_waving_text(surface, ombre, x + 6, y + 6, temps)
        draw_waving_text(surface, texte_surface, x, y, temps)

        # Sous-titre
        SUBTITRE = "The 250th Celebration of Independence"
        texte_sub = self.FONTS['subtitre'].render(SUBTITRE, True, BLANC)
        x_sub = LARGEUR_JEU // 2 - texte_sub.get_width() // 2
        y_sub = y + texte_surface.get_height()

        ombre_sub = texte_sub.copy()
        ombre_sub.fill((178, 34, 34, 180), special_flags=pygame.BLEND_RGBA_MULT)
        draw_waving_text(surface, ombre_sub, x_sub + 4, y_sub + 4, temps)
        draw_waving_text(surface, texte_sub, x_sub, y_sub, temps)