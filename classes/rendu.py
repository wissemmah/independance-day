"""
Rendu graphique du jeu - Thème Fête de l'Indépendance Américaine
"""
import pygame
from constantes import (
    LARGEUR_JEU,
    HAUTEUR_JEU,
    OR,
    BLANC,
    GRIS_FONCE,
    ROUGE,
    VERT,
    JAUNE,
    ORANGE,
    BLEU_NUIT,
    BLEU_BOUCLIER,
)
import os

FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts", "BebasNeue-Regular.ttf")


def charger_polices_bebas():
    """Charge les polices Bebas Neue en plusieurs tailles"""
    if os.path.exists(FONT_PATH):
        try:
            grosses_font = pygame.font.Font(FONT_PATH, 72)
            moyenne_font = pygame.font.Font(FONT_PATH, 36)
            petite_font = pygame.font.Font(FONT_PATH, 24)
            font = pygame.font.Font(FONT_PATH, 28)
        except Exception:
            grosses_font = pygame.font.Font(None, 72)
            moyenne_font = pygame.font.Font(None, 36)
            petite_font = pygame.font.Font(None, 24)
            font = pygame.font.Font(None, 28)
    else:
        grosses_font = pygame.font.Font(None, 72)
        moyenne_font = pygame.font.Font(None, 36)
        petite_font = pygame.font.Font(None, 24)
        font = pygame.font.Font(None, 28)
    return font, petite_font, moyenne_font, grosses_font


def dessiner_debug_info(jeu_instance, ecran, petite_font):
    """Affiche les informations de debug sur l'écran"""
    if not jeu_instance.debug_mode:
        return

    x_offset = 20
    y_offset = 120
    line_height = 25
    bg_alpha = 180
    
    # Préparer les infos à afficher
    debug_lines = [
        f"=== DEBUG MODE ===",
        f"FPS: {int(pygame.time.Clock().get_fps())}",
        f"Joueur: ({int(jeu_instance.joueur.rect.x)}, {int(jeu_instance.joueur.rect.y)})",
        f"Ennemis: {len(jeu_instance.mobs)}",
        f"Vagues: {getattr(jeu_instance, 'vague', 'N/A')}",
        f"Invincible: {jeu_instance.debug_invincible} [I]",
        f"Ennemis Inf.: {jeu_instance.debug_infinite_ennemis} [E]",
        f"Argent Inf.: {jeu_instance.debug_argent_infini} [M]",
        f"Vitesse: {jeu_instance.debug_game_speed}x [+/-]",
        f"Niv: [1][2][3][4]",
        f"Argent: {jeu_instance.argent}$",
        f"Vies: {jeu_instance.vies}",
    ]
    
    # Calculer la taille du fond
    total_height = len(debug_lines) * line_height + 10
    total_width = 350
    
    # Créer un fond semi-transparent
    bg_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, bg_alpha))
    ecran.blit(bg_surface, (x_offset - 5, y_offset - 5))
    
    # Bordure
    pygame.draw.rect(ecran, JAUNE, (x_offset - 5, y_offset - 5, total_width, total_height), 2)
    
    # Afficher le texte
    for idx, line in enumerate(debug_lines):
        y = y_offset + (idx * line_height)
        
        if "===" in line:
            color = JAUNE
            style = petite_font
        elif "[" in line and "]" in line:
            color = ORANGE
            style = petite_font
        else:
            color = BLANC
            style = petite_font
        
        txt = style.render(line, True, color)
        ecran.blit(txt, (x_offset, y))


def dessiner_hitboxes(jeu_instance, ecran):
    """Affiche les hitboxes de tous les éléments"""
    if not jeu_instance.debug_mode:
        return
    
    # Hitbox du joueur
    pygame.draw.rect(ecran, VERT, jeu_instance.joueur.rect, 2)
    pygame.draw.circle(ecran, VERT, jeu_instance.joueur.rect.center, 3)
    
    # Hitboxes des ennemis
    for mob in jeu_instance.mobs:
        pygame.draw.rect(ecran, ROUGE, mob.rect, 2)
        # Cercle au centre
        pygame.draw.circle(ecran, ROUGE, mob.rect.center, 2)
    
    # Hitboxes des projectiles du joueur
    for bullet in jeu_instance.balles:
        pygame.draw.rect(ecran, JAUNE, bullet.rect, 1)
    
    # Hitboxes des projectiles du boss
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles:
            pygame.draw.rect(ecran, ORANGE, projectile.rect, 1)
    
    # Hitboxes des items
    for item in jeu_instance.items:
        pygame.draw.rect(ecran, BLANC, item.rect, 1)


def dessiner_items_boutique(jeu_instance, ecran, cx, shop_y, petite_font):
    """Dessine les items de la boutique"""
    mx, my = pygame.mouse.get_pos()
    y = shop_y + 140 - int(jeu_instance.scroll_offset)

    prix_tir = 9999
    txt_tir = "Tir MAX"
    dispo_tir = False
    if jeu_instance.joueur.niveau_tir == 1:
        txt_tir = "Tir Double"
        prix_tir = 300
        dispo_tir = True
    elif jeu_instance.joueur.niveau_tir == 2:
        txt_tir = "Tir Quadruple"
        prix_tir = 600
        dispo_tir = True

    prix_cad = jeu_instance.joueur.niveau_cadence * 150
    txt_cad = f"Cadence Niv {jeu_instance.joueur.niveau_cadence + 1}"
    dispo_cad = True
    if jeu_instance.joueur.niveau_cadence >= 6:
        txt_cad = "Cadence MAX"
        prix_cad = 9999
        dispo_cad = False

    items_display = [
        (prix_tir, txt_tir, dispo_tir),
        (prix_cad, txt_cad, dispo_cad),
        (600, "Laser", not jeu_instance.joueur.a_laser),
        (200, "Extra Vie (Max +1)", jeu_instance.joueur.max_vies < 5),
        (50, "Invincibilite 10s", True),
        (50, "Bombe Nuke", True)
    ]

    clip_rect = pygame.Rect(cx - 310, shop_y + 140, 620, 300)

    for prix, titre, dispo in items_display:
        rect = pygame.Rect(cx - 280, y, 560, 70)

        peut_acheter = dispo and jeu_instance.argent >= prix
        is_hover = rect.collidepoint(mx, my) and peut_acheter and clip_rect.collidepoint(mx, my)

        # Fond item
        pygame.draw.rect(ecran, (70, 90, 120) if is_hover else (30, 40, 60), rect, border_radius=10)

        # Bordure
        pygame.draw.rect(ecran, OR if peut_acheter else GRIS_FONCE, rect, 2, border_radius=10)

        # Texte titre
        txt_titre = petite_font.render(titre, True, BLANC if peut_acheter else GRIS_FONCE)
        ecran.blit(txt_titre, (rect.x + 20, rect.centery - 20))

        # Prix
        if dispo:
            txt_prix = petite_font.render(f"{prix}$", True, OR if peut_acheter else GRIS_FONCE)
            ecran.blit(txt_prix, (rect.right - 80, rect.centery + 5))
        else:
            txt_max = petite_font.render("MAX", True, ROUGE)
            ecran.blit(txt_max, (rect.right - 60, rect.centery + 5))

        y += 90


# ---------------------------------------------------
# SCROLLBAR DE LA BOUTIQUE
# ---------------------------------------------------
def dessiner_scrollbar(jeu_instance, ecran, cx, shop_y):
    """Dessine la barre de défilement de la boutique"""
    scrollbar_x = cx + 290
    scrollbar_y = shop_y + 140
    scrollbar_height = 300

    pygame.draw.rect(ecran, (40, 40, 50), (scrollbar_x, scrollbar_y, 15, scrollbar_height), border_radius=7)

    content_height = 6 * 90
    visible_height = 260
    max_scroll = max(0, content_height - visible_height)

    if max_scroll > 0:
        handle_height = max(30, int((visible_height / content_height) * scrollbar_height))
        handle_y = scrollbar_y + int((jeu_instance.scroll_offset / max_scroll) * (scrollbar_height - handle_height))
        pygame.draw.rect(ecran, OR, (scrollbar_x, handle_y, 15, handle_height), border_radius=7)


# ---------------------------------------------------
# MENU PAUSE ET BOUTIQUE
# ---------------------------------------------------
def dessiner_pause_et_boutique(jeu_instance, ecran, grosse_font, moyenne_font, petite_font):
    """Dessine le menu pause avec la boutique"""
    overlay = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    ecran.blit(overlay, (0, 0))

    cx = LARGEUR_JEU // 2
    shop_width = 620
    shop_height = 480
    shop_x = cx - (shop_width // 2)
    shop_y = 100

    shop_rect = pygame.Rect(shop_x, shop_y, shop_width, shop_height)
    pygame.draw.rect(ecran, BLEU_NUIT, shop_rect, border_radius=15)
    pygame.draw.rect(ecran, OR, shop_rect, 3, border_radius=15)

    titre = grosse_font.render("BOUTIQUE", True, OR)
    ecran.blit(titre, titre.get_rect(center=(cx, shop_y + 40)))

    txt_argent = moyenne_font.render(f"{jeu_instance.argent}$", True, OR)
    ecran.blit(txt_argent, txt_argent.get_rect(center=(cx, shop_y + 90)))

    clip_rect = pygame.Rect(shop_x + 10, shop_y + 140, shop_width - 40, 300)
    ecran.set_clip(clip_rect)
    dessiner_items_boutique(jeu_instance, ecran, cx, shop_y, petite_font)
    ecran.set_clip(None)

    dessiner_scrollbar(jeu_instance, ecran, cx, shop_y)

    # Bouton OPTIONS en haut à droite
    jeu_instance.btn_options_boutique.dessiner(ecran)

    # Si le sous-menu est ouvert, afficher les options
    if jeu_instance.options_boutique_ouvert:
        # Fond du sous-menu
        submenu_rect = pygame.Rect(cx + 120, shop_y + 175, 200, 190)
        pygame.draw.rect(ecran, (30, 40, 60), submenu_rect, border_radius=10)
        pygame.draw.rect(ecran, OR, submenu_rect, 2, border_radius=10)

        # Boutons du sous-menu
        for btn in jeu_instance.btns_options_boutique_submenu:
            btn.dessiner(ecran)

    for b in jeu_instance.btns_pause:
        b.dessiner(ecran)


# ---------------------------------------------------
# ÉCRANS DE JEU
# ---------------------------------------------------
def dessiner_menu(jeu_instance, ecran):
    """Menu principal avec fond USA"""
    ecran.blit(jeu_instance.fond_menu, (0, 0))
    jeu_instance.draw_etoiles(ecran)
    jeu_instance.draw_fallings(ecran)
    temps = pygame.time.get_ticks()
    jeu_instance.afficher_titre(ecran, temps, texte="Happy 4th of July!", couleur=OR)
    for b in jeu_instance.btns_menu_img:
        b.draw(ecran)

    # Afficher le bouton niveau infini si débloqué
    if jeu_instance.niveau_infini_debloque:
        jeu_instance.btn_niveau_infini.dessiner(ecran)

    # Afficher le compteur de clés en haut à droite
    font_petite = pygame.font.Font(None, 28)
    nb_cles = len(jeu_instance.cles_trouvees)
    couleur_cles = OR if nb_cles >= 4 else BLANC
    txt_cles = font_petite.render(f"🔑 Clés: {nb_cles}/4", True, couleur_cles)
    ecran.blit(txt_cles, (LARGEUR_JEU - txt_cles.get_width() - 20, 20))

    # Si toutes les clés sont trouvées, afficher un message
    if nb_cles >= 4:
        font_msg = pygame.font.Font(None, 24)
        txt_msg = font_msg.render("✨ NIVEAU INFINI DÉBLOQUÉ !", True, OR)
        ecran.blit(txt_msg, (LARGEUR_JEU - txt_msg.get_width() - 20, 55))

    ecran.blit(jeu_instance.logo_trump, jeu_instance.logo_rect)


def dessiner_gif_screen(jeu_instance, ecran):
    ecran.blit(jeu_instance.fond_menu, (0, 0))
    jeu_instance.draw_gif(ecran)


def dessiner_transition(jeu_instance, ecran, grosse_font, font):
    """Écran de victoire de niveau - affiché après avoir terminé un niveau"""
    overlay = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    ecran.blit(overlay, (0, 0))

    # Titre de victoire
    niveau_termine = jeu_instance.niveau - 1  # Le niveau qu'on vient de finir
    t_victoire = grosse_font.render("VICTOIRE !", True, OR)
    ecran.blit(t_victoire, t_victoire.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 120)))

    # Message de niveau terminé
    t_niveau = font.render(f"Vous avez terminé le niveau {niveau_termine} !", True, VERT)
    ecran.blit(t_niveau, t_niveau.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 50)))

    # Prochain niveau
    t_suivant = font.render(f"Niveau {jeu_instance.niveau} à venir...", True, BLANC)
    ecran.blit(t_suivant, t_suivant.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 10)))

    # Instruction
    t_cont = font.render("Appuyez sur ESPACE pour continuer", True, JAUNE)
    ecran.blit(t_cont, t_cont.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 80)))


def dessiner_gameover(jeu_instance, ecran, grosse_font, font):
    overlay = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 230))
    ecran.blit(overlay, (0, 0))
    t_go = grosse_font.render("GAME OVER", True, ROUGE)
    ecran.blit(t_go, t_go.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 60)))
    t_score = font.render(f"Score Final: {jeu_instance.score_total}", True, OR)
    ecran.blit(t_score, t_score.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2)))
    ecran.blit(
        font.render("Appuie sur 'R' pour rejouer", True, BLANC),
        font.render("Appuie sur 'R' pour rejouer", True, BLANC).get_rect(
            center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 60))
    )


def dessiner_victoire(jeu_instance, ecran, grosse_font, font):
    overlay = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    ecran.blit(overlay, (0, 0))

    t_victoire = grosse_font.render("VICTOIRE !", True, OR)
    ecran.blit(t_victoire, t_victoire.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 100)))

    t_bravo = font.render("Tu as survécu aux 4 niveaux !", True, VERT)
    ecran.blit(t_bravo, t_bravo.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 - 30)))

    t_score = font.render(f"Score Final: {jeu_instance.score_total}", True, OR)
    ecran.blit(t_score, t_score.get_rect(center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 20)))

    ecran.blit(
        font.render("Appuie sur 'R' pour rejouer", True, BLANC),
        font.render("Appuie sur 'R' pour rejouer", True, BLANC).get_rect(
            center=(LARGEUR_JEU // 2, HAUTEUR_JEU // 2 + 80))
    )


def dessiner_options(jeu_instance, ecran, grosse_font, moyenne_font):
    """Dessine le menu des options"""
    # Fond avec le même style que le menu
    ecran.blit(jeu_instance.fond_menu, (0, 0))
    jeu_instance.draw_etoiles(ecran)

    # Titre
    titre = grosse_font.render("OPTIONS", True, OR)
    ecran.blit(titre, titre.get_rect(center=(LARGEUR_JEU // 2, 100)))

    # Sous-titre explicatif
    sous_titre = moyenne_font.render("Personnalisez votre experience", True, BLANC)
    ecran.blit(sous_titre, sous_titre.get_rect(center=(LARGEUR_JEU // 2, 180)))

    # Dessiner tous les boutons
    for btn in jeu_instance.btns_opt:
        btn.dessiner(ecran)


def dessiner_gameplay(jeu_instance, ecran, font, petite_font, grosse_font, moyenne_font):
    """Dessine l'écran de jeu"""
    # Obtenir l'offset de tremblement
    offset_x, offset_y = jeu_instance.vfx.get_tremblement_offset()

    # Créer une surface temporaire si tremblement actif
    if jeu_instance.vfx.tremblement_actif:
        surface_temp = pygame.Surface((LARGEUR_JEU, HAUTEUR_JEU))
        ecran_draw = surface_temp
    else:
        ecran_draw = ecran

    ecran_draw.blit(jeu_instance.image_fond, (jeu_instance.fond_x, jeu_instance.fond_y1))
    ecran_draw.blit(jeu_instance.image_fond, (jeu_instance.fond_x, jeu_instance.fond_y2))

    jeu_instance.all_sprites.draw(ecran_draw)
    jeu_instance.items.draw(ecran_draw)

    # Dessiner les projectiles du boss
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        for projectile in jeu_instance.boss.projectiles:
            ecran_draw.blit(projectile.image, projectile.rect)

    # Dessiner le laser du boss (par-dessus tout)
    if hasattr(jeu_instance, 'boss') and jeu_instance.boss:
        jeu_instance.boss.dessiner_laser(ecran_draw)

    # Barres de vie ennemis
    for m in jeu_instance.mobs:
        if m.max_pv > 1:
            w = m.rect.width
            h = 5
            ratio = m.pv / m.max_pv
            pygame.draw.rect(ecran_draw, ROUGE, (m.rect.x, m.rect.y - 10, w, h))
            pygame.draw.rect(ecran_draw, VERT, (m.rect.x, m.rect.y - 10, w * ratio, h))

    jeu_instance.vfx.draw(ecran_draw)

    # Bouclier d'invincibilité visuel
    if jeu_instance.joueur.invincible:
        pygame.draw.circle(ecran_draw, BLEU_BOUCLIER, jeu_instance.joueur.rect.center, 40, 3)

        # Compteur d'invincibilité
        temps_restant_invincibilite = (jeu_instance.joueur.fin_invincibilite - pygame.time.get_ticks()) / 1000
        if temps_restant_invincibilite > 0:
            # Afficher le temps restant en gros au centre-bas de l'écran
            temps_inv_txt = grosse_font.render(f"⚡ {temps_restant_invincibilite:.1f}s", True, BLEU_BOUCLIER)
            pos_x = LARGEUR_JEU // 2 - temps_inv_txt.get_width() // 2
            pos_y = HAUTEUR_JEU - 150

            # Fond semi-transparent
            fond_rect = pygame.Rect(pos_x - 20, pos_y - 10, temps_inv_txt.get_width() + 40,
                                    temps_inv_txt.get_height() + 20)
            fond_surface = pygame.Surface((fond_rect.width, fond_rect.height), pygame.SRCALPHA)
            fond_surface.fill((0, 100, 255, 180))
            ecran_draw.blit(fond_surface, fond_rect.topleft)

            # Texte du compteur
            ecran_draw.blit(temps_inv_txt, (pos_x, pos_y))

    # HUD
    ecran_draw.blit(font.render(f"Caisse: {jeu_instance.argent}$", True, OR), (20, 20))
    txt_n = font.render(f"Niveau: {jeu_instance.niveau}", True, JAUNE)
    ecran_draw.blit(txt_n, (LARGEUR_JEU // 2 - txt_n.get_width() // 2, 20))
    for i in range(jeu_instance.vies):
        ecran_draw.blit(jeu_instance.img_vie_ui, (LARGEUR_JEU - 70 - (i * 55), 20))
    txt_nuke = font.render(f"Nuke: {jeu_instance.joueur.nukes} [B]", True, ROUGE)
    ecran_draw.blit(txt_nuke, (20, 60))

    # TIMER - Ne pas afficher pendant la transition et la pause
    if jeu_instance.etat not in ("TRANSITION", "PAUSE"):
        # Timer global du niveau
        temps_ecoule = (pygame.time.get_ticks() - jeu_instance.debut_niveau) / 1000

        # Tous les niveaux durent 2 minutes (120 secondes)
        temps_niveau_actuel = jeu_instance.temps_niveau

        temps_restant = max(0, temps_niveau_actuel - temps_ecoule)
        minutes = int(temps_restant // 60)
        secondes = int(temps_restant % 60)

        # Couleur selon le temps restant
        if temps_restant > 60:
            couleur_timer = BLANC
        elif temps_restant > 30:
            couleur_timer = ORANGE
        else:
            couleur_timer = ROUGE

        # Afficher un label spécial pour le niveau 4 (boss)
        if jeu_instance.niveau == 4:
            txt_label = petite_font.render("TEMPS AVANT DÉFAITE:", True, ROUGE)
            ecran_draw.blit(txt_label, (LARGEUR_JEU // 2 - txt_label.get_width() // 2, 40))
            txt_timer = grosse_font.render(f"{minutes}:{secondes:02d}", True, couleur_timer)
            ecran_draw.blit(txt_timer, (LARGEUR_JEU // 2 - txt_timer.get_width() // 2, 65))
        else:
            # Niveaux 1, 2 et 3 : affichage normal
            txt_timer = moyenne_font.render(f"{minutes}:{secondes:02d}", True, couleur_timer)
            ecran_draw.blit(txt_timer, (LARGEUR_JEU // 2 - txt_timer.get_width() // 2, 55))

    # Appliquer le tremblement si actif
    if jeu_instance.vfx.tremblement_actif:
        ecran.fill((0, 0, 0))  # Fond noir pour éviter les artifacts
        ecran.blit(surface_temp, (offset_x, offset_y))

    # Afficher les hitboxes si debug mode
    if jeu_instance.debug_mode:
        dessiner_hitboxes(jeu_instance, ecran)
    
    # Afficher les infos debug si debug mode
    if jeu_instance.debug_mode:
        dessiner_debug_info(jeu_instance, ecran, petite_font)

    if jeu_instance.etat == "PAUSE":
        dessiner_pause_et_boutique(jeu_instance, ecran, grosse_font, moyenne_font, petite_font)
    elif jeu_instance.etat == "TRANSITION":
        dessiner_transition(jeu_instance, ecran, grosse_font, font)
    elif jeu_instance.etat == "GAMEOVER":
        dessiner_gameover(jeu_instance, ecran, grosse_font, font)


def dessiner_video_intro(jeu_instance, ecran, font):
    """Dessine la vidéo d'intro"""
    ecran.fill((0, 0, 0))

    if hasattr(jeu_instance, 'lecteur_video') and jeu_instance.lecteur_video:
        # Lire la frame suivante
        frame = jeu_instance.lecteur_video.lire_frame()

        if frame:
            # Redimensionner pour remplir l'écran
            frame_redim = jeu_instance.lecteur_video.redimensionner_frame(LARGEUR_JEU, HAUTEUR_JEU)
            if frame_redim:
                ecran.blit(frame_redim, (0, 0))

            # Texte pour skip
            txt_skip = font.render("Appuyez sur ESPACE ou cliquez pour passer", True, BLANC)
            ecran.blit(txt_skip, (LARGEUR_JEU // 2 - txt_skip.get_width() // 2, HAUTEUR_JEU - 50))

            # Limiter le FPS à celui de la vidéo
            if hasattr(jeu_instance, 'clock_video'):
                jeu_instance.clock_video.tick(jeu_instance.lecteur_video.fps)
        else:
            # Vidéo terminée, démarrer le jeu
            print("[INFO] Vidéo intro terminée")
            jeu_instance.lecteur_video.fermer()

            # Arrêter l'audio intro
            if hasattr(jeu_instance, 'audio_intro'):
                jeu_instance.audio_intro.arreter()

            jeu_instance.reset_partie()
            jeu_instance.etat = "JEU"
            pygame.mouse.set_visible(False)
            jeu_instance.musique.jouer_musique_niveau(1)


def dessiner_video_niveau2(jeu_instance, ecran, font):
    """Dessine la vidéo du niveau 2"""
    ecran.fill((0, 0, 0))

    if hasattr(jeu_instance, 'lecteur_video') and jeu_instance.lecteur_video:
        # Lire la frame suivante
        frame = jeu_instance.lecteur_video.lire_frame()

        if frame:
            # Redimensionner pour remplir l'écran
            frame_redim = jeu_instance.lecteur_video.redimensionner_frame(LARGEUR_JEU, HAUTEUR_JEU)
            if frame_redim:
                ecran.blit(frame_redim, (0, 0))

            # Texte pour skip
            txt_skip = font.render("Appuyez sur ESPACE ou cliquez pour passer", True, BLANC)
            ecran.blit(txt_skip, (LARGEUR_JEU // 2 - txt_skip.get_width() // 2, HAUTEUR_JEU - 50))

            # Limiter le FPS à celui de la vidéo
            if hasattr(jeu_instance, 'clock_video'):
                jeu_instance.clock_video.tick(jeu_instance.lecteur_video.fps)
        else:
            # Vidéo terminée, commencer le niveau 2
            print("[INFO] Vidéo niveau 2 terminée")
            jeu_instance.lecteur_video.fermer()

            # Arrêter l'audio
            if hasattr(jeu_instance, 'audio_niveau2'):
                jeu_instance.audio_niveau2.arreter()

            jeu_instance.etat = "JEU"
            pygame.mouse.set_visible(False)
            jeu_instance.debut_niveau = pygame.time.get_ticks()
            jeu_instance.musique.jouer_musique_niveau(2)


def dessiner_video_niveau3(jeu_instance, ecran, font):
    """Dessine la vidéo du niveau 3"""
    ecran.fill((0, 0, 0))

    if hasattr(jeu_instance, 'lecteur_video') and jeu_instance.lecteur_video:
        # Lire la frame suivante
        frame = jeu_instance.lecteur_video.lire_frame()

        if frame:
            # Redimensionner pour remplir l'écran
            frame_redim = jeu_instance.lecteur_video.redimensionner_frame(LARGEUR_JEU, HAUTEUR_JEU)
            if frame_redim:
                ecran.blit(frame_redim, (0, 0))

            # Texte pour skip
            txt_skip = font.render("Appuyez sur ESPACE ou cliquez pour passer", True, BLANC)
            ecran.blit(txt_skip, (LARGEUR_JEU // 2 - txt_skip.get_width() // 2, HAUTEUR_JEU - 50))

            # Limiter le FPS à celui de la vidéo
            if hasattr(jeu_instance, 'clock_video'):
                jeu_instance.clock_video.tick(jeu_instance.lecteur_video.fps)
        else:
            # Vidéo terminée, commencer le niveau 3
            print("[INFO] Vidéo niveau 3 terminée")
            jeu_instance.lecteur_video.fermer()

            # Arrêter l'audio
            if hasattr(jeu_instance, 'audio_niveau3'):
                jeu_instance.audio_niveau3.arreter()

            jeu_instance.etat = "JEU"
            pygame.mouse.set_visible(False)
            jeu_instance.debut_niveau = pygame.time.get_ticks()
            jeu_instance.musique.jouer_musique_niveau(3)


def dessiner_video_niveau4(jeu_instance, ecran, font):
    """Dessine la vidéo du niveau 4 (après avoir battu le boss)"""
    ecran.fill((0, 0, 0))

    if hasattr(jeu_instance, 'lecteur_video') and jeu_instance.lecteur_video:
        # Lire la frame suivante
        frame = jeu_instance.lecteur_video.lire_frame()

        if frame:
            # Redimensionner pour remplir l'écran
            frame_redim = jeu_instance.lecteur_video.redimensionner_frame(LARGEUR_JEU, HAUTEUR_JEU)
            if frame_redim:
                ecran.blit(frame_redim, (0, 0))

            # Texte pour skip
            txt_skip = font.render("Appuyez sur ESPACE ou cliquez pour passer", True, BLANC)
            ecran.blit(txt_skip, (LARGEUR_JEU // 2 - txt_skip.get_width() // 2, HAUTEUR_JEU - 50))

            # Limiter le FPS à celui de la vidéo
            if hasattr(jeu_instance, 'clock_video'):
                jeu_instance.clock_video.tick(jeu_instance.lecteur_video.fps)
        else:
            # Vidéo terminée, aller à l'écran de victoire
            print("[INFO] Vidéo niveau 4 terminée")
            jeu_instance.lecteur_video.fermer()

            # Arrêter l'audio
            if hasattr(jeu_instance, 'audio_niveau4'):
                jeu_instance.audio_niveau4.arreter()

            jeu_instance.etat = "VICTOIRE"
            pygame.mouse.set_visible(True)


def dessiner_jeu(jeu_instance, ecran, font, petite_font, grosse_font, moyenne_font):
    """Dessine tous les éléments selon l'état actuel"""
    ecran.fill(BLEU_NUIT)

    if jeu_instance.etat == "VIDEO_INTRO":
        dessiner_video_intro(jeu_instance, ecran, font)
    elif jeu_instance.etat == "VIDEO_NIVEAU2":
        dessiner_video_niveau2(jeu_instance, ecran, font)
    elif jeu_instance.etat == "VIDEO_NIVEAU3":
        dessiner_video_niveau3(jeu_instance, ecran, font)
    elif jeu_instance.etat == "VIDEO_NIVEAU4":
        dessiner_video_niveau4(jeu_instance, ecran, font)
    elif jeu_instance.etat == "MENU":
        dessiner_menu(jeu_instance, ecran)
    elif jeu_instance.etat == "GIF":
        dessiner_gif_screen(jeu_instance, ecran)
    elif jeu_instance.etat == "OPTIONS":
        dessiner_options(jeu_instance, ecran, grosse_font, moyenne_font)
    elif jeu_instance.etat == "GAMEOVER":
        dessiner_gameover(jeu_instance, ecran, grosse_font, font)
    elif jeu_instance.etat == "VICTOIRE":
        dessiner_victoire(jeu_instance, ecran, grosse_font, font)
    elif jeu_instance.etat in ("JEU", "GAME", "PAUSE", "TRANSITION"):  # CORRECTION ICI
        dessiner_gameplay(jeu_instance, ecran, font, petite_font, grosse_font, moyenne_font)

    pygame.display.flip()