import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json, os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

PRODUITS = [
    {"gamme":"Yukai","nom":"Yukai 1.5 kW","ref":"RAS-B05E2KVG","url":"https://www.climshop.com/181-yukai-ras-b05e2kvg-ras-05e2avg.html"},
    {"gamme":"Yukai","nom":"Yukai 2.0 kW","ref":"RAS-B07E2KVG","url":"https://www.climshop.com/182-yukai-ras-b07e2kvg-ras-07e2avg.html"},
    {"gamme":"Yukai","nom":"Yukai 2.5 kW","ref":"RAS-B10E2KVG","url":"https://www.climshop.com/183-yukai-ras-b10e2kvg-ras-10e2avg.html"},
    {"gamme":"Yukai","nom":"Yukai 3.3 kW","ref":"RAS-B13E2KVG","url":"https://www.climshop.com/184-yukai-ras-b13e2kvg-ras-13e2avg.html"},
    {"gamme":"Yukai","nom":"Yukai 4.2 kW","ref":"RAS-B16E2KVG","url":"https://www.climshop.com/185-yukai-ras-b16e2kvg-ras-16e2avg.html"},
    {"gamme":"Shorai Edge","nom":"Shorai Edge 2.0 kW","ref":"RAS-B07G3KVSG","url":"https://www.climshop.com/189-shorai-edge-ras-b07g3kvsg-ras-07j2avsg.html"},
    {"gamme":"Shorai Edge","nom":"Shorai Edge 2.5 kW","ref":"RAS-B10G3KVSG","url":"https://www.climshop.com/190-shorai-edge-ras-b10g3kvsg-ras-10j2avsg.html"},
    {"gamme":"Shorai Edge","nom":"Shorai Edge 3.5 kW","ref":"RAS-B13G3KVSG","url":"https://www.climshop.com/191-shorai-edge-ras-b13g3kvsg-ras-13j2avsg.html"},
    {"gamme":"Shorai Edge","nom":"Shorai Edge 4.6 kW","ref":"RAS-B16G3KVSG","url":"https://www.climshop.com/192-shorai-edge-ras-b16g3kvsg-ras-16j2avsg.html"},
    {"gamme":"Shorai Edge","nom":"Shorai Edge 5.0 kW","ref":"RAS-B18G3KVSG","url":"https://www.climshop.com/193-shorai-edge-ras-b18g3kvsg-ras-18j2avsg.html"},
    {"gamme":"Haori","nom":"Haori 2.5 kW","ref":"RAS-B10N4KVRG","url":"https://www.climshop.com/196-haori-ras-b10n4kvrg-ras-10j2avsg.html"},
    {"gamme":"Haori","nom":"Haori 4.6 kW","ref":"RAS-B16N4KVRG","url":"https://www.climshop.com/198-haori-ras-b16n4kvrg-ras-16j2avsg.html"},
]

def scrape(p):
    try:
        r = requests.get(p["url"], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.find(itemprop="price")
        if tag:
            ttc = float(tag.get("content", "0"))
            ht = round(ttc / 1.2, 2)
            return {"ttc": ttc, "ht": ht, "ok": True}
        return {"ttc": None, "ht": None, "ok": False}
    except:
        return {"ttc": None, "ht": None, "ok": False}

# Charger historique
hist_file = "historique.json"
historique = {}
if os.path.exists(hist_file):
    with open(hist_file) as f:
        historique = json.load(f)

resultats = []
for p in PRODUITS:
    prix = scrape(p)
    entry = {**p, **prix, "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
    # Détecter changement de prix
    prev = historique.get(p["ref"])
    entry["changed"] = prev is not None and prev != prix["ttc"] and prix["ok"]
    entry["prev_ttc"] = prev
    resultats.append(entry)
    if prix["ok"]:
        historique[p["ref"]] = prix["ttc"]

with open(hist_file, "w") as f:
    json.dump(historique, f)

# Grouper par gamme
gammes = {}
for r in resultats:
    gammes.setdefault(r["gamme"], []).append(r)

date_maj = datetime.now().strftime("%d/%m/%Y à %Hh%M")

def fmt(v):
    if v is None: return "—"
    return f"{v:,.0f} €".replace(",", " ")

def evol(r):
    if not r["ok"] or r["prev_ttc"] is None: return ""
    diff = r["ttc"] - r["prev_ttc"]
    if diff > 0: return f'<span class="up">▲ +{fmt(diff)}</span>'
    if diff < 0: return f'<span class="down">▼ {fmt(diff)}</span>'
    return '<span class="stable">= stable</span>'

tables = ""
for gamme, produits in gammes.items():
    rows = ""
    for r in produits:
        rows += f"""<tr>
          <td><strong>{r['nom']}</strong><span class="ref">{r['ref']}</span></td>
          <td class="prix">{fmt(r['ttc'])}</td>
          <td class="ht">{fmt(r['ht'])}</td>
          <td>{evol(r)}</td>
          <td><a href="{r['url']}" target="_blank">Voir →</a></td>
        </tr>"""
    tables += f'<h2>{gamme}</h2><table><thead><tr><th>Modèle</th><th>Prix TTC</th><th>Prix HT</th><th>Évolution</th><th>Lien</th></tr></thead><tbody>{rows}</tbody></table>'

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prix Toshiba — Climshop</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Arial,sans-serif;background:#f0f4f8;color:#1a2c3d}}
.header{{background:linear-gradient(135deg,#1a3a5c,#2e86c1);color:#fff;padding:22px 28px 18px}}
.header h1{{font-size:20px;margin-bottom:4px}}
.header p{{font-size:12px;opacity:.75;margin-top:4px}}
.container{{max-width:900px;margin:20px auto;padding:0 14px}}
h2{{font-size:13px;font-weight:700;color:#1a3a5c;text-transform:uppercase;letter-spacing:.5px;margin:22px 0 8px;padding-left:4px;border-left:3px solid #2e86c1}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:6px}}
th{{background:#2e86c1;color:#fff;padding:10px 12px;text-align:left;font-size:12px;font-weight:600}}
th:nth-child(2),th:nth-child(3),td:nth-child(2),td:nth-child(3){{text-align:right}}
td{{padding:11px 12px;border-bottom:1px solid #eef2f6;font-size:13px;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:#f7fafd}}
.prix{{font-weight:700;font-size:15px;color:#1a3a5c}}
.ht{{color:#7f8c8d;font-size:12px}}
.ref{{font-size:11px;color:#95a5a6;display:block;margin-top:2px}}
a{{color:#2e86c1;text-decoration:none;font-size:12px}}
a:hover{{text-decoration:underline}}
.up{{color:#e74c3c;font-size:12px}}
.down{{color:#27ae60;font-size:12px}}
.stable{{color:#95a5a6;font-size:12px}}
.footer{{text-align:center;color:#95a5a6;font-size:11px;margin:18px 0 32px}}
@media(max-width:550px){{th:nth-child(3),td:nth-child(3),th:nth-child(4),td:nth-child(4){{display:none}}}}
</style>
</head>
<body>
<div class="header">
  <h1>❄️ Prix Toshiba — Climshop.com</h1>
  <p>Mise à jour automatique · Dernière vérification : {date_maj}</p>
</div>
<div class="container">
{tables}
</div>
<div class="footer">Mis à jour automatiquement chaque jour via GitHub Actions · Source : climshop.com</div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html généré — {date_maj}")
