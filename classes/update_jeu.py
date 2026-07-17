"""
Logique de mise à jour du jeu
"""
import os
import pygame
import random
from constantes import *
from classes.ennemis import Tornade, UFO, Comet, Meteorite
from classes.soldat import Soldat
from classes.items import ItemVie, ItemCle
from classes.boss import Boss
from classes.Niveau_infini import update_niveau_infini
from classes.lecteur_video import LecteurVideo


def _passer_niveau_suivant(jeu_instance):
    """Prépare la transition vers le niveau suivant."""
    jeu_instance.niveau += 1


def _appliquer_combo_kill(jeu_instance, mob):
    """Met à jour combo, score et feedback à la destruction d'un ennemi."""
    now = pygame.time.get_ticks()
    if now - jeu_instance.combo_timer <= COMBO_FENETRE_MS:
        jeu_instance.combo += 1
    else:
        jeu_instance.combo = 1
    jeu_instance.combo_timer = now

    bonus = min(jeu_instance.combo - 1, 8) * 5
    points = mob.valeur + bonus
    jeu_instance.score_total += points
    jeu_instance.argent += points
    jeu_instance.ennemis_tues_niveau += 1

    jeu_instance.vfx.declencher_impact(intensite=4 + min(jeu_instance.combo, 6), duree=8)
    jeu_instance.vfx.ajouter(mob.rect.centerx, mob.rect.centery, GRIS_FONCE, 10 + min(jeu_instance.combo, 8))


def _objectif_atteint(jeu_instance):
    objectif = jeu_instance.objectif_kills_actuel()
    return objectif > 0 and jeu_instance.ennemis_tues_niveau >= objectif


def update_jeu(jeu_instance):
    """Met à jour la logique du jeu"""

    if jeu_instance.niveau == 999:
        update_niveau_infini(jeu_instance)
        return

    jeu_instance.update_fond()
    jeu_instance.vfx.update()
    jeu_instance.all_sprites.update()
    jeu_instance.items.update()

    # Expiration du combo
    if jeu_instance.combo > 0 and pygame.time.get_ticks() - jeu_instance.combo_timer > COMBO_FENETRE_MS:
        jeu_instance.combo = 0

    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles[:]:
            projectile.update()
            if not projectile.rect.colliderect(pygame.Rect(0, 0, LARGEUR_JEU, HAUTEUR_JEU)):
                jeu_instance.boss.projectiles.remove(projectile)

    balles = jeu_instance.joueur.verifier_tir_auto()
    if balles:
        jeu_instance.musique.jouer_effet("tir")
        jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.top, JAUNE, 2)
        for balle in balles:
            jeu_instance.all_sprites.add(balle)
            jeu_instance.balles.add(balle)

    # Clé secrète après 30 s
    if (not jeu_instance.cle_niveau_spawned and
            jeu_instance.niveau not in jeu_instance.cles_trouvees and
            jeu_instance.niveau <= 4):

        temps_ecoule_niveau = (pygame.time.get_ticks() - jeu_instance.debut_niveau) / 1000
        if temps_ecoule_niveau >= 30:
            x_pos = random.randint(100, LARGEUR_JEU - 100)
            cle = ItemCle(x_pos, -50)
            jeu_instance.items.add(cle)
            jeu_instance.all_sprites.add(cle)
            jeu_instance.cle_niveau_spawned = True

    temps_ecoule = (pygame.time.get_ticks() - jeu_instance.debut_niveau) / 1000
    temps_niveau_actuel = jeu_instance.temps_niveau
    temps_restant = temps_niveau_actuel - temps_ecoule

    # Victoire boss
    if jeu_instance.niveau == 4:
        if hasattr(jeu_instance, 'boss') and jeu_instance.boss not in jeu_instance.mobs:
            jeu_instance.musique.arreter_musique()
            jeu_instance.enregistrer_progression()

            if os.path.exists(jeu_instance.video_niveau4_path):
                try:
                    jeu_instance.lecteur_video = LecteurVideo(jeu_instance.video_niveau4_path)
                    if jeu_instance.lecteur_video.video:
                        jeu_instance.etat = "VIDEO_NIVEAU4"
                        if hasattr(jeu_instance, 'audio_niveau4'):
                            jeu_instance.audio_niveau4.jouer()
                        jeu_instance.clock_video = pygame.time.Clock()
                        return
                except Exception as e:
                    print(f"[WARN] Erreur lors du lancement de la vidéo: {e}")

            jeu_instance.etat = "VICTOIRE"
            pygame.mouse.set_visible(True)
            return

    # Fin de niveau : objectif kills (early clear) OU timer écoulé
    fin_par_objectif = jeu_instance.niveau < 4 and _objectif_atteint(jeu_instance)
    fin_par_timer = temps_restant <= 0

    if fin_par_objectif or fin_par_timer:
        if jeu_instance.niveau < 4:
            _passer_niveau_suivant(jeu_instance)
        elif jeu_instance.niveau == 4 and fin_par_timer:
            jeu_instance.etat = "GAMEOVER"
            pygame.mouse.set_visible(True)
            jeu_instance.musique.jouer_effet("gameover")
            jeu_instance.musique.arreter_musique()
            jeu_instance.enregistrer_progression()
            return

    # Transition entre niveaux
    if jeu_instance.niveau != jeu_instance.niveau_precedent and jeu_instance.niveau_precedent != 0:
        jeu_instance.etat = "TRANSITION"
        pygame.mouse.set_visible(True)
        jeu_instance.charger_fond_niveau(jeu_instance.niveau)
        jeu_instance.musique.jouer_musique_niveau(jeu_instance.niveau)
        jeu_instance.niveau_precedent = jeu_instance.niveau
        jeu_instance.vies = jeu_instance.joueur.max_vies
        jeu_instance.reset_objectifs_niveau()

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

    if jeu_instance.niveau_precedent == 0:
        jeu_instance.niveau_precedent = jeu_instance.niveau

    # Spawn
    now = pygame.time.get_ticks()
    nb_mobs = len(jeu_instance.mobs)

    if jeu_instance.niveau == 4:
        if not hasattr(jeu_instance, 'boss') and not hasattr(jeu_instance, 'boss_apparu'):
            jeu_instance.boss = Boss()
            jeu_instance.all_sprites.add(jeu_instance.boss)
            jeu_instance.mobs.add(jeu_instance.boss)
            jeu_instance.boss_apparu = True
        max_ennemis = 0
        delai_spawn = 99999
    else:
        cfg = SPAWN_CONFIG.get(jeu_instance.niveau, {"max": 2, "delay": 1000})
        max_ennemis = cfg["max"]
        delai_spawn = cfg["delay"]

    if nb_mobs < max_ennemis and now - jeu_instance.dernier_spawn > delai_spawn:
        if jeu_instance.niveau == 3:
            # Mix comètes (rebond) + météorites (chute)
            ennemi = Meteorite() if random.random() < 0.35 else Comet()
        elif jeu_instance.niveau == 2:
            ennemi = UFO()
        else:
            ennemi = Tornade(1)

        jeu_instance.all_sprites.add(ennemi)
        jeu_instance.mobs.add(ennemi)
        jeu_instance.dernier_spawn = now

    # Collisions balles / ennemis
    hits = pygame.sprite.groupcollide(jeu_instance.mobs, jeu_instance.balles, False, True)
    for mob, balles_touchees in hits.items():
        mob.pv -= len(balles_touchees)
        jeu_instance.musique.jouer_effet("degats")
        jeu_instance.vfx.ajouter(mob.rect.centerx, mob.rect.centery, JAUNE, 3)

        if mob.pv <= 0:
            if random.random() < 0.10 and jeu_instance.vies < jeu_instance.joueur.max_vies:
                vie_item = ItemVie(mob.rect.centerx, mob.rect.centery)
                jeu_instance.items.add(vie_item)

            if isinstance(mob, Tornade):
                jeu_instance.musique.jouer_effet("vent")
            elif isinstance(mob, (UFO, Comet, Meteorite)):
                jeu_instance.musique.jouer_effet("explosion")

            _appliquer_combo_kill(jeu_instance, mob)
            mob.kill()

    # Items
    recup_items = pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.items, True)
    for item in recup_items:
        if isinstance(item, ItemVie):
            if jeu_instance.vies < jeu_instance.joueur.max_vies:
                jeu_instance.vies += 1
                jeu_instance.musique.jouer_effet("extra_vie")
                jeu_instance.vfx.ajouter(item.rect.centerx, item.rect.centery, ROUGE, 10)
        elif isinstance(item, ItemCle):
            jeu_instance.cles_trouvees.add(jeu_instance.niveau)
            jeu_instance.musique.jouer_effet("coin")
            jeu_instance.vfx.ajouter(item.rect.centerx, item.rect.centery, (255, 215, 0), 20)
            if len(jeu_instance.cles_trouvees) >= 4:
                jeu_instance.niveau_infini_debloque = True
            jeu_instance.enregistrer_progression()

    # Collisions joueur / ennemis
    if pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.mobs, True):
        if not jeu_instance.joueur.invincible:
            jeu_instance.vies -= 1
            jeu_instance.combo = 0
            jeu_instance.vfx.declencher_degats()
            jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG, 15)
            jeu_instance.musique.jouer_effet("degats")

    if hasattr(jeu_instance, 'boss') and jeu_instance.boss and jeu_instance.boss.laser_actif:
        laser_rect = jeu_instance.boss.get_laser_rect()
        if laser_rect and jeu_instance.joueur.rect.colliderect(laser_rect):
            if not jeu_instance.joueur.invincible:
                jeu_instance.vies -= 2
                jeu_instance.combo = 0
                jeu_instance.vfx.declencher_degats()
                jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG, 20)
                jeu_instance.musique.jouer_effet("degats")
                jeu_instance.joueur.invincible = True
                jeu_instance.joueur.fin_invincibilite = pygame.time.get_ticks() + 2000

    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles[:]:
            if jeu_instance.joueur.rect.colliderect(projectile.rect):
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 1
                    jeu_instance.combo = 0
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.vfx.ajouter(
                        jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG, 10
                    )
                    jeu_instance.musique.jouer_effet("degats")
                jeu_instance.boss.projectiles.remove(projectile)

    # Ennemis hors écran : pénalité sur niveaux 1-2, et météorites au 3
    for m in list(jeu_instance.mobs):
        if m.rect.top > HAUTEUR_JEU:
            if jeu_instance.niveau < 3 or isinstance(m, Meteorite):
                m.kill()
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 1
                    jeu_instance.combo = 0
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.musique.jouer_effet("degats")
                    jeu_instance.vfx.ajouter(m.rect.centerx, HAUTEUR_JEU - 10, ROUGE, 5)

    if jeu_instance.vies <= 0:
        jeu_instance.etat = "GAMEOVER"
        pygame.mouse.set_visible(True)
        jeu_instance.musique.jouer_effet("gameover")
        jeu_instance.musique.arreter_musique()
        jeu_instance.enregistrer_progression()
