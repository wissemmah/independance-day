"""
Gestionnaire de musique et effets sonores
"""
import pygame
import os


class GestionnaireMusique:
    """Gère la musique et les effets sonores du jeu"""

    def __init__(self):
        self.volume_musique = 0.5
        self.volume_effets = 0.7
        self.musique_active = True
        self.effets_actifs = True
        self.musiques_niveaux = {}
        self.musique_menu = None
        self.effets_sonores = {}
        self.musique_en_cours = None
        self.charger_musiques()
        self.charger_musique_menu()
        self.charger_effets()

    def charger_musiques(self):
        """Charge les musiques des différents niveaux"""
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dossier_musiques = os.path.join(dossier, "assets", "musiques")
        os.makedirs(dossier_musiques, exist_ok=True)

        noms_niveaux = {
            1: ["Terre.mp3", "Terre.ogg", "Terre.wav", "terre.mp3", "terre.ogg"],
            2: ["Ciel.mp3", "Ciel.ogg", "Ciel.wav", "ciel.mp3", "ciel.ogg"],
            3: ["Espace.mp3", "Espace.ogg", "Espace.wav", "espace.mp3", "espace.ogg"],
            4: ["boss.mp3", "boss.ogg", "boss.wav", "Boss.mp3", "Boss.ogg"]  # Niveau 4 = musique du boss
        }

        for niveau, noms_possibles in noms_niveaux.items():
            for nom in noms_possibles:
                chemin = os.path.join(dossier_musiques, nom)
                if os.path.exists(chemin):
                    self.musiques_niveaux[niveau] = chemin
                    break

    def charger_musique_menu(self):
        """Charge la musique du menu"""
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dossier_musiques = os.path.join(dossier, "assets", "musiques")
        os.makedirs(dossier_musiques, exist_ok=True)

        noms_possibles = ["musiquedebut.wav", "musiquedebut.mp3", "musiquedebut.ogg", "menu.wav", "menu.mp3"]

        for nom in noms_possibles:
            chemin = os.path.join(dossier_musiques, nom)
            if os.path.exists(chemin):
                self.musique_menu = chemin
                break

    def charger_effets(self):
        """Charge les effets sonores"""
        dossier = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dossier_sons = os.path.join(dossier, "assets", "sons")
        os.makedirs(dossier_sons, exist_ok=True)

        noms_effets = {
            "tir": ["tir.wav", "tir.ogg", "shoot.wav", "shoot.ogg"],
            "explosion": ["explosion.wav", "explosion.ogg", "boom.wav"],
            "degats": ["degats.wav", "degats.ogg", "hit.wav", "hurt.wav"],
            "piece": ["piece.wav", "piece.ogg", "coin.wav", "money.wav"],
            "gameover": ["gameover.wav", "gameover.ogg", "death.wav"],
            "extra_vie": ["piece.wav", "heal.wav", "heart.wav", "soin.wav"],
            "nuke": ["nuke.wav", "bomb.wav"],
            "levelup": ["levelup.wav", "upgrade.wav", "powerup.wav"],
            "coin": ["Coin.wav", "coin.wav", "coins.wav", "piece.wav", "money.wav"],
            "vent": ["vent.wav", "wind.wav", "tornado.wav"]  # Pour les tornades
        }

        for nom_effet, fichiers_possibles in noms_effets.items():
            for fichier in fichiers_possibles:
                chemin = os.path.join(dossier_sons, fichier)
                if os.path.exists(chemin):
                    try:
                        self.effets_sonores[nom_effet] = pygame.mixer.Sound(chemin)
                        self.effets_sonores[nom_effet].set_volume(self.volume_effets)
                        break
                    except:
                        pass

    def jouer_musique_menu(self):
        """Joue la musique du menu"""
        if not self.musique_active:
            return
        if self.musique_menu and self.musique_en_cours != self.musique_menu:
            try:
                pygame.mixer.music.load(self.musique_menu)
                pygame.mixer.music.set_volume(self.volume_musique)
                pygame.mixer.music.play(-1)  # -1 pour boucle infinie
                self.musique_en_cours = self.musique_menu
            except:
                pass

    def jouer_musique_niveau(self, numero_niveau):
        """Joue la musique du niveau spécifié"""
        if not self.musique_active:
            return

        # Niveau infini : cycle entre les 4 musiques
        if numero_niveau == 999:
            self.jouer_musique_niveau_infini()
            return

        if numero_niveau in self.musiques_niveaux:
            musique = self.musiques_niveaux[numero_niveau]
            if self.musique_en_cours != musique:
                try:
                    pygame.mixer.music.load(musique)
                    pygame.mixer.music.set_volume(self.volume_musique)
                    pygame.mixer.music.play(-1)
                    self.musique_en_cours = musique
                except:
                    pass

    def arreter_musique(self):
        """Arrête la musique"""
        pygame.mixer.music.stop()
        self.musique_en_cours = None

    def basculer_musique(self):
        """Active/désactive la musique"""
        self.musique_active = not self.musique_active
        if not self.musique_active:
            self.arreter_musique()
        else:
            self.jouer_musique_menu()
        return self.musique_active

    def basculer_effets(self):
        """Active/désactive les effets sonores"""
        self.effets_actifs = not self.effets_actifs
        return self.effets_actifs

    def jouer_effet(self, nom_effet):
        """Joue un effet sonore"""
        if self.effets_actifs and nom_effet in self.effets_sonores:
            self.effets_sonores[nom_effet].play()

    def jouer_musique_niveau_infini(self):
        """Lance le cycle des 4 musiques pour le niveau infini"""
        if not self.musique_active:
            return

        # Créer une playlist avec les 4 musiques
        if not hasattr(self, 'playlist_infini'):
            self.playlist_infini = []
            for i in range(1, 5):
                if i in self.musiques_niveaux:
                    self.playlist_infini.append(self.musiques_niveaux[i])
            self.index_playlist = 0

        # Si la musique n'est pas en cours, lancer la première
        if not pygame.mixer.music.get_busy() and self.playlist_infini:
            try:
                musique = self.playlist_infini[self.index_playlist]
                pygame.mixer.music.load(musique)
                pygame.mixer.music.set_volume(self.volume_musique)
                pygame.mixer.music.play()
                self.musique_en_cours = musique

                # Passer à la suivante pour le prochain appel
                self.index_playlist = (self.index_playlist + 1) % len(self.playlist_infini)
            except:
                pass