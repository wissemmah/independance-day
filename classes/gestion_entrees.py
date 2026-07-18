"""
Gestion des entrées utilisateur et actions du jeu
"""
import pygame
import sys
import os
from constantes import *


def gerer_entrees_jeu(jeu_instance):
    """Gère toutes les entrées utilisateur"""
    pos_souris = pygame.mouse.get_pos()
    clic = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Remap en cours
        if jeu_instance.attente_remap and event.type == pygame.KEYDOWN:
            jeu_instance.controles[jeu_instance.attente_remap] = event.key
            jeu_instance.attente_remap = None
            jeu_instance.enregistrer_progression()
            _rafraichir_textes_options(jeu_instance)
            return True

        # Tutoriel
        if jeu_instance.etat == "TUTORIEL":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                jeu_instance.tutoriel_vu = True
                jeu_instance.etat = "MENU"
                jeu_instance.enregistrer_progression()
            continue

        # Skip video with SPACE, ESC or mouse click
        if jeu_instance.etat == "VIDEO_INTRO":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_intro'):
                    jeu_instance.audio_intro.arreter()

                jeu_instance.reset_partie()
                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.musique.jouer_musique_niveau(1)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_intro'):
                    jeu_instance.audio_intro.arreter()

                jeu_instance.reset_partie()
                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.musique.jouer_musique_niveau(1)
                return True

        # Skip level 2 video with SPACE, ESC or mouse click
        if jeu_instance.etat == "VIDEO_NIVEAU2":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau2'):
                    jeu_instance.audio_niveau2.arreter()

                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.debut_niveau = pygame.time.get_ticks()
                jeu_instance.musique.jouer_musique_niveau(2)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau2'):
                    jeu_instance.audio_niveau2.arreter()

                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.debut_niveau = pygame.time.get_ticks()
                jeu_instance.musique.jouer_musique_niveau(2)
                return True

        # Skip level 3 video with SPACE, ESC or mouse click
        if jeu_instance.etat == "VIDEO_NIVEAU3":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau3'):
                    jeu_instance.audio_niveau3.arreter()

                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.debut_niveau = pygame.time.get_ticks()
                jeu_instance.musique.jouer_musique_niveau(3)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau3'):
                    jeu_instance.audio_niveau3.arreter()

                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.debut_niveau = pygame.time.get_ticks()
                jeu_instance.musique.jouer_musique_niveau(3)
                return True

        # Skip level 4 video (après boss) with SPACE, ESC or mouse click
        if jeu_instance.etat == "VIDEO_NIVEAU4":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau4'):
                    jeu_instance.audio_niveau4.arreter()

                jeu_instance.etat = "VICTOIRE"
                pygame.mouse.set_visible(True)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                jeu_instance.lecteur_video.fermer()

                if hasattr(jeu_instance, 'audio_niveau4'):
                    jeu_instance.audio_niveau4.arreter()

                jeu_instance.etat = "VICTOIRE"
                pygame.mouse.set_visible(True)
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clic = True

            # Gestion du scroll de la boutique
            if jeu_instance.etat == "PAUSE":
                cx = LARGEUR_JEU // 2
                scrollbar_x = cx + 290
                scrollbar_rect = pygame.Rect(scrollbar_x, 140, 15, 300)
                if scrollbar_rect.collidepoint(pos_souris):
                    jeu_instance.scroll_dragging = True
                    jeu_instance.scroll_drag_start = pos_souris[1]

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            jeu_instance.scroll_dragging = False

        # Gestion de la molette de la souris
        if event.type == pygame.MOUSEWHEEL and jeu_instance.etat == "PAUSE":
            jeu_instance.scroll_offset -= event.y * 30
            # Limiter le scroll (6 items)
            max_scroll = max(0, (6 * 90) - 260)
            jeu_instance.scroll_offset = max(0, min(jeu_instance.scroll_offset, max_scroll))

        if event.type == pygame.KEYDOWN:
            # DEBUG MODE - Touche D
            if event.key == pygame.K_d:
                jeu_instance.debug_mode = not jeu_instance.debug_mode
                print(f"[DEBUG] Mode debug: {'ON' if jeu_instance.debug_mode else 'OFF'}")

            # DEBUG - Invincibilité (I)
            if event.key == pygame.K_i and jeu_instance.debug_mode:
                jeu_instance.debug_invincible = not jeu_instance.debug_invincible
                jeu_instance.joueur.invincible = jeu_instance.debug_invincible
                jeu_instance.joueur.fin_invincibilite = pygame.time.get_ticks() + 9999000
                print(f"[DEBUG] Invincibilité: {jeu_instance.debug_invincible}")

            # DEBUG - Ennemis infinis (E)
            if event.key == pygame.K_e and jeu_instance.debug_mode:
                jeu_instance.debug_infinite_ennemis = not jeu_instance.debug_infinite_ennemis
                print(f"[DEBUG] Ennemis infinis: {jeu_instance.debug_infinite_ennemis}")

            # DEBUG - Argent infini (M)
            if event.key == pygame.K_m and jeu_instance.debug_mode:
                jeu_instance.debug_argent_infini = not jeu_instance.debug_argent_infini
                print(f"[DEBUG] Argent infini: {jeu_instance.debug_argent_infini}")

            # DEBUG - Débloquer niveaux (1, 2, 3, 4)
            if jeu_instance.debug_mode and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                niveau_map = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}
                nouveau_niveau = niveau_map[event.key]
                jeu_instance.niveau = nouveau_niveau
                jeu_instance.niveau_precedent = nouveau_niveau - 1
                jeu_instance.reset_partie()
                jeu_instance.niveau = nouveau_niveau
                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.charger_fond_niveau(nouveau_niveau)
                jeu_instance.musique.jouer_musique_niveau(nouveau_niveau)
                print(f"[DEBUG] Saut au niveau {nouveau_niveau}")

            # DEBUG - Contrôle vitesse jeu (+ et -)
            if jeu_instance.debug_mode and event.key == pygame.K_PLUS:
                jeu_instance.debug_game_speed = min(3.0, jeu_instance.debug_game_speed + 0.25)
                print(f"[DEBUG] Vitesse du jeu: {jeu_instance.debug_game_speed}x")
            if jeu_instance.debug_mode and event.key == pygame.K_MINUS:
                jeu_instance.debug_game_speed = max(0.25, jeu_instance.debug_game_speed - 0.25)
                print(f"[DEBUG] Vitesse du jeu: {jeu_instance.debug_game_speed}x")

            pause_key = jeu_instance.cle_controle("pause")
            if event.key in (pause_key, pygame.K_p) and jeu_instance.etat in ("JEU", "PAUSE"):
                jeu_instance.etat = "PAUSE" if jeu_instance.etat == "JEU" else "JEU"
                pygame.mouse.set_visible(jeu_instance.etat == "PAUSE")
                if jeu_instance.etat == "PAUSE":
                    jeu_instance.scroll_offset = 0

            restart_key = jeu_instance.cle_controle("restart")
            if jeu_instance.etat == "GAMEOVER" and event.key == restart_key:
                jeu_instance.reset_partie()
                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.musique.jouer_musique_niveau(1)

            if jeu_instance.etat == "VICTOIRE" and event.key == restart_key:
                jeu_instance.reset_partie()
                jeu_instance.etat = "JEU"
                pygame.mouse.set_visible(False)
                jeu_instance.musique.jouer_musique_niveau(1)

            valider = jeu_instance.cle_controle("valider")
            if jeu_instance.etat == "TRANSITION" and event.key == valider:
                # Level 2 transition with video
                if (jeu_instance.niveau == 2 and os.path.exists(jeu_instance.video_niveau2_path)
                        and not getattr(jeu_instance, "lite_mode", False)):
                    from classes.lecteur_video import LecteurVideo

                    jeu_instance.musique.arreter_musique()

                    jeu_instance.lecteur_video = LecteurVideo(jeu_instance.video_niveau2_path)

                    if jeu_instance.lecteur_video.video:
                        jeu_instance.etat = "VIDEO_NIVEAU2"

                        if hasattr(jeu_instance, 'audio_niveau2'):
                            jeu_instance.audio_niveau2.jouer()

                        jeu_instance.clock_video = pygame.time.Clock()
                    else:
                        jeu_instance.etat = "JEU"
                        pygame.mouse.set_visible(False)
                        jeu_instance.debut_niveau = pygame.time.get_ticks()
                        jeu_instance.cle_niveau_spawned = False
                        jeu_instance.musique.jouer_musique_niveau(2)

                # Level 3 transition with video
                elif (jeu_instance.niveau == 3 and os.path.exists(jeu_instance.video_niveau3_path)
                      and not getattr(jeu_instance, "lite_mode", False)):
                    from classes.lecteur_video import LecteurVideo

                    jeu_instance.musique.arreter_musique()

                    jeu_instance.lecteur_video = LecteurVideo(jeu_instance.video_niveau3_path)

                    if jeu_instance.lecteur_video.video:
                        jeu_instance.etat = "VIDEO_NIVEAU3"

                        if hasattr(jeu_instance, 'audio_niveau3'):
                            jeu_instance.audio_niveau3.jouer()

                        jeu_instance.clock_video = pygame.time.Clock()
                    else:
                        jeu_instance.etat = "JEU"
                        pygame.mouse.set_visible(False)
                        jeu_instance.debut_niveau = pygame.time.get_ticks()
                        jeu_instance.cle_niveau_spawned = False
                        jeu_instance.musique.jouer_musique_niveau(3)

                else:
                    jeu_instance.etat = "JEU"
                    pygame.mouse.set_visible(False)
                    jeu_instance.debut_niveau = pygame.time.get_ticks()
                    jeu_instance.cle_niveau_spawned = False

            # Nuke
            if (jeu_instance.etat == "JEU" and event.key == jeu_instance.cle_controle("nuke")
                    and jeu_instance.joueur.nukes > 0):
                jeu_instance.joueur.nukes -= 1
                jeu_instance.nukes_used_run += 1
                if jeu_instance.niveau == 4:
                    jeu_instance.boss_nukes_used += 1
                jeu_instance.vfx.declencher_nuke()
                jeu_instance.musique.jouer_effet("nuke")

                from classes.boss import Boss

                for m in list(jeu_instance.mobs):
                    if isinstance(m, Boss):
                        m.pv -= 100
                        jeu_instance.vfx.ajouter(m.rect.centerx, m.rect.centery, ORANGE, 30)
                        if m.pv <= 0:
                            jeu_instance.argent += m.valeur
                            jeu_instance.score_total += m.valeur * 2
                            m.kill()
                        continue

                    # Ennemis normaux : meurent instantanément
                    jeu_instance.vfx.ajouter(m.rect.centerx, m.rect.centery, GRIS_FONCE, 20)
                    jeu_instance.argent += m.valeur
                    jeu_instance.score_total += m.valeur * 2
                    m.kill()

    # Gestion du drag de la scrollbar
    if jeu_instance.scroll_dragging and jeu_instance.etat == "PAUSE":
        delta_y = pos_souris[1] - jeu_instance.scroll_drag_start
        jeu_instance.scroll_drag_start = pos_souris[1]

        # Convertir le mouvement de la souris en scroll
        scrollbar_height = 300
        content_height = 6 * 90  # 6 items * 90px
        visible_height = 260
        max_scroll = max(0, content_height - visible_height)

        if max_scroll > 0:
            scroll_ratio = max_scroll / (scrollbar_height - 50)  # 50 = hauteur du handle
            jeu_instance.scroll_offset += delta_y * scroll_ratio
            jeu_instance.scroll_offset = max(0, min(jeu_instance.scroll_offset, max_scroll))

    # Gestion des clics sur boutons
    if clic:
        action = None

        # Retour au menu depuis le GIF
        if jeu_instance.etat == "GIF":
            jeu_instance.etat = "MENU"
            jeu_instance.gif_playing = False

        elif jeu_instance.etat == "MENU":
            # VÉRIFIER D'ABORD LE LOGO TRUMP (PRIORITÉ)
            if jeu_instance.logo_rect.collidepoint(pos_souris):
                jeu_instance.etat = "GIF"
                jeu_instance.gif_playing = True
                jeu_instance.gif_index = 0
                jeu_instance.gif_timer = 0
            else:
                # Ensuite les boutons du menu
                for btn in jeu_instance.btns_menu_img:
                    if btn.clic(pos_souris):
                        action = btn.action()
                        break

                # Vérifier le bouton niveau infini s'il est débloqué
                if jeu_instance.niveau_infini_debloque:
                    res = jeu_instance.btn_niveau_infini.verifier_clic(pos_souris)
                    if res:
                        action = res

        elif jeu_instance.etat == "PAUSE":
            # Gestion boutique
            clic_boutique(jeu_instance, pos_souris[0], pos_souris[1])

            # Gestion bouton OPTIONS boutique
            res = jeu_instance.btn_options_boutique.verifier_clic(pos_souris)
            if res:
                action = res

            # Si le sous-menu options est ouvert, gérer les clics sur les options
            if jeu_instance.options_boutique_ouvert:
                for btn in jeu_instance.btns_options_boutique_submenu:
                    res = btn.verifier_clic(pos_souris)
                    if res:
                        action = res

            # Gestion boutons pause
            for btn in jeu_instance.btns_pause:
                res = btn.verifier_clic(pos_souris)
                if res:
                    action = res

        elif jeu_instance.etat == "OPTIONS":
            liste = jeu_instance.btns_opt
            for btn in liste:
                res = btn.verifier_clic(pos_souris)
                if res:
                    action = res

        executer_action_menu(jeu_instance, action)

    # Update hover des boutons
    if jeu_instance.etat == "MENU":
        for btn in jeu_instance.btns_menu_img:
            btn.update(pos_souris)
        # Hover du bouton niveau infini si débloqué
        if jeu_instance.niveau_infini_debloque:
            jeu_instance.btn_niveau_infini.verifier_survol(pos_souris)

    # Hover des boutons pause et options
    boutons_a_hover = jeu_instance.btns_pause + jeu_instance.btns_opt + [jeu_instance.btn_options_boutique]
    if jeu_instance.options_boutique_ouvert:
        boutons_a_hover += jeu_instance.btns_options_boutique_submenu

    for btn in boutons_a_hover:
        btn.verifier_survol(pos_souris)

    return True


def clic_boutique(jeu_instance, mx, my):
    """Gère les clics dans la boutique"""
    cx = LARGEUR_JEU // 2
    shop_y = 100
    y_start = shop_y + 140

    # Zone visible de la boutique
    zone_visible = pygame.Rect(cx - 310, shop_y + 140, 620, 300)

    # Si le clic n'est pas dans la zone visible, ignorer
    if not zone_visible.collidepoint(mx, my):
        return

    prix_tir = 9999
    txt_tir = "Tir MAX"
    dispo_tir = False
    if jeu_instance.joueur.niveau_tir == 1:
        txt_tir = "Tir Double"
        prix_tir = 200
        dispo_tir = True
    elif jeu_instance.joueur.niveau_tir == 2:
        txt_tir = "Tir Quadruple"
        prix_tir = 400
        dispo_tir = True

    prix_cad = jeu_instance.joueur.niveau_cadence * 100
    txt_cad = f"Cadence Niv {jeu_instance.joueur.niveau_cadence + 1}"
    dispo_cad = True
    if jeu_instance.joueur.niveau_cadence >= 6:
        txt_cad = "Cadence MAX"
        prix_cad = 9999
        dispo_cad = False

    # Liste des items avec leurs conditions de disponibilité
    items = [
        ("tir", prix_tir, txt_tir, dispo_tir),
        ("cadence", prix_cad, txt_cad, dispo_cad),
        ("laser", 400, "Laser", not jeu_instance.joueur.a_laser),
        ("extra_vie", 200, "Extra Vie (Max +1)", jeu_instance.joueur.max_vies < 5),
        ("inv", 50, "Invincibilite 10s", True),
        ("nuke", 30, "Bombe Nuke", True)
    ]

    # Calculer la position Y de chaque item avec le scroll
    for idx, (action, prix, titre, dispo) in enumerate(items):
        y = y_start + (idx * 90) - int(jeu_instance.scroll_offset)
        rect = pygame.Rect(cx - 280, y, 560, 70)

        # Vérifier si le clic est dans ce rectangle ET si on peut acheter
        # Avec debug_argent_infini, ignorer la vérification du prix
        peut_acheter = dispo and (jeu_instance.argent >= prix or jeu_instance.debug_argent_infini)
        if rect.collidepoint(mx, my) and peut_acheter:
            buy = False

            if action == "tir":
                if jeu_instance.joueur.niveau_tir == 1:
                    jeu_instance.joueur.niveau_tir = 2
                    buy = True
                elif jeu_instance.joueur.niveau_tir == 2:
                    jeu_instance.joueur.niveau_tir = 3
                    buy = True
            elif action == "cadence":
                if jeu_instance.joueur.niveau_cadence < 6:
                    jeu_instance.joueur.niveau_cadence += 1
                    buy = True
            elif action == "laser":
                if not jeu_instance.joueur.a_laser:
                    jeu_instance.joueur.a_laser = True
                    buy = True
            elif action == "extra_vie":
                if jeu_instance.joueur.max_vies < 5:
                    jeu_instance.joueur.max_vies += 1  # Augmente le maximum
                    jeu_instance.vies += 1  # Donne une vie immédiatement
                    buy = True
            elif action == "inv":
                jeu_instance.joueur.invincible = True
                jeu_instance.joueur.fin_invincibilite = pygame.time.get_ticks() + 10000
                buy = True
            elif action == "nuke":
                jeu_instance.joueur.nukes += 1
                buy = True

            if buy:
                # Ne pas déduire l'argent si argent infini est activé
                if not jeu_instance.debug_argent_infini:
                    jeu_instance.argent -= prix
                jeu_instance.musique.jouer_effet("coin")
                return  # Sortir après un achat


def executer_action_menu(jeu_instance, action):
    """Exécute les actions des boutons de menu"""
    if not action:
        return

    if action == "LANCER_JEU":
        if getattr(jeu_instance, "lite_mode", False):
            jeu_instance.reset_partie()
            jeu_instance.etat = "JEU"
            pygame.mouse.set_visible(False)
            jeu_instance.musique.jouer_musique_niveau(1)
        else:
            jeu_instance.lancer_video_intro()

    elif action == "QUITTER":
        pygame.quit()
        sys.exit()
    elif action == "LANCER_NIVEAU_INFINI":
        jeu_instance.reset_partie()
        jeu_instance.niveau = 999
        jeu_instance.niveau_precedent = 999
        jeu_instance.etat = "JEU"
        jeu_instance.infini_debut = pygame.time.get_ticks()
        pygame.mouse.set_visible(False)
        jeu_instance.charger_fond_niveau(1)
        jeu_instance.musique.jouer_musique_niveau(1)
    elif action == "OUVRIR_OPTIONS_BOUTIQUE":
        jeu_instance.options_boutique_ouvert = not jeu_instance.options_boutique_ouvert
        if jeu_instance.options_boutique_ouvert:
            jeu_instance.btn_options_boutique.texte = "FERMER"
        else:
            jeu_instance.btn_options_boutique.texte = "OPTIONS"
    elif action == "ALLER_OPTIONS":
        jeu_instance.etat = "OPTIONS"
        _rafraichir_textes_options(jeu_instance)
    elif action == "RETOUR_DEPUIS_OPT":
        jeu_instance.attente_remap = None
        jeu_instance.etat = "MENU"
        jeu_instance.enregistrer_progression()
    elif action == "REPRENDRE":
        jeu_instance.etat = "JEU"
        pygame.mouse.set_visible(False)
    elif action == "RETOUR_MENU":
        jeu_instance.etat = "MENU"
        pygame.mouse.set_visible(True)
        jeu_instance.musique.jouer_musique_menu()
    elif action == "TOGGLE_MUSIQUE":
        a = jeu_instance.musique.basculer_musique()
        jeu_instance.btns_opt[0].texte = f"Musique : {'ON' if a else 'OFF'}"
    elif action == "TOGGLE_EFFETS":
        a = jeu_instance.musique.basculer_effets()
        jeu_instance.btns_opt[1].texte = f"Effets : {'ON' if a else 'OFF'}"
    elif action == "VOL_MUSIQUE":
        v = jeu_instance.musique.cycle_volume("musique")
        jeu_instance.btns_opt[2].texte = f"Vol. musique : {int(v * 100)}%"
    elif action == "VOL_EFFETS":
        v = jeu_instance.musique.cycle_volume("effets")
        jeu_instance.btns_opt[3].texte = f"Vol. effets : {int(v * 100)}%"
    elif action == "TOGGLE_FULLSCREEN":
        jeu_instance.plein_ecran = not jeu_instance.plein_ecran
        if jeu_instance.plein_ecran:
            try:
                info = pygame.display.Info()
                pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            except Exception as e:
                print(f"[WARN] Fullscreen error: {e}")
                jeu_instance.plein_ecran = False
                pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
        else:
            pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
        jeu_instance.btns_opt[4].texte = f"Plein Écran : {'OUI' if jeu_instance.plein_ecran else 'NON'}"
    elif action == "REMAP_NUKE":
        jeu_instance.attente_remap = "nuke"
        jeu_instance.btns_opt[5].texte = "Appuie sur une touche..."
    elif action == "REMAP_PAUSE":
        jeu_instance.attente_remap = "pause"
        jeu_instance.btns_opt[6].texte = "Appuie sur une touche..."
    elif action == "TOGGLE_MUSIQUE_PAUSE":
        a = jeu_instance.musique.basculer_musique()
        jeu_instance.btns_options_boutique_submenu[0].texte = f"Musique: {'ON' if a else 'OFF'}"
        jeu_instance.btns_opt[0].texte = f"Musique : {'ON' if a else 'OFF'}"
    elif action == "TOGGLE_EFFETS_PAUSE":
        a = jeu_instance.musique.basculer_effets()
        jeu_instance.btns_options_boutique_submenu[1].texte = f"Effets: {'ON' if a else 'OFF'}"
        jeu_instance.btns_opt[1].texte = f"Effets : {'ON' if a else 'OFF'}"
    elif action == "TOGGLE_FULLSCREEN_PAUSE":
        jeu_instance.plein_ecran = not jeu_instance.plein_ecran
        if jeu_instance.plein_ecran:
            try:
                info = pygame.display.Info()
                pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            except Exception as e:
                print(f"[WARN] Fullscreen error: {e}")
                jeu_instance.plein_ecran = False
                pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
        else:
            pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
        jeu_instance.btns_options_boutique_submenu[2].texte = f"Plein Écran: {'OUI' if jeu_instance.plein_ecran else 'NON'}"
        jeu_instance.btns_opt[4].texte = f"Plein Écran : {'OUI' if jeu_instance.plein_ecran else 'NON'}"


def _rafraichir_textes_options(jeu):
    jeu.btns_opt[0].texte = f"Musique : {'ON' if jeu.musique.musique_active else 'OFF'}"
    jeu.btns_opt[1].texte = f"Effets : {'ON' if jeu.musique.effets_actifs else 'OFF'}"
    jeu.btns_opt[2].texte = f"Vol. musique : {int(jeu.musique.volume_musique * 100)}%"
    jeu.btns_opt[3].texte = f"Vol. effets : {int(jeu.musique.volume_effets * 100)}%"
    jeu.btns_opt[4].texte = f"Plein Écran : {'OUI' if jeu.plein_ecran else 'NON'}"
    nuke_name = pygame.key.name(jeu.cle_controle("nuke")).upper()
    pause_name = pygame.key.name(jeu.cle_controle("pause")).upper()
    jeu.btns_opt[5].texte = f"Remap Nuke ({nuke_name})"
    jeu.btns_opt[6].texte = f"Remap Pause ({pause_name})"
    if jeu.attente_remap == "nuke":
        jeu.btns_opt[5].texte = "Appuie sur une touche..."
    if jeu.attente_remap == "pause":
        jeu.btns_opt[6].texte = "Appuie sur une touche..."
