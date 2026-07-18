"""
Gestion du niveau infini (Easter Egg)
PROGRESSION INFINIE JUSQU'À L'IMPOSSIBLE !
"""
import pygame
import random
from constantes import *
from classes.ennemis import Tornade, UFO, Meteorite, Comet
from classes.items import ItemVie


def update_niveau_infini(jeu_instance):
    """Met à jour la logique du niveau infini"""
    # Updates de base
    jeu_instance.update_fond()
    jeu_instance.vfx.update()
    if hasattr(jeu_instance, "joueur") and jeu_instance.joueur:
        jeu_instance.joueur.jeu = jeu_instance
    jeu_instance.all_sprites.update()
    jeu_instance.items.update()

    # Tir automatique du joueur
    balles = jeu_instance.joueur.verifier_tir_auto()
    if balles:
        jeu_instance.musique.jouer_effet("tir")
        jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.top, JAUNE, 2)
        for balle in balles:
            jeu_instance.all_sprites.add(balle)
            jeu_instance.balles.add(balle)

    if not getattr(jeu_instance, "infini_debut", 0):
        jeu_instance.infini_debut = jeu_instance.debut_niveau
    temps_ecoule = (pygame.time.get_ticks() - jeu_instance.infini_debut) / 1000
    if temps_ecoule >= 300:
        jeu_instance.try_achievement("infini_5min")

    # ===== PROGRESSION INFINIE - DIFFICULTÉ CROISSANTE =====
    # 0-5min : Phases 1-5 - Montée en difficulté classique
    # 5min : 1 BOSS apparaît
    # 10min : 2 BOSS + spawn accéléré
    # 15min : 3 BOSS + spawn très rapide
    # 20min+ : 4+ BOSS + spawn ultra rapide = IMPOSSIBLE !

    now = pygame.time.get_ticks()
    nb_mobs = len(jeu_instance.mobs)

    # ===== GESTION DES BOSS MULTIPLES =====
    # Calculer combien de boss doivent être présents
    nb_boss_requis = 0
    if temps_ecoule >= 300:  # 5 minutes
        nb_boss_requis = 1
    if temps_ecoule >= 600:  # 10 minutes
        nb_boss_requis = 2
    if temps_ecoule >= 900:  # 15 minutes
        nb_boss_requis = 3
    if temps_ecoule >= 1200:  # 20 minutes
        nb_boss_requis = 4
    if temps_ecoule >= 1500:  # 25 minutes (si quelqu'un survit jusque-là !)
        nb_boss_requis = 5

    # Compter les boss actuellement présents
    from classes.boss import Boss
    boss_actuels = [m for m in jeu_instance.mobs if isinstance(m, Boss)]
    nb_boss_actuels = len(boss_actuels)

    # Spawner les boss manquants
    if nb_boss_actuels < nb_boss_requis:
        nb_a_spawner = nb_boss_requis - nb_boss_actuels
        for i in range(nb_a_spawner):
            boss = Boss()
            jeu_instance.all_sprites.add(boss)
            jeu_instance.mobs.add(boss)
            print(f"[INFO] 🔥 BOSS #{nb_boss_actuels + i + 1} APPARAÎT ! Total: {nb_boss_actuels + i + 1} BOSS !")

    # ===== CALCUL DE LA DIFFICULTÉ EN FONCTION DU TEMPS =====
    # Déterminer le nombre max d'ennemis et le délai selon le temps

    if temps_ecoule < 60:
        # Phase 1 (0-1min) : Facile - Tornades simples uniquement
        max_ennemis = 2
        delai_spawn = 2000
        types_ennemis = ["tornade"]
    elif temps_ecoule < 120:
        # Phase 2 (1-2min) : Introduction progressive des UFO
        max_ennemis = 2
        delai_spawn = 1800
        types_ennemis = ["tornade", "tornade", "tornade", "ufo"]
    elif temps_ecoule < 180:
        # Phase 3 (2-3min) : Tornades difficiles + UFO
        max_ennemis = 3
        delai_spawn = 1600
        types_ennemis = ["tornade", "tornade", "ufo", "ufo"]
    elif temps_ecoule < 240:
        # Phase 4 (3-4min) : Météorites arrivent !
        max_ennemis = 3
        delai_spawn = 1500
        types_ennemis = ["tornade", "ufo", "meteorite"]
    elif temps_ecoule < 300:
        # Phase 5 (4-5min) : Comètes arrivent - TOUS les ennemis ! Préparation au boss
        max_ennemis = 4
        delai_spawn = 1400
        types_ennemis = ["tornade", "ufo", "meteorite", "comet"]
    elif temps_ecoule < 600:
        # Phase 6 (5-10min) : 1 BOSS + ennemis modérés
        max_ennemis = 3 + nb_boss_actuels  # 3 ennemis normaux + le boss
        delai_spawn = 2000
        types_ennemis = ["tornade", "ufo", "meteorite", "comet"]
    elif temps_ecoule < 900:
        # Phase 7 (10-15min) : 2 BOSS + spawn accéléré
        max_ennemis = 5 + nb_boss_actuels  # 5 ennemis normaux + 2 boss
        delai_spawn = 1500
        types_ennemis = ["tornade", "ufo", "meteorite", "comet"]
    elif temps_ecoule < 1200:
        # Phase 8 (15-20min) : 3 BOSS + spawn très rapide
        max_ennemis = 7 + nb_boss_actuels  # 7 ennemis normaux + 3 boss
        delai_spawn = 1000
        types_ennemis = ["tornade", "ufo", "meteorite", "comet"]
    else:
        # Phase 9+ (20min+) : 4+ BOSS + spawn ultra rapide = IMPOSSIBLE !
        max_ennemis = 10 + nb_boss_actuels  # 10 ennemis normaux + 4+ boss
        delai_spawn = 800  # Spawn très rapide
        types_ennemis = ["tornade", "ufo", "meteorite", "comet"]

    # Spawner les ennemis normaux (pas les boss)
    # Ne compter que les ennemis non-boss
    nb_ennemis_normaux = nb_mobs - nb_boss_actuels

    if nb_ennemis_normaux < max_ennemis:
        if now - jeu_instance.dernier_spawn > delai_spawn:
            type_ennemi = random.choice(types_ennemis)

            if type_ennemi == "tornade":
                # 0-1min : Tornades niveau 1 (1 PV, pas de barre de vie)
                # 1-2min : Tornades niveau 2 (2 PV, avec barre de vie)
                # 2min+ : Tornades niveau 3 (3 PV, avec barre de vie)
                if temps_ecoule < 60:
                    ennemi = Tornade(1)  # 1 PV - faciles
                elif temps_ecoule < 120:
                    ennemi = Tornade(2)  # 2 PV - moyennes
                else:
                    ennemi = Tornade(3)  # 3 PV - difficiles
            elif type_ennemi == "ufo":
                ennemi = UFO()
            elif type_ennemi == "meteorite":
                ennemi = Meteorite()
            else:  # comet
                ennemi = Comet()

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
                jeu_instance.musique.jouer_effet("vent")
            elif isinstance(mob, Boss):
                jeu_instance.musique.jouer_effet("explosion")
                print(f"[INFO] 💀 BOSS VAINCU ! Reste: {nb_boss_actuels - 1} boss")
            else:
                jeu_instance.musique.jouer_effet("explosion")

            mob.kill()
            jeu_instance.score_total += mob.valeur
            jeu_instance.argent += mob.valeur
            jeu_instance.vfx.ajouter(mob.rect.centerx, mob.rect.centery, GRIS_FONCE, 10)

    # Ramassage des vaches (vies)
    recup_vies = pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.items, True)
    for vie_item in recup_vies:
        if jeu_instance.vies < jeu_instance.joueur.max_vies:
            jeu_instance.vies += 1
            jeu_instance.musique.jouer_effet("extra_vie")
            jeu_instance.vfx.ajouter(vie_item.rect.centerx, vie_item.rect.centery, ROUGE, 10)

    # Collisions joueur/ennemis
    if pygame.sprite.spritecollide(jeu_instance.joueur, jeu_instance.mobs, True):
        if not jeu_instance.joueur.invincible:
            jeu_instance.vies -= 1
            jeu_instance.vfx.declencher_degats()
            jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery, ROUGE_SANG, 15)
            jeu_instance.musique.jouer_effet("degats")

    # Collision laser des boss avec le joueur (enlève 2 vies !)
    for boss in boss_actuels:
        if boss.laser_actif:
            laser_rect = boss.get_laser_rect()
            if laser_rect and jeu_instance.joueur.rect.colliderect(laser_rect):
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 2  # Le laser enlève 2 vies !
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery,
                                             ROUGE_SANG, 20)
                    jeu_instance.musique.jouer_effet("degats")
                    # Rendre temporairement invincible pour éviter mort instantanée
                    jeu_instance.joueur.invincible = True
                    jeu_instance.joueur.fin_invincibilite = pygame.time.get_ticks() + 2000  # 2 secondes

        # Collision projectiles des boss avec le joueur
        for projectile in boss.projectiles[:]:
            if jeu_instance.joueur.rect.colliderect(projectile.rect):
                if not jeu_instance.joueur.invincible:
                    jeu_instance.vies -= 1
                    jeu_instance.vfx.declencher_degats()
                    jeu_instance.vfx.ajouter(jeu_instance.joueur.rect.centerx, jeu_instance.joueur.rect.centery,
                                             ROUGE_SANG, 10)
                    jeu_instance.musique.jouer_effet("degats")
                boss.projectiles.remove(projectile)

    # Mettre à jour les projectiles des boss
    for boss in boss_actuels:
        for projectile in boss.projectiles[:]:
            projectile.update()
            # Vérifier si le projectile est mort
            if not projectile.rect.colliderect(pygame.Rect(0, 0, LARGEUR_JEU, HAUTEUR_JEU)):
                boss.projectiles.remove(projectile)

    # Ennemis hors écran (pas pour comètes/météorites/boss)
    for m in list(jeu_instance.mobs):
        if m.rect.top > HAUTEUR_JEU and not isinstance(m, (Comet, Meteorite, Boss)):
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