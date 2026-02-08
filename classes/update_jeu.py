"""
Logique de mise à jour du jeu
"""
import pygame
import random
from constantes import *
from classes.ennemis import Tornade, UFO, Comet
from classes.soldat import Soldat
from classes.items import ItemVie, ItemCle
from classes.boss import Boss
from classes.Niveau_infini import update_niveau_infini


def update_jeu(jeu_instance):
    """Met à jour la logique du jeu"""

    # SI NIVEAU INFINI (999), utiliser la logique spéciale
    if jeu_instance.niveau == 999:
        update_niveau_infini(jeu_instance)
        return  # Sortir, ne pas exécuter la logique normale

    # SINON, logique normale des niveaux 1-4
    jeu_instance.update_fond()
    jeu_instance.vfx.update()
    jeu_instance.all_sprites.update()
    jeu_instance.items.update()

    # Mettre à jour les projectiles du boss
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles[:]:
            projectile.update()
            # Vérifier si le projectile est mort
            if not projectile.rect.colliderect(pygame.Rect(0, 0, LARGEUR_JEU, HAUTEUR_JEU)):
                jeu_instance.boss.projectiles.remove(projectile)

    # Tir automatique
    balles = jeu_instance.joueur.verifier_tir_auto()
    if balles:
        jeu_instance.musique.jouer_effet("tir")
        jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.top, JAUNE, 2)
        for balle in balles:
            jeu_instance.all_sprites.add(balle)
            jeu_instance.balles.add(balle)

    # SPAWN DE LA CLÉ CACHÉE (Easter Egg)
    # La clé apparaît après 30 secondes si elle n'a pas déjà été trouvée dans ce niveau
    if (not jeu_instance.cle_niveau_spawned and
            jeu_instance.niveau not in jeu_instance.cles_trouvees and
            jeu_instance.niveau <= 4):  # Pas dans le niveau infini

        temps_ecoule_niveau = (pygame.time.get_ticks() - jeu_instance.debut_niveau) / 1000

        # DEBUG pour niveau 4
        if jeu_instance.niveau == 4 and temps_ecoule_niveau < 35:
            if int(temps_ecoule_niveau) % 5 == 0:  # Afficher tous les 5 secondes
                print(
                    f"[DEBUG] Niveau 4 - Temps écoulé: {temps_ecoule_niveau:.1f}s - Clé spawned: {jeu_instance.cle_niveau_spawned}")

        if temps_ecoule_niveau >= 30:  # Après 30 secondes
            # Faire apparaître la clé en haut de l'écran (position X aléatoire)
            x_pos = random.randint(100, LARGEUR_JEU - 100)
            cle = ItemCle(x_pos, -50)  # Commence en haut de l'écran
            jeu_instance.items.add(cle)
            jeu_instance.all_sprites.add(cle)
            jeu_instance.cle_niveau_spawned = True
            print(f"[INFO] 🔑 Clé secrète apparue dans le niveau {jeu_instance.niveau} !")

    # --- VÉRIFICATION DU TIMER ET VICTOIRE ---
    temps_ecoule = (pygame.time.get_ticks() - jeu_instance.debut_niveau) / 1000

    # Tous les niveaux durent 2 minutes (120 secondes)
    temps_niveau_actuel = jeu_instance.temps_niveau  # 120 secondes
    temps_restant = temps_niveau_actuel - temps_ecoule

    # VICTOIRE NIVEAU 4 : Tuer le boss
    if jeu_instance.niveau == 4:
        if hasattr(jeu_instance, 'boss') and jeu_instance.boss not in jeu_instance.mobs:
            # Boss vaincu ! Lancer la vidéo de fin
            import os
            from classes.lecteur_video import LecteurVideo
            
            jeu_instance.musique.arreter_musique()
            
            # Vérifier si la vidéo existe
            if os.path.exists(jeu_instance.video_niveau4_path):
                try:
                    jeu_instance.lecteur_video = LecteurVideo(jeu_instance.video_niveau4_path)
                    if jeu_instance.lecteur_video.video:
                        jeu_instance.etat = "VIDEO_NIVEAU4"
                        # Recharger et jouer l'audio
                        if hasattr(jeu_instance, 'audio_niveau4'):
                            jeu_instance.audio_niveau4.jouer()
                            print("[INFO] Audio niveau 4 lancé")
                        jeu_instance.clock_video = pygame.time.Clock()
                        print("[INFO] Vidéo de victoire niveau 4 lancée")
                        return
                except Exception as e:
                    print(f"[WARN] Erreur lors du lancement de la vidéo: {e}")
            
            # Si pas de vidéo, aller directement à l'écran de victoire
            jeu_instance.etat = "VICTOIRE"
            pygame.mouse.set_visible(True)
            return

    # Si le temps est écoulé
    if temps_restant <= 0:
        if jeu_instance.niveau < 4:
            # Passer au niveau suivant après 2 minutes
            jeu_instance.niveau += 1
        elif jeu_instance.niveau == 4:
            # Niveau 4 : si 2 minutes écoulées sans tuer le boss = GAME OVER
            jeu_instance.etat = "GAMEOVER"
            pygame.mouse.set_visible(True)
            jeu_instance.musique.jouer_effet("gameover")
            jeu_instance.musique.arreter_musique()
            return

    # --- TRANSITION ENTRE NIVEAUX ---
    if jeu_instance.niveau != jeu_instance.niveau_precedent and jeu_instance.niveau_precedent != 0:
        jeu_instance.etat = "TRANSITION"
        pygame.mouse.set_visible(True)
        jeu_instance.charger_fond_niveau(jeu_instance.niveau)
        jeu_instance.musique.jouer_musique_niveau(jeu_instance.niveau)
        jeu_instance.niveau_precedent = jeu_instance.niveau
        jeu_instance.vies = jeu_instance.joueur.max_vies  # Réinitialisation au maximum de vies acheté

        # Réinitialiser le flag de spawn de clé pour le nouveau niveau
        jeu_instance.cle_niveau_spawned = False

        # Changer le joueur selon le niveau
        old_stats = {
            'niveau_tir': jeu_instance.joueur.niveau_tir,
            'niveau_cadence': jeu_instance.joueur.niveau_cadence,
            'a_laser': jeu_instance.joueur.a_laser,
            'invincible': jeu_instance.joueur.invincible,
            'fin_invincibilite': jeu_instance.joueur.fin_invincibilite,
            'nukes': jeu_instance.joueur.nukes,
            'max_vies': jeu_instance.joueur.max_vies
        }

        jeu_instance.joueur.kill()
        jeu_instance.joueur = Soldat(jeu_instance.niveau)

        # Restaurer les stats
        jeu_instance.joueur.niveau_tir = old_stats['niveau_tir']
        jeu_instance.joueur.niveau_cadence = old_stats['niveau_cadence']
        jeu_instance.joueur.a_laser = old_stats['a_laser']
        jeu_instance.joueur.invincible = old_stats['invincible']
        jeu_instance.joueur.fin_invincibilite = old_stats['fin_invincibilite']
        jeu_instance.joueur.nukes = old_stats['nukes']
        jeu_instance.joueur.max_vies = old_stats['max_vies']

        jeu_instance.all_sprites.add(jeu_instance.joueur)

        for m in jeu_instance.mobs:
            m.kill()

        # NE PAS réinitialiser debut_niveau ici - on le fait quand on appuie sur ESPACE

    if jeu_instance.niveau_precedent == 0:
        jeu_instance.niveau_precedent = jeu_instance.niveau

    # --- SPAWN CONTRÔLÉ ---
    now = pygame.time.get_ticks()
    nb_mobs = len(jeu_instance.mobs)

    # NIVEAU 4 : BOSS UNIQUEMENT (apparaît au début du niveau)
    if jeu_instance.niveau == 4:
        # Faire apparaître le boss au début du niveau 4
        if not hasattr(jeu_instance, 'boss') and not hasattr(jeu_instance, 'boss_apparu'):
            jeu_instance.boss = Boss()
            jeu_instance.all_sprites.add(jeu_instance.boss)
            jeu_instance.mobs.add(jeu_instance.boss)
            jeu_instance.boss_apparu = True
            print("[INFO] BOSS APPARAÎT ! Vous avez 2 minutes pour le vaincre !")

        # Pas de spawn d'ennemis supplémentaires au niveau 4
        max_ennemis = 0

    # NIVEAU 3 : COMÈTES UNIQUEMENT
    elif jeu_instance.niveau == 3:
        max_ennemis = 3  # Avant : 5, maintenant 3
        delai_spawn = 1200  # Avant : 800ms, maintenant 1200ms (plus lent)

    # NIVEAUX 1 et 2
    else:
        max_ennemis = 2
        delai_spawn = 1000

    if nb_mobs < max_ennemis:
        if now - jeu_instance.dernier_spawn > delai_spawn:
            # NIVEAU 3 : Comètes uniquement
            if jeu_instance.niveau == 3:
                ennemi = Comet()
            # NIVEAU 2 : UFO
            elif jeu_instance.niveau == 2:
                ennemi = UFO()
            # NIVEAU 1 : Tornades
            else:
                ennemi = Tornade(jeu_instance.niveau)

            jeu_instance.all_sprites.add(ennemi)
            jeu_instance.mobs.add(ennemi)
            jeu_instance.dernier_spawn = now

    # Collisions balles/ennemis
    hits = pygame.sprite.groupcollide(jeu_instance.mobs, jeu_instance.balles, False, True)
    for mob, balles_touchees in hits.items():
        mob.pv -= len(balles_touchees)
        jeu_instance.musique.jouer_effet("degats")
        jeu_instance.vfx.ajouter(mob.rect.centerx, mob.rect.centery, JAUNE, 3)

        if mob.pv <= 0:
            # Drop de vache (vie) si on a moins que le maximum de vies
            if random.random() < 0.10 and jeu_instance.vies < jeu_instance.joueur.max_vies:
                vie_item = ItemVie(mob.rect.centerx, mob.rect.centery)
                jeu_instance.items.add(vie_item)

            # Son différent selon le type d'ennemi
            if isinstance(mob, Tornade):
                jeu_instance.musique.jouer_effet("vent")  # 🌪️ Vent pour tornades
            elif isinstance(mob, UFO) or isinstance(mob, Comet):
                jeu_instance.musique.jouer_effet("explosion")  # 💥 Explosion pour UFO et comètes

            mob.kill()
            jeu_instance.score_total += mob.valeur
            jeu_instance.argent += mob.valeur
            jeu_instance.vfx.ajouter(mob.rect.centerx, mob.rect.centery, GRIS_FONCE, 10)

    # Ramassage des items (vies et clés)
    recup_items = pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.items, True)
    for item in recup_items:
        if isinstance(item, ItemVie):
            if jeu_instance.vies < jeu_instance.joueur.max_vies:
                jeu_instance.vies += 1
                jeu_instance.musique.jouer_effet("extra_vie")
                jeu_instance.vfx.ajouter(item.rect.centerx, item.rect.centery, ROUGE, 10)
        elif isinstance(item, ItemCle):
            # Clé ramassée !
            jeu_instance.cles_trouvees.add(jeu_instance.niveau)
            jeu_instance.musique.jouer_effet("coin")
            jeu_instance.vfx.ajouter(item.rect.centerx, item.rect.centery, (255, 215, 0), 20)
            print(f"[INFO] ✨ Clé du niveau {jeu_instance.niveau} trouvée ! ({len(jeu_instance.cles_trouvees)}/4)")

            # Débloquer le niveau infini si toutes les clés sont trouvées
            if len(jeu_instance.cles_trouvees) >= 4:
                jeu_instance.niveau_infini_debloque = True
                print("[INFO] 🔓 NIVEAU INFINI DÉBLOQUÉ !")

    # Collisions joueur/ennemis
    if pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.mobs, True):
        if not jeu_instance.joueur.invincible:
            jeu_instance.vies -= 1
            jeu_instance.vfx.declencher_degats()
            jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG, 15)
            jeu_instance.musique.jouer_effet("degats")

    # Collision laser du boss avec le joueur (enlève 2 vies !)
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss and jeu_instance.boss.laser_actif:
        laser_rect = jeu_instance.boss.get_laser_rect()
        if laser_rect and jeu_instance.joueur.rect.colliderect(laser_rect):
            if not jeu_instance.joueur.invincible:
                jeu_instance.vies -= 2  # Le laser enlève 2 vies !
                jeu_instance.vfx.declencher_degats()
                jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG,
                                         20)
                jeu_instance.musique.jouer_effet("degats")
                # Rendre temporairement invincible pour éviter mort instantanée
                jeu_instance.joueur.invincible = True
                jeu_instance.joueur.fin_invincibilite = pygame.time.get_ticks() + 2000  # 2 secondes

    # Collision projectiles du boss avec le joueur
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles[:]:
            if jeu_instance.joueur.rect.colliderect(projectile.rect):
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 1
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery,
                                             ROUGE_SANG, 10)
                    jeu_instance.musique.jouer_effet("degats")
                jeu_instance.boss.projectiles.remove(projectile)

    # Ennemis hors écran - NE S'APPLIQUE PAS AU NIVEAU 3 et 4 (comètes rebondissent, boss reste en haut)
    if jeu_instance.niveau < 3:
        for m in list(jeu_instance.mobs):
            if m.rect.top > HAUTEUR_JEU:
                m.kill()
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 1
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.musique.jouer_effet("degats")
                    jeu_instance.vfx.ajouter(m.rect.centerx, HAUTEUR_JEU - 10, ROUGE, 5)

    if jeu_instance.vies <= 0:
        jeu_instance.etat = "GAMEOVER"
        pygame.mouse.set_visible(True)
        jeu_instance.musique.jouer_effet("gameover")
        jeu_instance.musique.arreter_musique()