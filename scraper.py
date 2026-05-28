name: Mise à jour prix climatisation

on:
  schedule:
    - cron: '0 7 * * *'
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Installer les dépendances
        run: |
          pip install playwright requests beautifulsoup4
          playwright install chromium
          playwright install-deps chromium
      - name: Lancer le scraper
        run: python scraper.py
      - name: Commit et push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "Prix mis à jour automatiquement"
          git push
