import json, os, re
from datetime import datetime

# Playwright pour contourner le blocage JS de climshop
from playwright.sync_api import sync_playwright

MARQUES = {
    "toshiba": {
        "nom": "Toshiba", "couleur": "#2e86c1",
        "desc": "Yukai · Shorai Edge · Haori · Multi-splits",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Yukai","nom":"Yukai 1.5 kW","ref":"RAS-B05E2KVG","url":"https://www.climshop.com/181-yukai-ras-b05e2kvg-ras-05e2avg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Yukai","nom":"Yukai 2.0 kW","ref":"RAS-B07E2KVG","url":"https://www.climshop.com/182-yukai-ras-b07e2kvg-ras-07e2avg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Yukai","nom":"Yukai 2.5 kW","ref":"RAS-B10E2KVG","url":"https://www.climshop.com/183-yukai-ras-b10e2kvg-ras-10e2avg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Yukai","nom":"Yukai 3.3 kW","ref":"RAS-B13E2KVG","url":"https://www.climshop.com/184-yukai-ras-b13e2kvg-ras-13e2avg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Yukai","nom":"Yukai 4.2 kW","ref":"RAS-B16E2KVG","url":"https://www.climshop.com/185-yukai-ras-b16e2kvg-ras-16e2avg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Shorai Edge","nom":"Shorai Edge 2.0 kW","ref":"RAS-B07G3KVSG","url":"https://www.climshop.com/189-shorai-edge-ras-b07g3kvsg-ras-07j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Shorai Edge","nom":"Shorai Edge 2.5 kW","ref":"RAS-B10G3KVSG","url":"https://www.climshop.com/190-shorai-edge-ras-b10g3kvsg-ras-10j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Shorai Edge","nom":"Shorai Edge 3.5 kW","ref":"RAS-B13G3KVSG","url":"https://www.climshop.com/191-shorai-edge-ras-b13g3kvsg-ras-13j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Shorai Edge","nom":"Shorai Edge 4.6 kW","ref":"RAS-B16G3KVSG","url":"https://www.climshop.com/192-shorai-edge-ras-b16g3kvsg-ras-16j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Shorai Edge","nom":"Shorai Edge 5.0 kW","ref":"RAS-B18G3KVSG","url":"https://www.climshop.com/193-shorai-edge-ras-b18g3kvsg-ras-18j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Haori","nom":"Haori 2.5 kW","ref":"RAS-B10N4KVRG","url":"https://www.climshop.com/196-haori-ras-b10n4kvrg-ras-10j2avsg.html"},
            {"gamme":"Mural & Console","sous_gamme":"Haori","nom":"Haori 4.6 kW","ref":"RAS-B16N4KVRG","url":"https://www.climshop.com/198-haori-ras-b16n4kvrg-ras-16j2avsg.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 2.9 kW","ref":"RAS-2M10G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 4.0 kW","ref":"RAS-2M14G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 5.2 kW","ref":"RAS-2M18G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Tri-split 5.2 kW","ref":"RAS-3M18G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Tri-split 7.5 kW","ref":"RAS-3M26G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Quadri-split 8.0 kW","ref":"RAS-4M27G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Penta-split 10.0 kW","ref":"RAS-5M34G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 1.5 kW","ref":"RAS-B05B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 2.0 kW","ref":"RAS-B07B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 2.5 kW","ref":"RAS-B10B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 3.3 kW","ref":"RAS-B13B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 4.2 kW","ref":"RAS-B16B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Packs bi-split","nom":"Bi-split Yukai 1.5+3.3 kW","ref":"BISPLIT-YUKAI-05-13","url":"https://www.climshop.com/260-bisplit-ras2m18g3avge-rasb05e2kvge-rasb13e2kvge.html"},
        ]
    },
    "daikin": {
        "nom": "Daikin", "couleur": "#0066cc",
        "desc": "Sensira · Comfora · Perfera · Stylish",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 2.0 kW","ref":"FTXF20F/RXF20F","url":"https://www.climshop.com/23-ftxf20e-rxf20e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 2.5 kW","ref":"FTXF25F/RXF25F","url":"https://www.climshop.com/58-ftxf25e-rxf25e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 3.5 kW","ref":"FTXF35F/RXF35F","url":"https://www.climshop.com/59-ftxf35e-rxf35e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 5.0 kW","ref":"FTXF50F/RXF50D","url":"https://www.climshop.com/61-ftxf50e-rxf50e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 7.1 kW","ref":"FTXF71F/RXF71D","url":"https://www.climshop.com/63-ftxf71e-rxf71e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 2.5 kW","ref":"FTXP25N/RXP25N","url":"https://www.climshop.com/65-ftxp25n-rxp25m.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 3.5 kW","ref":"FTXP35N/RXP35N","url":"https://www.climshop.com/68-ftxp35n-rxp35n.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 5.0 kW","ref":"FTXP50N/RXP50N","url":"https://www.climshop.com/daikin-ftxp50m-rxp50m-xml-428_429_439_227_312_609-3776.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 2.0 kW","ref":"FTXM20R/RXM20R","url":"https://www.climshop.com/daikin-ftxm20r-rxm20r-xml-428_429_439_227_312_610-3789.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 2.5 kW","ref":"FTXM25R/RXM25R","url":"https://www.climshop.com/72-ftxm25r-rxm25r.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 3.5 kW","ref":"FTXM35R/RXM35R","url":"https://www.climshop.com/73-ftxm35r-rxm35r.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 5.0 kW","ref":"FTXM50R/RXM50R","url":"https://www.climshop.com/daikin-ftxm50r-rxm50r-xml-428_429_439_227_312_610-3792.html"},
            {"gamme":"Mural & Console","sous_gamme":"Stylish","nom":"Stylish 2.5 kW","ref":"FTXA25AW/RXA25A","url":"https://www.climshop.com/90-ftxa25aw-rxa25a-blanc.html"},
        ]
    },
    "mitsubishi": {
        "nom": "Mitsubishi Electric", "couleur": "#cc0000",
        "desc": "HR Essentiel · AP Compact · EF Design · LN",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 2.5 kW","ref":"MSZ-HR25VFK","url":"https://www.climshop.com/126-msz-hr25vf-muz-hr25vf.html"},
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 3.5 kW","ref":"MSZ-HR35VFK","url":"https://www.climshop.com/128-msz-hr35vf-muz-hr35vf.html"},
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 5.0 kW","ref":"MSZ-HR50VFK","url":"https://www.climshop.com/130-msz-hr50vf-muz-hr50vf.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 2.5 kW","ref":"MSZ-AP25VGK","url":"https://www.climshop.com/1msz-ap25vgk-1muz-ap25vg-xml-428_429_439_216_318_619-3865.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 3.5 kW","ref":"MSZ-AP35VGK","url":"https://www.climshop.com/1msz-ap35vgk-1muz-ap35vg-xml-428_429_439_216_318_619-3864.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 5.0 kW","ref":"MSZ-AP50VGK","url":"https://www.climshop.com/1msz-ap50vgk-1muz-ap50vg-xml-428_429_439_216_318_619-3866.html"},
            {"gamme":"Mural & Console","sous_gamme":"EF Design","nom":"EF 2.5 kW","ref":"MSZ-EF25VGKW","url":"https://www.climshop.com/142-msz-ef25vgkw-muz-ef25vg-blanc.html"},
            {"gamme":"Mural & Console","sous_gamme":"EF Design","nom":"EF 3.5 kW","ref":"MSZ-EF35VGKW","url":"https://www.climshop.com/145-msz-ef35vgkw-muz-ef35vg-blanc.html"},
            {"gamme":"Mural & Console","sous_gamme":"LN Design De Luxe","nom":"LN 2.5 kW","ref":"MSZ-LN25VG2W","url":"https://www.climshop.com/157-msz-ln25vg2w-muz-ln25vghz2-blanc.html"},
            {"gamme":"Mural & Console","sous_gamme":"LN Design De Luxe","nom":"LN 3.5 kW","ref":"MSZ-LN35VG2W","url":"https://www.climshop.com/161-msz-ln35vg2w-muz-ln35vghz2-blanc-hyper.html"},
        ]
    },
    "atlantic": {
        "nom": "Atlantic Fujitsu", "couleur": "#006699",
        "desc": "Takao Plus · Takao M1",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 2.0 kW","ref":"ASYH7KJCA","url":"https://www.climshop.com/218-takao-plus-2kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 2.5 kW","ref":"ASYH9KJCA","url":"https://www.climshop.com/219-takao-plus-2-5kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 3.4 kW","ref":"ASYH12KJCA","url":"https://www.climshop.com/220-takao-plus-3-4kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 4.2 kW","ref":"ASYH14KJCA","url":"https://www.climshop.com/221-takao-plus-4-2kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao M2","nom":"Takao M2 3.4 kW","ref":"ASYG12KMCC","url":"https://www.climshop.com/220-takao-m2-asyg12-kmccui-ayog.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao M2","nom":"Takao M2 5.2 kW","ref":"ASYG18KMCC","url":"https://www.climshop.com/takaom2-fujitsu-atlantic-xsl-428_429_439_255_314_630.html"},
        ]
    },
    "lg": {
        "nom": "LG", "couleur": "#a50034",
        "desc": "Standard Wifi · Dualcool Premium · Artcool Gallery",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 2.5 kW","ref":"EZ09CYN","url":"https://www.climshop.com/223-lg-standard-wifi-s09etnsj-s09etua3.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 3.5 kW","ref":"EZ12CYN","url":"https://www.climshop.com/standard-wifi-s12etnsj-s12etua3-xml-428_429_439_343_344_637-3953.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 5.0 kW","ref":"EZ18CYN","url":"https://www.climshop.com/225-lg-standard-wifi-s18etnsk-s18etul2.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 7.0 kW","ref":"EZ24CYN","url":"https://www.climshop.com/226-lg-standard-wifi-s24etnsj-s24etua3.html"},
            {"gamme":"Mural & Console","sous_gamme":"Dualcool Premium","nom":"Dualcool 2.5 kW","ref":"H09S1P","url":"https://www.climshop.com/841-dualcool-premium-lg-h09s1p-ns1-et-h09s1p-u18.html"},
            {"gamme":"Mural & Console","sous_gamme":"Dualcool Premium","nom":"Dualcool 3.5 kW","ref":"H12S1P","url":"https://www.climshop.com/842-dualcool-premium-lg-h12s1p-ns1-et-h12s1p-u18.html"},
            {"gamme":"Mural & Console","sous_gamme":"Artcool Gallery","nom":"Artcool Gallery 3.7 kW","ref":"A12GA2","url":"https://www.climshop.com/838-artcool-gallery-premium-a12ga2nse-et-a12ga2u18.html"},
        ]
    },
    "samsung": {
        "nom": "Samsung", "couleur": "#1428a0",
        "desc": "AR35 Wifi · CEBU S2 · WindFree Comfort S2",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 2.0 kW","ref":"AR07TXHQ","url":"https://www.climshop.com/903-ar35-wifi-samsung-2000w.html"},
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 3.5 kW","ref":"AR12TXHQ","url":"https://www.climshop.com/904-ar35-wifi-samsung-3500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 7.0 kW","ref":"AR24TXHQ","url":"https://www.climshop.com/906-ar35-wifi-samsung-7200w.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 2.0 kW","ref":"AR07BXEA","url":"https://www.climshop.com/907-cebus2-samsung-2000w.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 2.5 kW","ref":"AR09BXEA","url":"https://www.climshop.com/908-cebus2-samsung-2500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 3.5 kW","ref":"AR12BXEA","url":"https://www.climshop.com/909-cebus2-samsung-3500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 5.0 kW","ref":"AR18BXEA","url":"https://www.climshop.com/911-cebus2-samsung-5000w.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 2.5 kW","ref":"AR09BXCA","url":"https://www.climshop.com/912-windfree-samsung-2500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 3.5 kW","ref":"AR12BXCA","url":"https://www.climshop.com/913-windfree-samsung-3500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 5.0 kW","ref":"AR18BXCA","url":"https://www.climshop.com/914-windfree-samsung-5000w.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 7.0 kW","ref":"AR24BXCA","url":"https://www.climshop.com/915-windfree-samsung-7000w.html"},
        ]
    }
}

MARQUES_ORDRE = ["toshiba","daikin","mitsubishi","atlantic","lg","samsung"]

ICONES = {
    "toshiba":    '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#2e86c1"/><text x="20" y="26" text-anchor="middle" font-size="11" font-weight="bold" fill="white" font-family="Arial">TOSH</text></svg>',
    "daikin":     '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#0066cc"/><text x="20" y="26" text-anchor="middle" font-size="11" font-weight="bold" fill="white" font-family="Arial">DAIK</text></svg>',
    "mitsubishi": '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#cc0000"/><text x="20" y="26" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="Arial">MITS</text></svg>',
    "atlantic":   '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#006699"/><text x="20" y="26" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="Arial">ATL</text></svg>',
    "lg":         '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#a50034"/><text x="20" y="26" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="Arial">LG</text></svg>',
    "samsung":    '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#1428a0"/><text x="20" y="26" text-anchor="middle" font-size="9" font-weight="bold" fill="white" font-family="Arial">SAMS</text></svg>',
}

def mon_prix(ttc):
    return round(ttc * 0.80 * 1.40 * 1.20, 2)

def fmt(v):
    if v is None: return "—"
    return f"{v:,.2f} €".replace(",", " ").replace(".", ",")

def scrape_all(urls_refs):
    """Scrape multiple URLs using Playwright browser"""
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        for url, ref in urls_refs:
            if url in results:
                continue
            try:
                print(f"  {url.split('/')[-1]}...", end=" ", flush=True)
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(2000)
                
                # Méthode 1 : itemprop="price"
                ttc = None
                el = page.query_selector('[itemprop="price"]')
                if el:
                    val = el.get_attribute("content") or el.inner_text()
                    try:
                        ttc = float(re.sub(r"[^\d.]", "", val.replace(",",".")))
                    except: pass
                
                # Méthode 2 : .current-price span
                if not ttc:
                    el = page.query_selector(".current-price span")
                    if el:
                        val = el.inner_text().strip()
                        try:
                            ttc = float(re.sub(r"[^\d,]", "", val).replace(",","."))
                        except: pass
                
                # Méthode 3 : data-price attribute
                if not ttc:
                    el = page.query_selector("[data-price]")
                    if el:
                        try:
                            ttc = float(el.get_attribute("data-price"))
                        except: pass
                
                # Méthode 4 : chercher dans le contenu de la page
                if not ttc:
                    content = page.content()
                    m = re.search(r'"price"\s*:\s*"?([0-9]+(?:[.,][0-9]+)?)"?', content)
                    if m:
                        try:
                            ttc = float(m.group(1).replace(",","."))
                            if ttc < 50: ttc = None
                        except: pass
                
                if ttc and ttc > 50:
                    results[url] = {"ttc": ttc, "ht": round(ttc/1.2, 2), "ok": True}
                    print(fmt(ttc))
                else:
                    results[url] = {"ttc": None, "ht": None, "ok": False}
                    print("❌")
                    
            except Exception as e:
                results[url] = {"ttc": None, "ht": None, "ok": False}
                print(f"❌ ({str(e)[:30]})")
        
        browser.close()
    return results

hist_file = "historique.json"
historique = {}
if os.path.exists(hist_file):
    with open(hist_file) as f:
        historique = json.load(f)

date_maj = datetime.now().strftime("%d/%m/%Y à %Hh%M")

def evol_html(ref, ttc, ok):
    if not ok: return ""
    prev = historique.get(ref)
    if prev is None: return ""
    diff = ttc - prev
    if diff > 0: return f'<span class="up">▲ +{fmt(diff)}</span>'
    if diff < 0: return f'<span class="down">▼ {fmt(diff)}</span>'
    return '<span class="stable">= stable</span>'

CSS = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,sans-serif;background:#f0f4f8;color:#1a2c3d}.header{background:linear-gradient(135deg,#1a3a5c,#2e86c1);color:#fff;padding:18px 24px 14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}.header h1{font-size:17px}.header p{font-size:11px;opacity:.8;margin-top:2px}.badge{background:rgba(255,255,255,.2);border-radius:20px;padding:3px 10px;font-size:10px}.nav{background:#fff;border-bottom:2px solid #e0e6ed;padding:0 16px;display:flex;gap:0;overflow-x:auto}.nav a{display:inline-block;padding:10px 12px;font-size:12px;color:#555;text-decoration:none;border-bottom:3px solid transparent;white-space:nowrap}.nav a:hover,.nav a.active{color:#2e86c1;border-bottom-color:#2e86c1}.home-btn{background:#2e86c1!important;color:#fff!important;border-radius:6px;margin:6px 8px 6px 0;padding:6px 12px!important;font-weight:700;border-bottom:none!important}.container{max-width:1050px;margin:16px auto;padding:0 12px}h2{font-size:12px;font-weight:700;color:#1a3a5c;text-transform:uppercase;letter-spacing:.5px;margin:20px 0 6px;padding-left:5px;border-left:3px solid #2e86c1}h3{font-size:11px;font-weight:600;color:#777;text-transform:uppercase;margin:12px 0 5px;padding-left:4px}table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 5px rgba(0,0,0,.07);margin-bottom:4px}th{background:#2e86c1;color:#fff;padding:8px 10px;text-align:left;font-size:11px;font-weight:600}th:nth-child(2),th:nth-child(3),td:nth-child(2),td:nth-child(3){text-align:right}.myprix-th{background:#1e8449!important;text-align:right}td{padding:9px 10px;border-bottom:1px solid #eef2f6;font-size:12px;vertical-align:middle}tr:last-child td{border-bottom:none}tr:hover td{background:#f7fafd}tr:hover td.myprix{background:#d5f5e3}.prix{font-weight:700;font-size:13px;color:#1a3a5c;text-align:right}.ht{color:#999;font-size:11px;text-align:right}.myprix{background:#eaf4e8;text-align:right}.mon-prix{font-weight:700;font-size:13px;color:#1e8449}.ref{font-size:10px;color:#bbb;display:block;margin-top:1px}a.lien{color:#2e86c1;text-decoration:none;font-size:11px}.up{color:#e74c3c;font-size:11px}.down{color:#27ae60;font-size:11px}.stable{color:#bbb;font-size:11px}.note{background:#eaf4e8;border-left:3px solid #1e8449;padding:7px 12px;border-radius:0 6px 6px 0;font-size:11px;color:#1e5631;margin-bottom:14px}.footer{text-align:center;color:#bbb;font-size:10px;margin:14px 0 24px}@media(max-width:600px){th:nth-child(3),td:nth-child(3),th:nth-child(4),td:nth-child(4){display:none}}"""

# Collecter toutes les URLs uniques
all_urls = []
for slug in MARQUES_ORDRE:
    for p in MARQUES[slug]["produits"]:
        if p["url"] not in [u for u,r in all_urls]:
            all_urls.append((p["url"], p["ref"]))

print(f"\n{'='*50}")
print(f"  Scraping {len(all_urls)} URLs avec Playwright")
print(f"{'='*50}\n")

prix_cache = scrape_all(all_urls)

# Page d'accueil
cards = ""
for slug in MARQUES_ORDRE:
    m = MARQUES[slug]
    nb = len(m["produits"])
    cards += f'<a href="{slug}/index.html" class="card"><div class="card-icon">{ICONES[slug]}</div><div class="card-body"><div class="card-title">{m["nom"]}</div><div class="card-desc">{m["desc"]}</div><div class="card-nb">{nb} modèles</div></div><div class="card-arrow">→</div></a>'

accueil = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tarifs Climatisation — 2D Energies</title><link rel="manifest" href="/manifest.json"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Arial,sans-serif;background:#f0f4f8;color:#1a2c3d}}.header{{background:linear-gradient(135deg,#1a3a5c,#2e86c1);color:#fff;padding:22px 24px 18px}}.header h1{{font-size:20px;margin-bottom:3px}}.header p{{font-size:11px;opacity:.8}}.container{{max-width:700px;margin:24px auto;padding:0 14px}}.subtitle{{font-size:13px;color:#777;margin-bottom:18px}}.cards{{display:flex;flex-direction:column;gap:9px}}.card{{display:flex;align-items:center;gap:12px;background:#fff;border-radius:10px;padding:14px;text-decoration:none;color:inherit;box-shadow:0 1px 5px rgba(0,0,0,.07);transition:.2s}}.card:hover{{box-shadow:0 3px 14px rgba(0,0,0,.12);transform:translateY(-1px)}}.card-icon{{width:44px;height:44px;flex-shrink:0}}.card-icon svg{{width:44px;height:44px}}.card-body{{flex:1}}.card-title{{font-size:15px;font-weight:700;margin-bottom:2px}}.card-desc{{font-size:11px;color:#999}}.card-nb{{font-size:10px;color:#bbb;margin-top:2px}}.card-arrow{{font-size:16px;color:#ccc}}.footer{{text-align:center;color:#bbb;font-size:10px;margin:20px 0}}</style></head><body>
<div class="header"><h1>❄️ Tarifs Climatisation</h1><p>2D Energies · Mis à jour automatiquement chaque jour · Source : climshop.com</p></div>
<div class="container"><p class="subtitle">Sélectionne une marque pour voir les tarifs et tes prix de vente</p><div class="cards">{cards}</div></div>
<div class="footer">Mis à jour le {date_maj} · climshop.com</div></body></html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(accueil)
print("\n✅ index.html (accueil)")

# Pages par marque
for slug in MARQUES_ORDRE:
    marque = MARQUES[slug]
    os.makedirs(slug, exist_ok=True)

    resultats = []
    for p in marque["produits"]:
        prix = prix_cache.get(p["url"], {"ttc": None, "ht": None, "ok": False})
        entry = {**p, **prix, "prev_ttc": historique.get(p["ref"])}
        resultats.append(entry)
        if prix["ok"]:
            historique[p["ref"]] = prix["ttc"]

    gammes = {}
    for r in resultats:
        gammes.setdefault(r["gamme"], {}).setdefault(r["sous_gamme"], []).append(r)

    nav = '<a href="../index.html" class="home-btn">🏠 Accueil</a>' + "".join(
        f'<a href="../{s}/index.html" class="{"active" if s==slug else ""}">{MARQUES[s]["nom"]}</a>'
        for s in MARQUES_ORDRE)

    tables = ""
    for gamme, sgs in gammes.items():
        tables += f"<h2>{gamme}</h2>"
        for sg, produits in sgs.items():
            tables += f"<h3>{sg}</h3><table><thead><tr><th>Modèle</th><th>Prix TTC</th><th>Prix HT</th><th>Évolution</th><th class='myprix-th'>Mon prix</th><th>Lien</th></tr></thead><tbody>"
            for r in produits:
                mp = fmt(mon_prix(r["ttc"])) if r["ok"] else "—"
                tables += f"<tr><td><strong>{r['nom']}</strong><span class='ref'>{r['ref']}</span></td><td class='prix'>{fmt(r['ttc'])}</td><td class='ht'>{fmt(r['ht'])}</td><td>{evol_html(r['ref'],r['ttc'],r['ok'])}</td><td class='myprix'><span class='mon-prix'>{mp}</span></td><td><a class='lien' href='{r['url']}' target='_blank'>Voir →</a></td></tr>"
            tables += "</tbody></table>"

    page = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tarifs {marque['nom']} — 2D Energies</title><style>{CSS}</style><script>if(window.navigator.standalone===true&&!document.referrer){{window.location.replace("../index.html");}}</script></head><body>
<div class="header"><div><h1>❄️ Tarifs {marque['nom']}</h1><p>Mis à jour automatiquement · {date_maj} · Source : climshop.com</p></div><span class="badge">Mon prix = Climshop −20% × +40% × +20%</span></div>
<nav class="nav">{nav}</nav>
<div class="container"><div class="note">💡 <strong>Mon prix</strong> = prix Climshop × 0.80 × 1.40 × 1.20</div>{tables}</div>
<div class="footer">Mis à jour automatiquement chaque jour via GitHub Actions · Source : climshop.com</div></body></html>"""

    with open(f"{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"✅ {slug}/index.html")

with open(hist_file, "w") as f:
    json.dump(historique, f)
print(f"\n✅ Terminé — {date_maj}")
