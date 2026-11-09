# -*- coding: utf-8 -*-
import os, json, html, shutil, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "site")
esc = html.escape
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
MOIS_L = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
PAGES = []          # (url, title, group) pour le plan du site / recherche


def d_fr(iso, long=False):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {(MOIS_L if long else MOIS)[m-1]}" + (f" {y}" if long else "")


def prog_url(p): return f"formations/{p['slug']}.html"
def fam_url(f): return f"domaines/{f['slug']}.html"
def pole_url(p): return f"poles/{p['slug']}.html"
def campus_url(c): return f"campus/{c[1]}.html"


FAM_ORDER = {f["slug"]: i for i, f in enumerate(FAMILLES)}
for i, p in enumerate(P):
    p["id"] = i
    p["fam_obj"] = FAM_BY_SLUG[p["fam"]]
    p["pole_obj"] = POLE_BY_SLUG[p["fam_obj"]["pole"]]
P_SORTED = sorted(P, key=lambda p: (FAM_ORDER[p["fam"]], LEVEL_ORDER[p["typ"]], p["titre"]))


# ------------------------------------------------------------------ motifs SVG
def motif(i, color):
    c = color
    shapes = [
        f'<circle cx="22" cy="22" r="16" fill="{c}" opacity=".95"/><circle cx="42" cy="42" r="16" fill="none" stroke="{c}" stroke-width="3"/>',
        f'<rect x="6" y="36" width="12" height="22" rx="4" fill="{c}"/><rect x="26" y="20" width="12" height="38" rx="4" fill="{c}" opacity=".7"/><rect x="46" y="6" width="12" height="52" rx="4" fill="{c}" opacity=".4"/>',
        f'<path d="M8 32a24 24 0 0 1 48 0" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/><path d="M20 32a12 12 0 0 1 24 0" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" opacity=".5"/>',
        f'<path d="M32 6 58 52H6Z" fill="{c}" opacity=".9"/><circle cx="32" cy="38" r="7" fill="#fff"/>',
        f'<rect x="8" y="8" width="22" height="22" rx="7" fill="{c}"/><rect x="34" y="8" width="22" height="22" rx="11" fill="{c}" opacity=".5"/><rect x="8" y="34" width="22" height="22" rx="11" fill="{c}" opacity=".5"/><rect x="34" y="34" width="22" height="22" rx="7" fill="{c}" opacity=".85"/>',
        f'<circle cx="32" cy="32" r="26" fill="none" stroke="{c}" stroke-width="3" stroke-dasharray="4 6"/><circle cx="32" cy="32" r="12" fill="{c}"/>',
        f'<path d="M6 44C16 12 26 12 32 32S48 52 58 20" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>',
        f'<path d="M8 56V24L32 8l24 16v32Z" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round"/><rect x="24" y="34" width="16" height="22" rx="3" fill="{c}"/>',
        f'<path d="M8 20h48M8 32h34M8 44h20" stroke="{c}" stroke-width="7" stroke-linecap="round"/>',
    ]
    return f'<svg class="motif" viewBox="0 0 64 64" aria-hidden="true">{shapes[i % len(shapes)]}</svg>'


# ------------------------------------------------------------------ carte de France
FR_OUTLINE = [(2.5, 51.1), (4.2, 49.95), (5.8, 49.5), (8.2, 49.0), (7.6, 47.6), (6.1, 46.2), (7.0, 45.9), (7.0, 44.4), (7.7, 43.8), (6.5, 43.1),
              (4.8, 43.4), (3.1, 43.1), (3.0, 42.5), (1.5, 42.7), (-0.3, 42.8), (-1.8, 43.4), (-1.2, 44.7), (-1.2, 46.0), (-2.4, 47.3), (-4.4, 47.9),
              (-4.7, 48.5), (-3.0, 48.8), (-1.6, 48.7), (-1.3, 49.7), (0.2, 49.7), (1.6, 50.2)]
K = 52


def proj(lon, lat): return ((lon + 5.5) * 0.69 * K + 14, (51.6 - lat) * K + 12)


LABEL = {"PAR": ("end", -11, -8), "VDE": ("start", 11, 14), "BDX": ("end", -11, 4), "NAN": ("end", -11, 4), "REN": ("end", -11, 4), "ROU": ("end", -11, -6),
         "LIL": ("start", 11, 4), "STR": ("end", -11, 4), "LYO": ("start", 11, 4), "MTP": ("end", -11, 16), "AIX": ("middle", 0, 24), "SOP": ("start", 11, 4), "TLS": ("end", -11, 4)}


def fr_map(base):
    pts = " ".join(f"{proj(*p)[0]:.1f},{proj(*p)[1]:.1f}" for p in FR_OUTLINE)
    out = [f'<svg viewBox="0 0 560 520" role="img" aria-label="Carte des campus Ynov en France"><polygon class="shape" points="{pts}" stroke-linejoin="round"/>']
    for k, c in enumerate(CAMPUS):
        x, y = proj(c[4], c[5]); a, dx, dy = LABEL[c[0]]
        short = c[2].replace("Paris Ouest ", "").replace("Paris Est ", "").replace("Nice - ", "")
        out.append(f'<a href="{base}{campus_url(c)}"><g class="pin" data-c="{c[0]}" style="--pd:{k*0.26:.2f}s"><circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="9"/>'
                   f'<circle class="core" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/><text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{a}">{esc(short)}</text></g></a>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ composants
def arrow(): return '<span class="ar">→</span>'


def badge(p):
    s = f'<span class="badge b-{p["typ"]}">{p["typ"]}</span>'
    if p["online"]: s += ' <span class="badge b-online">En ligne</span>'
    if "SOP" in p["campus"]: s += ' <span class="badge b-sop">Sophia</span>'
    return s


def prog_card(p, base, idx=0):
    f = p["fam_obj"]
    nb = len(p["campus"]) + (1 if p["online"] else 0)
    return (f'<a class="prog reveal" style="--d:{idx%3}" href="{base}{prog_url(p)}"><div class="top">{badge(p)}</div>'
            f'<h3>{esc(p["titre"])}</h3><div class="fam">{esc(f["nom"])}</div>'
            f'<div class="foot"><span>{p["duree"]} · dès {esc(p["entree"])}</span><span class="link-ar">{nb} campus <span>→</span></span></div></a>')


def campus_names(p, base, link=True):
    out = []
    for code in p["campus"]:
        c = CAMPUS_BY_CODE[code]
        cls = ' class="on"' if code == "SOP" else ""
        out.append(f'<a{cls} href="{base}{campus_url(c)}">{esc(c[2])}</a>' if link else f'<span>{esc(c[2])}</span>')
    if p["online"]:
        out.append(f'<a href="{base}campus/connect.html">Connect · 100 % en ligne</a>')
    return "".join(out)


def cta_band(base, title="Candidatures ouvertes pour la rentrée 2027", text="Dossier en ligne, réponse sous 48 h après l'entretien.", extra=True):
    b2 = f'<a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="{base}evenements.html">Portes ouvertes</a>' if extra else ""
    return (f'<div class="cta-band reveal"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div class="acts"><a class="btn btn-lime" href="{base}admission.html#candidater">Candidater {arrow()}</a>{b2}</div></div>')


POLE_G = {"#5AFFB6": "g-tech", "#FF84EF": "g-media", "#4A8CFF": "g-archi"}


def page_hero(base, crumbs, title, lead="", chips="", color="#859CFF"):
    cr = "".join(f'<span>{f"<a href=\"{base}{u}\">{esc(t)}</a>" if u else esc(t)}</span>' for t, u in crumbs)
    return (f'<section class="page-hero {POLE_G.get(color, "")}" style="--hc:{color}"><div class="blob"></div><div class="wrap"><nav class="crumbs" aria-label="Fil d’Ariane">{cr}</nav>'
            f'<h1 class="reveal">{title}</h1>{f"<p class=\"lead reveal\" style=\"--d:1\">{lead}</p>" if lead else ""}{chips}</div></section>')


def sec_head(eyebrow, title, text=""):
    return (f'<div class="sec-head"><div class="reveal"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div>'
            f'{f"<p class=\"reveal\" style=\"--d:1\">{text}</p>" if text else ""}</div>')


# ------------------------------------------------------------------ gabarit
NAV = [("formations/index.html", "Formations"), ("campus/index.html", "Campus"), ("pedagogie.html", "Pédagogie"), ("alternance.html", "Alternance"), ("admission.html", "Admission")]


def header(base, current):
    def cur(k): return ' class="current"' if current == k else ""
    mega_f = ""
    for pl in POLES:
        fams = "".join(f'<a href="{base}{fam_url(f)}">{esc(f["nom"])}</a>' for f in FAMILLES if f["pole"] == pl["slug"])
        mega_f += f'<div><a class="pole-t" href="{base}{pole_url(pl)}"><i class="dot" style="background:{pl["color"]}"></i>{esc(pl["nom"])}</a>{fams}</div>'
    mega_c = '<div style="grid-column:1/-1;display:grid;grid-template-columns:repeat(3,1fr);gap:0 20px">' + "".join(f'<a href="{base}{campus_url(c)}">{esc(c[2])}</a>' for c in CAMPUS) + f'<a href="{base}campus/connect.html">Connect · en ligne</a></div>'
    mega_a = "".join(f'<a href="{base}{u}">{t}</a>' for u, t in [("a-propos.html", "Qui sommes-nous"), ("vie-de-campus.html", "Vie de campus"), ("projets.html", "Projets étudiants"), ("metiers.html", "Guide des métiers"), ("alumni.html", "Alumni"),
                                                                 ("entreprises.html", "Entreprises"), ("ystart.html", "Ystart, incubateur"), ("parents.html", "Parents"), ("actualites.html", "Actualités")])
    drawer = "".join(f'<a href="{base}{u}">{t}</a>' for u, t in NAV) + "".join(f'<a href="{base}{u}">{t}</a>' for u, t in [("a-propos.html", "À propos"), ("vie-de-campus.html", "Vie de campus"), ("projets.html", "Projets étudiants"), ("metiers.html", "Guide des métiers"),
                                                                                                                       ("entreprises.html", "Entreprises"), ("evenements.html", "Portes ouvertes"), ("faq.html", "FAQ"), ("contact.html", "Contact")])
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<div class="concept-bar"><div class="wrap"><span><b>Concept de refonte</b> — projet étudiant non officiel, sans lien avec Ynov. Contenus issus du site public ynov.com (relevé du 6 nov. 2026).</span><button aria-label="Fermer le bandeau">×</button></div></div>
<header class="site-head"><div class="wrap nav">
<a class="brand" href="{base}index.html" aria-label="Accueil"><i>y</i>ynov<span class="sr"> concept</span></a>
<ul class="menu">
<li{cur("formations")}><button type="button" aria-haspopup="true">Formations <small>▾</small></button><div class="mega">{mega_f}</div></li>
<li{cur("campus")}><button type="button" aria-haspopup="true">Campus <small>▾</small></button><div class="mega" style="width:min(640px,92vw)">{mega_c}</div></li>
<li{cur("pedagogie")}><a href="{base}pedagogie.html">Pédagogie</a></li>
<li{cur("alternance")}><a href="{base}alternance.html">Alternance</a></li>
<li{cur("admission")}><a href="{base}admission.html">Admission</a></li>
<li{cur("about")}><button type="button" aria-haspopup="true">Ynov <small>▾</small></button><div class="mega sm">{mega_a}</div></li>
</ul>
<div class="head-cta"><button class="kbd-btn" data-cmdk aria-label="Rechercher"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span class="t">Rechercher</span><kbd>Ctrl K</kbd></button>
<a class="btn btn-primary btn-sm" href="{base}admission.html#candidater">Candidater {arrow()}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span></button></div></div></header>
<div class="drawer">{drawer}</div>
<div class="cmdk" role="dialog" aria-label="Recherche"><div class="cmdk-box"><input type="search" placeholder="Rechercher une formation, un campus, une page…" aria-label="Rechercher"><ul></ul></div></div>'''


def footer(base):
    def col(t, items): return f'<div><h4>{t}</h4><ul>' + "".join(f'<li><a href="{base}{u}">{l}</a></li>' for u, l in items) + '</ul></div>'
    return f'''<footer class="foot"><div class="wrap"><div class="foot-grid">
<div><a class="brand" href="{base}index.html"><i>y</i>ynov</a><p style="max-width:300px;font-size:15px">L'école des transformations digitales — du BTS au Mastère, en 2, 3 ou 5 ans, sur 14 campus.</p>
<p style="font-size:14px">Appel gratuit : <a href="tel:0800600633" style="color:#fff;font-weight:600">0800 600 633</a></p></div>
{col("Formations", [(fam_url(f), f["nom"]) for f in FAMILLES[:6]] + [("formations/index.html", "Toutes les formations →")])}
{col("Campus", [(campus_url(c), c[2]) for c in CAMPUS[:6]] + [("campus/index.html", "Tous les campus →")])}
{col("Étudier", [("admission.html", "Admission"), ("alternance.html", "Alternance"), ("pedagogie.html", "Pédagogie"), ("projets.html", "Projets étudiants"), ("evenements.html", "Portes ouvertes"), ("parents.html", "Parents"), ("faq.html", "FAQ")])}
{col("Ynov", [("a-propos.html", "Qui sommes-nous"), ("entreprises.html", "Entreprises"), ("alumni.html", "Alumni"), ("handicap.html", "Handicap"), ("fondation.html", "Fondation"), ("presse.html", "Presse"), ("recrutement.html", "Nous rejoindre")])}
</div><div class="disc"><span>Concept de refonte non officiel · maquette de travail, aucune donnée n'est collectée ni envoyée.</span><span><a href="{base}mentions.html">Mentions &amp; sources</a> · <a href="{base}plan-du-site.html">Plan du site</a> · <a href="{base}contact.html">Contact</a></span></div></div></footer>'''


def page(path, title, body, desc="", current="", group="Pages", index=True, extra_head="", extra_js=""):
    depth = path.count("/")
    base = "../" * depth
    full = f'''<!DOCTYPE html>
<html lang="fr" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Ynov — concept de refonte</title><meta name="description" content="{esc(desc or title)}">
<meta name="robots" content="noindex"><meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%234F46FF'/%3E%3Ctext x='16' y='23' font-size='20' font-weight='800' text-anchor='middle' fill='white' font-family='sans-serif'%3Ey%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">{extra_head}</head>
<body data-base="{base}">
{header(base, current)}
<main id="main">{body}</main>
{footer(base)}
<script src="{base}assets/data.js"></script><script src="{base}assets/app.js"></script>{extra_js}
</body></html>'''
    fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as fh: fh.write(full)
    if index: PAGES.append((path, title, group))


# ================================================================== PAGES
def build_home():
    b = ""
    hero_words = [("Ton", 0, False), ("avenir", 1, False), ("se", 2, False), ("construit", 3, False), ("en", 4, False), ("faisant.", 5, True)]
    h1 = " ".join(f'<span class="w"><span style="--i:{i}">{("<em>"+w+"</em>") if em else w}</span></span>' for w, i, em in hero_words)
    b += f'''<section class="hero"><div class="blob"></div><div class="blob b2"></div><div class="wrap">
<div class="hero-grid"><div>
<a class="pill reveal" href="{"admission.html"}"><b>Rentrée 2027</b> Candidatures ouvertes depuis le 1er octobre <span>→</span></a>
<h1>{h1}</h1>
<p class="lead reveal" style="--d:3">Ynov est l'école des transformations digitales : des formations en 2, 3 ou 5 ans, du BTS au Mastère, en initial ou en alternance, avec des projets réels dès le premier jour.</p>
<div class="cta reveal" style="--d:4"><a class="btn btn-primary" href="admission.html#candidater">Candidater {arrow()}</a><a class="btn btn-ghost" href="formations/index.html">Explorer les {len(P)} formations</a></div>
</div>
<div class="hero-visual" aria-hidden="true">
<div class="hv-card c1 hv-float"><span class="tag" style="background:#DDFFF1;color:#0A0006">Technologies &amp; Ingénierie</span><h3>Coder · Sécuriser · Automatiser</h3><p>IA, data, cybersécurité, cloud.</p><div class="bars" style="--c:#4F46FF"><i style="--k:0"></i><i style="--k:1"></i><i style="--k:2"></i><i style="--k:3"></i></div></div>
<div class="hv-card c2 hv-float"><span class="tag" style="background:#FFE8FB;color:#0A0006">Médias &amp; Création</span><h3>Imaginer · Créer · Médiatiser</h3><p>3D, jeu vidéo, design, audiovisuel, marketing.</p><div class="bars" style="--c:#FF5C39"><i style="--k:1"></i><i style="--k:2"></i><i style="--k:3"></i><i style="--k:4"></i></div></div>
<div class="hv-card c3 hv-float"><span class="tag" style="background:#E3EDFF;color:#0A0006">Architectures &amp; Bâtiment</span><h3>Concevoir · Construire · Transformer</h3><p>Architecture d'intérieur, BIM, jumeaux numériques.</p><div class="bars" style="--c:#0E9F6E"><i style="--k:2"></i><i style="--k:3"></i><i style="--k:4"></i><i style="--k:5"></i></div></div>
</div></div>
<div class="stats-strip reveal">''' + "".join(
        f'<div class="stat"><div class="n"><span data-count="{n.replace(" ", "").replace("+", "")}" data-suffix="{"+" if "+" in n else ""}">{n}</span></div><div class="l">{l}</div><div class="s">{s}</div></div>' for n, l, s in STATS) + '''</div></div></section>'''

    chips = ["3D & Gaming", "UX Design", "Création vidéo", "Influence", "Programmation", "Ethical hacking", "Web apps", "IA & Machine learning", "Big data", "Cybersécurité", "Maîtrise d'œuvre",
             "Jumeaux numériques", "Architecture d'intérieur", "Design d'espace", "BIM", "Rénovation"]
    b += '<div class="marquee" aria-hidden="true"><div class="track">' + "".join(f'<span class="chip">{c}</span>' for c in chips * 2) + '</div></div>'

    # pôles
    cards = ""
    for i, pl in enumerate(POLES):
        mets = "".join(f"<li>{esc(m)}</li>" for m in pl["metiers"][:4])
        cards += (f'<a class="card pole-card reveal" style="--d:{i};--soft:{pl["soft"]};--c:{pl["color"]}" href="{pole_url(pl)}"><div class="verbs">{pl["verbes"]}</div><h3>{esc(pl["nom"])}</h3>'
                  f'<p>{esc(pl["intro"])}</p><ul>{mets}</ul><span class="more">Découvrir le pôle <span>→</span></span></a>')
    b += f'<section class="sec"><div class="wrap">{sec_head("3 pôles d’excellence", "Trois regards, trois manières d’intervenir sur le réel.", "Ces pôles portent la transformation digitale des nouveaux métiers. Ils ne se mélangent pas : ils dialoguent, sur des projets communs.")}<div class="grid g3">{cards}</div></div></section>'

    # finder + familles
    fopts = "".join(f'<option value="{f["slug"]}">{esc(f["nom"])}</option>' for f in FAMILLES)
    copts = "".join(f'<option value="{c[0]}">{esc(c[2])}</option>' for c in CAMPUS)
    fam_cards = ""
    for i, f in enumerate(FAMILLES):
        n = len([p for p in P if p["fam"] == f["slug"]]); col = POLE_BY_SLUG[f["pole"]]["color"]
        fam_cards += (f'<a class="card fam-card reveal" style="--d:{i%3}" href="{fam_url(f)}">{motif(i, col)}<span class="num">{i+1:02d}</span><h3 style="margin-top:36px">{esc(f["nom"])}</h3>'
                      f'<p style="margin-bottom:12px">{esc(f["accroche"])}</p><span class="count">{n} formation{"s" if n>1 else ""}</span></a>')
    b += f'''<section class="sec alt" style="padding-top:0"><div class="wrap">
<form id="finder" class="finder reveal"><div class="field"><label for="f-n">Je cherche</label><select id="f-n" name="niveau"><option value="">Tous les niveaux</option><option>BTS</option><option>Bachelor</option><option>Mastère</option></select></div>
<div class="field"><label for="f-f">Dans le domaine</label><select id="f-f" name="fam"><option value="">Tous les domaines</option>{fopts}</select></div>
<div class="field"><label for="f-c">Sur le campus</label><select id="f-c" name="campus"><option value="">Partout en France</option>{copts}</select></div>
<button class="btn btn-accent" type="submit">Trouver {arrow()}</button></form>
<div style="height:96px"></div>{sec_head("9 domaines", "Du BTS au Mastère, une formation pour chaque envie.", f"{len(P)} programmes, tous accessibles en alternance selon le niveau.")}
<div class="grid g3">{fam_cards}</div></div></section>'''

    # pédagogie
    ped = "".join(f'<div class="reveal" style="--d:{i}"><div class="t">{t}</div><span class="d">{d}</span><p>{esc(x)}</p></div>' for i, (t, d, x) in enumerate(PEDAGOGIE))
    b += f'''<section class="sec dark"><div class="wrap"><div class="sec-head"><div class="reveal"><span class="eyebrow">Learning by doing</span><h2>Avant, tu allais en cours.<br>Chez Ynov, tu diriges des projets.</h2></div>
<p class="reveal" style="--d:1;color:#C3CAC5">Une idée se teste, se confronte au réel, se présente, s'améliore. La première réponse est rarement la meilleure, et recommencer, c'est déjà avancer.</p></div>
<div class="ped">{ped}</div><p style="margin-top:34px"><a class="btn btn-lime" href="pedagogie.html">Comprendre la pédagogie {arrow()}</a></p></div></section>'''

    # projets étudiants
    pcards = "".join(f'<a class="proj-feature reveal" style="--d:{i}" href="projets/{pj["slug"]}.html"><div><span class="badge b-Bachelor">Projet étudiant</span><h3>{esc(pj["titre"])}</h3><p>{esc(pj["accroche"])}</p><div class="tagrow">' + "".join(f"<span>{esc(t)}</span>" for t in pj["tags"]) + f'</div><span class="link-ar">Découvrir <span>→</span></span></div><div class="pf-vis pf-{pj["slug"]}" aria-hidden="true"></div></a>' for i, pj in enumerate(PROJETS))
    b += f'<section class="sec"><div class="wrap">{sec_head("Projets étudiants", "Ce que les étudiants construisent dès la première année.", "Deux exemples de projets de B1, réalisés à Ynov Sophia.")}<div class="grid g2">{pcards}</div><p style="margin-top:28px"><a class="link-ar" href="projets.html">Tous les projets étudiants <span>→</span></a></p></div></section>'

    # alternance
    b += f'''<section class="sec"><div class="wrap split"><div class="reveal"><span class="eyebrow">Alternance</span><h2>2 à 3 années d’expérience professionnelle à la sortie.</h2>
<p class="lead">Dès le Bachelor 2 ou 3 selon la formation, et dès le Mastère 1, tu alternes entre l'école et l'entreprise. Les frais de formation sont pris en charge par l'entreprise ou son OPCO.</p>
<ul class="checks"><li>Maîtrise des compétences techniques sur du réel</li><li>Employabilité maximisée, carrière accélérée</li><li>Job datings sur chaque campus et accompagnement des équipes</li></ul>
<a class="btn btn-primary" href="alternance.html">Tout savoir sur l’alternance {arrow()}</a></div>
<div class="reveal" style="--d:1"><div class="big-num"><span data-count="4200" data-suffix="+">4 200+</span></div><p class="lead" style="margin-top:10px">apprenants en alternance</p>
<div class="rhythm"><div class="row"><div class="ent" style="flex:7">≈ 70 % en entreprise</div><div class="eco" style="flex:3">école</div></div><p class="note" style="margin:0">Selon la formation : 1 semaine école / 2 semaines entreprise, ou 2 jours école / 3 jours entreprise.</p></div></div></div></section>'''

    # carte campus
    cl = "".join(f'<a href="{campus_url(c)}" data-c="{c[0]}"><span>{esc(c[2])}</span><small>{len([p for p in P if c[0] in p["campus"]])} formations</small></a>' for c in CAMPUS)
    cl += '<a class="online" href="campus/connect.html"><span>Connect — 100 % en ligne</span><small>alternance à distance</small></a>'
    b += f'''<section class="sec alt"><div class="wrap">{sec_head("14 campus", "Au cœur des grandes métropoles.", "13 campus physiques et un campus 100 % en ligne. Survole la carte, clique sur ta ville.")}
<div class="mapbox"><div class="fr-map reveal">{fr_map("")}</div><div class="campus-list reveal" style="--d:1">{cl}</div></div></div></section>'''

    # actus
    n = NEWS[:5]
    big = n[0]
    items = f'<a class="news-item big reveal" href="actualites.html"><time>{d_fr(big[0], True)}</time><span class="cat">{esc(big[2])}</span><h3>{esc(big[1])}</h3></a>'
    for i, (dt, t, cat) in enumerate(n[1:]):
        items += f'<a class="news-item reveal" style="--d:{i+1}" href="actualites.html"><time>{d_fr(dt, True)}</time><span class="cat">{esc(cat)}</span><h3>{esc(t)}</h3></a>'
    b += f'<section class="sec"><div class="wrap">{sec_head("Actualités", "Ce qui se passe dans les campus.")}<div class="news">{items}</div><p style="margin-top:32px"><a class="link-ar" href="actualites.html">Toutes les actualités <span>→</span></a></p></div></section>'

    # confiance
    part = ["Cheops Technology", "SFR Business", "Autodesk", "Dassault Systèmes", "Blackmagic Design", "Unreal Engine", "Graphisoft", "La Banque Postale", "CGI", "Webedia", "Trimble", "Hugging Face", "Formica"]
    b += f'''<section class="sec tight alt"><div class="wrap"><div class="split"><div class="reveal"><span class="eyebrow">Réseau</span><h2>+ de 5 000 entreprises partenaires, près de 10 000 alumni.</h2>
<p class="lead">Des intervenants en activité, des studios, des agences, des éditeurs : ils entrent dans les projets de l'école et recrutent ensuite.</p><a class="link-ar" href="entreprises.html">Espace entreprises <span>→</span></a></div>
<div class="pill-list reveal" style="--d:1">{"".join(f"<li>{p}</li>" for p in part)}</div></div></div></section>'''

    b += f'<section class="sec" style="padding-top:40px"><div class="wrap">{cta_band("")}</div></section>'
    page("index.html", "L'école des transformations digitales", b, "Concept de refonte du site d'une école du numérique : formations, campus, alternance, admission.", "home")


def build_catalogue():
    cards = "".join(prog_card(p, "../", i) for i, p in enumerate(P_SORTED))
    fams = "".join(f'<label class="opt"><input type="checkbox" name="fam" value="{f["slug"]}"> {esc(f["nom"])}<small>{len([p for p in P if p["fam"]==f["slug"]])}</small></label>' for f in FAMILLES)
    nivs = "".join(f'<label class="opt"><input type="checkbox" name="niveau" value="{n}"> {n}<small>{len([p for p in P if p["typ"]==n])}</small></label>' for n in ["BTS", "Bachelor", "Mastère"])
    copts = '<option value="">Tous les campus</option>' + "".join(f'<option value="{c[0]}">{esc(c[2])}</option>' for c in CAMPUS)
    body = page_hero("../", [("Accueil", "index.html"), ("Formations", None)], "Toutes nos formations",
                     f"{len(P)} programmes en BTS, Bachelor et Mastère. Filtre par niveau, domaine ou campus.")
    body += f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="cat-layout" id="catalogue">
<aside class="filters"><div><h4>Niveau</h4>{nivs}</div><div><h4>Domaine</h4>{fams}</div>
<div class="field"><label for="campus">Campus</label><select id="campus">{copts}</select></div>
<label class="opt"><input type="checkbox" id="online"> Disponible en ligne (Connect)</label>
<button id="reset" class="btn btn-ghost btn-sm" type="button">Réinitialiser</button></aside>
<div><div class="result-bar"><div class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<input id="q" type="search" placeholder="Rechercher : IA, cyber, UX, BIM…" aria-label="Rechercher une formation"></div><strong id="count"></strong></div>
<div class="grid g2">{cards}</div><p id="empty" hidden class="callout">Aucune formation ne correspond à ces filtres. Essaie d'élargir ta recherche.</p></div></div></div></section>'''
    page("formations/index.html", "Toutes les formations", body, "Catalogue des BTS, Bachelors et Mastères.", "formations", "Formations")


def build_formations():
    for p in P:
        f, pl = p["fam_obj"], p["pole_obj"]; base = "../"
        chips = (f'<div class="meta-chips"><span class="mchip"><b>{p["typ"]}</b></span><span class="mchip">Durée <b>{p["duree"]}</b></span><span class="mchip">Entrée <b>{esc(p["entree"])}</b></span>'
                 f'{f"<span class=\"mchip\"><b>{p["rncp"]}</b></span>" if p["rncp"] else ""}<span class="mchip">Rentrée <b>sept. 2027</b></span></div>')
        hero = page_hero(base, [("Accueil", "index.html"), ("Formations", "formations/index.html"), (f["nom"], fam_url(f)), (p["short"], None)], esc(p["titre"]), esc(p["accroche"]), chips, pl["color"])
        if p["skills"]:
            sk = "".join(f"<li>{esc(s)}</li>" for s in p["skills"])
            skills = f'<h2 class="reveal">Ce que tu vas apprendre</h2><ul class="skills reveal">{sk}</ul>'
        else:
            skills = (f'<h2 class="reveal">Un tremplin vers le Bachelor</h2><p class="lead reveal">Ce BTS se prépare en deux ans après le bac. Le programme détaillé et le calendrier sont communiqués par le campus choisi : '
                      f'<a class="link-ar" href="{base}contact.html">demande la brochure <span>→</span></a></p>')
        proj_block = ""
        if p["slug"] in PROJ_BY_PROG:
            pj = PROJ_BY_SLUG[PROJ_BY_PROG[p["slug"]]]
            proj_block = (f'<h2 class="reveal" style="margin-top:56px">Un exemple de projet étudiant</h2>'
                          f'<a class="proj-feature reveal" href="{base}projets/{pj["slug"]}.html"><div><span class="badge b-Bachelor">Projet étudiant</span>'
                          f'<h3>{esc(pj["titre"])}</h3><p>{esc(pj["accroche"])}</p><div class="tagrow">' + "".join(f"<span>{esc(t)}</span>" for t in pj["tags"]) +
                          f'</div><span class="link-ar">Découvrir le projet <span>→</span></span></div><div class="pf-vis pf-{pj["slug"]}" aria-hidden="true"></div></a>')
        sib = sorted([x for x in P if x["fam"] == p["fam"]], key=lambda x: (LEVEL_ORDER[x["typ"]], x["titre"]))
        steps = ""
        for lvl, lab in [("BTS", "Bac+2"), ("Bachelor", "Bac+3"), ("Mastère", "Bac+5")]:
            cur = p["typ"] == lvl
            names = "<br>".join(esc(x["short"]) for x in sib if x["typ"] == lvl) or "—"
            steps += f'<div class="step{" on" if cur else ""}"><small>{lvl} · {lab}</small>{names if not cur else esc(p["short"])}</div>'
        path = f'<h2 class="reveal" style="margin-top:56px">Où ça mène dans ce domaine</h2><div class="path reveal">{steps}</div>'
        camp = f'<h2 class="reveal" style="margin-top:56px">Où l’étudier</h2><div class="campus-chips reveal">{campus_names(p, base)}</div>'
        if not p["campus"] and p["online"]:
            camp = f'<h2 class="reveal" style="margin-top:56px">Où l’étudier</h2><p class="lead reveal">Cette formation est proposée uniquement sur <a class="link-ar" href="{base}campus/connect.html">Connect <span>→</span></a>, le campus 100 % en ligne d’Ynov.</p>'
        if p["typ"] == "Mastère": alt_row = "Dès le Mastère 1"
        elif p["typ"] == "Bachelor": alt_row = "Dès le Bachelor 2 ou 3 (selon formation)"
        else: alt_row = "Selon le campus"
        facts = (f'<li><span>Niveau</span><span>{p["typ"]}</span></li><li><span>Durée</span><span>{p["duree"]}</span></li><li><span>Entrée</span><span>{esc(p["entree"])}</span></li>'
                 f'<li><span>Rentrée</span><span>Septembre 2027</span></li><li><span>Alternance</span><span>{alt_row}</span></li>'
                 f'{f"<li><span>Titre</span><span>{p["rncp"]}</span></li>" if p["rncp"] else ""}<li><span>Campus</span><span>{len(p["campus"])+(1 if p["online"] else 0)}</span></li>')
        rel = "".join(prog_card(x, base, i) for i, x in enumerate([x for x in sib if x is not p][:4]))
        rel_sec = f'<section class="sec alt"><div class="wrap">{sec_head("Dans le même domaine", esc(f["nom"]))}<div class="grid g2">{rel}</div></div></section>' if rel else ""
        body = hero + f'''<section class="sec" style="padding-top:30px"><div class="wrap detail"><div>{skills}{proj_block}{path}{camp}</div>
<aside class="sticky"><div class="side-card reveal"><ul class="facts">{facts}</ul><a class="btn btn-accent" style="width:100%;justify-content:center" href="{base}admission.html#candidater">Candidater {arrow()}</a>
<a class="btn btn-ghost" style="width:100%;justify-content:center;margin-top:10px" href="{base}contact.html">Recevoir la brochure</a></div></aside></div></section>{rel_sec}
<section class="sec" style="padding:40px 0 90px"><div class="wrap">{cta_band(base)}</div></section>'''
        page(prog_url(p), p["titre"], body, p["accroche"], "formations", "Formations")


def build_domaines_poles():
    for i, f in enumerate(FAMILLES):
        pl = POLE_BY_SLUG[f["pole"]]; base = "../"
        sub = ""
        for lvl, lab in [("BTS", "BTS — Bac+2"), ("Bachelor", "Bachelors — Bac+3"), ("Mastère", "Mastères — Bac+5")]:
            ps = [p for p in P if p["fam"] == f["slug"] and p["typ"] == lvl]
            if ps: sub += f'<h2 class="reveal" style="font-size:1.7rem;margin-top:44px">{lab}</h2><div class="grid g2">' + "".join(prog_card(p, base, k) for k, p in enumerate(ps)) + "</div>"
        mets = "".join(f"<li>{esc(m)}</li>" for m in pl["metiers"])
        body = page_hero(base, [("Accueil", "index.html"), ("Formations", "formations/index.html"), (f["nom"], None)], esc(f["nom"]), esc(f["texte"]), "", pl["color"])
        body += f'''<section class="sec" style="padding-top:20px"><div class="wrap">{sub}
<h2 class="reveal" style="margin-top:72px;font-size:1.7rem">Métiers du pôle « {esc(pl["nom"])} »</h2><ul class="pill-list reveal">{mets}</ul>
<p class="reveal" style="margin-top:28px"><a class="link-ar" href="{base}{pole_url(pl)}">Découvrir le pôle <span>→</span></a></p></div></section>
<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base)}</div></section>'''
        page(fam_url(f), f["nom"], body, f["accroche"], "formations", "Domaines")
    for pl in POLES:
        base = "../"
        fams = "".join(f'<a class="card fam-card reveal" style="--d:{k}" href="{base}{fam_url(f)}">{motif(FAM_ORDER[f["slug"]], pl["color"])}<h3 style="margin-top:36px">{esc(f["nom"])}</h3><p>{esc(f["accroche"])}</p>'
                       f'<span class="count">{len([p for p in P if p["fam"]==f["slug"]])} formations</span></a>' for k, f in enumerate([f for f in FAMILLES if f["pole"] == pl["slug"]]))
        mets = "".join(f"<li>{esc(m)}</li>" for m in pl["metiers"])
        body = page_hero(base, [("Accueil", "index.html"), ("Formations", "formations/index.html"), (pl["nom"], None)], esc(pl["nom"]), esc(pl["intro"]), f'<p class="reveal" style="margin-top:18px;font:700 14px var(--f-body);letter-spacing:.08em;text-transform:uppercase;color:var(--ink)"><i class="dotc" style="background:{pl["color"]}"></i>{pl["verbes"]}</p>', pl["color"])
        body += f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="prose reveal"><p class="lead">{esc(pl["corps"])}</p></div>
<h2 class="reveal" style="margin-top:56px">Les domaines de formation</h2><div class="grid g3">{fams}</div>
<h2 class="reveal" style="margin-top:72px">Tu deviendras…</h2><ul class="pill-list reveal">{mets}</ul></div></section>
<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base)}</div></section>'''
        page(pole_url(pl), pl["nom"], body, pl["intro"], "formations", "Pôles")


def build_campus():
    # index
    cards = ""
    for k, c in enumerate(CAMPUS):
        n = len([p for p in P if c[0] in p["campus"]])
        nxt = sorted([j for j in JPO if j[0] == c[0]], key=lambda x: x[1])
        j = f'<span class="count">Prochaine JPO : {d_fr(nxt[0][1])}</span>' if nxt else ""
        cards += (f'<a class="card fam-card reveal" style="--d:{k%3}" href="../{campus_url(c)}">{motif(k,"#4A8CFF" if k%3==0 else "#FF84EF" if k%3==1 else "#5AFFB6")}<span class="num">{k+1:02d}</span>'
                  f'<h3 style="margin-top:36px">{esc(c[2])}</h3><p style="margin-bottom:12px">{esc(c[3])} · {n} formations</p>{j}</a>')
    cards += (f'<a class="card fam-card reveal" href="connect.html" style="background:var(--ink);color:#fff;border-color:var(--ink)">{motif(3, "#EEFF57")}<span class="num" style="color:#A5ADA8">14</span>'
              f'<h3 style="margin-top:36px">Connect</h3><p style="color:#C3CAC5;margin-bottom:12px">Le campus 100 % en ligne, avec alternance.</p><span class="count">{len([p for p in P if p["online"]])} formations</span></a>')
    body = page_hero("../", [("Accueil", "index.html"), ("Campus", None)], "14 campus, partout en France", "Des campus modernes et inspirants au cœur des grandes villes — et un campus 100 % en ligne.")
    body += f'''<section class="sec" style="padding-top:10px"><div class="wrap"><div class="mapbox" style="margin-bottom:64px"><div class="fr-map reveal">{fr_map("../")}</div>
<div class="reveal" style="--d:1"><span class="eyebrow">Des lieux pour apprendre</span><h2>Un campus, ce n’est pas un endroit où tu passes.</h2><p class="lead">C’est là où il se passe quelque chose : cours, travail individuel, projets collectifs, présentations, événements, plateaux TV, studios son, salles gaming, labos informatiques.</p>
<a class="link-ar" href="../vie-de-campus.html">La vie de campus <span>→</span></a></div></div>
<div class="grid g3">{cards}</div></div></section>'''
    page("campus/index.html", "Nos campus", body, "Les 13 campus physiques et le campus en ligne.", "campus", "Campus")

    for k, c in enumerate(CAMPUS):
        base = "../"
        progs = [p for p in P_SORTED if c[0] in p["campus"]]
        by_f = {}
        for p in progs: by_f.setdefault(p["fam"], []).append(p)
        blocks = ""
        for f in FAMILLES:
            if f["slug"] in by_f:
                col = POLE_BY_SLUG[f["pole"]]["color"]
                blocks += (f'<h3 class="reveal" style="margin:40px 0 14px;display:flex;align-items:center;gap:10px"><i style="width:10px;height:10px;border-radius:50%;background:{col};display:inline-block"></i>École {esc(f["nom"])}</h3>'
                           f'<div class="grid g2">' + "".join(prog_card(p, base, i) for i, p in enumerate(by_f[f["slug"]])) + "</div>")
        jp = sorted([j for j in JPO if j[0] == c[0]], key=lambda x: x[1])
        jpo_html = "".join(f'<div class="jpo reveal"><div class="date"><b>{int(j[1][8:])}</b><span>{MOIS[int(j[1][5:7])-1]}</span></div><div class="info"><b>Journée portes ouvertes — {esc(c[2])}</b><span>{j[2]} · {d_fr(j[1], True)}</span></div>'
                           f'<a class="btn btn-ghost btn-sm" href="{base}contact.html">Réserver {arrow()}</a></div>' for j in jp)
        jpo_sec = f'<h2 class="reveal" style="margin-top:72px">Viens nous rencontrer</h2><div class="grid" style="gap:12px">{jpo_html}</div><p class="note" style="margin-top:12px">Dates relevées le 6 novembre 2026 ; à confirmer auprès du campus.</p>' if jp else ""
        extra = ""
        if c[0] == "SOP":
            team = "".join(f'<div class="card hov reveal"><span class="note" style="text-transform:uppercase;letter-spacing:.08em;font-weight:600">{r}</span><h3 style="margin:6px 0 0">{esc(n)}</h3></div>' for r, n in SOPHIA_EQUIPE)
            yd = "".join(f"<li>{esc(x)}</li>" for x in SOPHIA_YDAYS)
            extra = (f'<h2 class="reveal" style="margin-top:72px">L’équipe du campus</h2><div class="grid g4">{team}</div>'
                     f'<h2 class="reveal" style="margin-top:72px">Projets Ydays des étudiants de Sophia</h2><p class="lead reveal">Chaque année, les étudiants montent des projets inter-formations. Quelques-uns des projets présentés par le campus :</p><ul class="pill-list reveal">{yd}</ul>')
        if c[0] == "MTP":
            extra = '<h2 class="reveal" style="margin-top:72px">À savoir</h2><div class="callout reveal">Campus livré en août 2024 : 6 600 m² dans la ZAC Cambacérès, un amphithéâtre de 200 places, 2 studios de tournage, 3 box de post-production et des salles équipées pour la modélisation 3D.</div>'
        if c[0] == "LIL":
            extra = '<h2 class="reveal" style="margin-top:72px">À savoir</h2><div class="callout reveal">Ouvert en 2022, le campus s’est agrandi en 2024 de 3 000 m² dans l’ancien siège des 3 Suisses à Croix : 12 salles de cours, un studio de création 3D, deux studios de tournage et une cyberwar room.</div>'
        if c[0] in ("VDE", "ROU", "STR"):
            extra = '<div class="callout reveal" style="margin-top:56px">Campus ouvert en 2024.</div>'
        chips = f'<div class="meta-chips"><span class="mchip">📍 <b>{esc(c[3])}</b></span><span class="mchip"><b>{len(progs)}</b> formations</span><span class="mchip">Alternance dès le Bachelor 2/3 &amp; au Mastère</span></div>'
        body = page_hero(base, [("Accueil", "index.html"), ("Campus", "campus/index.html"), (c[2], None)], f"Ynov {esc(c[2])}",
                         f"Un campus au cœur de {esc(c[3].split(' (')[0])} : {len(progs)} formations du BTS au Mastère, des projets réels et un réseau d’entreprises partenaires.", chips, "#859CFF")
        body += f'<section class="sec" style="padding-top:10px"><div class="wrap"><h2 class="reveal">Les formations à {esc(c[2])}</h2>{blocks}{jpo_sec}{extra}</div></section><section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base, "Rejoins le campus de " + esc(c[2]))}</div></section>'
        page(campus_url(c), f"Campus {c[2]}", body, f"Ynov {c[2]} : formations, portes ouvertes, équipe.", "campus", "Campus")

    # Connect
    on = [p for p in P_SORTED if p["online"]]
    only = [p for p in on if not p["campus"]]
    body = page_hero("../", [("Accueil", "index.html"), ("Campus", "campus/index.html"), ("Connect", None)], "Connect, le campus 100 % en ligne",
                     "Étudier chez Ynov à distance, avec alternance. Depuis la rentrée 2025, un campus virtuel immersif et gamifié.", f'<div class="meta-chips"><span class="mchip"><b>{len(on)}</b> formations en ligne</span><span class="mchip"><b>{len(only)}</b> exclusives à Connect</span></div>', "#EEFF57")
    body += f'<section class="sec" style="padding-top:10px"><div class="wrap"><h2 class="reveal">Exclusives à Connect</h2><div class="grid g2">{"".join(prog_card(p, "../", i) for i, p in enumerate(only))}</div>' \
            f'<h2 class="reveal" style="margin-top:64px">Aussi disponibles en ligne</h2><div class="grid g2">{"".join(prog_card(p, "../", i) for i, p in enumerate([x for x in on if x["campus"]]))}</div></div></section>' \
            f'<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band("../")}</div></section>'
    page("campus/connect.html", "Connect – campus en ligne", body, "Le campus 100 % en ligne d'Ynov.", "campus", "Campus")


def prose_page(path, title, lead, crumbs, body_html, current="about", group="Ynov", color="#859CFF", band=True):
    base = "../" * path.count("/")
    body = page_hero(base, [("Accueil", "index.html")] + crumbs, title, lead, "", color) + body_html
    if band: body += f'<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base)}</div></section>'
    page(path, title, body, lead, current, group)


def build_static():
    # À propos
    tl = "".join(f'<div class="tl reveal"><b>{y}</b><p>{esc(t)}</p></div>' for y, t in HISTOIRE)
    piliers = "".join(f'<div class="card hov reveal" style="--d:{i}"><h3>{esc(t)}</h3><p style="margin:0">{esc(x)}</p></div>' for i, (t, x) in enumerate(PILIERS))
    prose_page("a-propos.html", "Qui sommes-nous ?", "Un acteur de l’enseignement supérieur privé, spécialisé dans la formation aux métiers en transformation.", [("À propos", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="split" style="align-items:start"><div class="reveal"><span class="eyebrow">Notre raison d’être</span><h2>Les expertises prennent toute leur force quand elles se rencontrent.</h2>
<p class="lead">Les technologies évoluent à une vitesse inédite, les métiers se transforment, les disciplines se rapprochent. Ynov cultive une conviction : aucune grande réalisation ne naît d’une compétence isolée, elle naît d’une intelligence collective.</p>
<p>Trois pôles d’excellence, trois manières d’intervenir sur le réel, que l’école ne cherche pas à confondre mais à faire dialoguer. Le monde a besoin d’experts solides, capables aussi d’écouter d’autres langages et de construire avec les autres.</p></div>
<div class="timeline reveal" style="--d:1">{tl}</div></div></div></section>
<section class="sec alt"><div class="wrap">{sec_head("Vision &amp; stratégie", "Une présence nationale, des expertises complémentaires.", "9 000 étudiants, 3 pôles d’excellence, des formations en BTS, Bachelors et Mastères en initial ou en alternance.")}
<div class="grid g2">{piliers}</div></div></section>
<section class="sec"><div class="wrap">{sec_head("En chiffres", "Ynov aujourd’hui.")}<div class="stats-strip reveal" style="margin:0">{"".join(f"<div class=\"stat\"><div class=\"n\">{n}</div><div class=\"l\">{l}</div><div class=\"s\">{s}</div></div>" for n, l, s in STATS)}</div></div></section>''')

    # Pédagogie
    ped = "".join(f'<div class="card hov reveal" style="--d:{i}"><span class="badge b-Bachelor" style="align-self:flex-start;margin-bottom:14px">{d}</span><h3>{t}</h3><p style="margin:0">{esc(x)}</p></div>' for i, (t, d, x) in enumerate(PEDAGOGIE))
    piliers = "".join(f'<div class="card hov reveal" style="--d:{i}"><span class="num" style="font:800 2.4rem var(--f-head);color:var(--accent)">{i+1}</span><h3>{esc(t)}</h3><p style="margin:0">{esc(x)}</p></div>' for i, (t, x) in enumerate(PILIERS))
    prose_page("pedagogie.html", "Apprendre en faisant", "Une pédagogie fondée sur l’expérience, la pratique et les projets, dès le premier jour.", [("Pédagogie", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="quote reveal">« Une idée se teste, se confronte au réel, se présente, s’améliore. Recommencer, c’est déjà avancer. »</div>
{sec_head("Quatre dispositifs", "Comment ça se passe concrètement.")}<div class="grid g4">{ped}</div></div></section>
<section class="sec"><div class="wrap"><div class="callout reveal" style="display:flex;gap:20px;justify-content:space-between;align-items:center;flex-wrap:wrap"><span><b>Exemple d’Ymmersion :</b> le Projet RED « Mr Ybot », un jeu en terminal en Go, fait en équipe de 3 en trois semaines.</span><a class="btn btn-accent btn-sm" href="projets/mr-ybot.html">Voir le projet {arrow()}</a></div></div></section>
<section class="sec alt"><div class="wrap">{sec_head("Les quatre piliers", "Ce qui structure chaque parcours.")}<div class="grid g4">{piliers}</div></div></section>
<section class="sec"><div class="wrap split"><div class="reveal"><span class="eyebrow">Partenariats pédagogiques</span><h2>Des outils et des plateformes de l’industrie.</h2>
<p class="lead">En intelligence artificielle, le partenariat avec Hugging Face donne accès à un compte PRO, à du GPU et à des crédits de calcul. En 3D, en BIM ou en audiovisuel, les étudiants travaillent sur les logiciels des professionnels.</p></div>
<div class="reveal" style="--d:1"><div class="callout">Les Ydays ont lieu chaque mercredi (selon le campus) : tu rejoins une équipe autour d’une idée qui te motive, quelle que soit ta formation.</div></div></div></section>''', "pedagogie")

    # Vie de campus
    prose_page("vie-de-campus.html", "La vie de campus", "Un campus, c’est là où il se passe quelque chose.", [("Vie de campus", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3">
<div class="card hov reveal"><div class="ic" style="background:var(--accent-soft)">🎬</div><h3>Des équipements pour créer</h3><p style="margin:0">Plateaux TV, studios son, salles gaming, labos informatiques : selon les campus et les formations.</p></div>
<div class="card hov reveal" style="--d:1"><div class="ic" style="background:var(--coral-soft)">🎉</div><h3>Des événements toute l’année</h3><p style="margin:0">Halloween Creators Festival, concours d’éloquence, concours national d’architecture d’intérieur, e-sport league, Paris Games Week.</p></div>
<div class="card hov reveal" style="--d:2"><div class="ic" style="background:var(--mint-soft)">🤝</div><h3>Une vie associative active</h3><p style="margin:0">BDE, BDS, tournois sportifs, soirées, week-ends : les étudiants font vivre le campus.</p></div></div>
<h2 class="reveal" style="margin-top:80px">Concours national d’architecture d’intérieur</h2>
<p class="lead reveal" style="max-width:760px">Organisé avec Formica® : concevoir une chambre d’hôtel 4 étoiles de 20 m². Réservé aux lycéens de Terminale et aux étudiants de 3e année de Bachelor et de Mastère, avec une année de scolarité offerte pour les lauréats lycéens.</p>
<h2 class="reveal" style="margin-top:56px">Ystart, l’incubateur étudiant</h2><p class="lead reveal" style="max-width:760px">Pour passer d’une idée de projet à une entreprise, pendant tes études. <a class="link-ar" href="ystart.html">En savoir plus <span>→</span></a></p></div></section>''', "about")

    # Alternance
    p_ent = "".join(f"<li><b>{esc(k)}</b> — {esc(', '.join(v))}</li>" for k, v in PARTENAIRES.items())
    prose_page("alternance.html", "L’alternance, la clé pour réussir", "Pratique en entreprise et études en parallèle : 2 à 3 années d’expérience professionnelle au terme de tes études.", [("Alternance", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3">
<div class="card hov reveal"><h3>Pour les étudiants</h3><p>Compétences pratiques, familiarisation avec le monde du travail, souvent un emploi à la clé. Les équipes de chaque campus t’aident à trouver ton entreprise.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Pour les entreprises</h3><p>Recruter des jeunes qui suivent des programmes à la pointe, de l’alternance du Bachelor 2 au Mastère, sur toutes les formations.</p><a class="link-ar" href="entreprises.html">Espace entreprises <span>→</span></a></div>
<div class="card hov reveal" style="--d:2"><h3>Un financement assuré</h3><p>Tu es salarié à part entière, et les frais de formation sont pris en charge par l’entreprise ou son OPCO.</p></div></div>
<h2 class="reveal" style="margin-top:80px">Deux contrats possibles</h2>
<table class="tbl reveal"><thead><tr><th></th><th>Contrat d’apprentissage</th><th>Contrat de professionnalisation</th></tr></thead><tbody>
<tr><td><b>Âge</b></td><td>16 à 29 ans (sauf dérogation)</td><td>16 à 25 ans, et plus sous conditions</td></tr>
<tr><td><b>Durée</b></td><td>6 mois à 3 ans (si durée limitée)</td><td>CDD de 6 à 12 mois minimum</td></tr>
<tr><td><b>Contrat</b></td><td>CDD ou CDI</td><td>CDD ou CDI</td></tr>
<tr><td><b>Rémunération</b></td><td>27 % à 100 % du Smic</td><td>55 % à 100 % du Smic</td></tr></tbody></table>
<p class="note" style="margin-top:10px">Selon l’âge et le niveau d’études, ou du salaire minimum conventionnel si plus favorable.</p>
<div class="split" style="margin-top:80px"><div class="reveal"><h2>Quel rythme ?</h2><p class="lead">1 semaine d’école pour 2 en entreprise, ou 2 jours d’école pour 3 en entreprise, selon la formation. Près de 70 % du temps en entreprise.</p></div>
<div class="rhythm reveal" style="--d:1"><div class="row"><div class="ent" style="flex:2">Entreprise · 2 sem.</div><div class="eco" style="flex:1">École · 1 sem.</div></div><div class="row"><div class="ent" style="flex:3">Entreprise · 3 j</div><div class="eco" style="flex:2">École · 2 j</div></div></div></div>
<h2 class="reveal" style="margin-top:80px">Des partenaires dans chaque domaine</h2><ul class="checks reveal">{p_ent}</ul></div></section>''', "alternance")

    # Admission
    steps = "".join(f'<div class="step-card reveal" style="--d:{i}"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for i, (t, x) in enumerate(ADMISSION_STEPS))
    fopts = "".join(f'<option>{esc(p["titre"])}</option>' for p in P_SORTED)
    copts = "".join(f'<option>{esc(c[2])}</option>' for c in CAMPUS) + "<option>Connect (en ligne)</option>"
    prose_page("admission.html", "Rejoindre Ynov", "Un processus d’admission clair et rapide. Inscriptions ouvertes depuis le 1er octobre 2026 pour la rentrée 2027-2028.", [("Admission", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3">
<div class="card hov reveal"><span class="badge b-BTS" style="align-self:flex-start;margin-bottom:12px">Post-bac</span><h3>Bachelor 1 · BTS</h3><p style="margin:0">Pour les lycéens de Terminale et les bacheliers. On cherche avant tout de la motivation et un vrai projet.</p></div>
<div class="card hov reveal" style="--d:1"><span class="badge b-Bachelor" style="align-self:flex-start;margin-bottom:12px">Admission parallèle</span><h3>Bachelor 3</h3><p style="margin:0">Pour les titulaires d’un Bac+2 : tu valides un titre de niveau 6 et prépares l’alternance.</p></div>
<div class="card hov reveal" style="--d:2"><span class="badge b-Mastère" style="align-self:flex-start;margin-bottom:12px">Admission parallèle</span><h3>Mastère 1</h3><p style="margin:0">Pour les titulaires d’un Bac+3 : tu deviens expert de ton domaine avec un rythme d’alternance privilégié.</p></div></div>
<h2 class="reveal" style="margin-top:80px">En 4 étapes</h2><div class="steps">{steps}</div>
<div class="split" style="margin-top:80px;align-items:start"><div class="reveal"><span class="eyebrow">Le rendez-vous</span><h2>Une heure d’échange, seul ou avec tes parents.</h2>
<ul class="checks"><li>Accueil et visite du campus, rencontre avec des étudiants</li><li>Présentation de l’école, de ses valeurs et de la pédagogie</li><li>Tu racontes qui tu es, ton parcours, tes motivations</li><li>Infos sur le financement et conseils de logement</li></ul>
<p class="note">Le dossier est validé sous réserve d’un effectif minimal ou maximal ; si le minimum n’est pas atteint, un transfert sur un autre campus peut être proposé.</p></div>
<form class="demo side-card reveal" id="candidater" style="--d:1"><h3>Candidater</h3><p class="note">Formulaire de démonstration : aucune donnée n’est envoyée ni enregistrée.</p>
<div class="field" style="margin-bottom:14px"><label for="a-n">Prénom et nom</label><input id="a-n" required placeholder="Alex Martin"></div>
<div class="field" style="margin-bottom:14px"><label for="a-f">Formation visée</label><select id="a-f">{fopts}</select></div>
<div class="field" style="margin-bottom:18px"><label for="a-c">Campus</label><select id="a-c">{copts}</select></div>
<button class="btn btn-accent" type="submit" style="width:100%;justify-content:center">Envoyer ma candidature {arrow()}</button>
<div class="ok callout">Merci ! Dans la vraie vie, un conseiller te rappellerait sous 48 h.</div></form></div></div></section>''', "admission", band=False)

    # Événements
    by = sorted(JPO, key=lambda j: (j[1], j[0]))
    copts = '<option value="">Tous les campus</option>' + "".join(f'<option value="{c[0]}">{esc(c[2])}</option>' for c in CAMPUS)
    rows = "".join(f'<div class="jpo reveal" data-c="{j[0]}"><div class="date"><b>{int(j[1][8:])}</b><span>{MOIS[int(j[1][5:7])-1]}</span></div><div class="info"><b>Journée portes ouvertes — {esc(CAMPUS_BY_CODE[j[0]][2])}</b><span>{j[2]} · {d_fr(j[1], True)}</span></div>'
                   f'<a class="btn btn-ghost btn-sm" href="contact.html">Réserver {arrow()}</a></div>' for j in by)
    js = '<script>(function(){var s=document.getElementById("evc"),r=[].slice.call(document.querySelectorAll(".jpo[data-c]"));s.addEventListener("change",function(){r.forEach(function(x){x.hidden=s.value&&x.dataset.c!==s.value})})})()</script>'
    prose_page("evenements.html", "Portes ouvertes & événements", "Viens visiter un campus, rencontrer les équipes et les étudiants.", [("Événements", None)],
               f'''<section class="sec" style="padding-top:10px"><div class="wrap"><div class="field" style="max-width:360px;margin-bottom:28px"><label for="evc">Filtrer par campus</label><select id="evc">{copts}</select></div>
<div class="grid" style="gap:12px">{rows}</div><p class="note" style="margin-top:14px">Dates relevées le 6 novembre 2026, à confirmer auprès de chaque campus. D’autres dates existent en décembre.</p>
<div class="callout reveal" style="margin-top:40px"><b>Stage découverte</b> — Ynov Lyon propose 2 jours pour tester ta filière.</div></div></section>{js}''', "campus", band=False)

    # Actualités
    news = "".join(f'<a class="news-item reveal" href="#"><time>{d_fr(d, True)}</time><span class="cat">{esc(c)}</span><h3>{esc(t)}</h3></a>' for d, t, c in NEWS)
    prose_page("actualites.html", "Actualités", "Ce qui se passe dans les campus, les projets étudiants et les partenariats.", [("Actualités", None)],
               f'<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g3">{news}</div><p class="note" style="margin-top:20px">Titres relevés sur ynov.com ; les articles complets restent sur le site officiel.</p></div></section>', "about", band=False)

    # Métiers
    mx = max(m[2] for m in METIERS)
    rows = "".join(f'<tr><td><b>{esc(m[1])}</b><br><span class="note">{esc(m[0])}</span></td><td>{m[3]}</td><td><div class="salary"><i style="--w:{m[2]/mx*100:.0f}%"></i><b>{m[2]:,}</b> €</div></td></tr>'.replace(",", " ") for m in sorted(METIERS, key=lambda x: -x[2]))
    pol = "".join(f'<div class="card hov reveal" style="--d:{i}"><h3><i class="dotc" style="background:{pl["color"]}"></i>{esc(pl["nom"])}</h3><ul class="pill-list" style="padding:0;margin:0">' + "".join(f"<li>{esc(m)}</li>" for m in pl["metiers"]) + "</ul></div>" for i, pl in enumerate(POLES))
    prose_page("metiers.html", "Guide des métiers", "Les débouchés vers lesquels mènent les formations, avec des salaires moyens annuels indicatifs.", [("Métiers", None)],
               f'''<section class="sec" style="padding-top:10px"><div class="wrap"><table class="tbl reveal"><thead><tr><th>Métier</th><th>Niveau d’études</th><th>Salaire moyen annuel</th></tr></thead><tbody>{rows}</tbody></table>
<h2 class="reveal" style="margin-top:80px">Tu deviendras…</h2><div class="grid g3">{pol}</div></div></section>''', "about")

    # Alumni
    prose_page("alumni.html", "Le réseau Alumni", "Près de 10 000 diplômés : une communauté pour se retrouver, se recommander et transmettre.", [("Alumni", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3">
<div class="card hov reveal"><h3>Pour les alumni</h3><p style="margin:0">Retrouver ses camarades de promo, participer à des événements de networking sur son ancien campus, devenir membre de jury, intervenant ou mentor.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Pour les étudiants</h3><p style="margin:0">Un réseau d’anciens qui peut ouvrir la porte de l’alternance ou du stage de tes rêves, et répondre à tes questions de professionnalisation.</p></div>
<div class="card hov reveal" style="--d:2"><h3>Pour les équipes</h3><p style="margin:0">Un relais précieux pour garder les formations en phase avec les métiers.</p></div></div>
<p class="reveal" style="margin-top:40px"><a class="btn btn-primary" href="contact.html">Rejoindre la communauté Alumni</a></p></div></section>''', band=False)

    # Entreprises
    parts = "".join(f'<div class="card hov reveal"><h3>{esc(k)}</h3><ul class="pill-list" style="padding:0;margin:0">' + "".join(f"<li>{esc(x)}</li>" for x in v) + "</ul></div>" for k, v in PARTENAIRES.items())
    prose_page("entreprises.html", "Recruter nos talents", "Alternants, stagiaires, intervenants, projets : devenez partenaire des formations de demain.", [("Entreprises", None)],
               f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="stats-strip reveal" style="margin:0 0 72px;grid-template-columns:repeat(4,1fr)">
<div class="stat"><div class="n">13</div><div class="l">campus + Connect</div></div><div class="stat"><div class="n">9 500</div><div class="l">étudiants</div></div><div class="stat"><div class="n">1 600</div><div class="l">intervenants professionnels</div></div><div class="stat"><div class="n">5 000+</div><div class="l">entreprises partenaires</div></div></div>
<div class="split"><div class="reveal"><h2>Recrutez un alternant</h2><p class="lead">Toutes les formations proposent l’alternance, du Bachelor 2 au Mastère selon les cursus : profils digitaux, informatiques, business ou créatifs.</p><a class="btn btn-primary" href="contact.html">Je recrute {arrow()}</a>
<a class="btn btn-ghost" style="margin-left:8px" href="https://ymatch.ynov.com" rel="noopener">Plateforme Ymatch ↗</a></div>
<div class="reveal" style="--d:1"><h2>Devenez partenaire</h2><p class="lead">Accès à un vivier de talents, contribution à la formation des étudiants, expertise sur des projets concrets, image d’employeur engagé.</p><p class="note">Témoignages d’entreprises partenaires : Cheops Technology, SFR Business.</p></div></div>
<h2 class="reveal" style="margin-top:80px">Ils soutiennent nos filières</h2><div class="grid g2">{parts}</div></div></section>''', band=False)

    # Ystart
    prose_page("ystart.html", "Ystart, l’incubateur étudiant", "Transformer une idée en projet structuré, viable et prêt à se développer.", [("Ystart", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="prose reveal"><p class="lead">Avec Ystart, Ynov accompagne ses étudiants et alumni qui souhaitent entreprendre pendant leurs études. Chaque année, de nombreux projets naissent dans les Ydays ; Ystart leur apporte le cadre et les méthodes pour devenir des entreprises.</p></div>
<div class="grid g4" style="margin-top:40px"><div class="card hov reveal"><h3>Structurer</h3><p style="margin:0">Cadrer son idée et définir un modèle économique.</p></div><div class="card hov reveal" style="--d:1"><h3>Accélérer</h3><p style="margin:0">Développer un produit avec un accompagnement dédié.</p></div>
<div class="card hov reveal" style="--d:2"><h3>Tester</h3><p style="margin:0">Valider le marché avant de se lancer.</p></div><div class="card hov reveal" style="--d:3"><h3>Entreprendre</h3><p style="margin:0">S’inscrire dans une démarche entrepreneuriale concrète.</p></div></div>
<p style="margin-top:36px"><a class="btn btn-primary" href="contact.html">Postuler à l’incubateur</a></p></div></section>''', band=False)

    # Fondation
    prose_page("fondation.html", "Fondation « Briser les codes pour réinventer la Tech »", "Sous l’égide de la Fondation de France, pour une société plus inclusive et équitable dans la tech et l’enseignement supérieur privé.", [("Fondation", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3"><div class="card hov reveal"><h3>Promouvoir la diversité</h3><p style="margin:0">Des parcours, des origines socio-économiques et des genres variés, notamment dans des domaines souvent dominés par un groupe restreint.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Lutter contre la précarité</h3><p style="margin:0">Des bourses spécifiques pour réduire les inégalités d’accès à l’enseignement supérieur privé.</p></div>
<div class="card hov reveal" style="--d:2"><h3>Inclure les femmes dans la tech</h3><p style="margin:0">Encourager les femmes à rejoindre les métiers de l’informatique et de la tech.</p></div></div></div></section>''', band=False)

    # Handicap
    prose_page("handicap.html", "Ynov Hand You", "L’inclusion est une valeur chère à Ynov : l’accessibilité des personnes en situation de handicap est une priorité de chaque campus.", [("Handicap", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g2">
<div class="card hov reveal"><h3>L’accès pour tous aux campus</h3><p style="margin:0">Tous les campus sont conçus ou adaptés pour être accessibles.</p></div>
<div class="card hov reveal" style="--d:1"><h3>L’égalité des opportunités</h3><p style="margin:0">Chaque apprenant doit pouvoir développer l’ensemble des compétences visées par son diplôme.</p></div>
<div class="card hov reveal"><h3>Un confort de travail optimal</h3><p style="margin:0">Adapter l’environnement d’apprentissage, avec un réseau de partenaires, tout en respectant les exigences pédagogiques.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Une équipe à l’écoute</h3><p style="margin:0">Un référent handicap sur chaque campus pour l’intégration, le suivi pédagogique et l’insertion professionnelle.</p></div></div></div></section>''', band=False)

    # Impact
    prose_page("impact.html", "Impact & Sustainability", "Une politique IMPACT pour intégrer des pratiques responsables, sociales et environnementales.", [("Impact", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3"><div class="card hov reveal"><h3>Inclusion</h3><p style="margin:0">L’accès à l’éducation pour tous, avec la politique Ynov Hand You et un référent handicap par campus.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Bien-être &amp; satisfaction</h3><p style="margin:0">Des dispositifs de soutien pour veiller au bien-être et à la santé mentale des étudiants.</p></div>
<div class="card hov reveal" style="--d:2"><h3>Citoyens engagés</h3><p style="margin:0">Former des citoyens responsables, capables de prendre des décisions éclairées en matière de développement durable.</p></div></div></div></section>''', band=False)

    # Parents
    prose_page("parents.html", "Parents : accompagner votre enfant", "Choisir une orientation, c’est commencer à tracer la suite du parcours. Voici des repères clairs.", [("Parents", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g3"><div class="card hov reveal"><h3>Apprendre en faisant</h3><p style="margin:0">Dès les premières années, des projets concrets, des Ydays et des collaborations avec des professionnels.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Des diplômes reconnus</h3><p style="margin:0">Des titres RNCP de niveaux 6 et 7 reconnus par l’État, dont Ynov est certificateur.</p></div>
<div class="card hov reveal" style="--d:2"><h3>Un financement par l’alternance</h3><p style="margin:0">Salaire pour l’étudiant et frais de formation pris en charge par l’entreprise ou son OPCO.</p></div></div>
<p style="margin-top:36px"><a class="btn btn-primary" href="formations/index.html">Découvrir les formations</a> <a class="btn btn-ghost" href="admission.html">Comprendre l’admission</a></p></div></section>''')

    # VAE
    prose_page("vae.html", "Valider ses acquis de l’expérience (VAE)", "Capitalisez sur votre expérience et validez un titre enregistré au RNCP.", [("VAE", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="prose reveal"><p class="lead">La VAE permet à toute personne, quels que soient son âge, sa nationalité, son niveau d’études et son statut, de faire reconnaître son expérience pour obtenir un diplôme, un titre ou un certificat de qualification.</p>
<p>La seule condition : avoir exercé une activité salariée, non salariée ou bénévole en rapport avec la certification visée. La VAE favorise l’évolution professionnelle, l’employabilité et l’engagement dans un parcours de formation continue.</p></div>
<p style="margin-top:28px"><a class="btn btn-primary" href="contact.html">Nous contacter</a></p></div></section>''', band=False)

    # Qualiopi / CFA
    prose_page("qualite.html", "Qualité, CFA & Qualiopi", "Un centre de formation d’apprentis certifié, engagé dans une démarche d’amélioration continue.", [("Qualité", None)],
               '''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="grid g2"><div class="card hov reveal"><h3>Centre de formation des apprentis</h3><p style="margin:0">Ynov Campus est un CFA qui apporte aux apprentis une formation générale et technique complétant celle reçue en entreprise.</p></div>
<div class="card hov reveal" style="--d:1"><h3>Certification Qualiopi</h3><p style="margin:0">Engagé dans la démarche depuis 2020, le groupe est certifié au titre des actions de formation et de l’apprentissage ; Connect l’est aussi.</p></div></div>
<h2 class="reveal" style="margin-top:72px">Taux de réussite (année académique 24/25)</h2>
<table class="tbl reveal"><thead><tr><th>Titre</th><th>Présentés</th><th>Certifiés</th><th>Réussite</th></tr></thead><tbody>
<tr><td><b>Architecte d’intérieur – Designer</b><br><span class="note">RNCP41709 · niveau 7</span></td><td>64 sur 64</td><td>44</td><td>69 %</td></tr>
<tr><td><b>Chef de projet systèmes embarqués</b><br><span class="note">RNCP39766 · niveau 7</span></td><td>28 sur 28</td><td>28</td><td>100 %</td></tr></tbody></table>
<p class="note" style="margin-top:10px">Extrait ; la liste complète des titres est publiée sur le site officiel.</p></div></section>''', band=False)

    # Presse
    pr = "".join(f'<div class="jpo reveal"><div class="date" style="width:84px"><b style="font-size:1.1rem">{d_fr(d) if d else "2026"}</b></div><div class="info"><b>{esc(t)}</b><span>Communiqué de presse</span></div></div>' for d, t in PRESSE)
    prose_page("presse.html", "Espace presse", "Communiqués, dossiers de presse et revue de presse du groupe.", [("Presse", None)],
               f'<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid" style="gap:12px;max-width:900px">{pr}</div></div></section>', band=False)

    # Recrutement
    cities = "".join(f"<li>{c}</li>" for c in ["Aix-en-Provence", "Bordeaux", "Lyon", "Mérignac", "Nantes", "Paris", "Sophia", "Toulouse", "Montpellier", "Lille", "Rennes", "Rouen", "Strasbourg", "Val d’Europe", "Connect"])
    prose_page("recrutement.html", "Nous rejoindre", "Intervenants, équipes pédagogiques, admission, vie de campus : Ynov recrute sur tous ses campus.", [("Recrutement", None)],
               f'<section class="sec" style="padding-top:20px"><div class="wrap"><ul class="pill-list reveal">{cities}</ul><p class="note" style="margin-top:24px">Les offres sont publiées sur le site officiel.</p></div></section>', band=False)

    # FAQ
    acc = "".join(f'<details class="reveal"><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>' for q, a in FAQ)
    prose_page("faq.html", "Questions fréquentes", "Diplômes, contrats, rythme, financement : les réponses essentielles.", [("FAQ", None)],
               f'<section class="sec" style="padding-top:10px"><div class="wrap"><div class="acc" style="max-width:900px">{acc}</div></div></section>')

    # Contact
    copts = "".join(f'<option>{esc(c[2])}</option>' for c in CAMPUS) + "<option>Connect (en ligne)</option>"
    prose_page("contact.html", "Nous contacter", "Choisis le campus qui t’intéresse, ou appelle-nous gratuitement.", [("Contact", None)],
               f'''<section class="sec" style="padding-top:10px"><div class="wrap split" style="align-items:start"><div class="reveal"><h2>Parlons de ton projet.</h2><p class="lead">Appel gratuit depuis un mobile ou un poste fixe :</p>
<p style="font:800 2.4rem var(--f-head);letter-spacing:-.03em"><a href="tel:0800600633">0800 600 633</a></p><p class="note">Les équipes d’admission te répondent sous 48 h.</p></div>
<form class="demo side-card reveal" style="--d:1"><p class="note">Formulaire de démonstration : aucune donnée n’est envoyée ni enregistrée.</p>
<div class="field" style="margin-bottom:14px"><label for="c-n">Nom</label><input id="c-n" placeholder="Alex Martin"></div>
<div class="field" style="margin-bottom:14px"><label for="c-c">Campus</label><select id="c-c">{copts}</select></div>
<div class="field" style="margin-bottom:18px"><label for="c-m">Message</label><textarea id="c-m" placeholder="Je voudrais recevoir la brochure…"></textarea></div>
<button class="btn btn-accent" type="submit" style="width:100%;justify-content:center">Envoyer {arrow()}</button><div class="ok callout">Message reçu (pour de faux, cette fois).</div></form></div></section>''', band=False)

    # Mentions
    prose_page("mentions.html", "Mentions & sources", "Ce site est une maquette de travail.", [("Mentions", None)],
               '''<section class="sec" style="padding-top:10px"><div class="wrap"><div class="prose reveal"><div class="callout">Concept de refonte <b>non officiel</b>, réalisé comme exercice de design et de contenu. Il n’est ni édité, ni validé, ni affilié à Ynov ou à ses campus. Aucun formulaire n’envoie de données.</div>
<h2>Sources</h2><p>Les noms de programmes, durées, niveaux d’entrée, listes de campus, chiffres clés, dates de portes ouvertes et actualités proviennent des pages publiques de ynov.com, relevées le 6 novembre 2026. Les textes ont été reformulés. Les dates et disponibilités par campus sont susceptibles d’avoir changé : le site officiel fait foi.</p>
<h2>Identité visuelle</h2><p>La palette, la typographie et les illustrations géométriques sont propres à ce concept ; le logo et la charte d’Ynov n’ont pas été reproduits.</p></div></div></section>''', band=False)

    # 404
    prose_page("404.html", "Page introuvable", "Cette page n’existe pas — ou plus.", [("404", None)],
               f'<section class="sec" style="padding-top:10px"><div class="wrap"><a class="btn btn-primary" href="index.html">Retour à l’accueil</a> <button class="btn btn-ghost" data-cmdk>Rechercher</button></div></section>', band=False)


def term_lines(lines):
    out = ""
    for i, (cls, txt) in enumerate(lines):
        out += f'<div class="tl-line {cls}" style="--i:{i}">{esc(txt) if txt else "&nbsp;"}</div>'
    return out


def build_projets():
    base = "../"
    # ---------- Mr Ybot
    t = [("", "Enter operator alias: Neo"), ("", ""), ("hd", "=== SELECT AFFILIATION ==="), ("", ""), ("", "[1] Anonymous  // 100 HP"), ("", "[2] LulzSec    // 80 HP"),
         ("", "[3] Lazarus    // 120 HP"), ("", ""), ("", "Choice: 3"), ("ok", "[+] Operator Neo // Lazarus // 60/120 HP"), ("", ""),
         ("hd", "TRAINING NETWORK // COMBAT SIMULATION"), ("in", "[>] Corruption Script injected into Training Malware."), ("in", "[>] Corruption 1/3 // Training Malware HP: 30/40"),
         ("warn", "[!] CRITICAL ATTACK PATTERN DETECTED"), ("ko", "[<] Training Malware attacks Neo for 10 damage.")]
    term = (f'<div class="term reveal" style="--d:1"><div class="term-bar"><i></i><i></i><i></i><span>mr-ybot — go run .</span></div><div class="term-body">{term_lines(t)}<div class="tl-line caret" style="--i:{len(t)}">&gt; _</div></div>'
            f'<p class="term-note">Mise en scène à partir des textes du jeu (alias fictif).</p></div>')
    affs = [("Anonymous", "100 PV", "L’équilibre : un profil polyvalent."), ("LulzSec", "80 PV", "Plus fragile, pour les joueurs qui aiment le risque."), ("Lazarus", "120 PV", "Le plus résistant pour encaisser les attaques critiques.")]
    aff_html = "".join(f'<div class="card hov reveal" style="--d:{i}"><span class="badge b-Mastère" style="align-self:flex-start;margin-bottom:12px">{h}</span><h3>{n}</h3><p style="margin:0">{d}</p></div>' for i, (n, h, d) in enumerate(affs))
    mech = [
        ("Un opérateur, une affiliation", "Alias vérifié (lettres uniquement), choix parmi trois affiliations cyber, avec des points de vie différents. L’opérateur démarre à moitié de ses PV, avec 100 Ethereum, 3 AntiVirus Patch, la compétence Packet Punch et 10 emplacements d’inventaire."),
        ("Combat au tour par tour", "Face à un « Training Malware » (40 PV, attaque 5), le joueur attaque, utilise une compétence ou fouille son inventaire. L’ennemi suit un schéma : toutes les trois tours, une attaque critique inflige des dégâts doublés."),
        ("Objets et compétences", "Le Corruption Script injecte un poison : 3 fois 10 dégâts, un tick par seconde. Un livre de compétence, Exploit Manual, débloque Zero-Day Blast. L’AntiVirus Patch soigne."),
        ("Marchand et forge", "Un marchand vend des objets en Ethereum ; une forge fabrique des équipements à partir de matériaux : Neural Visor (API Key + Security Token), Firewall Jacket (2 Encrypted Data + 1 Firewall Module), Proxy Boots (1 Encrypted Data + 1 Security Token). Un module étend la capacité d’inventaire."),
    ]
    mech_html = "".join(f'<div class="card hov reveal" style="--d:{i%2}"><h3>{t_}</h3><p style="margin:0">{d}</p></div>' for i, (t_, d) in enumerate(mech))
    tree = ('<pre class="tree reveal">Projet-Red-Mr-Ybot/\n├─ main.go\n└─ src/\n   ├─ character/   personnage, inventaire, équipements\n   ├─ combat/      monstres, combats, compétences\n   ├─ economy/     marchand, forge\n   ├─ items/       objets, prix, recettes\n   └─ utils/       menus, dialogues, interface</pre>')
    skills = "".join(f"<li>{x}</li>" for x in ["Programmer en Go : structures, packages, tranches, boucles de jeu", "Concevoir une interface en ligne de commande lisible et immersive",
                                               "Modéliser des règles de jeu : économie, combat, progression", "Organiser un projet en modules et le versionner avec Git à plusieurs"])
    chips = '<div class="meta-chips"><span class="mchip"><b>Projet étudiant</b></span><span class="mchip">Ymmersion · <b>B1</b></span><span class="mchip">Ynov <b>Sophia</b></span><span class="mchip">Langage <b>Go</b></span><span class="mchip">Équipe de <b>3</b></span></div>'
    body = page_hero(base, [("Accueil", "index.html"), ("Projets étudiants", "projets.html"), ("Mr Ybot", None)], "Projet RED — « Mr Ybot »",
                     "Un jeu de rôle en ligne de commande, écrit en Go, dont l’univers emprunte à la cybersécurité : opérateurs, malwares, pare-feu et monnaie en Ethereum.", chips, "#859CFF")
    body += f"""<section class="sec" style="padding-top:20px"><div class="wrap split" style="align-items:start"><div class="reveal"><span class="eyebrow">Le projet</span><h2>Trois semaines pour passer de zéro à un vrai jeu.</h2>
<p class="lead">C’est le projet final de l’Ymmersion, la période d’intégration d’Ynov : une piscine Go, un poste de développement configuré, deux jours de Git, puis un sujet commun, le Projet RED, à traiter en équipe.</p>
<p>L’équipe a gardé les mécaniques demandées par le sujet — personnage, inventaire, marchand, fabrication, combats — et leur a donné un habillage cyber : l’interface, les objets et les ennemis parlent le langage de la sécurité informatique.</p>
<div class="callout"><b>Ma part :</b> le système de combat, les actions, les compétences et les ennemis.</div></div>{term}</div></section>
<section class="sec alt"><div class="wrap">{sec_head("Trois affiliations", "Choisir son camp, c’est choisir sa résistance.", "Chaque affiliation fixe les points de vie maximum de l’opérateur.")}<div class="grid g3">{aff_html}</div></div></section>
<section class="sec"><div class="wrap">{sec_head("Les mécaniques", "Ce qui se passe dans le terminal.")}<div class="grid g2">{mech_html}</div></div></section>
<section class="sec alt"><div class="wrap split" style="align-items:start"><div class="reveal"><span class="eyebrow">Sous le capot</span><h2>Un code organisé en modules.</h2><p class="lead">Chaque domaine du jeu vit dans son propre paquet Go, ce qui permet de se répartir le travail à plusieurs.</p></div>{tree}</div></section>
<section class="sec"><div class="wrap"><div class="split" style="align-items:start"><div class="reveal"><span class="eyebrow">Compétences travaillées</span><h2>Ce que ce projet apprend.</h2></div><ul class="skills reveal" style="--d:1;grid-template-columns:1fr">{skills}</ul></div>
<div class="grid g2" style="margin-top:56px"><a class="card hov reveal" href="{base}formations/bachelor-cybersecurite.html"><h3>Bachelor Cybersécurité</h3><p>Le domaine dont ce projet emprunte l’univers.</p><span class="more">Voir la formation <span>→</span></span></a>
<a class="card hov reveal" style="--d:1" href="{base}pedagogie.html"><h3>L’Ymmersion</h3><p>Comment se passent les trois premières semaines.</p><span class="more">Voir la pédagogie <span>→</span></span></a></div></div></section>
<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base)}</div></section>"""
    page("projets/mr-ybot.html", "Projet RED — Mr Ybot", body, PROJ_BY_SLUG["mr-ybot"]["accroche"], "about", "Projets")

    # ---------- RecrutIA
    meters = [("Précision du modèle", 82, "var(--violet)"), ("Équité entre profils", 54, "var(--menthe)"), ("Biais détecté", 38, "var(--rouge)")]
    meter_html = "".join(f'<div class="meter"><div class="mt"><span>{n}</span><b>{v} %</b></div><div class="mb"><i style="--v:{v}%;--c:{c}"></i></div></div>' for n, v, c in meters)
    console = (f'<div class="term light reveal" style="--d:1"><div class="term-bar"><i></i><i></i><i></i><span>console de données — RecrutIA</span></div><div class="term-body" style="font-family:var(--f-body)">'
               f'<p style="margin:0 0 18px;color:#C3CAC5;font-size:14px">Tri des CV · tableau de bord de l’entraînement</p>{meter_html}</div>'
               f'<p class="term-note">Illustration du thème du jeu : les valeurs sont fictives.</p></div>')
    steps = [("Un rôle", "Tu es data scientist chez RecrutIA, une entreprise fictive dont l’IA trie des CV."), ("Des décisions", "Au fil de 15 pages connectées, chaque choix sur les données d’entraînement fait évoluer l’IA."),
             ("Trois fins", "Selon tes décisions, le modèle devient équitable, biaisé ou ingérable : trois fins possibles."), ("Deux thèmes", "Une version claire avec un bouton jour/nuit, et une version sombre façon « console de données ».")]
    st_html = "".join(f'<div class="step-card reveal" style="--d:{i}"><h3>{t_}</h3><p>{d}</p></div>' for i, (t_, d) in enumerate(steps))
    skills = "".join(f"<li>{x}</li>" for x in ["Structurer un site en pages HTML connectées par des liens", "Mettre en forme avec CSS : deux thèmes, composants réutilisables",
                                               "Écrire un petit script JavaScript pour le mode jour/nuit", "Raconter une notion d’IA — le biais des données — à travers un jeu"])
    chips = '<div class="meta-chips"><span class="mchip"><b>Projet étudiant</b></span><span class="mchip">Data · <b>B1</b></span><span class="mchip">Ynov <b>Sophia</b></span><span class="mchip"><b>HTML</b> / <b>CSS</b> / JS</span><span class="mchip"><b>15</b> pages</span></div>'
    body = page_hero(base, [("Accueil", "index.html"), ("Projets étudiants", "projets.html"), ("RecrutIA", None)], "RecrutIA — « Survie contre le Biais »",
                     "Un mini-jeu de décisions en HTML/CSS : tu incarnes un·e data scientist qui entraîne une IA de tri de CV, et tu découvres comment les données fabriquent le biais.", chips, "#EEFF57")
    body += f"""<section class="sec" style="padding-top:20px"><div class="wrap split" style="align-items:start"><div class="reveal"><span class="eyebrow">Le projet</span><h2>Apprendre ce qu’est un biais en jouant.</h2>
<p class="lead">Réalisé en première année dans la filière Data, ce projet web transforme une notion d’IA en histoire à embranchements : quinze pages, trois fins, deux ambiances visuelles.</p>
<p>L’idée de l’orienter vers l’entraînement d’un modèle de langage est venue de l’étudiant, avec l’aide de son mentor. Le jeu a été renommé « RecrutIA », du nom de l’entreprise fictive.</p>
<a class="btn btn-primary" href="https://adsansgluten.github.io/Jeu-LLM-Projet-HTML/" target="_blank" rel="noopener">Jouer en ligne ↗</a></div>{console}</div></section>
<section class="sec alt"><div class="wrap">{sec_head("Le principe", "Un jeu en quatre ingrédients.")}<div class="steps">{st_html}</div></div></section>
<section class="sec"><div class="wrap"><div class="split" style="align-items:start"><div class="reveal"><span class="eyebrow">Compétences travaillées</span><h2>Ce que ce projet apprend.</h2></div><ul class="skills reveal" style="--d:1;grid-template-columns:1fr">{skills}</ul></div>
<div class="callout reveal" style="margin-top:48px"><b>Suite envisagée :</b> une version en Go, jouable dans le terminal.</div>
<div class="grid g2" style="margin-top:32px"><a class="card hov reveal" href="{base}formations/bachelor-developpement-ia-data-engineering.html"><h3>Bachelor Développement IA &amp; data engineering</h3><p>La formation dans laquelle ce projet s’inscrit.</p><span class="more">Voir la formation <span>→</span></span></a>
<a class="card hov reveal" style="--d:1" href="{base}projets/mr-ybot.html"><h3>Autre projet : Mr Ybot</h3><p>Un jeu en terminal en Go, pour la cybersécurité.</p><span class="more">Voir le projet <span>→</span></span></a></div></div></section>
<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band(base)}</div></section>"""
    page("projets/recrutia.html", "RecrutIA — Survie contre le Biais", body, PROJ_BY_SLUG["recrutia"]["accroche"], "about", "Projets")

    # ---------- index des projets
    base = ""
    cards = "".join(f'<a class="proj-feature reveal" style="--d:{i}" href="projets/{pj["slug"]}.html"><div><span class="badge b-Bachelor">Projet étudiant</span><h3>{esc(pj["titre"])}</h3>'
                    f'<p>{esc(pj["accroche"])}</p><p class="note" style="margin:0 0 14px">{esc(pj["contexte"])} · {esc(pj["equipe"])}</p><div class="tagrow">' + "".join(f"<span>{esc(t)}</span>" for t in pj["tags"]) +
                    f'</div><span class="link-ar">Découvrir le projet <span>→</span></span></div><div class="pf-vis pf-{pj["slug"]}" aria-hidden="true"></div></a>' for i, pj in enumerate(PROJETS))
    yd = "".join(f"<li>{esc(x)}</li>" for x in SOPHIA_YDAYS)
    body = page_hero("", [("Accueil", "index.html"), ("Projets étudiants", None)], "Projets étudiants",
                     "Chez Ynov, on apprend en construisant. Voici des exemples de ce que des étudiants ont réalisé dès leur première année.")
    body += f"""<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g2">{cards}</div>
<div class="split" style="margin-top:96px;align-items:start"><div class="reveal"><span class="eyebrow">Ymmersions</span><h2>Trois semaines, un défi réel.</h2><p class="lead">À la rentrée, les étudiants travaillent en équipe sur un défi concret : c’est de là que sont nés des projets comme « Mr Ybot ».</p><a class="link-ar" href="pedagogie.html">La pédagogie <span>→</span></a></div>
<div class="reveal" style="--d:1"><span class="eyebrow">Ydays · Ynov Sophia</span><h3>Quelques projets inter-formations</h3><ul class="pill-list">{yd}</ul></div></div></div></section>
<section class="sec" style="padding:20px 0 90px"><div class="wrap">{cta_band("")}</div></section>"""
    page("projets.html", "Projets étudiants", body, "Exemples de projets réalisés par des étudiants.", "about", "Pages")


def build_sitemap():
    groups = {}
    for path, title, g in PAGES: groups.setdefault(g, []).append((path, title))
    html_ = ""
    for g in ["Pages", "Formations", "Domaines", "Pôles", "Campus", "Projets", "Ynov"]:
        if g in groups:
            items = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in sorted(groups[g], key=lambda x: x[1]))
            html_ += f'<div class="reveal"><h3>{g}</h3><ul class="checks" style="gap:6px">{items}</ul></div>'
    body = page_hero("", [("Accueil", "index.html"), ("Plan du site", None)], "Plan du site", f"{len(PAGES)} pages.") + f'<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g3">{html_}</div></div></section>'
    page("plan-du-site.html", "Plan du site", body, "Toutes les pages.", "", "Pages", index=False)


def build_assets():
    shutil.copy(os.path.join(ROOT, "src", "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(ROOT, "src", "app.js"), os.path.join(OUT, "assets", "app.js"))
    progs = [dict(t=p["titre"], s=p["short"], f=p["fam"], fn=p["fam_obj"]["nom"], typ=p["typ"], c=p["campus"], on=p["online"]) for p in P_SORTED]
    idx = []
    for p in P_SORTED: idx.append(dict(t=p["titre"], g=f'{p["typ"]} · {p["fam_obj"]["nom"]}', u=prog_url(p), k=p["short"] + " " + p["fam_obj"]["nom"]))
    for f in FAMILLES: idx.append(dict(t=f["nom"], g="Domaine", u=fam_url(f), k=f["accroche"]))
    for pl in POLES: idx.append(dict(t=pl["nom"], g="Pôle", u=pole_url(pl), k=pl["verbes"]))
    for pj in PROJETS: idx.append(dict(t=pj["titre"], g="Projet étudiant", u=f"projets/{pj['slug']}.html", k=pj["accroche"] + " " + " ".join(pj["tags"])))
    for c in CAMPUS: idx.append(dict(t="Campus " + c[2], g="Campus", u=campus_url(c), k=c[3] + " portes ouvertes"))
    idx.append(dict(t="Connect – campus en ligne", g="Campus", u="campus/connect.html", k="distance online"))
    for u, t, k in [("admission.html", "Admission & candidature", "candidater inscription dossier"), ("alternance.html", "Alternance", "contrat apprentissage professionnalisation"), ("pedagogie.html", "Pédagogie", "ymmersion yday projet"),
                    ("evenements.html", "Portes ouvertes", "jpo événements"), ("metiers.html", "Guide des métiers", "salaire débouchés"), ("entreprises.html", "Entreprises", "recruter partenaire"),
                    ("faq.html", "FAQ", "questions financement"), ("contact.html", "Contact", "téléphone brochure"), ("a-propos.html", "Qui sommes-nous", "histoire vision"), ("vie-de-campus.html", "Vie de campus", "asso bde"),
                    ("alumni.html", "Alumni", "réseau anciens"), ("projets.html", "Projets étudiants", "ymmersion jeu go terminal recrutia"), ("ystart.html", "Ystart", "incubateur startup"), ("handicap.html", "Handicap", "hand you inclusion"), ("actualites.html", "Actualités", "news")]:
        idx.append(dict(t=t, g="Page", u=u, k=k))
    with open(os.path.join(OUT, "assets", "data.js"), "w", encoding="utf-8") as fh:
        fh.write("window.PROGS=" + json.dumps(progs, ensure_ascii=False) + ";\nwindow.INDEX=" + json.dumps(idx, ensure_ascii=False) + ";\n")


if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    build_home(); build_catalogue(); build_formations(); build_domaines_poles(); build_campus(); build_static(); build_projets(); build_sitemap(); build_assets()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("OK", len(PAGES), "pages indexées,", n, "fichiers")
