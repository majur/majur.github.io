#!/usr/bin/env python3
"""Generates static HTML pages for navrh4. Run once after content changes."""
import os
from pathlib import Path

BASE = Path(__file__).parent

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


def cat_key(name):
    return name.lower().replace(" ", "-")


def tag_key(name):
    return name.lower().replace("-sk", "").replace(" ", "")


def posts_for_category(name):
    return [p for p in POSTS if name in p["categories"]]


def posts_for_tag(name):
    return [p for p in POSTS if name in p["tags"]]


def head(title, depth=0, article=False):
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Juraj Maťaše</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">
<script src="{prefix}js/theme.js"></script>
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
        ("projekty", "Projekty", f"{prefix}projekty.html"),
        ("cv", "CV", f"{prefix}cv.html"),
    ]
    items_parts = []
    for key, label, href in links:
        cls = ' class="active"' if key == active else ""
        items_parts.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    items = "".join(items_parts)
    return f"""<nav class="navbar" id="navbar">
  <div class="nav-container">
    <a href="{prefix}index.html" class="nav-logo">
      <span class="nav-logo-mark">JM</span>
      Juraj Maťaše
    </a>
    <ul class="nav-links">
      {items}
      <li><button class="theme-switch" onclick="toggleTheme()" aria-label="Prepínač témy">☀ / ☾</button></li>
    </ul>
  </div>
</nav>"""


def footer(depth=0):
    return """<footer class="footer">
  <div class="footer-inner">
    <div class="footer-logo">Juraj Maťaše<span>.</span></div>
    <div class="footer-copy">© 2026 · Niektoré práva vyhradené (CC BY 4.0) · Statický web</div>
  </div>
</footer>"""


def post_card(post, depth=0):
    prefix = "../" * depth
    cats = " · ".join(post["categories"])
    tags = "".join(f'<span class="mini-tag">{t}</span>' for t in post["tags"][:2])
    return f"""<article class="post-card">
        <div class="post-card-accent"></div>
        <div class="post-card-body">
          <div class="post-card-cat">{cats}</div>
          <h3 class="post-card-title"><a href="{prefix}clanky/{post['slug']}.html">{post['title']}</a></h3>
          <p class="post-card-excerpt">{post['excerpt']}</p>
          <div class="post-card-meta">
            <span>{post['date']}</span>
            {tags}
          </div>
        </div>
      </article>"""


def archive_list(posts, depth=0):
    prefix = "../" * depth
    items = ""
    for p in posts:
        items += f"""<li class="archive-item">
          <span class="archive-date">{p['date']}</span>
          <a href="{prefix}clanky/{p['slug']}.html" class="archive-link">{p['title']}</a>
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
<body>
{nav("blog")}

<section class="hero">
  <div class="hero-inner">
    <div class="hero-avatar" aria-hidden="true">JM</div>
    <div class="hero-content">
      <div class="hero-eyebrow">Osobný blog</div>
      <h1 class="hero-title">Technológie, <em>sloboda</em> a&nbsp;beh</h1>
      <p class="hero-subtitle">Píšem o programovaní, open source, slobode na internete a občas aj o behu.</p>
      <div class="hero-meta">
        <span class="hero-badge">QA inžinier</span>
        <span class="hero-badge">Bratislava</span>
        <span class="hero-badge">Ruby on Rails</span>
      </div>
    </div>
  </div>
</section>

<div class="container">
  <section class="featured">
    <div class="section-label">Najnovší článok</div>
    <article class="featured-card">
      <div class="featured-img">[ Ruby on Rails logo ]</div>
      <div class="featured-body">
        <span class="featured-cat">{featured['categories'][0]}</span>
        <h2 class="featured-title">
          <a href="clanky/{featured['slug']}.html">{featured['title']}</a>
        </h2>
        <p class="featured-excerpt">{featured['excerpt']}</p>
        <div class="featured-meta">
          <span>{featured['date']}</span>
          <span class="featured-meta-sep"></span>
          <span>{featured['read_time']} čítania</span>
          <span class="featured-meta-sep"></span>
          {''.join(f'<span class="mini-tag">{t}</span>' for t in featured['tags'])}
        </div>
      </div>
    </article>
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
<body>
{nav("kategorie")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow">Archív</div>
    <h1 class="page-title">Kategórie</h1>
    <p class="page-subtitle">Články zoradené podľa témy.</p>
  </div>
</section>

<div class="page-content">
  <div class="category-grid">
    {cards}
  </div>
</div>

{footer()}
</body>
</html>
"""
    write(BASE / "kategorie.html", html)


def generate_category_pages():
    for key, cat in CATEGORIES.items():
        posts = posts_for_category(cat["name"])
        html = f"""{head(cat['name'])}
<body>
{nav("kategorie")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow"><a href="kategorie.html">Kategórie</a></div>
    <h1 class="page-title">{cat['name']}</h1>
    <p class="page-subtitle">{len(posts)} {'článok' if len(posts) == 1 else 'články' if len(posts) < 5 else 'článkov'}</p>
  </div>
</section>

<div class="page-content">
  {archive_list(posts)}
</div>

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
<body>
{nav("stitky")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow">Archív</div>
    <h1 class="page-title">Štítky</h1>
    <p class="page-subtitle">Preskúmajte články podľa kľúčových slov.</p>
  </div>
</section>

<div class="page-content">
  <div class="tags-strip" style="border-top:none;padding-top:0;">
    {chips}
  </div>
</div>

{footer()}
</body>
</html>
"""
    write(BASE / "stitky.html", html)


def generate_tag_pages():
    for key, tag in TAGS.items():
        posts = posts_for_tag(tag["name"])
        html = f"""{head(tag['name'])}
<body>
{nav("stitky")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow"><a href="stitky.html">Štítky</a></div>
    <h1 class="page-title">{tag['name']}</h1>
    <p class="page-subtitle">{len(posts)} {'článok' if len(posts) == 1 else 'články' if len(posts) < 5 else 'článkov'}</p>
  </div>
</section>

<div class="page-content">
  {archive_list(posts) if posts else '<p style="color:var(--text-muted)">Zatiaľ žiadne články.</p>'}
</div>

{footer()}
</body>
</html>
"""
        write(BASE / tag["slug"], html)


def generate_projekty():
    html = f"""{head("Projekty")}
<body>
{nav("projekty")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow">Portfólio</div>
    <h1 class="page-title">Moje projekty</h1>
    <p class="page-subtitle">Side projekty v Ruby on Rails a okolí.</p>
  </div>
</section>

<div class="page-content">
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

{footer()}
</body>
</html>
"""
    write(BASE / "projekty.html", html)


def generate_cv():
    html = f"""{head("CV")}
<body>
{nav("cv")}

<section class="page-header">
  <div class="page-header-inner">
    <div class="hero-eyebrow">Profil</div>
    <h1 class="page-title">Životopis</h1>
  </div>
</section>

<div class="page-content">
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
      </section>

      <section class="cv-section">
        <h2>Vzdelanie a kurzy</h2>
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
      </section>
    </div>
  </div>
</div>

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
    md_map = {
        "how-to-create-simple-backend-with-rails": "2024-03-31-how-to-create-simple-backend-with-rails.md",
        "ahoj-jekyll": "2023-03-31-ahoj-jekyll.md",
        "socialna-siet-buducnosti-ma-23-rokov": "2023-03-26-socialna-siet-buducnosti-ma-23-rokov.md",
        "moj-setup": "2021-10-06-moj-setup.md",
        "preco-hodnota-bitcoinu-stupa": "2021-02-26-preco-hodnota-bitcoinu-stupa.md",
        "trumpov-twitter-a-sloboda-slova": "2021-01-15-trumpov-twitter-a-sloboda-slova.md",
        "maraton-pohronskym-inovcom-2018": "2018-03-09-maraton-pohronskym-inovcom-2018.md",
    }
    md_path = BASE.parent.parent / "_posts" / md_map[slug]
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
        tags = "".join(f'<a href="../stitok-{tag_key(t)}.html" class="mini-tag">{t}</a> ' for t in post["tags"])
        cats = post["categories"][0]

        prev_nav = ""
        if prev_p:
            prev_nav = f"""<a href="{prev_p['slug']}.html" class="post-nav-card prev">
        <div class="post-nav-label">← Predošlý článok</div>
        <div class="post-nav-title">{prev_p['title']}</div>
      </a>"""
        else:
            prev_nav = '<div></div>'

        next_nav = ""
        if next_p:
            next_nav = f"""<a href="{next_p['slug']}.html" class="post-nav-card next">
        <div class="post-nav-label">Nasledujúci článok →</div>
        <div class="post-nav-title">{next_p['title']}</div>
      </a>"""
        else:
            next_nav = '<div></div>'

        html = f"""{head(post['title'], depth=1, article=True)}
<body>
{nav("blog", depth=1)}

<header class="article-header">
  <div class="article-header-inner">
    <nav class="breadcrumb">
      <a href="../index.html">Domov</a> › <span>Článok</span>
    </nav>
    <span class="article-cat-badge">{cats}</span>
    <h1 class="article-title">{post['title']}</h1>
    <div class="article-meta">
      <span>Juraj Maťaše</span>
      <span class="featured-meta-sep"></span>
      <span>{post['date']}</span>
      <span class="featured-meta-sep"></span>
      <span>{post['read_time']} čítania</span>
    </div>
    <div class="article-tags">{tags}</div>
  </div>
</header>

<div class="article-container">
  <article class="article-body">
    {body}
  </article>
  <nav class="post-nav">
    {prev_nav}
    {next_nav}
  </nav>
</div>

{footer()}
{PRISM_SCRIPTS}
</body>
</html>
"""
        write(BASE / "clanky" / f"{post['slug']}.html", html)


if __name__ == "__main__":
    print("Generating navrh4 static site...")
    generate_index()
    generate_kategorie()
    generate_category_pages()
    generate_stitky()
    generate_tag_pages()
    generate_projekty()
    generate_cv()
    generate_articles()
    print("Done.")
