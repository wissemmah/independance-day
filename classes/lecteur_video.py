"""
Lecteur de vidéo simple pour pygame avec son
"""
import pygame
import os

try:
    import cv2

    VIDEO_DISPONIBLE = True
except ImportError:
    VIDEO_DISPONIBLE = False
    print("[WARN] opencv-python non installé (pip install opencv-python)")


class LecteurVideo:
    """Lecteur vidéo avec son pour pygame"""

    def __init__(self, chemin_video, chemin_audio=None):
        self.chemin = chemin_video
        self.video = None
        self.fps = 30
        self.frame_actuelle = None
        self.termine = False
        self.frame_count = 0
        self.total_frames = 0

        if VIDEO_DISPONIBLE and os.path.exists(chemin_video):
            try:
                self.video = cv2.VideoCapture(chemin_video)
                self.fps = self.video.get(cv2.CAP_PROP_FPS)
                self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
                print(f"[INFO] Vidéo chargée: {os.path.basename(chemin_video)}")
                print(f"       FPS: {self.fps}, Frames: {self.total_frames}")

                # Load optional audio
                if chemin_audio:
                    self.charger_audio(chemin_audio)

            except Exception as e:
                print(f"[WARN] Erreur chargement vidéo: {e}")
                self.video = None

    def charger_audio(self, chemin_audio):
        """Loads and plays audio file"""
        if os.path.exists(chemin_audio):
            try:
                pygame.mixer.music.load(chemin_audio)
                pygame.mixer.music.play()
                print(f"[INFO] Audio lancé: {os.path.basename(chemin_audio)}")
            except Exception as e:
                print(f"[WARN] Erreur chargement audio: {e}")
        else:
            print(f"[WARN] Fichier audio introuvable: {chemin_audio}")

    def lire_frame(self):
        """Reads next video frame"""
        if not self.video or self.termine:
            return None

        ret, frame = self.video.read()
        if not ret:
            self.termine = True
            return None

        # Convert BGR (OpenCV) to RGB (Pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Transpose for pygame
        frame = frame.swapaxes(0, 1)

        self.frame_actuelle = pygame.surfarray.make_surface(frame)
        self.frame_count += 1

        return self.frame_actuelle

    def redimensionner_frame(self, largeur, hauteur):
        """Resize current frame"""
        if self.frame_actuelle:
            return pygame.transform.scale(self.frame_actuelle, (largeur, hauteur))
        return None

    def reset(self):
        """Reset video to beginning"""
        if self.video:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.termine = False
            self.frame_count = 0
            try:
                pygame.mixer.music.rewind()
            except:
                pass

    def fermer(self):
        """Free resources and stop playback"""
        if self.video:
            self.video.release()
            self.video = None

        try:
            pygame.mixer.music.stop()
        except:
            pass

    def est_termine(self):
        """Check if video has finished"""
        return self.termine

    def get_duree(self):
        """Get video duration in seconds"""
        if self.video and self.fps > 0:
            return self.total_frames / self.fps
        return 0