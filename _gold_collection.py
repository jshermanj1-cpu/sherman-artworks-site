# -*- coding: utf-8 -*-
"""Generate gold-collection.html, the landing page for the gold-plated range.

The four gold-plated category pages stay the source of truth for products,
prices, cart and modal behaviour. This page is the hub the homepage rail and
the nav point at: one place that gathers the range and hands visitors on to
the category page that actually sells it.

about.html supplies the shared chrome (head, top bar, nav, footer, cart
drawer, consent banner, scripts) exactly the way _subcategory_pages.py leans
on a category landing page. Only the hero, the card grid, the CTA band copy
and the page metadata are rewritten here.

Run after editing about.html, then re-run _he_pages.py to refresh
he/gold-collection.html and the sitemap.
"""

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).parent
BASE = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"

SOURCE = "about.html"
TARGET = "gold-collection.html"

TITLE = "The Gold Collection - Sherman Art Works | Handmade Glass Judaica"
DESC = ("Handmade glass Judaica finished with gold plating: Shabbat candlesticks, "
        "Kiddush cups, trays and Havdalah sets, made to order in our studio in Israel.")
OG_TITLE = "The Gold Collection, Sherman Art Works"
HERO_IMAGE = "Blue_Pamotim_gold_1_kdduli"

# id, page, photo, min price in shekels
CARDS = [
    ("gc1", "candlesticks-gold-plated.html", "Blue_Pamotim_gold_1_kdduli", 680),
    ("gc2", "kiddush-cups-gold-plated.html", "Blue_high_cup_gold_1_an740y", 552),
    ("gc3", "trays-bowls-gold-plated.html", "Black_tray_gold_wdxp9o", 441),
    ("gc4", "havdalah-sets-gold-plated.html", "Black_havdalah_set_gold_zblb7f", 1467),
]

# Overrides applied to both language halves of the page's T_PAGE dict, and to
# the matching [data-t] elements in the static markup.
COPY = {
    "hero_eyebrow": ("New In", "\u05d7\u05d3\u05e9 \u05d1\u05d7\u05e0\u05d5\u05ea"),
    "hero_headline": ("The Gold Collection", "\u05e7\u05d5\u05dc\u05e7\u05e6\u05d9\u05d9\u05ea \u05d4\u05d6\u05d4\u05d1"),
    "hero_subtitle": (
        "Our most popular pieces, now in a gold plated finish.",
        "\u05d4\u05e4\u05e8\u05d9\u05d8\u05d9\u05dd \u05d4\u05e4\u05d5\u05e4\u05d5\u05dc\u05e8\u05d9\u05d9\u05dd \u05d1\u05d9\u05d5\u05ea\u05e8 \u05e9\u05dc\u05e0\u05d5, \u05e2\u05db\u05e9\u05d9\u05d5 \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1."),
    "gold_hub_tag": ("The Collection", "\u05d4\u05e7\u05d5\u05dc\u05e7\u05e6\u05d9\u05d4"),
    "gold_hub_title": ("Browse the Gold Collection",
                       "\u05d3\u05e4\u05d3\u05e4\u05d5 \u05d1\u05e7\u05d5\u05dc\u05e7\u05e6\u05d9\u05d9\u05ea \u05d4\u05d6\u05d4\u05d1"),
    "gold_hub_sub": (
        "Every piece is handmade in our studio and finished with gold plating.",
        "\u05db\u05dc \u05e4\u05e8\u05d9\u05d8 \u05e0\u05e2\u05e9\u05d4 \u05d1\u05e2\u05d1\u05d5\u05d3\u05ea \u05d9\u05d3 \u05d1\u05e1\u05d8\u05d5\u05d3\u05d9\u05d5 \u05e9\u05dc\u05e0\u05d5 \u05d5\u05de\u05e6\u05d5\u05e4\u05d4 \u05d6\u05d4\u05d1."),
    "cat_cta_browse": ("Browse Collection", "\u05dc\u05e7\u05d5\u05dc\u05e7\u05e6\u05d9\u05d4"),
    "gc1_title": ("Gold-Plated Candlesticks",
                  "\u05e4\u05de\u05d5\u05d8\u05d9\u05dd \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1"),
    "gc1_desc": ("Shabbat candlesticks in handmade glass, finished with gold plating and sold as a pair.",
                 "\u05e4\u05de\u05d5\u05d8\u05d9 \u05e9\u05d1\u05ea \u05de\u05d6\u05db\u05d5\u05db\u05d9\u05ea \u05d1\u05e2\u05d1\u05d5\u05d3\u05ea \u05d9\u05d3, \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1, \u05e0\u05de\u05db\u05e8\u05d9\u05dd \u05db\u05d6\u05d5\u05d2."),
    "gc2_title": ("Gold-Plated Kiddush Cups",
                  "\u05db\u05d5\u05e1\u05d5\u05ea \u05e7\u05d9\u05d3\u05d5\u05e9 \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1"),
    "gc2_desc": ("Handmade glass Kiddush cups finished with gold plating, with a matching plate available.",
                 "\u05db\u05d5\u05e1\u05d5\u05ea \u05e7\u05d9\u05d3\u05d5\u05e9 \u05de\u05d6\u05db\u05d5\u05db\u05d9\u05ea \u05d1\u05e2\u05d1\u05d5\u05d3\u05ea \u05d9\u05d3 \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1, \u05e2\u05dd \u05ea\u05d7\u05ea\u05d9\u05ea \u05ea\u05d5\u05d0\u05de\u05ea."),
    "gc3_title": ("Gold-Plated Trays & Bowls",
                  "\u05de\u05d2\u05e9\u05d9\u05dd \u05d5\u05e7\u05e2\u05e8\u05d5\u05ea \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1"),
    "gc3_desc": ("Glass trays and Kiddush cup plates finished with gold plating.",
                 "\u05de\u05d2\u05e9\u05d9 \u05d6\u05db\u05d5\u05db\u05d9\u05ea \u05d5\u05ea\u05d7\u05ea\u05d9\u05d5\u05ea \u05dc\u05db\u05d5\u05e1 \u05e7\u05d9\u05d3\u05d5\u05e9 \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1."),
    "gc4_title": ("Gold-Plated Havdalah Sets",
                  "\u05e1\u05d8\u05d9 \u05d4\u05d1\u05d3\u05dc\u05d4 \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1"),
    "gc4_desc": ("Complete Havdalah sets in handmade glass, finished with gold plating.",
                 "\u05e1\u05d8\u05d9 \u05d4\u05d1\u05d3\u05dc\u05d4 \u05e9\u05dc\u05de\u05d9\u05dd \u05de\u05d6\u05db\u05d5\u05db\u05d9\u05ea \u05d1\u05e2\u05d1\u05d5\u05d3\u05ea \u05d9\u05d3, \u05d1\u05e6\u05d9\u05e4\u05d5\u05d9 \u05d6\u05d4\u05d1."),
    "cta_tag": ("Made to Order", "\u05d1\u05d9\u05e6\u05d5\u05e2 \u05dc\u05e4\u05d9 \u05d4\u05d6\u05de\u05e0\u05d4"),
    "cta_title": ("Something Made Just for You",
                  "\u05de\u05e9\u05d4\u05d5 \u05e9\u05e0\u05e2\u05e9\u05d4 \u05d1\u05d3\u05d9\u05d5\u05e7 \u05e2\u05d1\u05d5\u05e8\u05db\u05dd"),
    "cta_sub": ("Every piece here is made to order. Tell us the colour you want and we will make it.",
                "\u05db\u05dc \u05e4\u05e8\u05d9\u05d8 \u05db\u05d0\u05df \u05e0\u05e2\u05e9\u05d4 \u05dc\u05e4\u05d9 \u05d4\u05d6\u05de\u05e0\u05d4. \u05e1\u05e4\u05e8\u05d5 \u05dc\u05e0\u05d5 \u05d0\u05d9\u05d6\u05d4 \u05e6\u05d1\u05e2 \u05d0\u05ea\u05dd \u05e8\u05d5\u05e6\u05d9\u05dd \u05d5\u05e0\u05d9\u05d9\u05e6\u05e8 \u05d0\u05d5\u05ea\u05d5."),
    "cta_btn1": ("Browse the Shop", "\u05d3\u05e4\u05d3\u05e4\u05d5 \u05d1\u05d7\u05e0\u05d5\u05ea"),
    "cta_btn2": ("Commission a Custom Piece",
                 "\u05d4\u05d6\u05de\u05e0\u05d4 \u05d1\u05d4\u05ea\u05d0\u05de\u05d4 \u05d0\u05d9\u05e9\u05d9\u05ea"),
}

ARROW = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" '
         'aria-hidden="true"><path d="M4 10 H16 M11 5 L16 10 L11 15"/></svg>')


def replace_one(text, pattern, replacement, label, flags=0):
    out, n = re.subn(pattern, replacement, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError("%s: expected exactly one match" % label)
    return out


def card_html(key, page, photo, min_ils):
    src = "%s/w_600,h_600,c_pad,b_rgb:f5f0e8,q_auto,f_auto/%s.jpg" % (CDN, photo)
    return """    <a href="{page}" class="cat-card">
      <div class="cat-card-img-wrap">
        <img class="cat-card-img" loading="lazy" width="600" height="600"
             src="{src}"
             alt="{alt}" />
      </div>
      <div class="cat-card-body">
        <h3 class="cat-card-title" data-t="{key}_title">{title}</h3>
        <p class="cat-card-desc"   data-t="{key}_desc">{desc}</p>
        <span class="cat-card-from" data-min-ils="{min_ils}">from &#8362;{min_ils:,}</span>
        <span class="cat-card-cta">
          <span data-t="cat_cta_browse">Browse Collection</span>
          {arrow}
        </span>
      </div>
    </a>""".format(page=page, src=src, key=key, min_ils=min_ils, arrow=ARROW,
                   alt=html.escape(COPY[key + "_title"][0] + " by Sherman Art Works", quote=True),
                   title=html.escape(COPY[key + "_title"][0]),
                   desc=html.escape(COPY[key + "_desc"][0]))


def content():
    cards = "\n\n".join(card_html(*c) for c in CARDS)
    return """<!-- ══════════════════════════════════════════════
     PAGE HERO
══════════════════════════════════════════════ -->
<section class="page-hero">
  <div class="page-hero-inner">
    <div class="page-eyebrow" data-t="hero_eyebrow">{eyebrow}</div>
    <h1 class="page-headline"  data-t="hero_headline">{headline}</h1>
    <p  class="page-subtitle"  data-t="hero_subtitle">{subtitle}</p>
  </div>
</section>

<!-- ══════════════════════════════════════════════
     THE FOUR GOLD-PLATED COLLECTIONS
     Each card hands off to the category page that owns the products,
     the cart and the size and plate options.
══════════════════════════════════════════════ -->
<section class="section" id="collections">
  <div class="section-header">
    <div class="ornament" aria-hidden="true">✦ ✦ ✦</div>
    <div class="section-tag" data-t="gold_hub_tag">{tag}</div>
    <h2 class="section-title" data-t="gold_hub_title">{title}</h2>
    <p  class="section-sub"   data-t="gold_hub_sub">{sub}</p>
  </div>

  <div class="category-grid">

{cards}

  </div>
</section>

""".format(eyebrow=html.escape(COPY["hero_eyebrow"][0]),
           headline=html.escape(COPY["hero_headline"][0]),
           subtitle=html.escape(COPY["hero_subtitle"][0]),
           tag=html.escape(COPY["gold_hub_tag"][0]),
           title=html.escape(COPY["gold_hub_title"][0]),
           sub=html.escape(COPY["gold_hub_sub"][0]),
           cards=cards)


def structured_data():
    url = "%s/%s" % (BASE, TARGET)
    collection = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "The Gold Collection", "url": url, "description": DESC,
        "isPartOf": {"@type": "WebSite", "name": "Sherman Art Works", "url": BASE},
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": COPY[key + "_title"][0], "url": "%s/%s" % (BASE, page)}
            for i, (key, page, _photo, _min) in enumerate(CARDS)]},
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sherman Art Works", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "The Gold Collection", "item": url},
    ]}
    return (json.dumps(collection, ensure_ascii=False, separators=(",", ":")),
            json.dumps(crumbs, separators=(",", ":")))


def main():
    out = (SITE / SOURCE).read_text(encoding="utf-8")
    url = "%s/%s" % (BASE, TARGET)
    he_url = "%s/he/%s" % (BASE, TARGET)
    image = "%s/w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto/%s.jpg" % (CDN, HERO_IMAGE)

    for pattern, replacement, label in [
        (r"<title>.*?</title>", "<title>%s</title>" % html.escape(TITLE), "title"),
        (r'<meta name="description" content=".*?" />',
         '<meta name="description" content="%s" />' % html.escape(DESC, quote=True), "description"),
        (r'<meta property="og:title" content=".*?" />',
         '<meta property="og:title" content="%s" />' % html.escape(OG_TITLE, quote=True), "og title"),
        (r'<meta property="og:description" content=".*?" />',
         '<meta property="og:description" content="%s" />' % html.escape(DESC, quote=True), "og description"),
        (r'<meta property="og:image" content=".*?" />',
         '<meta property="og:image" content="%s" />' % image, "og image"),
        (r'<meta property="og:url" content=".*?" />',
         '<meta property="og:url" content="%s" />' % url, "og url"),
        (r'<link rel="canonical" href=".*?" />',
         '<link rel="canonical" href="%s" />' % url, "canonical"),
        (r'<link rel="alternate" hreflang="en" href=".*?" />',
         '<link rel="alternate" hreflang="en" href="%s" />' % url, "alternate en"),
        (r'<link rel="alternate" hreflang="he-IL" href=".*?" />',
         '<link rel="alternate" hreflang="he-IL" href="%s" />' % he_url, "alternate he"),
        (r'<link rel="alternate" hreflang="x-default" href=".*?" />',
         '<link rel="alternate" hreflang="x-default" href="%s" />' % url, "alternate x-default"),
        (r'<meta name="twitter:title" content=".*?" />',
         '<meta name="twitter:title" content="%s" />' % html.escape(OG_TITLE, quote=True), "twitter title"),
        (r'<meta name="twitter:description" content=".*?" />',
         '<meta name="twitter:description" content="%s" />' % html.escape(DESC, quote=True), "twitter description"),
        (r'<meta name="twitter:image" content=".*?" />',
         '<meta name="twitter:image" content="%s" />' % image, "twitter image"),
    ]:
        out = replace_one(out, pattern, replacement, label)

    # Language toggle has to land on the Hebrew twin of this page, not about.
    out = replace_one(out, r"location\.href='/he/%s'" % re.escape(SOURCE),
                      "location.href='/he/%s'" % TARGET, "language toggle")

    # Structured data: swap about's BreadcrumbList for a CollectionPage + crumbs.
    collection, crumbs = structured_data()
    out = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", out, flags=re.S)
    out = replace_one(
        out, r'  <link rel="canonical"',
        '  <script type="application/ld+json">%s</script>\n'
        '  <script type="application/ld+json">%s</script>\n  <link rel="canonical"' % (collection, crumbs),
        "structured data anchor")

    # Body: everything from the page hero up to the CTA band becomes the hub.
    out = replace_one(
        out,
        r'<!-- ══════════════════════════════════════════════\n     PAGE HERO\n.*?'
        r'(<!-- ══════════════════════════════════════════════\n     CTA BAND)',
        lambda m: content() + m.group(1), "page body", re.S)

    # The CTA band's shop link points at the gold range rather than everything.
    out = replace_one(out, r'<a href="index\.html#shop"    class="btn-primary" data-t="cta_btn1">[^<]*</a>',
                      '<a href="index.html#shop"    class="btn-primary" data-t="cta_btn1">%s</a>'
                      % html.escape(COPY["cta_btn1"][0]), "cta button 1")

    # Runtime dictionary: override the keys this page uses, and add the new ones
    # so setLang() and _he_pages.py both resolve them.
    for key, (en_value, he_value) in COPY.items():
        # The value pattern has to tolerate escaped apostrophes: about.html carries
        # "A grandfather\'s passion", and a naive '[^']*' stops at that backslash
        # escape, replacing half a string and leaving the rest as loose JS.
        matches = list(re.finditer(r"(\b%s:\s+)'(?:\\.|[^'\\])*'" % re.escape(key), out))
        if len(matches) == 2:
            for match, value in reversed(list(zip(matches, (en_value, he_value)))):
                out = out[:match.start()] + match.group(1) + repr(value) + out[match.end():]
        elif not matches:
            for anchor, value in (("    en: {", en_value), ("    he: {", he_value)):
                out = replace_one(out, re.escape(anchor),
                                  "%s\n      %s: %s," % (anchor, key, repr(value)),
                                  "new key %s in %s" % (key, anchor.strip()))
        else:
            raise RuntimeError("%s: expected 0 or 2 values, found %d" % (key, len(matches)))

    out = re.sub(r"[ \t]+$", "", out, flags=re.M)
    (SITE / TARGET).write_text(out, encoding="utf-8")
    print("%s: %d collection cards" % (TARGET, len(CARDS)))


if __name__ == "__main__":
    main()
