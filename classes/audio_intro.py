"""
Gestionnaire audio d'intro - Indépendant de la vidéo
"""
import pygame
import os


class AudioIntro:
    """Gère l'audio d'intro indépendamment"""

    def __init__(self):
        self.audio_path = None
        self.en_cours = False
        self.demarrage = 0

    def charger(self, chemin_audio):
        """Charge le fichier audio"""
        if os.path.exists(chemin_audio):
            self.audio_path = chemin_audio
            print(f"[INFO] Audio intro trouvé: {chemin_audio}")
            return True
        else:
            print(f"[WARN] Audio intro introuvable: {chemin_audio}")
            return False

    def jouer(self):
        """Lance la lecture de l'audio"""
        if not self.audio_path:
            print("[WARN] Aucun audio chargé")
            return False

        try:
            # Vérifier que le fichier existe avant de jouer
            import os
            if not os.path.exists(self.audio_path):
                print(f"[ERREUR] Fichier audio introuvable: {self.audio_path}")
                return False

            # Arrêter toute musique en cours
            pygame.mixer.music.stop()

            # Charger et jouer l'audio intro
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.set_volume(1.0)  # Volume max
            pygame.mixer.music.play()

            self.en_cours = True
            self.demarrage = pygame.time.get_ticks()

            print(f"[INFO] Audio intro lancé depuis: {self.audio_path}")
            return True

        except Exception as e:
            print(f"[ERREUR] Impossible de jouer l'audio: {e}")
            return False

    def arreter(self):
        """Arrête l'audio"""
        try:
            pygame.mixer.music.stop()
            self.en_cours = False
            print("[INFO] Audio intro arrêté")
        except Exception as e:
            print(f"[WARN] Erreur arrêt audio: {e}")

    def est_en_cours(self):
        """Vérifie si l'audio est en cours de lecture"""
        if self.en_cours:
            # Vérifier si la musique joue toujours
            if not pygame.mixer.music.get_busy():
                self.en_cours = False
                return False
            return True
        return False

    def get_volume(self):
        """Retourne le volume actuel"""
        return pygame.mixer.music.get_volume()

    def set_volume(self, volume):
        """Définit le volume (0.0 à 1.0)"""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))