import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json, os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

# Icônes SVG inline par marque (simples et propres)
ICONES = {
    "toshiba":    '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#2e86c1"/><text x="20" y="26" text-anchor="middle" font-size="11" font-weight="bold" fill="white" font-family="Arial">TOSH</text></svg>',
    "daikin":     '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#0066cc"/><text x="20" y="26" text-anchor="middle" font-size="11" font-weight="bold" fill="white" font-family="Arial">DAIK</text></svg>',
    "mitsubishi": '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#cc0000"/><text x="20" y="26" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="Arial">MITS</text></svg>',
    "atlantic":   '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#006699"/><text x="20" y="26" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="Arial">ATL</text></svg>',
    "lg":         '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#a50034"/><text x="20" y="26" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="Arial">LG</text></svg>',
    "samsung":    '<svg viewBox="0 0 40 40" fill="none"><rect width="40" height="40" rx="8" fill="#1428a0"/><text x="20" y="26" text-anchor="middle" font-size="9" font-weight="bold" fill="white" font-family="Arial">SAMS</text></svg>',
}

MARQUES = {
    "toshiba": {
        "nom": "Toshiba", "couleur": "#2e86c1",
        "desc": "Yukai · Shorai Edge · Haori · Multi-splits",
        "produits": [
            # Mural & Console
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
            # Multi-splits — Groupes extérieurs
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 2.9 kW (RAS-2M10G3AVG-E)","ref":"RAS-2M10G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 4.0 kW (RAS-2M14G3AVG-E)","ref":"RAS-2M14G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Bi-split 5.2 kW (RAS-2M18G3AVG-E)","ref":"RAS-2M18G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Tri-split 5.2 kW (RAS-3M18G3AVG-E)","ref":"RAS-3M18G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Tri-split 7.5 kW (RAS-3M26G3AVG-E)","ref":"RAS-3M26G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Quadri-split 8.0 kW (RAS-4M27G3AVG-E)","ref":"RAS-4M27G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            {"gamme":"Multi-splits","sous_gamme":"Groupes extérieurs","nom":"Penta-split 10.0 kW (RAS-5M34G3AVG-E)","ref":"RAS-5M34G3AVG-E","url":"https://www.climshop.com/291-unites-ext-toshiba-ras.html"},
            # Multi-splits — Unités intérieures
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 1.5 kW (RAS-B05B2KVG-E)","ref":"RAS-B05B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 2.0 kW (RAS-B07B2KVG-E)","ref":"RAS-B07B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 2.5 kW (RAS-B10B2KVG-E)","ref":"RAS-B10B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 3.3 kW (RAS-B13B2KVG-E)","ref":"RAS-B13B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            {"gamme":"Multi-splits","sous_gamme":"Unités intérieures Naka","nom":"Naka 4.2 kW (RAS-B16B2KVG-E)","ref":"RAS-B16B2KVG-E","url":"https://www.climshop.com/845-unites-interieures-naka-toshiba.html"},
            # Packs bi-split
            {"gamme":"Multi-splits","sous_gamme":"Packs bi-split","nom":"Bi-split Yukai 1.5+3.3 kW","ref":"BISPLIT-YUKAI-05-13","url":"https://www.climshop.com/260-bisplit-ras2m18g3avge-rasb05e2kvge-rasb13e2kvge.html"},
        ]
    },
    "daikin": {
        "nom": "Daikin", "couleur": "#0066cc",
        "desc": "Sensira · Comfora · Perfera · Stylish",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 2.0 kW","ref":"FTXF20F/RXF20F","url":"https://www.climshop.com/23-ftxf20e-rxf20e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 2.5 kW","ref":"FTXF25F/RXF25F","url":"https://www.climshop.com/58-ftxf25e-rxf25e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 3.5 kW","ref":"FTXF35F/RXF35F","url":"https://www.climshop.com/sensira-daikin-ftxf35a-rxf35a-xml-428_429_439_227_312_613-3773.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 5.0 kW","ref":"FTXF50F/RXF50D","url":"https://www.climshop.com/61-ftxf50e-rxf50e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Sensira","nom":"Sensira 7.1 kW","ref":"FTXF71F/RXF71D","url":"https://www.climshop.com/63-ftxf71e-rxf71e.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 2.5 kW","ref":"FTXP25M/RXP25M","url":"https://www.climshop.com/ftxp25m-rxp25m-xml-428_429_439_227_312_614-3784.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 3.5 kW","ref":"FTXP35M/RXP35M","url":"https://www.climshop.com/ftxp35m-rxp35m-xml-428_429_439_227_312_614-3785.html"},
            {"gamme":"Mural & Console","sous_gamme":"Comfora","nom":"Comfora 5.0 kW","ref":"FTXP50M/RXP50M","url":"https://www.climshop.com/ftxp50m-rxp50m-xml-428_429_439_227_312_614-3786.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 2.0 kW","ref":"FTXM20R/RXM20R","url":"https://www.climshop.com/ftxm20r-rxm20r-xml-428_429_439_227_312_610-3765.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 2.5 kW","ref":"FTXM25R/RXM25R","url":"https://www.climshop.com/ftxm25r-rxm25r-xml-428_429_439_227_312_610-3766.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 3.5 kW","ref":"FTXM35R/RXM35R","url":"https://www.climshop.com/ftxm35r-rxm35r-xml-428_429_439_227_312_610-3767.html"},
            {"gamme":"Mural & Console","sous_gamme":"Perfera","nom":"Perfera 5.0 kW","ref":"FTXM50R/RXM50R","url":"https://www.climshop.com/ftxm50r-rxm50r-xml-428_429_439_227_312_610-3768.html"},
            {"gamme":"Mural & Console","sous_gamme":"Stylish","nom":"Stylish 2.0 kW","ref":"FTXA20AW/RXA20A","url":"https://www.climshop.com/stylishftxa20awrxa20a-xml-428_429_439_227_312_611-3793.html"},
            {"gamme":"Mural & Console","sous_gamme":"Stylish","nom":"Stylish 2.5 kW","ref":"FTXA25AW/RXA25A","url":"https://www.climshop.com/stylishftxa25awrxa25a-xml-428_429_439_227_312_611-3795.html"},
            {"gamme":"Mural & Console","sous_gamme":"Stylish","nom":"Stylish 3.5 kW","ref":"FTXA35AW/RXA35A","url":"https://www.climshop.com/stylishftxa35awrxa35a-xml-428_429_439_227_312_611-3796.html"},
        ]
    },
    "mitsubishi": {
        "nom": "Mitsubishi Electric", "couleur": "#cc0000",
        "desc": "HR Essentiel · AP Compact · EF Design · LN",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 2.5 kW","ref":"MSZ-HR25VFK/MUZ-HR25VF","url":"https://www.climshop.com/126-msz-hr25vf-muz-hr25vf.html"},
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 3.5 kW","ref":"MSZ-HR35VFK/MUZ-HR35VF","url":"https://www.climshop.com/msz-hr35vf-muz-hr35vf-xml-428_429_439_216_316_617-3802.html"},
            {"gamme":"Mural & Console","sous_gamme":"HR Essentiel","nom":"HR 5.0 kW","ref":"MSZ-HR50VFK/MUZ-HR50VF","url":"https://www.climshop.com/msz-hr50vf-muz-hr50vf-xml-428_429_439_216_316_617-3803.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 2.5 kW","ref":"MSZ-AP25VGK/MUZ-AP25VG","url":"https://www.climshop.com/msz-ap25vgk-muz-ap25vg-xml-428_429_439_216_316_618-3808.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 3.5 kW","ref":"MSZ-AP35VGK/MUZ-AP35VG","url":"https://www.climshop.com/msz-ap35vgk-muz-ap35vg-xml-428_429_439_216_316_618-3809.html"},
            {"gamme":"Mural & Console","sous_gamme":"AP Compact","nom":"AP 5.0 kW","ref":"MSZ-AP50VGK/MUZ-AP50VG","url":"https://www.climshop.com/msz-ap50vgk-muz-ap50vg-xml-428_429_439_216_316_618-3810.html"},
            {"gamme":"Mural & Console","sous_gamme":"EF Design","nom":"EF 2.5 kW","ref":"MSZ-EF25VGKW/MUZ-EF25VG","url":"https://www.climshop.com/msz-ef25vgkw-muz-ef25vg-xml-428_429_439_216_316_619-3816.html"},
            {"gamme":"Mural & Console","sous_gamme":"EF Design","nom":"EF 3.5 kW","ref":"MSZ-EF35VGKW/MUZ-EF35VG","url":"https://www.climshop.com/msz-ef35vgkw-muz-ef35vg-xml-428_429_439_216_316_619-3817.html"},
            {"gamme":"Mural & Console","sous_gamme":"LN Design De Luxe","nom":"LN 2.5 kW","ref":"MSZ-LN25VG2W/MUZ-LN25VG2","url":"https://www.climshop.com/msz-ln25vg2w-muz-ln25vg2-xml-428_429_439_216_316_621-3828.html"},
            {"gamme":"Mural & Console","sous_gamme":"LN Design De Luxe","nom":"LN 3.5 kW","ref":"MSZ-LN35VG2W/MUZ-LN35VG2","url":"https://www.climshop.com/msz-ln35vg2w-muz-ln35vg2-xml-428_429_439_216_316_621-3829.html"},
        ]
    },
    "atlantic": {
        "nom": "Atlantic Fujitsu", "couleur": "#006699",
        "desc": "Takao Plus · Takao M1 · Takao M2",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 2.0 kW","ref":"ASYH7KJCA/AOYH7KJCA","url":"https://www.climshop.com/218-takao-plus-2kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 2.5 kW","ref":"ASYH9KJCA/AOYH9KJCA","url":"https://www.climshop.com/219-takao-plus-2-5kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 3.4 kW","ref":"ASYH12KJCA/AOYH12KJCA","url":"https://www.climshop.com/220-takao-plus-3-4kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao Plus","nom":"Takao Plus 4.2 kW","ref":"ASYH14KJCA/AOYH14KJCA","url":"https://www.climshop.com/221-takao-plus-4-2kw.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao M1","nom":"Takao M1 3.4 kW","ref":"ASYG12KPC/AOYG12KPC","url":"https://www.climshop.com/asyg12kpcui-aoyg12kpcue-takaom1-xml-428_429_439_255_314_629-3938.html"},
            {"gamme":"Mural & Console","sous_gamme":"Takao M1","nom":"Takao M1 5.2 kW","ref":"ASYG18KLC/AOYG18KLC","url":"https://www.climshop.com/asyg18klcui-aoyg18klcue-takaom1-xml-428_429_439_255_314_629-3940.html"},
        ]
    },
    "lg": {
        "nom": "LG", "couleur": "#a50034",
        "desc": "Standard Wifi · Dualcool Premium · Artcool Gallery",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 2.5 kW","ref":"S09ET.NSJ/S09ET.UA3","url":"https://www.climshop.com/standard-wifi-s09et-nsj-ua3-xml-428_429_439_263_330_643-3997.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 3.5 kW","ref":"S12ET.NSJ/S12ET.UA3","url":"https://www.climshop.com/standard-wifi-s12et-nsj-ua3-xml-428_429_439_263_330_643-3998.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 5.0 kW","ref":"S18ET.NSJ/S18ET.UA3","url":"https://www.climshop.com/standard-wifi-s18et-nsj-ua3-xml-428_429_439_263_330_643-3999.html"},
            {"gamme":"Mural & Console","sous_gamme":"Standard Wifi","nom":"Standard 7.0 kW","ref":"S24ET.NSJ/S24ET.UA3","url":"https://www.climshop.com/standard-wifi-s24et-nsj-ua3-xml-428_429_439_263_330_643-4000.html"},
            {"gamme":"Mural & Console","sous_gamme":"Dualcool Premium","nom":"Dualcool 2.5 kW","ref":"H09S1P.NS1/H09S1P.U12","url":"https://www.climshop.com/dualcool-premium-h09s1p-ns1-u12-xml-428_429_439_263_330_644-4001.html"},
            {"gamme":"Mural & Console","sous_gamme":"Dualcool Premium","nom":"Dualcool 3.5 kW","ref":"H12S1P.NS1/H12S1P.U12","url":"https://www.climshop.com/dualcool-premium-h12s1p-ns1-u12-xml-428_429_439_263_330_644-4002.html"},
            {"gamme":"Mural & Console","sous_gamme":"Artcool Gallery","nom":"Artcool Gallery 2.5 kW","ref":"A09GA2.NSE/A09GA2.U18","url":"https://www.climshop.com/artcool-gallery-a09ga2-nse-u18-xml-428_429_439_263_330_645-4003.html"},
            {"gamme":"Mural & Console","sous_gamme":"Artcool Gallery","nom":"Artcool Gallery 3.7 kW","ref":"A12GA2.NSE/A12GA2.U18","url":"https://www.climshop.com/838-artcool-gallery-premium-a12ga2nse-et-a12ga2u18.html"},
        ]
    },
    "samsung": {
        "nom": "Samsung", "couleur": "#1428a0",
        "desc": "AR35 Wifi · CEBU S2 · WindFree Comfort S2",
        "produits": [
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 2.0 kW","ref":"AR07TXHQASINEU","url":"https://www.climshop.com/903-ar35-wifi-samsung-2000w.html"},
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 2.5 kW","ref":"AR09TXHQASINEU","url":"https://www.climshop.com/ar35-wifi-samsung-2500w-xml-428_429_439_289_360_685-4043.html"},
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 3.5 kW","ref":"AR12TXHQASINEU","url":"https://www.climshop.com/904-ar35-wifi-samsung-3500w.html"},
            {"gamme":"Mural & Console","sous_gamme":"AR35 Wifi","nom":"AR35 7.0 kW","ref":"AR24TXHQASINEU","url":"https://www.climshop.com/906-ar35-wifi-samsung-7200w.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 2.0 kW","ref":"AR07BXEAAWKNEU","url":"https://www.climshop.com/cebu-s2-2000w-xml-428_429_439_289_360_686-4045.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 2.5 kW","ref":"AR09BXEAAWKNEU","url":"https://www.climshop.com/cebu-s2-2500w-xml-428_429_439_289_360_686-4046.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 3.5 kW","ref":"AR12BXEAAWKNEU","url":"https://www.climshop.com/cebu-s2-3500w-xml-428_429_439_289_360_686-4047.html"},
            {"gamme":"Mural & Console","sous_gamme":"CEBU S2","nom":"CEBU S2 5.0 kW","ref":"AR18BXEAAWKNEU","url":"https://www.climshop.com/cebu-s2-5000w-xml-428_429_439_289_360_686-4048.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 2.5 kW","ref":"AR09BXCAAWKNEU","url":"https://www.climshop.com/windfree-comfort-s2-2500w-xml-428_429_439_289_360_687-4050.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 3.5 kW","ref":"AR12BXCAAWKNEU","url":"https://www.climshop.com/windfree-comfort-s2-3500w-xml-428_429_439_289_360_687-4051.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 5.0 kW","ref":"AR18BXCAAWKNEU","url":"https://www.climshop.com/windfree-comfort-s2-5000w-xml-428_429_439_289_360_687-4052.html"},
            {"gamme":"Mural & Console","sous_gamme":"WindFree Comfort S2","nom":"WindFree 7.0 kW","ref":"AR24BXCAAWKNEU","url":"https://www.climshop.com/windfree-comfort-s2-7000w-xml-428_429_439_289_360_687-4053.html"},
        ]
    }
}

MARQUES_ORDRE = ["toshiba","daikin","mitsubishi","atlantic","lg","samsung"]

def mon_prix(ttc):
    return round(ttc * 0.80 * 1.40 * 1.20, 2)

def fmt(v):
    if v is None: return "—"
    return f"{v:,.2f} €".replace(",", " ").replace(".", ",")

def scrape(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.find(itemprop="price")
        if tag:
            ttc = float(tag.get("content", "0"))
            return {"ttc": ttc, "ht": round(ttc/1.2, 2), "ok": True}
        return {"ttc": None, "ht": None, "ok": False}
    except:
        return {"ttc": None, "ht": None, "ok": False}

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

CSS = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,sans-serif;background:#f0f4f8;color:#1a2c3d}.header{background:linear-gradient(135deg,#1a3a5c,#2e86c1);color:#fff;padding:18px 24px 14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}.header h1{font-size:17px}.header p{font-size:11px;opacity:.8;margin-top:2px}.badge{background:rgba(255,255,255,.2);border-radius:20px;padding:3px 10px;font-size:10px}.nav{background:#fff;border-bottom:2px solid #e0e6ed;padding:0 16px;display:flex;gap:0;overflow-x:auto}.nav a{display:inline-block;padding:10px 12px;font-size:12px;color:#555;text-decoration:none;border-bottom:3px solid transparent;white-space:nowrap}.nav a:hover,.nav a.active{color:#2e86c1;border-bottom-color:#2e86c1}.container{max-width:1050px;margin:16px auto;padding:0 12px}h2{font-size:12px;font-weight:700;color:#1a3a5c;text-transform:uppercase;letter-spacing:.5px;margin:20px 0 6px;padding-left:5px;border-left:3px solid #2e86c1}h3{font-size:11px;font-weight:600;color:#777;text-transform:uppercase;margin:12px 0 5px;padding-left:4px}table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 5px rgba(0,0,0,.07);margin-bottom:4px}th{background:#2e86c1;color:#fff;padding:8px 10px;text-align:left;font-size:11px;font-weight:600}th:nth-child(2),th:nth-child(3),td:nth-child(2),td:nth-child(3){text-align:right}.myprix-th{background:#1e8449!important;text-align:right}td{padding:9px 10px;border-bottom:1px solid #eef2f6;font-size:12px;vertical-align:middle}tr:last-child td{border-bottom:none}tr:hover td{background:#f7fafd}tr:hover td.myprix{background:#d5f5e3}.prix{font-weight:700;font-size:13px;color:#1a3a5c;text-align:right}.ht{color:#999;font-size:11px;text-align:right}.myprix{background:#eaf4e8;text-align:right}.mon-prix{font-weight:700;font-size:13px;color:#1e8449}.ref{font-size:10px;color:#bbb;display:block;margin-top:1px}a.lien{color:#2e86c1;text-decoration:none;font-size:11px}.up{color:#e74c3c;font-size:11px}.down{color:#27ae60;font-size:11px}.stable{color:#bbb;font-size:11px}.note{background:#eaf4e8;border-left:3px solid #1e8449;padding:7px 12px;border-radius:0 6px 6px 0;font-size:11px;color:#1e5631;margin-bottom:14px}.footer{text-align:center;color:#bbb;font-size:10px;margin:14px 0 24px}@media(max-width:600px){th:nth-child(3),td:nth-child(3),th:nth-child(4),td:nth-child(4){display:none}}"""

# Page d'accueil
cards = ""
for slug in MARQUES_ORDRE:
    m = MARQUES[slug]
    nb = len(m["produits"])
    icone = ICONES[slug]
    cards += f'<a href="{slug}/index.html" class="card"><div class="card-icon">{icone}</div><div class="card-body"><div class="card-title">{m["nom"]}</div><div class="card-desc">{m["desc"]}</div><div class="card-nb">{nb} modèles</div></div><div class="card-arrow">→</div></a>'

accueil = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tarifs Climatisation — 2D Energies</title>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Arial,sans-serif;background:#f0f4f8;color:#1a2c3d}}.header{{background:linear-gradient(135deg,#1a3a5c,#2e86c1);color:#fff;padding:22px 24px 18px}}.header h1{{font-size:20px;margin-bottom:3px}}.header p{{font-size:11px;opacity:.8}}.container{{max-width:700px;margin:24px auto;padding:0 14px}}.subtitle{{font-size:13px;color:#777;margin-bottom:18px}}.cards{{display:flex;flex-direction:column;gap:9px}}.card{{display:flex;align-items:center;gap:12px;background:#fff;border-radius:10px;padding:14px;text-decoration:none;color:inherit;box-shadow:0 1px 5px rgba(0,0,0,.07);transition:.2s}}.card:hover{{box-shadow:0 3px 14px rgba(0,0,0,.12);transform:translateY(-1px)}}.card-icon{{width:44px;height:44px;flex-shrink:0}}.card-icon svg{{width:44px;height:44px}}.card-body{{flex:1}}.card-title{{font-size:15px;font-weight:700;margin-bottom:2px}}.card-desc{{font-size:11px;color:#999}}.card-nb{{font-size:10px;color:#bbb;margin-top:2px}}.card-arrow{{font-size:16px;color:#ccc}}.footer{{text-align:center;color:#bbb;font-size:10px;margin:20px 0}}</style></head><body>
<div class="header"><h1>❄️ Tarifs Climatisation</h1><p>2D Energies · Mis à jour automatiquement chaque jour · Source : climshop.com</p></div>
<div class="container"><p class="subtitle">Sélectionne une marque pour voir les tarifs et tes prix de vente</p><div class="cards">{cards}</div></div>
<div class="footer">Mis à jour le {date_maj} · climshop.com</div></body></html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(accueil)
print("✅ index.html (accueil)")

# Pages par marque
for slug in MARQUES_ORDRE:
    marque = MARQUES[slug]
    os.makedirs(slug, exist_ok=True)

    resultats = []
    for p in marque["produits"]:
        print(f"  {p['nom']}...", end=" ", flush=True)
        prix = scrape(p["url"])
        entry = {**p, **prix, "prev_ttc": historique.get(p["ref"])}
        resultats.append(entry)
        if prix["ok"]:
            historique[p["ref"]] = prix["ttc"]
        print(fmt(prix["ttc"]) if prix["ok"] else "❌")

    gammes = {}
    for r in resultats:
        gammes.setdefault(r["gamme"], {}).setdefault(r["sous_gamme"], []).append(r)

    nav = '<a href="../index.html">← Accueil</a>' + "".join(
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

    page = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tarifs {marque['nom']} — 2D Energies</title><style>{CSS}</style></head><body>
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
