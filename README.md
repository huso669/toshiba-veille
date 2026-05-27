# Veille Prix Toshiba — Climshop.com

Page web mise à jour automatiquement chaque jour avec les prix des climatiseurs Toshiba sur climshop.com.

## Modèles suivis
- Gamme Yukai (1.5 à 4.2 kW)
- Gamme Shorai Edge (2.0 à 5.0 kW)
- Gamme Haori (2.5 et 4.6 kW)

## Comment ça marche
Un script Python tourne automatiquement chaque matin à 7h via GitHub Actions.
Il scrape les prix sur climshop.com et met à jour `index.html`.
La page est publiée via GitHub Pages.

## Mise à jour manuelle
Va dans l'onglet **Actions** de ce dépôt → clique sur **"Mise à jour prix Toshiba"** → **"Run workflow"**.
