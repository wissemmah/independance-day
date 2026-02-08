# 🎮 Mode Debug - Guide d'utilisation

## Activation
- **D** : Activer/Désactiver le mode debug

## Fonctionnalités du Debug Mode

### 🔍 Affichage
Une fois le mode debug activé (touche **D**), les informations suivantes s'affichent :

- **FPS** : Nombre d'images par seconde
- **Position du joueur** : Coordonnées (X, Y)
- **Nombre d'ennemis** : Ennemis actifs à l'écran
- **Numéro de vague** : Vague actuelle
- **Invincibilité** : État de l'invincibilité
- **Ennemis infinis** : Mode ennemis illimités activé
- **Vitesse du jeu** : Multiplicateur actuel
- **Hitboxes** : Affichage des zones de collision
  - 🟢 Vert : Joueur
  - 🔴 Rouge : Ennemis
  - 🟡 Jaune : Projectiles du joueur
  - 🟠 Orange : Projectiles du boss
  - ⚪ Blanc : Items

### ⚡ Pouvoirs du Debug (disponibles quand le mode debug est ON)

| Touche | Action |
|--------|--------|
| **I** | Toggle invincibilité infinie |
| **E** | Toggle spawn d'ennemis infinis |
| **1** | Sauter au niveau 1 |
| **2** | Sauter au niveau 2 |
| **3** | Sauter au niveau 3 |
| **4** | Sauter au niveau 4 (Boss) |
| **+** | Augmenter la vitesse du jeu (×0.25) |
| **-** | Diminuer la vitesse du jeu (×0.25) |

## Exemples d'utilisation

### 🧪 Tester les niveaux rapidement
1. Appuyer sur **D** pour activer le debug
2. Appuyer sur **2** pour sauter au niveau 2
3. Tester le niveau et appuyer sur **D** pour voir les FPS, ennemis, etc.

### 🛡️ Tester l'invincibilité
1. Appuyer sur **D**
2. Appuyer sur **I** pour activer l'invincibilité
3. Les ennemis ne peuvent plus faire de dégâts

### 🚀 Mode ralenti pour observer le jeu
1. Appuyer sur **D**
2. Appuyer plusieurs fois sur **-** pour ralentir (ex: 0.5x = ralenti)
3. Parfait pour observer les patterns d'ennemis

### 👾 Tester les limites de spawning
1. Appuyer sur **D**
2. Appuyer sur **E** pour activer les ennemis infinis
3. Observer les performances avec beaucoup d'ennemis

## ℹ️ Notes

- Le mode debug **n'affecte pas les économies** (argent, vies, etc.)
- Les informations debug sont affichées en haut à gauche
- Les hitboxes aident à debug les collisions
- La vitesse du jeu peut être réglée de **0.25x à 3.0x**

## 🐛 Affichage dans les consoles

Chaque action de debug est loggée dans la console :
```
[DEBUG] Mode debug: ON
[DEBUG] Invincibilité: True
[DEBUG] Ennemis infinis: True
[DEBUG] Saut au niveau 2
[DEBUG] Vitesse du jeu: 1.5x
```
