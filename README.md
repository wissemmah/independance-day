# Independence Day : Deluxe Edition — 250th Anniversary

Projet réalisé en **février 2026**.

Shoot 'em up arcade horizontal en Python / Pygame : 4 niveaux, boss final, mode infini débloquable via des clés secrètes.

## Prérequis

- Python 3.10+
- Pygame

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le jeu

```bash
python Main.py
```

Outils utiles :

```bash
python run_debug.py      # lancement avec options debug
python run_tests.py      # smoke tests runtime
python check_assets.py   # vérifie les assets
```

## Binaires (Windows / macOS)

Sans Python : télécharge les artefacts de la [Release](https://github.com/wissemmah/independance-day/releases) ou du workflow **Build releases**.

| Plateforme | Fichier | Lancement |
|------------|---------|-----------|
| Windows | `IndependenceDay-Windows.zip` | Dézipper → double-clic `IndependenceDay.exe` |
| macOS | `IndependenceDay-macOS.dmg` | Ouvrir le DMG → glisser l’app dans Applications |

### Build local

```bash
# macOS → .app + .dmg
bash scripts/build_mac_dmg.sh

# Windows → dossier + .zip (à lancer sous Windows)
scripts\build_windows.bat
```

Ou déclencher le workflow GitHub Actions **Build releases** (onglet Actions → Run workflow).

## Contrôles

| Action | Touche |
|--------|--------|
| Déplacement | Flèches gauche / droite |
| Tir | Automatique |
| Nuke | `B` |
| Pause / boutique | `Échap` / pause in-game |
| Debug | `D` (voir `DEBUG_MODE.md`) |

---

## Lore (Histoire et univers)

Le jeu se déroule lors de la 250ᵉ fête de l’indépendance des États-Unis. Toute une ville est en pleine célébration quand une catastrophe survient : des tornades géantes apparaissent et menacent de tout détruire.

Le président Donald Trump, présent sur place pour l’événement, fait appel au seul héros disponible : un vétéran et ancien soldat, protecteur de la ville. Sa mission : détruire les tornades à l’aide d’une arme spéciale tirant de grosses balles visibles.

Après la destruction des tornades, le président vient le féliciter avec son char d’assaut — mais une nouvelle menace surgit : une invasion d’OVNIs et d’extraterrestres. Le héros reçoit alors un avion de combat pour défendre le ciel.

Une fois l’invasion repoussée, une troisième catastrophe arrive : des météorites foncent vers la Terre. Le héros reçoit un vaisseau spatial ultra-puissant appelé :

**Star-Spangled Destroyer X — Édition 250ᵉ anniversaire**

Il part dans l’espace pour sauver la planète.

Alors que tout semble terminé, un boss final apparaît : une tête géante ennemie flottant dans l’espace qui tire des lasers. Le héros doit la vaincre lors d’un combat final.

Après la victoire, le héros revient sur Terre et est remercié publiquement lors d’une grande célébration.

## Gameplay

### Structure des niveaux

| Niveau | Menace | Personnage | Objectif |
|--------|--------|------------|----------|
| 1 | Tornades | Vétéran au sol | Détruire les tornades (objectif de kills ou survivre au timer) |
| 2 | Invasion alien | Pilote d’avion | Détruire les UFO (zigzag + plongeons) |
| 3 | Météorites / comètes | Astronaute | Mix comètes rebondissantes + météorites |
| 4 | Boss final | Vaisseau | Battre le boss avant la fin du timer |

### Système de vies

- 3 vies au départ (représentées par des vaches)
- À 0 vie = partie perdue

### Bonus & mode infini

- Items ramassables en passant dessus
- Une clé secrète apparaît dans chaque niveau (~30 s) : **4/4 clés → mode infini**
- High score sauvegardé localement dans `data/highscore.json`

### Objectif

Terminer les 4 niveaux, maximiser le score, battre le boss, débloquer le mode infini.
