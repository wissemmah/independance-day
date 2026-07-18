# Signature macOS (Gatekeeper)

Les builds non signés peuvent être bloqués par macOS (« développeur non identifié »).

## Contournement joueur (sans certificat)

1. Clic droit sur `IndependenceDay.app` → **Ouvrir** → confirmer  
   ou  
2. Réglages Système → Confidentialité et sécurité → **Ouvrir quand même**

## Signature ad-hoc (dev local)

```bash
codesign --force --deep --sign - dist/IndependenceDay.app
```

## Signature Developer ID (distribution)

Nécessite un compte Apple Developer :

```bash
codesign --force --deep --options runtime \
  --sign "Developer ID Application: VOTRE NOM (TEAMID)" \
  dist/IndependenceDay.app

xcrun notarytool submit dist/IndependenceDay-macOS.dmg \
  --apple-id "email@example.com" --team-id TEAMID --wait
```

Sans certificat Apple, la CI livre un DMG non notarisé (comportement attendu).
