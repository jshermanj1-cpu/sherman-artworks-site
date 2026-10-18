# -*- coding: utf-8 -*-
"""_hanukkah_page.py - build the Hanukkah menorah page from data/products.json.

Every menorah shape exists sixteen times over - eight glass colours, each with
silver-tone or gold-tone sockets and base - and there are three shapes, so the
page carries forty-eight products, and a photo or a price lives on five surfaces
of it at once: the runtime catalogue in
js/hanukkah-menorahs.js, the no-JS cards crawlers read, two ProductGroup blocks,
the share image, and the homepage category card. Hand-keeping five copies in
step is how every other category on this site drifted, so here data/products.json
is the only copy anyone edits and this script writes the rest.

What it owns, each between marker comments so nothing around it is touched:

  js/hanukkah-menorahs.js   the PRODUCTS array (every menorah, photo or not)
  hanukkah-menorahs.html    static cards + ProductGroup JSON-LD + og/twitter image,
                            and the shape switcher above the grid
  hanukkah-menorahs-*.html  one page per shape (SHAPES below), written whole from
                            the landing page: its own title, hero, breadcrumb,
                            cards and ProductGroups, and data-shape on the grid
                            so the runtime shows only that shape
  index.html                the Hanukkah category card's image and its "from" price
  every English page        the shape links under Hanukkah in the phone menu

While the Hanukkah sale runs (_hanukkah_sale.py), the meta descriptions and the
homepage card lead with the sale price. Rerun the chain after the sale ends and
they go back to the regular copy, like the card prices and the JSON-LD.

A menorah with no photo yet is held back: products.json marks it
"active": false, and it gets no static card, no JSON-LD and no feed item until
_menorah_photos.py (or a hand edit) gives it one. The runtime array keeps it, so
the page can be previewed while photos are still being shot.

    python _hanukkah_page.py           write in place
    python _hanukkah_page.py --check   report only, exit 1 if anything is stale
"""

from _hanukkah_sale import price_html, offer_fields, running, sale
import html
import json
import re
import sys
from pathlib import Path

from _usd import usd_from_ils
# The switcher, its translation keys and the phone-menu links work exactly as
# on the other categories, so they come from the same engine.
from _subcategory_pages import ensure_landing_switcher, ensure_mobile_navigation, replace_one, switcher

SITE = Path(__file__).parent
BASE = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"
PAGE = "hanukkah-menorahs.html"
JS = "js/hanukkah-menorahs.js"
CATEGORY = "hanukkah-menorahs"
COLOR_NOTE = ("* Colors and measurements may appear slightly different in person, "
              "as each item is handmade.")

# The homepage card and the share image lead with this piece when it has a photo,
# otherwise with the first menorah that does.
COVER = "gold-tone-terracotta-trapezoid-menorah"

# One ProductGroup per family_id: a shape in one finish, its variants the glass
# colours. A new shape means new families here (and in _he_pages.py's
# PRODUCT_GROUP_HE), never a rename of these - productGroupID is what Google keys
# the variants on.
GROUPS = {
    "silver-tone-half-moon-hanukkah-menorahs": {
        "name": "Half-Moon Glass Hanukkah Menorahs with Silver-Tone Sockets",
        "description": "Handmade half-moon Hanukkah menorahs of double-sided glass in eight colors, "
                       "with silver-tone sockets and base, crafted in our studio in Israel."},
    "gold-tone-half-moon-hanukkah-menorahs": {
        "name": "Half-Moon Glass Hanukkah Menorahs with Gold-Tone Sockets",
        "description": "Handmade half-moon Hanukkah menorahs of double-sided glass in eight colors, "
                       "with gold-tone sockets and base, crafted in our studio in Israel."},
    "silver-tone-rectangular-hanukkah-menorahs": {
        "name": "Rectangular Glass Hanukkah Menorahs with Silver-Tone Sockets",
        "description": "Handmade rectangular Hanukkah menorahs of double-sided glass in eight colors, "
                       "with silver-tone sockets and base, crafted in our studio in Israel."},
    "gold-tone-rectangular-hanukkah-menorahs": {
        "name": "Rectangular Glass Hanukkah Menorahs with Gold-Tone Sockets",
        "description": "Handmade rectangular Hanukkah menorahs of double-sided glass in eight colors, "
                       "with gold-tone sockets and base, crafted in our studio in Israel."},
    "silver-tone-trapezoid-hanukkah-menorahs": {
        "name": "Trapezoid Glass Hanukkah Menorahs with Silver-Tone Sockets",
        "description": "Handmade trapezoid Hanukkah menorahs of double-sided glass in eight colors, "
                       "with silver-tone sockets and base, crafted in our studio in Israel."},
    "gold-tone-trapezoid-hanukkah-menorahs": {
        "name": "Trapezoid Glass Hanukkah Menorahs with Gold-Tone Sockets",
        "description": "Handmade trapezoid Hanukkah menorahs of double-sided glass in eight colors, "
                       "with gold-tone sockets and base, crafted in our studio in Israel."},
}

# One page per shape. The key is the products' "shape"; "kind" names its
# switcher and menu keys (switch_hanukkah_<kind>, which js/site.js also carries
# for the phone menu on every page); "headline" is the page's h1 and its label in
# the switcher and the menu, like the other categories. Hebrew titles and
# descriptions live in _he_pages.py's META with every other page's, and each
# page needs a line in its PAGES list and in sitemap.xml.
SHAPES = {
    "half-moon": {
        "kind": "half_moon",
        "file": "hanukkah-menorahs-half-moon.html",
        "cover": "silver-tone-blue-half-moon-menorah",
        "title": "Half-Moon Glass Hanukkah Menorahs | Sherman Art Works",
        "headline": "Half-Moon Menorahs",
        "subtitle": "Double-sided handmade glass in a half-moon shape, in eight colors.",
        "body": "Choose silver-tone or gold-tone sockets and base. Each menorah is shaped by hand in our studio in Israel.",
        "he": {
            "headline": "חנוכיות חצי עיגול",
            "subtitle": "זכוכית דו־צדדית בעבודת יד בצורת חצי עיגול, בשמונה צבעים.",
            "body": "בחרו קנים ובסיס בגוון כסף או בגוון זהב. כל חנוכיה מעוצבת בעבודת יד בסטודיו שלנו בישראל.",
        },
    },
    "rectangular": {
        "kind": "rectangular",
        "file": "hanukkah-menorahs-rectangular.html",
        "cover": "silver-tone-blue-rectangular-menorah",
        "title": "Rectangular Glass Hanukkah Menorahs | Sherman Art Works",
        "headline": "Rectangular Menorahs",
        "subtitle": "Double-sided handmade glass in a rectangular shape, in eight colors.",
        "body": "Choose silver-tone or gold-tone sockets and base. Each menorah is shaped by hand in our studio in Israel.",
        "he": {
            "headline": "חנוכיות מלבניות",
            "subtitle": "זכוכית דו־צדדית בעבודת יד בצורת מלבן, בשמונה צבעים.",
            "body": "בחרו קנים ובסיס בגוון כסף או בגוון זהב. כל חנוכיה מעוצבת בעבודת יד בסטודיו שלנו בישראל.",
        },
    },
    "trapezoid": {
        "kind": "trapezoid",
        "file": "hanukkah-menorahs-trapezoid.html",
        "cover": "silver-tone-blue-trapezoid-menorah",
        "title": "Trapezoid Glass Hanukkah Menorahs | Sherman Art Works",
        "headline": "Trapezoid Menorahs",
        "subtitle": "Double-sided handmade glass in a trapezoid shape, in eight colors.",
        "body": "Choose silver-tone or gold-tone sockets and base. Each menorah is shaped by hand in our studio in Israel.",
        "he": {
            "headline": "חנוכיות טרפז",
            "subtitle": "זכוכית דו־צדדית בעבודת יד בצורת טרפז, בשמונה צבעים.",
            "body": "בחרו קנים ובסיס בגוון כסף או בגוון זהב. כל חנוכיה מעוצבת בעבודת יד בסטודיו שלנו בישראל.",
        },
    },
}

# Meta descriptions, kept to 155 characters so results do not cut them off. While
# the sale runs they lead with its price ({price}); afterwards the regular copy.
# Hebrew ones live in _he_pages.py's META, switched the same way.
# "Modern" and "colorful" are the words shoppers type; the pages never said them.
LANDING_DESC = ("Modern, colorful handmade glass Hanukkah menorahs from Israel: half-moon, rectangular "
                "and trapezoid, silver-tone or gold-tone sockets. Shipped worldwide.")
LANDING_DESC_SALE = ("Modern, colorful handmade glass Hanukkah menorahs from Israel in three shapes and "
                     "eight colors. Hanukkah price {price} until December 4.")
SHAPE_DESC = ("Modern {shape} Hanukkah menorahs handmade in Israel of double-sided glass, eight colors, "
              "silver-tone or gold-tone sockets and base. Shipped worldwide.")
SHAPE_DESC_SALE = ("Modern {shape} glass Hanukkah menorahs, handmade in Israel in eight colors. "
                   "Hanukkah price {price} until December 4.")

# The shape of _subcategory_pages.CATEGORIES that its switcher and menu helpers read.
NAV = {
    "landing": PAGE,
    "landing_label": "Hanukkah",
    "landing_key": "cat9_title",
    "aria": "Menorah shapes",
    "prefix": "switch_hanukkah_",
    "all_label": ("All Menorahs", "כל החנוכיות"),
    "pages": {s["kind"]: {"file": s["file"], "headline": s["headline"], "he": {"headline": s["he"]["headline"]}}
              for s in SHAPES.values()},
}

# The Hanukkah guides, linked under the landing page's questions. The shape pages
# are copied from the landing page, so they carry the same links. Each entry is
# (page, translation key, English, Hebrew).
GUIDES = (
    ("hanukkah-menorah-guide.html", "hguide_choose",
     "Read our guide: how to choose a Hanukkah menorah",
     "למדריך: איך בוחרים חנוכיה"),
    ("how-to-light-hanukkah-candles.html", "hguide_light",
     "How to light the Hanukkah menorah: the blessings, the order and the 2026 dates",
     "איך מדליקים נרות חנוכה: הברכות, סדר ההדלקה ותאריכי 2026"),
    ("hanukkah-gift-guide.html", "hguide_gifts",
     "Hanukkah gift ideas, and when to order before the first night",
     "רעיונות למתנה לחנוכה, ועד מתי להזמין לפני הנר הראשון"),
    ("menorah-vs-hanukkiah.html", "hguide_hanukkiah",
     "Menorah or hanukkiah? The difference, and the story of Hanukkah",
     "מנורה או חנוכיה? ההבדל, וסיפור חנוכה"),
)

# Fields copied into the runtime array, in this order. "id" then "sku" must be
# adjacent lines - _validate_skus.py matches them as one pair.
JS_FIELDS = ("id", "sku", "family_id", "finish", "shape", "name_en", "name_he",
             "description_en", "description_he", "color_en", "color_he",
             "measurements", "price_ils", "photos")


def load():
    data = json.loads((SITE / "data" / "products.json").read_text(encoding="utf-8"))
    return [p for p in data if p.get("category") == CATEGORY]


def live(products):
    return [p for p in products if p.get("active") is not False and p.get("photos")]


def image(photo, transform="w_800,q_auto,f_auto"):
    return f"{CDN}/{transform}/{photo}.jpg"


def js_array(products):
    rows = []
    for p in products:
        lines = [f"    {json.dumps(k)}: {json.dumps(p.get(k, '' if k != 'photos' else []), ensure_ascii=False)}"
                 for k in JS_FIELDS]
        rows.append("  {\n" + ",\n".join(lines) + "\n  }")
    return "const PRODUCTS = [\n" + ",\n".join(rows) + "\n];"


def card(p):
    name = html.escape(p["name_en"])
    return (
        f'    <article class="product-card" id="{p["id"]}">\n'
        '      <div class="product-card-img-wrap">\n'
        f'        <img class="product-card-img" src="{image(p["photos"][0], "w_600,c_fit,q_auto,f_auto")}" '
        f'alt="{html.escape(p["name_en"], quote=True)}" loading="lazy" />\n'
        '      </div>\n'
        '      <div class="product-card-body">\n'
        f'        <h2 class="product-card-name">{name}</h2>\n'
        f'        <p class="product-card-desc">{html.escape(p["description_en"])}</p>\n'
        '        <div class="product-card-meta">\n'
        f'          <span class="product-card-price">{price_html(p)}</span>\n'
        '        </div>\n'
        f'        <p class="product-color-note">{COLOR_NOTE}</p>\n'
        '      </div>\n'
        '    </article>')


def variant(p):
    sku = p["sku"]
    return {
        "@type": "Product",
        "name": p["name_en"],
        "url": f"{BASE}/{PAGE}#{p['id']}",
        "description": p["description_en"],
        "image": [image(ph) for ph in p["photos"]],
        "color": p["color_en"],
        "sku": sku,
        "brand": {"@type": "Brand", "name": "Sherman Art Works"},
        "itemCondition": "https://schema.org/NewCondition",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "ILS",
            "price": str(p["price_ils"]),
            **offer_fields(p),
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {"@id": f"{BASE}/#seller"},
            "shippingDetails": [{"@id": f"{BASE}/#shipping-il"},
                                {"@id": f"{BASE}/#shipping-international"}],
            "hasMerchantReturnPolicy": {"@id": f"{BASE}/#return-policy"},
            "mpn": sku,
        },
        "mpn": sku,
    }


def jsonld(products):
    blocks = []
    unknown = sorted({p["family_id"] for p in products} - set(GROUPS))
    if unknown:
        raise RuntimeError("no GROUPS entry for family_id(s): " + ", ".join(unknown))
    for family, g in GROUPS.items():
        members = [p for p in products if p.get("family_id") == family]
        if not members:
            continue
        node = {
            "@context": "https://schema.org",
            "@type": "ProductGroup",
            "@id": f"{BASE}/{PAGE}#{family}",
            "name": g["name"],
            "description": g["description"],
            "brand": {"@type": "Brand", "name": "Sherman Art Works"},
            "productGroupID": family,
            "variesBy": ["https://schema.org/color"],
            "hasVariant": [variant(p) for p in members],
        }
        blocks.append('  <script type="application/ld+json">'
                      + json.dumps(node, ensure_ascii=False, separators=(",", ":"))
                      + "</script>")
    return "\n".join(blocks)


def cover(products, preferred=COVER):
    by_id = {p["id"]: p for p in products}
    if preferred in by_id:
        return by_id[preferred]["photos"][0]
    return products[0]["photos"][0] if products else None


def sale_price_text(products):
    """The sale price as the descriptions quote it, e.g. "₪1,000 ($336)"."""
    p = min(live(products), key=lambda item: item["price_ils"])
    return f'₪{sale(p["price_ils"], p["id"]):,} (${sale(usd_from_ils(p["price_ils"]), p["id"])})'


def meta_desc(products, shape=None):
    on_sale = bool(running() and live(products))
    if shape:
        tpl = SHAPE_DESC_SALE if on_sale else SHAPE_DESC
    else:
        tpl = LANDING_DESC_SALE if on_sale else LANDING_DESC
    desc = tpl.format(shape=shape or "", price=sale_price_text(products) if on_sale else "")
    if len(desc) > 155:
        raise RuntimeError(f"meta description is {len(desc)} characters, over 155: {desc}")
    return desc


def set_descriptions(out, desc, label):
    """The description, og:description and twitter:description, all the same."""
    value = html.escape(desc, quote=True)
    for attr, key in (("name", "description"), ("property", "og:description"), ("name", "twitter:description")):
        tag = f'<meta {attr}="{key}" content="{value}" />'
        out = replace_one(out, rf'<meta {attr}="{re.escape(key)}" content="[^"]*" />',
                          lambda m, v=tag: v, f"{label} {key}")
    return out


def between(text, start, end, inner, label):
    """Replace what sits between two marker comments. Raises if they are missing."""
    pat = re.compile(re.escape(start) + r"\n.*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise RuntimeError(f"{label}: markers {start!r} ... {end!r} not found")
    body = (inner + "\n") if inner else ""
    return pat.sub(lambda m: start + "\n" + body + end, text, count=1)


def ensure_guide_links(src):
    """The guide links under the questions, and their keys in both T_PAGE
    blocks, each between markers so a rerun rewrites rather than repeats them."""
    links = "\n".join(f'    <p  class="guide-note"><a href="{page}" data-t="{key}">{html.escape(en)}</a></p>'
                      for page, key, en, _ in GUIDES)
    start, end = "    <!-- hanukkah:guides -->", "    <!-- /hanukkah:guides -->"
    if start not in src:
        pat = re.compile(r'(<section class="section section-divider" id="guide">.*?)(\n  </div>\n</section>)', re.S)
        if not pat.search(src):
            raise RuntimeError(f"{PAGE}: no questions section for the guide links")
        src = pat.sub(lambda m: m.group(1) + "\n" + start + "\n" + end + m.group(2), src, count=1)
    src = between(src, start, end, links, PAGE)
    for lang, close in (("en", "\n  },\n  he: {"), ("he", "\n  }\n};")):
        kstart, kend = f"      // hanukkah:guides {lang}", f"      // /hanukkah:guides {lang}"
        if kstart not in src:
            at = src.find(close, src.find("const T_PAGE"))
            if at < 0:
                raise RuntimeError(f"{PAGE}: T_PAGE {lang} block not found")
            src = src[:at] + "\n" + kstart + "\n" + kend + src[at:]
        keys = "\n".join(f"      {key}: {json.dumps(en if lang == 'en' else he, ensure_ascii=False)},"
                         for _, key, en, he in GUIDES)
        src = between(src, kstart, kend, keys, PAGE)
    return src


def build_page(src, products):
    shown = live(products)
    indent = "  "
    src = ensure_landing_switcher(NAV, src)
    src = ensure_guide_links(src)
    out = between(src, "<!-- hanukkah:jsonld -->", indent + "<!-- /hanukkah:jsonld -->",
                  jsonld(shown), PAGE)
    out = between(out, "<!-- hanukkah:cards -->", "    <!-- /hanukkah:cards -->",
                  "\n".join(card(p) for p in shown), PAGE)
    photo = cover(shown)
    share = image(photo, "w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto") if photo else ""
    for attr, key in (("property", "og:image"), ("name", "twitter:image")):
        out = re.sub(rf'<meta {attr}="{key}" content="[^"]*" />',
                     f'<meta {attr}="{key}" content="{share}" />', out, count=1)
    return set_descriptions(out, meta_desc(products), PAGE)


def build_shape_page(landing, products, shape):
    """One shape's page, written whole from the finished landing page."""
    cfg = SHAPES[shape]
    name = cfg["file"]
    mine = [p for p in live(products) if p.get("shape") == shape]
    url = f"{BASE}/{name}"
    he_url = f"{BASE}/he/{name}"
    photo = cover(mine, cfg["cover"])
    share = image(photo, "w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto") if photo else ""
    title = html.escape(cfg["headline"] + " | Sherman Art Works", quote=True)
    out = landing
    for pattern, value, label in (
        (r"<title>.*?</title>", f"<title>{html.escape(cfg['title'])}</title>", "title"),
        (r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{title}" />', "og title"),
        (r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{url}" />', "og url"),
        (r'<meta property="og:image" content="[^"]*" />', f'<meta property="og:image" content="{share}" />', "og image"),
        (r'<meta name="twitter:title" content="[^"]*" />', f'<meta name="twitter:title" content="{title}" />', "twitter title"),
        (r'<meta name="twitter:image" content="[^"]*" />', f'<meta name="twitter:image" content="{share}" />', "twitter image"),
        (r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', "canonical"),
        (r'<link rel="alternate" hreflang="en" href="[^"]*" />', f'<link rel="alternate" hreflang="en" href="{url}" />', "alternate en"),
        (r'<link rel="alternate" hreflang="he-IL" href="[^"]*" />', f'<link rel="alternate" hreflang="he-IL" href="{he_url}" />', "alternate he"),
        (r'<link rel="alternate" hreflang="x-default" href="[^"]*" />', f'<link rel="alternate" hreflang="x-default" href="{url}" />', "alternate default"),
        (rf"location\.href='/he/{re.escape(PAGE)}'", f"location.href='/he/{name}'", "language toggle"),
    ):
        # A function, not a template: a value with a backslash or "\1" stays literal.
        out = replace_one(out, pattern, lambda m, v=value: v, f"{name} {label}")
    out = set_descriptions(out, meta_desc(products, shape), name)

    out = between(out, "<!-- hanukkah:jsonld -->", "  <!-- /hanukkah:jsonld -->", jsonld(mine), name)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sherman Art Works", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Hanukkah Menorahs", "item": f"{BASE}/{PAGE}"},
        {"@type": "ListItem", "position": 3, "name": cfg["headline"], "item": url},
    ]}
    out = replace_one(out, r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"BreadcrumbList".*?</script>',
                      lambda m: '<script type="application/ld+json">' + json.dumps(crumbs, separators=(",", ":")) + "</script>",
                      f"{name} breadcrumb list")

    # Shop · Hanukkah · <shape>, with Hanukkah linking back to all the menorahs.
    out = replace_one(out, r'<span data-t="bc_current">[^<]*</span>',
                      lambda m: (f'<a href="{PAGE}" data-t="cat9_title">Hanukkah</a>\n'
                                 '      <span class="breadcrumb-sep">·</span>\n'
                                 f'      <span data-t="bc_current">{html.escape(cfg["headline"])}</span>'),
                      f"{name} visible breadcrumb")
    for key, en, he in (("bc_current", cfg["headline"], cfg["he"]["headline"]),
                        ("hero_headline", cfg["headline"], cfg["he"]["headline"]),
                        ("hero_subtitle", cfg["subtitle"], cfg["he"]["subtitle"]),
                        ("hero_body", cfg["body"], cfg["he"]["body"])):
        if key != "bc_current":     # the breadcrumb above already wrote its text
            out = replace_one(out, rf'(<[^>]+data-t="{key}"[^>]*>)[^<]*(</[^>]+>)',
                              lambda m, v=en: m.group(1) + html.escape(v) + m.group(2), f"{name} {key}")
        # The runtime copy too, or setLang() would put the landing page's back.
        values = list(re.finditer(rf"({key}:\s+)'(?:\\.|[^'\\])*'", out))
        if len(values) != 2:
            raise RuntimeError(f"{name} {key}: expected an English and a Hebrew value")
        for m, v in reversed(list(zip(values, (en, he)))):
            out = out[:m.start()] + m.group(1) + repr(v) + out[m.end():]

    nav = switcher(NAV).replace(' class="cat-switch-item active" aria-current="page"', ' class="cat-switch-item"', 1)
    nav = nav.replace(f'href="{name}" class="cat-switch-item"',
                      f'href="{name}" class="cat-switch-item active" aria-current="page"')
    out = replace_one(out, rf'<nav class="cat-switch" aria-label="{NAV["aria"]}">.*?</nav>',
                      lambda m: nav, f"{name} switcher", re.S)
    out = between(out, "<!-- hanukkah:cards -->", "    <!-- /hanukkah:cards -->",
                  "\n".join(card(p) for p in mine), name)
    out = replace_one(out, r'<div class="products-grid" id="grid-products">',
                      lambda m: f'<div class="products-grid" id="grid-products" data-shape="{shape}">', f"{name} grid")
    return out


def build_index(src, products):
    shown = live(products)
    photo = cover(shown)
    src_attr = image(photo, "w_600,h_600,c_pad,b_rgb:faf7f2,q_auto,f_auto") if photo else "data:,"
    pat = re.compile(r'(<a href="hanukkah-menorahs\.html" class="cat-card">\s*'
                     r'<div class="cat-card-img-wrap">\s*<img [^>]*?src=")[^"]*(")', re.S)
    if not pat.search(src):
        raise RuntimeError("index.html: Hanukkah category card not found")
    src = pat.sub(lambda m: m.group(1) + src_attr + m.group(2), src, count=1)
    if not shown:
        return src
    # data-min-ils stays the regular price: js/site.js applies the sale to it at
    # runtime and strikes the old figure. The static text is what crawlers read,
    # so it carries the price a shopper pays today.
    low = min(shown, key=lambda item: item["price_ils"])
    regular = low["price_ils"]
    ils, usd = sale(regular, low["id"]), sale(usd_from_ils(regular), low["id"])
    pat = re.compile(r'(<a href="hanukkah-menorahs\.html" class="cat-card">.*?<span class="cat-card-from" data-min-ils=")'
                     r'\d+(">)[^<]*(</span>)', re.S)
    if not pat.search(src):
        raise RuntimeError("index.html: Hanukkah card price not found")
    return pat.sub(lambda m: f"{m.group(1)}{regular}{m.group(2)}from ₪{ils:,} · ${usd}{m.group(3)}", src, count=1)


def build_js(src, products):
    return between(src, "// <generated by _hanukkah_page.py>", "// </generated>",
                   js_array(products), JS)


def main():
    check = "--check" in sys.argv
    products = load()
    if not products:
        raise SystemExit("no hanukkah-menorahs products in data/products.json")
    unknown = sorted({str(p.get("shape")) for p in products} - set(SHAPES))
    if unknown:
        raise RuntimeError("no SHAPES entry for shape(s): " + ", ".join(unknown))
    stale, written = [], {}
    for rel, fn in ((PAGE, build_page), ("index.html", build_index), (JS, build_js)):
        path = SITE / rel
        src = path.read_text(encoding="utf-8")
        out = fn(src, products)
        written[rel] = out
        if out != src:
            stale.append(rel)
            if not check:
                path.write_text(out, encoding="utf-8")
    for shape, cfg in SHAPES.items():
        path = SITE / cfg["file"]
        out = build_shape_page(written[PAGE], products, shape)
        if not path.exists() or path.read_text(encoding="utf-8") != out:
            stale.append(cfg["file"])
            if not check:
                path.write_text(out, encoding="utf-8")
    if not check:
        ensure_mobile_navigation(NAV)
    shown = len(live(products))
    waiting = len(products) - shown
    note = f"{shown} of {len(products)} menorahs live" + (
        f", {waiting} waiting for a photo" if waiting else "")
    if not stale:
        print(f"Hanukkah page is current ({note})")
        return 0
    print(("stale: " if check else "wrote: ") + ", ".join(stale) + f" ({note})")
    return 1 if check else 0


if __name__ == "__main__":
    sys.exit(main())
