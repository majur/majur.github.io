#!/usr/bin/env python3
"""Generates static HTML pages for navrh4. Run once after content changes."""
import os
import re
from pathlib import Path

BASE = Path(__file__).parent
POSTS_DIR = BASE.parent.parent / "_posts"

POST_MD_MAP = {
    "how-to-create-simple-backend-with-rails": "2024-03-31-how-to-create-simple-backend-with-rails.md",
    "ahoj-jekyll": "2023-03-31-ahoj-jekyll.md",
    "socialna-siet-buducnosti-ma-23-rokov": "2023-03-26-socialna-siet-buducnosti-ma-23-rokov.md",
    "moj-setup": "2021-10-06-moj-setup.md",
    "preco-hodnota-bitcoinu-stupa": "2021-02-26-preco-hodnota-bitcoinu-stupa.md",
    "trumpov-twitter-a-sloboda-slova": "2021-01-15-trumpov-twitter-a-sloboda-slova.md",
    "maraton-pohronskym-inovcom-2018": "2018-03-09-maraton-pohronskym-inovcom-2018.md",
}

POSTS = [
    {
        "slug": "how-to-create-simple-backend-with-rails",
        "title": "How to create simple backend with rails",
        "date": "31. mar 2024",
        "date_iso": "2024-03-31",
        "categories": ["Dev"],
        "tags": ["Backend", "Ruby", "Rails"],
        "excerpt": "A bigger project from my portfolio is a CMS written in Ruby on Rails. But I need a few smaller projects first. The first one is a simple backend for a todo list application.",
        "read_time": "7 min",
    },
    {
        "slug": "ahoj-jekyll",
        "title": "Ahoj Jekyll!",
        "date": "31. mar 2023",
        "date_iso": "2023-03-31",
        "categories": ["Dev"],
        "tags": ["100DaysToOffload-sk", "jekyll"],
        "excerpt": "Nový blog, nová platforma. Prečo som si vybral Jekyll a ako som ho nastavil pre dvojjazyčný obsah.",
        "read_time": "5 min",
    },
    {
        "slug": "socialna-siet-buducnosti-ma-23-rokov",
        "title": "Sociálna sieť budúcnosti má 23 rokov",
        "date": "26. mar 2023",
        "date_iso": "2023-03-26",
        "categories": ["Internet"],
        "tags": ["100DaysToOffload-sk"],
        "excerpt": "RSS je technológia stará viac ako dve dekády, no stále je jedným z najlepších spôsobov, ako sledovať obsah na webe.",
        "read_time": "6 min",
    },
    {
        "slug": "moj-setup",
        "title": "Môj setup",
        "date": "6. okt 2021",
        "date_iso": "2021-10-06",
        "categories": ["Dev"],
        "tags": [],
        "excerpt": "Zabudnite na ideálny setup. Nepotrebujete ho. Musíte len začať s tým, čo máte.",
        "read_time": "4 min",
    },
    {
        "slug": "preco-hodnota-bitcoinu-stupa",
        "title": "Prečo hodnota Bitcoinu stúpa?",
        "date": "26. feb 2021",
        "date_iso": "2021-02-26",
        "categories": ["Sloboda", "Bitcoin"],
        "tags": [],
        "excerpt": "Bitcoin nie je len špekulatívna bublina. Za jeho rastúcou hodnotou stoja fundamentálne ekonomické princípy.",
        "read_time": "8 min",
    },
    {
        "slug": "trumpov-twitter-a-sloboda-slova",
        "title": "Trumpov twitter a sloboda slova",
        "date": "15. jan 2021",
        "date_iso": "2021-01-15",
        "categories": ["Sloboda"],
        "tags": [],
        "excerpt": "Keď súkromná spoločnosť umlčí prezidenta, musíme sa zamyslieť nad tým, čo znamená sloboda slova v digitálnom veku.",
        "read_time": "4 min",
    },
    {
        "slug": "maraton-pohronskym-inovcom-2018",
        "title": "Maratón Pohronským Inovcom 2018",
        "date": "9. mar 2018",
        "date_iso": "2018-03-09",
        "categories": ["Beh"],
        "tags": [],
        "excerpt": "Zážitok z bežeckého maratónu cez jedno z najkrajších slovenských pohorí.",
        "read_time": "10 min",
    },
]

CATEGORIES = {
    "dev": {"name": "Dev", "slug": "kategoria-dev.html"},
    "internet": {"name": "Internet", "slug": "kategoria-internet.html"},
    "sloboda": {"name": "Sloboda", "slug": "kategoria-sloboda.html"},
    "bitcoin": {"name": "Bitcoin", "slug": "kategoria-bitcoin.html"},
    "beh": {"name": "Beh", "slug": "kategoria-beh.html"},
}

TAGS = {
    "rails": {"name": "Rails", "slug": "stitok-rails.html"},
    "ruby": {"name": "Ruby", "slug": "stitok-ruby.html"},
    "backend": {"name": "Backend", "slug": "stitok-backend.html"},
    "jekyll": {"name": "jekyll", "slug": "stitok-jekyll.html"},
    "100daystooffload": {"name": "100DaysToOffload-sk", "slug": "stitok-100daystooffload.html"},
}

FONT_SHOWCASE = [
    {
        "name": "Playfair Display",
        "group": "Serif",
        "tone": "Najpoužívanejší editoriálny serif na nadpisy: dramatický, ale stále čitateľný.",
        "sample": "Technológie, sloboda a silný titulok.",
        "quirk": "Kontrast medzi tenkými a hrubými ťahmi a nápadné R a Q.",
        "pros": [
            "Veľmi známy headline serif, ktorý hneď pôsobí profesionálne.",
            "Výborne funguje v hero sekciách a magazínových titulkoch.",
        ],
        "cons": [
            "Vie byť trochu „overused“, ak chceš extra osobitý dojem.",
            "Potrebuje dosť priestoru, aby kontrast nevypadal krehko.",
        ],
    },
    {
        "name": "Cormorant Garamond",
        "group": "Serif",
        "tone": "Elegantnejšia a jemnejšia alternatíva k Playfairu s veľmi editorial náladou.",
        "sample": "Technológie, sloboda a výrazný editorial tón.",
        "quirk": "Jemné, takmer kaligrafické krivky v písmenách a, g a R.",
        "pros": [
            "Pôsobí luxusne, literárne a viac „fashion“ než bežné serifky.",
            "Skvelo funguje vo veľkých nadpisoch a citáciách.",
        ],
        "cons": [
            "V malých veľkostiach môže pôsobiť krehko.",
            "Potrebuje viac priestoru a čisté okolie.",
        ],
    },
    {
        "name": "DM Serif Display",
        "group": "Serif",
        "tone": "Čistý display serif, ktorý sa používa presne tam, kde má nadpis pôsobiť kultivovane.",
        "sample": "Píšem o programovaní, open source a internete.",
        "quirk": "Pekne rozpoznateľné zakrivenia v a, g a J.",
        "pros": [
            "Pôsobí moderne, ale stále má klasickú serióznosť.",
            "Je to bezpečná voľba pre titulky aj blogové sekcie.",
        ],
        "cons": [
            "Je skôr na titulky než na dlhé bloky textu.",
            "Môže pôsobiť menej originálne než iné display serifky.",
        ],
    },
    {
        "name": "Instrument Serif",
        "group": "Serif",
        "tone": "Novší editoriálny serif s výraznejšími tvarmi a veľmi dobrým headline charakterom.",
        "sample": "Technológie, sloboda a trochu luxusný serif.",
        "quirk": "Výrazné tvary písmen a, g, R a Q s moderným editorial nádychom.",
        "pros": [
            "Pôsobí súčasne a má výraznejšiu osobnosť než klasické book serify.",
            "Dobre sa číta v headline veľkostiach a vyzerá veľmi „2026“. ",
        ],
        "cons": [
            "Nie je tak overený ako Playfair Display alebo Cormorant Garamond.",
            "V dlhom texte je už priveľmi display.",
        ],
    },
    {
        "name": "Alegreya",
        "group": "Serif",
        "tone": "Knižný serif s kaligrafickou energiou a príjemným tempom čítania.",
        "sample": "Píšem o programovaní, open source a internete.",
        "quirk": "Otvorené tvary a charakteristické g, y a italic rytmus.",
        "pros": [
            "Vyzerá živšie než bežné book serify.",
            "Je dobrý kompromis medzi čitateľnosťou a charakterom.",
        ],
        "cons": [
            "Nemá taký módny náboj ako Fraunces alebo Bodoni Moda.",
            "V čistom minimalistickom layout-e môže pôsobiť jemnejšie.",
        ],
    },
    {
        "name": "Merriweather",
        "group": "Serif",
        "tone": "Robustný serif, ktorý je bezpečný, ľahko čitateľný a stále dosť výrazný do nadpisov.",
        "sample": "Technológie, sloboda a čitateľný headline.",
        "quirk": "Stabilné tvary a výrazné vnútorné priestory v písmenách.",
        "pros": [
            "Má obrovské rozšírenie na webe a drží sa dobre v rôznych veľkostiach.",
            "Je spoľahlivý na dlhšie články aj menšie headliny.",
        ],
        "cons": [
            "Je menej showy než Playfair alebo Cormorant.",
            "Ak chceš vizuálny šok, je skôr príliš bezpečný.",
        ],
    },
    {
        "name": "Montserrat",
        "group": "Sans",
        "tone": "Jeden z najpoužívanejších moderných heading sansov: čistý, geometrický a veľmi univerzálny.",
        "sample": "Technológie, sloboda a moderný nadpis.",
        "quirk": "Presné kruhy a výrazné M, R a W.",
        "pros": [
            "Je mimoriadne známy a funguje takmer všade.",
            "Skvelý pre startupy, produktové weby a jednoduché layouty.",
        ],
        "cons": [
            "Pôsobí veľmi rozšírene, až genericky.",
            "Nemá veľa prekvapenia, ak chceš charakter.",
        ],
    },
    {
        "name": "Poppins",
        "group": "Sans",
        "tone": "Zaoblený geometrický sans, ktorý je dnes všade v produktových a marketingových headlinoch.",
        "sample": "Technológie, sloboda a čistý headline.",
        "quirk": "Takmer kruhové tvary a jemne mäkší dojem v a, o a p.",
        "pros": [
            "Pôsobí prístupne a veľmi aktuálne.",
            "Dobre sa kombinuje s výraznejším serifom v texte.",
        ],
        "cons": [
            "Je tak populárny, že môže pôsobiť stereotypne.",
            "Na luxusný editorial má príliš startup vibe.",
        ],
    },
    {
        "name": "Raleway",
        "group": "Sans",
        "tone": "Elegantný sans pre veľké nadpisy, s jemnejším a trochu módnym dojmom.",
        "sample": "Technológie, sloboda a výrazný headline.",
        "quirk": "Charakteristické W a jemne vzdušný rytmus písmen.",
        "pros": [
            "Vyzerá ľahšie a uhladenejšie než Montserrat.",
            "V hero sekciách vie pôsobiť veľmi sofistikovane.",
        ],
        "cons": [
            "V slabšej váhe sa môže strácať.",
            "Nie je tak bezprostredne čitateľný ako Poppins alebo Oswald.",
        ],
    },
    {
        "name": "Oswald",
        "group": "Sans",
        "tone": "Condensed headline klasika, ktorá je stále veľmi silná pre správy, kampane a informačné weby.",
        "sample": "Technológie, sloboda a úzky titulok.",
        "quirk": "Stlačené proporcie a vertikálny tlak v tvare písmen.",
        "pros": [
            "Získa veľa vizuálneho priestoru aj v úzkom stĺpci.",
            "Má jasnú headline identitu a okamžitý dôraz.",
        ],
        "cons": [
            "Pôsobí tvrdšie a menej jemne než iné možnosti.",
            "Nie je vhodný na dlhé textové bloky.",
        ],
    },
    {
        "name": "Bebas Neue",
        "group": "Sans",
        "tone": "Ultra-populárny all-caps display sans, ktorý stále funguje na billboardové a posterové headliny.",
        "sample": "TECHNOLÓGIE, SLOBODA A SILNÝ TITULOK.",
        "quirk": "All-caps rytmus a veľmi silná vertikálna prítomnosť.",
        "pros": [
            "Okamžite priťahuje pozornosť.",
            "Je ideálny pre krátke, úderné headliny.",
        ],
        "cons": [
            "Funguje takmer len vo veľkých veľkostiach a v kapitálkach.",
            "Na jemnejší editorial je priveľmi agresívny.",
        ],
    },
    {
        "name": "Anton",
        "group": "Sans",
        "tone": "Ťažký, masívny headline font, ktorý sa stále veľmi často používa pre silné marketingové nadpisy.",
        "sample": "Technológie, sloboda a veľký náraz.",
        "quirk": "Hrubé ťahy a masívne tvary písmen bez zbytočných detailov.",
        "pros": [
            "Má veľký vizuálny dopad aj bez veľa slov.",
            "V kombinácii s jemnejším body fontom funguje veľmi spoľahlivo.",
        ],
        "cons": [
            "Môže pôsobiť príliš tvrdo alebo „bannerovo“.",
            "Na dlhé titulky je už príliš hlučný.",
        ],
    },
]

ASYM_FONT_SHOWCASE = [
    {
        "name": "Fraunces",
        "group": "Serif",
        "tone": "Referenčný asymetrický serif s výrazným osobitým charakterom a mnohými prekvapivými rezmi.",
        "sample": "Technológie, sloboda a trochu rozbitý serif.",
        "quirk": "Asymetrické tvary v a, g, r a Q sú presne to, čo ho robí zapamätateľným.",
        "pros": [
            "Má najlepšiu rovnováhu medzi hrou a použiteľnosťou.",
            "Skvelo funguje v nadpisoch aj kratších editorial sekciách.",
        ],
        "cons": [
            "Nie každému sedí jeho zámerne zvláštny charakter.",
            "Pri zlom párovaní môže pôsobiť príliš výrazne.",
        ],
    },
    {
        "name": "Syne",
        "group": "Sans",
        "tone": "Geometrický sans s asymetriou v detailoch, ktorý pôsobí futuristicky, ale nie sterilne.",
        "sample": "Technológie, sloboda a zvláštny rytmus.",
        "quirk": "Neočakávané proporcie v písmenách a jemne rozbitý vizuálny rytmus.",
        "pros": [
            "Vyzerá sviežo a odlišne od bežných geometric sansov.",
            "Vie dodať nadpisu dizajnérsky a mierne experimentálny tón.",
        ],
        "cons": [
            "Je už menej univerzálny než Poppins alebo Montserrat.",
            "V dlhých titulkoch môže pôsobiť trochu nepravidelne.",
        ],
    },
    {
        "name": "Bricolage Grotesque",
        "group": "Sans",
        "tone": "Hravý grotesk s viditeľnými zvláštnosťami, ktorý je výborný pre výrazné headingy.",
        "sample": "Technológie, sloboda a trochu rozbitý grotesk.",
        "quirk": "Nepravidelné tvary a nečakané malé odchýlky v kresbe písmen.",
        "pros": [
            "Pôsobí súčasne a má veľa charakteru.",
            "Je veľmi dobrý na vizuálne identitu a silné nadpisy.",
        ],
        "cons": [
            "Nie je to čistý minimalistický sans.",
            "V konzervatívnom layoute môže byť až príliš výrazný.",
        ],
    },
    {
        "name": "Recursive",
        "group": "Sans",
        "tone": "Variabilný sans, ktorý vie byť zvláštny, živý a veľmi dobre prispôsobiteľný.",
        "sample": "Technológie, sloboda a premenný charakter.",
        "quirk": "Asymetria sa mení podľa rezu a v niektorých rezoch pôsobí takmer ručne.",
        "pros": [
            "Ponúka veľmi veľa možností pre rôzne typy nadpisov.",
            "Je užitočný tam, kde chceš jeden font s viacerými osobnosťami.",
        ],
        "cons": [
            "Vyžaduje trochu viac práce pri nastavovaní rezov.",
            "Môže pôsobiť menej priamočiare než pevnejšie display fonty.",
        ],
    },
    {
        "name": "Eczar",
        "group": "Serif",
        "tone": "Živý serif s trochu robustnejším, ale stále veľmi osobitým výrazom.",
        "sample": "Technológie, sloboda a trochu divný serif.",
        "quirk": "Výrazné a, g a y pôsobia hravo a nie celkom klasicky.",
        "pros": [
            "Má silný charakter bez prehnanej okázalosti.",
            "V titulkoch vie pôsobiť veľmi sviežo a trochu nezvyčajne.",
        ],
        "cons": [
            "Nie je to úplne tradičný knižný serif.",
            "V dlhom texte môže byť výrazný tvar až rušivý.",
        ],
    },
    {
        "name": "Unbounded",
        "group": "Sans",
        "tone": "Kompaktný display sans s nepravidelným tvaroslovím a veľmi výrazným headline efektom.",
        "sample": "Technológie, sloboda a nejaké hranice.",
        "quirk": "Neprirodzene dynamické krivky a presne ten pocit, že písmo je trochu mimo osi.",
        "pros": [
            "Okamžite vyzerá netradične a zapamätateľne.",
            "Dobre funguje v krátkych výrazných titulkoch.",
        ],
        "cons": [
            "Nie je to font na dlhšie texty.",
            "V jemnejšom editorial kontexte môže byť príliš hlučný.",
        ],
    },
    {
        "name": "Truculenta",
        "group": "Sans",
        "tone": "Hravý a trochu zubatý sans s veľmi zvláštnym, mladistvým výrazom.",
        "sample": "Technológie, sloboda a trochu trucu.",
        "quirk": "Asymetrické a neohrabané tvary, ktoré pôsobia zámerne nepokojne.",
        "pros": [
            "Vie byť veľmi charakteristický a zábavný.",
            "Na krátke nadpisy má silný osobitý hlas.",
        ],
        "cons": [
            "Nie je vhodný pre seriózny alebo luxusný branding.",
            "Môže pôsobiť až príliš infantilne, ak sa preženie.",
        ],
    },
    {
        "name": "Tilt Warp",
        "group": "Display",
        "tone": "Extrémne posunutý display font, ktorý priamo ukazuje asymetriu ako súčasť identity.",
        "sample": "Technológie, sloboda a naklonený nadpis.",
        "quirk": "Rozpohybované tvary a doslova naklonený vizuálny rytmus.",
        "pros": [
            "Skvelý, keď chceš niečo okamžite nezabudnuteľné.",
            "Má silný posterový charakter.",
        ],
        "cons": [
            "Je dosť experimentálny pre bežný blog.",
            "V malých veľkostiach sa jeho efekt stráca.",
        ],
    },
    {
        "name": "Tilt Neon",
        "group": "Display",
        "tone": "Neonovo pôsobiaci display font s podivne rozsvietenými tvarmi a silnou identitou.",
        "sample": "Technológie, sloboda a žiarivý titulok.",
        "quirk": "Nepravidelné geometrie a pocit pohybu v každom znaku.",
        "pros": [
            "Veľmi silný a moderný vizuálny podpis.",
            "Pracuje výborne pri veľkých headline veľkostiach.",
        ],
        "cons": [
            "Môže pôsobiť až príliš graficky alebo tematicky.",
            "Nie je vhodný na dlhý text ani pokojný editorial.",
        ],
    },
    {
        "name": "Tilt Prism",
        "group": "Display",
        "tone": "Najexperimentálnejší z Tilt rodiny, vhodný len tam, kde chceš veľkú dávku typografickej deformácie.",
        "sample": "Technológie, sloboda a prizmatický efekt.",
        "quirk": "Rozštiepené a na pohľad deformované tvary, ktoré pôsobia opticky asymetricky.",
        "pros": [
            "Je veľmi výrazný a vizuálne nezameniteľný.",
            "Dobre funguje ako jednorazový hero experiment.",
        ],
        "cons": [
            "Pre bežné použitie je až príliš špecifický.",
            "Rýchlo sa môže stať dominantnejším než obsah.",
        ],
    },
    {
        "name": "Rakkas",
        "group": "Display",
        "tone": "Rozkošne nepravidelný display serif s výrazne ornamentálnymi a asymetrickými ťahmi.",
        "sample": "Technológie, sloboda a ozdobný titulok.",
        "quirk": "Hravo deformované písmená a neštandardná optická váha.",
        "pros": [
            "Má veľa osobnosti a výborný dekoratívny náboj.",
            "Na krátke výrazné titulky je veľmi silný.",
        ],
        "cons": [
            "V serióznom obsahu môže pôsobiť príliš hravo.",
            "Na dlhší headline je už dosť extrémny.",
        ],
    },
    {
        "name": "Bungee",
        "group": "Display",
        "tone": "Plakátový all-caps font s výrazným skokom v proporciách a silnou asymetriou kompozície.",
        "sample": "TECHNOLÓGIE, SLOBODA A VEĽKÝ NÁRAZ.",
        "quirk": "Extrémna vertikálna energia a typografická „odpruženosť“.",
        "pros": [
            "Okamžite pritiahne pozornosť.",
            "Skvelý na krátke slogany, kampane a alternatívne headliny.",
        ],
        "cons": [
            "Funguje len v špecifickom kontexte.",
            "Na bežný článok je príliš hlučný a posterový.",
        ],
    },
]


def cat_key(name):
    return name.lower().replace(" ", "-")


def tag_key(name):
    return name.lower().replace("-sk", "").replace(" ", "")


def posts_for_category(name):
    return [p for p in POSTS if name in p["categories"]]


def posts_for_tag(name):
    return [p for p in POSTS if name in p["tags"]]


def asset_src(web_path, depth=0):
    """Path relative to generated HTML (navrh4 root or clanky/)."""
    if web_path.startswith("/assets/"):
        web_path = web_path[len("/assets/") :]
    elif web_path.startswith("/"):
        web_path = web_path.lstrip("/")
    prefix = "../" * depth
    return f"{prefix}assets/{web_path}"


def load_post_image(slug, depth=0):
    md_name = POST_MD_MAP.get(slug)
    if not md_name:
        return ""
    md_path = POSTS_DIR / md_name
    if not md_path.exists():
        return ""
    front_matter = md_path.read_text(encoding="utf-8").split("---", 2)[1]
    match = re.search(r"^\s*path:\s*(.+)$", front_matter, re.MULTILINE)
    if not match:
        return ""
    return asset_src(match.group(1).strip(), depth=depth)


def enrich_posts():
    for post in POSTS:
        post["image"] = load_post_image(post["slug"])


def post_href(post, depth=0):
    prefix = "../" * depth
    return f"{prefix}clanky/{post['slug']}.html"


def image_fit_modifier(image_path):
    name = image_path.lower()
    if "logo" in name or name.endswith(".png"):
        return "contain"
    return "cover"


def post_media_html(post, variant="card", depth=0):
    image = post.get("image")
    if not image:
        slug = post.get("slug")
        if slug:
            image = load_post_image(slug, depth=depth)
    if not image:
        return ""
    alt = post["title"]
    fit = image_fit_modifier(image)
    if variant == "featured":
        return (
            f'<div class="featured-img featured-img--{fit}">'
            f'<img src="{image}" alt="{alt}" width="640" height="400" loading="eager" decoding="async">'
            f"</div>"
        )
    if variant == "archive":
        thumb_fit = "contain" if fit == "contain" else "cover"
        return (
            f'<span class="archive-thumb archive-thumb--{thumb_fit}">'
            f'<img src="{image}" alt="" width="72" height="72" loading="lazy" decoding="async">'
            f"</span>"
        )
    return (
        f'<div class="post-card-media post-card-media--{fit}">'
        f'<img src="{image}" alt="{alt}" width="480" height="270" loading="lazy" decoding="async">'
        f"</div>"
    )


def head(title, depth=0, article=False, extra_head=""):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title} — Juraj Maťaše</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Syne:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">
<script src="{prefix}js/theme.js"></script>
{extra_head}
</head>"""


PRISM_SCRIPTS = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-clike.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-ruby.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markdown.min.js"></script>
<script>Prism.highlightAll();</script>
"""

LANG_MAP = {
    "terminal": "bash",
    "shell": "bash",
    "": "plaintext",
}


def normalize_lang(lang):
    lang = lang.lower().strip()
    return LANG_MAP.get(lang, lang or "plaintext")


def nav(active, depth=0):
    prefix = "../" * depth
    links = [
        ("blog", "Blog", f"{prefix}index.html"),
        ("kategorie", "Kategórie", f"{prefix}kategorie.html"),
        ("stitky", "Štítky", f"{prefix}stitky.html"),
        ("fonty", "Fonty", f"{prefix}fonty.html"),
        ("projekty", "Projekty", f"{prefix}projekty.html"),
        ("cv", "CV", f"{prefix}cv.html"),
    ]
    items_parts = []
    for key, label, href in links:
        cls = ' class="active"' if key == active else ""
        items_parts.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    items = "".join(items_parts)
    return f"""<header class="site-chrome site-header">
<nav class="navbar" id="navbar">
  <div class="nav-container">
    <a href="{prefix}index.html" class="nav-logo">
      <span class="nav-logo-mark">JM</span>
      <span class="nav-logo-text">Juraj Maťaše</span>
    </a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Otvoriť menu">
      <span class="nav-toggle-bar" aria-hidden="true"></span>
      <span class="nav-toggle-bar" aria-hidden="true"></span>
      <span class="nav-toggle-bar" aria-hidden="true"></span>
    </button>
    <ul class="nav-links" id="nav-menu">
      <li class="nav-menu-header">
        <span class="nav-menu-title">Menu</span>
        <button type="button" class="nav-close" id="nav-close" aria-label="Zavrieť menu">×</button>
      </li>
      {items}
      <li class="nav-theme-item"><button type="button" class="theme-switch" onclick="toggleTheme()" aria-label="Prepínač témy">☀ / ☾</button></li>
    </ul>
  </div>
  <button type="button" class="nav-backdrop" id="nav-backdrop" aria-label="Zavrieť menu" aria-hidden="true" tabindex="-1"></button>
</nav>
</header>"""


def page_main_open():
    return "<main class=\"page-main\">"


def page_main_close():
    return "</main>"


def page_top(eyebrow, title, subtitle=""):
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ""
    return f"""<section class="page-header vt-top">
  <div class="page-header-inner">
    <div class="vt-top-core">
      <div class="hero-eyebrow">{eyebrow}</div>
      <h1 class="page-title">{title}</h1>
      {subtitle_html}
    </div>
  </div>
</section>"""


def hero_top():
    return """<section class="hero page-header vt-top">
  <div class="page-header-inner hero-inner">
    <div class="hero-avatar" aria-hidden="true">JM</div>
    <div class="vt-top-core hero-content">
      <div class="hero-eyebrow">Osobný blog</div>
      <h1 class="page-title hero-title">Technológie, <em>sloboda</em> a&nbsp;beh</h1>
      <p class="page-subtitle hero-subtitle">Píšem o programovaní, open source, slobode na internete a občas aj o behu.</p>
      <div class="page-top-extra hero-meta">
        <span class="hero-badge">QA inžinier</span>
        <span class="hero-badge">Bratislava</span>
        <span class="hero-badge">Ruby on Rails</span>
      </div>
    </div>
  </div>
</section>"""


def article_top(post, depth=1):
    prefix = "../" * depth
    tags = "".join(
        f'<a href="{prefix}stitok-{tag_key(t)}.html" class="mini-tag">{t}</a> '
        for t in post["tags"]
    )
    cats = post["categories"][0]
    meta = f"Juraj Maťaše · {post['date']} · {post['read_time']} čítania"
    return f"""<header class="article-header page-header vt-top">
  <div class="page-header-inner article-header-inner">
    <div class="vt-top-core">
      <div class="hero-eyebrow"><nav class="breadcrumb" aria-label="Navigácia"><a href="{prefix}index.html">Domov</a> › <span>Článok</span></nav></div>
      <p class="page-top-lead"><span class="article-cat-badge">{cats}</span></p>
      <h1 class="page-title article-title">{post['title']}</h1>
      <p class="page-subtitle article-meta-line">{meta}</p>
      <div class="page-top-extra article-tags">{tags}</div>
    </div>
  </div>
</header>"""


def footer(depth=0):
    return """<footer class="site-chrome footer">
  <div class="footer-inner">
    <div class="footer-logo">Juraj Maťaše<span>.</span></div>
    <div class="footer-copy">© 2026 · Niektoré práva vyhradené (CC BY 4.0) · Statický web</div>
  </div>
</footer>"""


def font_specimen_url(name):
    family = name.replace(" ", "+")
    return f"https://fonts.google.com/specimen/{family}"


def font_import_url(name):
    family = name.replace(" ", "+")
    return f"family={family}:wght@400;500;600;700"


def font_card(font):
    group = font["group"].lower()
    family_fallback = "serif" if group == "serif" else "sans-serif"
    source_label = "Google Fonts"
    source_url = font_specimen_url(font["name"])
    pros = "".join(f"<li>{item}</li>" for item in font["pros"])
    cons = "".join(f"<li>{item}</li>" for item in font["cons"])
    quirk = font.get("quirk", "")
    quirk_html = f'<p class="font-card-quirk">{quirk}</p>' if quirk else ""
    return f"""<article class="font-card font-card--{group}">
      <div class="font-card-head">
        <div>
          <div class="font-card-kicker">{font['group']} · {source_label}</div>
          <h2 class="font-card-title">{font['name']}</h2>
        </div>
        <a class="font-card-source" href="{source_url}" target="_blank" rel="noreferrer">Zdroj</a>
      </div>
      <div class="font-card-sample" style="font-family: '{font['name']}', {family_fallback};">
        {font['sample']}
      </div>
      {quirk_html}
      <p class="font-card-tone">{font['tone']}</p>
      <div class="font-card-meta">
        <div class="font-meta-block">
          <h3>Plusy</h3>
          <ul>{pros}</ul>
        </div>
        <div class="font-meta-block">
          <h3>Mínusy</h3>
          <ul>{cons}</ul>
        </div>
      </div>
    </article>"""


def post_card(post, depth=0):
    cats = " · ".join(post["categories"])
    tags = "".join(f'<span class="mini-tag">{t}</span>' for t in post["tags"][:2])
    media = post_media_html(post, depth=depth)
    card_class = "post-card post-card--linked"
    if media:
        card_class += " post-card--has-media"
    return f"""<a href="{post_href(post, depth)}" class="{card_class}">
        {media}
        <div class="post-card-body">
          <div class="post-card-cat">{cats}</div>
          <h3 class="post-card-title">{post['title']}</h3>
          <p class="post-card-excerpt">{post['excerpt']}</p>
          <div class="post-card-meta">
            <span>{post['date']}</span>
            {tags}
          </div>
        </div>
      </a>"""


def archive_list(posts, depth=0):
    items = ""
    for p in posts:
        thumb = post_media_html(p, variant="archive", depth=depth)
        items += f"""<li class="archive-item">
          <a href="{post_href(p, depth)}" class="archive-item-link">
            {thumb}
            <span class="archive-date">{p['date']}</span>
            <span class="archive-title">{p['title']}</span>
          </a>
        </li>\n"""
    return f'<ul class="archive-list">{items}</ul>'


def write(path, content):
    path.write_text(content, encoding="utf-8")
    print("  wrote", path.relative_to(BASE))


def generate_index():
    featured = POSTS[0]
    rest = POSTS[1:]
    prefix = ""
    cards = "\n".join(post_card(p) for p in rest)
    tags_html = "".join(
        f'<a href="stitok-{tag_key(t["name"])}.html" class="tag-chip">{t["name"]}</a>'
        for t in TAGS.values()
    )

    html = f"""{head("Blog")}
<body class="site-shell">
{nav("blog")}
{page_main_open()}

{hero_top()}

<div class="container vt-body">
  <section class="featured">
    <div class="section-label">Najnovší článok</div>
    <a href="clanky/{featured['slug']}.html" class="featured-card featured-card--linked">
      {post_media_html(featured, variant="featured") or '<div class="featured-img featured-img--empty"></div>'}
      <div class="featured-body">
        <span class="featured-cat">{featured['categories'][0]}</span>
        <h2 class="featured-title">{featured['title']}</h2>
        <p class="featured-excerpt">{featured['excerpt']}</p>
        <div class="featured-meta">
          <span>{featured['date']}</span>
          <span class="featured-meta-sep"></span>
          <span>{featured['read_time']} čítania</span>
          <span class="featured-meta-sep"></span>
          {''.join(f'<span class="mini-tag">{t}</span>' for t in featured['tags'])}
        </div>
      </div>
    </a>
  </section>

  <section class="posts-section">
    <div class="section-label">Ďalšie články</div>
    <div class="posts-grid">
{cards}
    </div>
    <div class="tags-strip">
      {tags_html}
    </div>
  </section>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "index.html", html)


def generate_kategorie():
    cards = ""
    for key, cat in CATEGORIES.items():
        count = len(posts_for_category(cat["name"]))
        cards += f"""<a href="{cat['slug']}" class="category-card">
        <div class="category-card-name">{cat['name']}</div>
        <div class="category-card-count">{count} {'článok' if count == 1 else 'články' if count < 5 else 'článkov'}</div>
      </a>\n"""

    html = f"""{head("Kategórie")}
<body class="site-shell">
{nav("kategorie")}
{page_main_open()}

{page_top("Archív", "Kategórie", "Články zoradené podľa témy.")}

<div class="page-content vt-body">
  <div class="category-grid">
    {cards}
  </div>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "kategorie.html", html)


def generate_category_pages():
    for key, cat in CATEGORIES.items():
        posts = posts_for_category(cat["name"])
        count = f"{len(posts)} {'článok' if len(posts) == 1 else 'články' if len(posts) < 5 else 'článkov'}"
        html = f"""{head(cat['name'])}
<body class="site-shell">
{nav("kategorie")}
{page_main_open()}

{page_top('<a href="kategorie.html">Kategórie</a>', cat['name'], count)}

<div class="page-content vt-body">
  {archive_list(posts)}
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
        write(BASE / cat["slug"], html)


def generate_stitky():
    chips = "".join(
        f'<a href="{t["slug"]}" class="tag-chip">{t["name"]}</a>' for t in TAGS.values()
    )
    html = f"""{head("Štítky")}
<body class="site-shell">
{nav("stitky")}
{page_main_open()}

{page_top("Archív", "Štítky", "Preskúmajte články podľa kľúčových slov.")}

<div class="page-content vt-body">
  <div class="tags-strip" style="border-top:none;padding-top:0;">
    {chips}
  </div>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "stitky.html", html)


def generate_tag_pages():
    for key, tag in TAGS.items():
        posts = posts_for_tag(tag["name"])
        count = f"{len(posts)} {'článok' if len(posts) == 1 else 'články' if len(posts) < 5 else 'článkov'}"
        html = f"""{head(tag['name'])}
<body class="site-shell">
{nav("stitky")}
{page_main_open()}

{page_top('<a href="stitky.html">Štítky</a>', tag['name'], count)}

<div class="page-content vt-body">
  {archive_list(posts) if posts else '<p style="color:var(--text-muted)">Zatiaľ žiadne články.</p>'}
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
        write(BASE / tag["slug"], html)


def generate_fonty():
    font_showcase = FONT_SHOWCASE + ASYM_FONT_SHOWCASE
    import_links = "&".join(font_import_url(font["name"]) for font in font_showcase)
    extra_head = f'<link href="https://fonts.googleapis.com/css2?{import_links}&display=swap" rel="stylesheet">'
    type_map = [
        {
            "font": "Fraunces",
            "role": "Hlavný výraz",
            "use": "H1, hero nadpisy, article titles a veľké citácie.",
            "avoid": "Menu, tagy a drobné UI akcenty.",
        },
        {
            "font": "Syne",
            "role": "Malé akcenty",
            "use": "Menu, sekčné labely, badge, tagy a malé CTA.",
            "avoid": "Veľké titulky a dlhé riadky textu.",
        },
        {
            "font": "DM Sans",
            "role": "Čitateľný text",
            "use": "Body text, odstavce, meta informácie a bežné UI.",
            "avoid": "Dramatické veľké titulky, kde má byť viac osobnosti.",
        },
        {
            "font": "JetBrains Mono",
            "role": "Kód a technické detaily",
            "use": "Kódové bloky, shell výstupy, technické poznámky a identifikátory.",
            "avoid": "Marketingové nadpisy alebo text, ktorý má pôsobiť mäkko.",
        },
    ]
    type_map_cards = "\n".join(
        f"""<article class="type-map-card">
      <div class="type-map-font">{item['font']}</div>
      <div class="type-map-role">{item['role']}</div>
      <p class="type-map-use">{item['use']}</p>
      <div class="type-map-label">Kde áno</div>
      <p class="type-map-avoid">{item['avoid']}</p>
      <div class="type-map-label">Kde nie</div>
    </article>"""
        for item in type_map
    )
    current_stack = """<div class="font-stack">
      <span class="font-stack-item">Fraunces · nadpisy</span>
      <span class="font-stack-item">Syne · menu a akcenty</span>
      <span class="font-stack-item">DM Sans · text</span>
      <span class="font-stack-item">JetBrains Mono · kód</span>
    </div>"""
    headline_serifs = "\n".join(font_card(font) for font in FONT_SHOWCASE[:6])
    headline_sans = "\n".join(font_card(font) for font in FONT_SHOWCASE[6:])
    asym_headlines = "\n".join(font_card(font) for font in ASYM_FONT_SHOWCASE)
    html = f"""{head("Fonty", extra_head=extra_head)}
<body class="site-shell page-fonty">
{nav("fonty")}
{page_main_open()}

{page_top("Typografia", "12 populárnych fontov do nadpisov", "Vybral som fonty, ktoré sa dnes často objavujú v headlinoch, hero sekciách a brandových layoutoch. Pri serifoch sleduj osobitosť a, g, R, Q; pri sansoch kontrast, šírku a rytmus.")}

<div class="page-content vt-body font-showcase">
  <section class="font-intro">
    <div class="font-intro-card">
      <div class="font-intro-label">Súčasný stack</div>
      {current_stack}
      <p class="font-intro-text">Pros a mínusy sú moja praktická typografická poznámka pre blog a podobné projekty. Zohľadnil som fonty, ktoré sa často odporúčajú pre nadpisy v aktuálnych fontových roundupoch. Popularitu tu beriem ako praktický signál z dizajnovej praxe, nie ako presné štatistické meranie.</p>
    </div>
  </section>

  <section class="font-section">
    <div class="section-label">Mapa použitia</div>
    <div class="type-map">
      {type_map_cards}
    </div>
  </section>

  <section class="font-section">
    <div class="section-label">Asymetrické headliny</div>
    <div class="font-grid">
      {asym_headlines}
    </div>
  </section>

  <section class="font-section">
    <div class="section-label">Serify pre headliny</div>
    <div class="font-grid">
      {headline_serifs}
    </div>
  </section>

  <section class="font-section">
    <div class="section-label">Sansy pre headliny</div>
    <div class="font-grid">
      {headline_sans}
    </div>
  </section>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "fonty.html", html)


def generate_projekty():
    html = f"""{head("Projekty")}
<body class="site-shell">
{nav("projekty")}
{page_main_open()}

{page_top("Portfólio", "Moje projekty", "Side projekty v Ruby on Rails a okolí.")}

<div class="page-content vt-body">
  <div class="projects-grid">
    <article class="project-card">
      <div class="project-icon">⚙</div>
      <h3 class="project-title">Blog on Rails</h3>
      <p class="project-desc">Jednoduché CMS, pri ktorom si skúšam nové funkcie Ruby on Rails. Ako napríklad nové funkcie pre vlastnú autentifikáciu vo verzii 7.1.</p>
      <a href="https://github.com/majur/blog-on-rails" class="project-link">GitHub →</a>
    </article>
    <article class="project-card">
      <div class="project-icon">🔑</div>
      <h3 class="project-title">Token service</h3>
      <p class="project-desc">Backend, ktorý dokáže vytvárať a overovať tokeny.</p>
      <a href="https://github.com/majur/token_service" class="project-link">GitHub →</a>
    </article>
    <article class="project-card">
      <div class="project-icon">✓</div>
      <h3 class="project-title">Todolist backend</h3>
      <p class="project-desc">Chcel som si vyskúšať, ako sa píše backend. Článok o postupe je <a href="clanky/how-to-create-simple-backend-with-rails.html">tu</a>.</p>
      <a href="https://github.com/majur/todo_rails_backend" class="project-link">GitHub →</a>
    </article>
  </div>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "projekty.html", html)


def generate_cv():
    html = f"""{head("CV")}
<body class="site-shell">
{nav("cv")}
{page_main_open()}

{page_top("Profil", "Životopis")}

<div class="page-content vt-body">
  <div class="cv-layout">
    <aside class="cv-sidebar">
      <div class="cv-avatar" aria-hidden="true">JM</div>
      <ul class="contact-list">
        <li>📧 <a href="mailto:juraj@matase.sk">juraj@matase.sk</a></li>
        <li>💼 <a href="https://www.linkedin.com/in/juraj-matase">LinkedIn</a></li>
        <li>🌐 <a href="https://juraj.matase.sk">juraj.matase.sk</a></li>
        <li>👨‍💻 <a href="https://github.com/majur">@majur</a></li>
        <li>🏢 Bratislava, Slovensko</li>
      </ul>
      <a href="#" class="cv-download">↓ Stiahnuť PDF</a>
    </aside>
    <div class="cv-main">
      <h2 class="cv-name">Juraj Maťaše</h2>

      <section class="cv-section">
        <h2>Pracovné skúsenosti</h2>
        <div class="cv-job">
          <h3>Automation QA Tester</h3>
          <div class="cv-job-meta">Siemens s.r.o., Bratislava — 2024 – dnes</div>
          <p>Pracujem na projekte vývoja firmvéru pre regulátory termostatov v kancelárskych budovách. Stack v Pythone, veľa práce s Linuxom.</p>
        </div>
        <div class="cv-job">
          <h3>Automation QA Tester</h3>
          <div class="cv-job-meta">Indra Avitech s.r.o., Bratislava — 2023 – 2024</div>
          <p>Automatizované testy v Pythone s pytest a Playwright. Test cases v Gherkine, manuálne testovanie, quality owner produktu.</p>
        </div>
        <div class="cv-job">
          <h3>Senior QA Tester</h3>
          <div class="cv-job-meta">NER System s.r.o., Bratislava — 2020 – 2023</div>
          <p>Jediný tester v tíme vyvíjajúcom Ruby on Rails aplikáciu. Regresné testy v Cypress, testovanie iOS a Android aplikácií.</p>
        </div>
        <div class="cv-job">
          <h3>Test Manager</h3>
          <div class="cv-job-meta">Indra Avitech s.r.o., Bratislava — 2018 – 2020</div>
          <p>Vedenie tímu testerov, komunikácia s oddeleniami, nábor a onboarding. Prechod tímu na plne remote počas COVID-19.</p>
        </div>
        <div class="cv-job">
          <h3>QA Tester</h3>
          <div class="cv-job-meta">Indra Avitech s.r.o., Bratislava — 2016 – 2018</div>
          <p>Testovanie webových a desktopových aplikácií, údržba test suite a písanie test scenárov.</p>
        </div>
        <div class="cv-job">
          <h3>Web developer (freelancer)</h3>
          <div class="cv-job-meta">Trnava — 2012 – 2016</div>
          <p>WordPress, HTML, CSS. Vývoj, testovanie a project management na voľnej nohe.</p>
        </div>
      </section>

      <section class="cv-section">
        <h2>Skills</h2>
        <div class="table-scroll">
        <table class="cv-table">
          <thead><tr><th>Hard skills</th><th>Úroveň</th><th>Skúsenosti</th></tr></thead>
          <tbody>
            <tr><td>Software testing</td><td>⭐️⭐️⭐️⭐️⭐️</td><td>11 rokov</td></tr>
            <tr><td>HTML a CSS</td><td>⭐️⭐️⭐️⭐️</td><td>13 rokov</td></tr>
            <tr><td>Ruby on Rails</td><td>⭐️⭐️⭐️</td><td>4 roky (hobby)</td></tr>
            <tr><td>JavaScript</td><td>⭐️⭐️⭐️</td><td>3 roky</td></tr>
            <tr><td>Cypress</td><td>⭐️⭐️⭐️⭐️</td><td>3 roky</td></tr>
            <tr><td>Python</td><td>⭐️⭐️⭐️</td><td>3 roky</td></tr>
            <tr><td>Playwright</td><td>⭐️⭐️⭐️</td><td>2 roky</td></tr>
            <tr><td>Git a GitHub</td><td>⭐️⭐️⭐️</td><td>4 roky</td></tr>
          </tbody>
        </table>
        </div>
      </section>

      <section class="cv-section">
        <h2>Vzdelanie a kurzy</h2>
        <div class="table-scroll">
        <table class="cv-table">
          <thead><tr><th>Kurz / škola</th><th>Rok</th><th>Poznámka</th></tr></thead>
          <tbody>
            <tr><td>Stredná odborná škola energetiky</td><td>2002 – 2006</td><td>Automatizácia</td></tr>
            <tr><td>ISTQB Foundation</td><td>2018</td><td></td></tr>
            <tr><td>Team leadership course</td><td>2018</td><td></td></tr>
            <tr><td>Facilitation course</td><td>2019</td><td></td></tr>
            <tr><td>Cypress</td><td>2021</td><td>Test automation</td></tr>
          </tbody>
        </table>
        </div>
      </section>
    </div>
  </div>
</div>

{page_main_close()}
{footer()}
</body>
</html>
"""
    write(BASE / "cv.html", html)


ARTICLE_BODIES = {
    "how-to-create-simple-backend-with-rails": open(BASE.parent.parent / "_posts/2024-03-31-how-to-create-simple-backend-with-rails.md").read().split("---", 2)[2] if False else None,
}


def md_to_html_simple(text):
    """Minimal markdown to HTML for article bodies."""
    import re
    lines = text.strip().split("\n")
    out = []
    in_pre = False
    in_ul = False
    buf = []

    def flush_paragraph():
        nonlocal buf
        if buf:
            p = " ".join(buf).strip()
            if p:
                p = re.sub(r"`([^`]+)`", r"<code>\1</code>", p)
                p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
                p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
                p = p.replace('href="/cv/"', 'href="../cv.html"')
                p = re.sub(r'(\]\()/assets/', r'\1../assets/', p)
                p = re.sub(r'(\]\(/assets/)', r'](../assets/', p)
                out.append(f"<p>{p}</p>")
            buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            lang = normalize_lang(line[3:].strip())
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(
                    lines[i]
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                i += 1
            code = "\n".join(code_lines)
            out.append(
                f'<pre class="language-{lang}"><code class="language-{lang}">{code}</code></pre>'
            )
            i += 1
            continue
        if line.startswith("## "):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("# "):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h2>{line[2:]}</h2>")
        elif line.startswith("- "):
            flush_paragraph()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = line[2:]
            item = re.sub(r"`([^`]+)`", r"<code>\1</code>", item)
            item = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', item)
            out.append(f"<li>{item}</li>")
        elif line.startswith("> "):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            quote = line[2:]
            quote = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", quote)
            out.append(f"<blockquote><p>{quote}</p></blockquote>")
        elif line.strip() == "---":
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("<hr>")
        elif line.strip() == "":
            flush_paragraph()
        elif line.startswith("!["):
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            m = re.match(r"!\[([^\]]*)\]\([^)]+\)", line)
            if m:
                out.append(f"<p><em>[{m.group(1)}]</em></p>")
        else:
            buf.append(line.strip())
        i += 1
    flush_paragraph()
    if in_ul:
        out.append("</ul>")
    return "\n    ".join(out)


def load_article_body(slug):
    md_path = POSTS_DIR / POST_MD_MAP[slug]
    body = md_path.read_text(encoding="utf-8").split("---", 2)[2]
    # strip jekyll annotations
    import re
    body = re.sub(r"\{: [^}]+\}", "", body)
    body = re.sub(r"\{:[^}]+\}", "", body)
    return md_to_html_simple(body)


def generate_articles():
    for idx, post in enumerate(POSTS):
        prev_p = POSTS[idx + 1] if idx + 1 < len(POSTS) else None
        next_p = POSTS[idx - 1] if idx > 0 else None
        body = load_article_body(post["slug"])
        prev_nav = ""
        if prev_p:
            prev_nav = f"""<a href="{prev_p['slug']}.html" class="post-nav-card prev" data-vt-direction="prev">
        <div class="post-nav-label">← Predošlý článok</div>
        <div class="post-nav-title">{prev_p['title']}</div>
      </a>"""
        else:
            prev_nav = '<div></div>'

        next_nav = ""
        if next_p:
            next_nav = f"""<a href="{next_p['slug']}.html" class="post-nav-card next" data-vt-direction="next">
        <div class="post-nav-label">Nasledujúci článok →</div>
        <div class="post-nav-title">{next_p['title']}</div>
      </a>"""
        else:
            next_nav = '<div></div>'

        html = f"""{head(post['title'], depth=1, article=True)}
<body class="site-shell page-article">
{nav("blog", depth=1)}
{page_main_open()}

{article_top(post)}

<div class="article-container">
  <article class="article-body vt-body">
    {body}
  </article>
  <nav class="post-nav vt-article-nav" aria-label="Navigácia medzi článkami">
    {prev_nav}
    {next_nav}
  </nav>
</div>

{page_main_close()}
{footer()}
{PRISM_SCRIPTS}
</body>
</html>
"""
        write(BASE / "clanky" / f"{post['slug']}.html", html)


if __name__ == "__main__":
    print("Generating navrh4 static site...")
    enrich_posts()
    generate_index()
    generate_kategorie()
    generate_category_pages()
    generate_stitky()
    generate_tag_pages()
    generate_fonty()
    generate_projekty()
    generate_cv()
    generate_articles()
    print("Done.")
