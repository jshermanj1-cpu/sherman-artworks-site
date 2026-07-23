"""Generate the three shofar sub-category pages from shofars.html.

shofars.html is the template AND the landing page (every shofar, shuffled).
This script derives shofars-custom.html, shofars-rams.html and shofars-kudu.html
from it, so the nav, footer, modal and page JS only ever exist in one file.

    python _shofar_pages.py

Rerun it after ANY edit to shofars.html, js/shofar-products.js or the shofar
price table - the generated pages carry static SEO copies of the product cards
and their own JSON-LD, and those go stale silently otherwise.

What differs per page: title/meta/OG/canonical, the breadcrumb, the hero copy,
which switcher chip is active, the static product cards, the JSON-LD, PAGE_KEY,
and the ram's-horn plating notes block. Everything else is copied verbatim.
"""

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).parent
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"
BASE = "https://shermanartworks.com"
USD_RATE = 3.117  # keep in step with the static "≈ $" figures in shofars.html
COLOR_NOTE = "* Colors may appear slightly different in person, as each item is handmade."

# Minimum price per size ladder - the "from ₪X" on a card, for the no-JS view.
SIZE_MIN = {
    "RAMS_SIZES": 418, "RAMS_CUSTOM_SIZES": 742,
    "KUDU_SIZES": 1214, "KUDU_CUSTOM_SIZES": 1297,
}

PAGES = {
    "custom": {
        "file": "shofars-custom.html",
        "title": "Custom Shofars - Personalised Ram's & Kudu | Sherman Art Works",
        "desc": "Order a custom shofar - ram's horn or kudu, hand-plated in 925 silver and engraved with the symbol you choose plus an optional Hebrew or English inscription.",
        "og_title": "Custom Shofars, Sherman Art Works",
        "hero_headline": "Custom Shofars",
        "hero_subtitle": "Your symbol, your inscription.",
        "hero_body": "Ram's-horn and kudu shofars made to order with an engraved symbol of your choice and an optional inscription in Hebrew or English.",
        "bc": "Custom Shofars",
        "image": "Cover_silver_Magen_David_with_name_adq1oi",
        "notes": False,
    },
    "rams": {
        "file": "shofars-rams.html",
        "title": "Ram's Horn Shofars, Hand-Plated in 925 Silver | Sherman Art Works",
        "desc": "Kosher ram's-horn shofars from 30 to 65 cm, each hand-decorated and plated in 925 silver in our studio in Israel. Ten designs plus a fully personalised option.",
        "og_title": "Ram's Horn Shofars, Sherman Art Works",
        "hero_headline": "Ram's Horn Shofars",
        "hero_subtitle": "Decorated by hand in 925 silver.",
        "hero_body": "Natural kosher ram's-horn shofars from 30 to 65 cm, each hand-plated in 925 silver. Start with the personalised one, or choose a design and size.",
        "bc": "Ram's Horn Shofars",
        "image": "Magen_David_1_ram_pgvhoa",
        "notes": True,
    },
    "kudu": {
        "file": "shofars-kudu.html",
        "title": "Kudu Shofars, Hand-Plated in 925 Silver | Sherman Art Works",
        "desc": "Kosher kudu-horn shofars up to 129 cm, each hand-decorated and plated in 925 silver in our studio in Israel. Ten designs plus a fully personalised option.",
        "og_title": "Kudu Shofars, Sherman Art Works",
        "hero_headline": "Kudu Shofars",
        "hero_subtitle": "Decorated by hand in 925 silver.",
        "hero_body": "Natural kosher kudu-horn shofars up to 129 cm long, each hand-plated in 925 silver. Start with the personalised one, or choose a design and size.",
        "bc": "Kudu Shofars",
        "image": "Kudu_Jerusalem_Lions_xelufl",
        "notes": False,
    },
}

PLATING_NOTE_EN = ("The silver plating sometimes comes as one continuous piece, and sometimes in two "
                   "parts, depending on the shape and size of the horn. If you have a preference, open "
                   "the shofar you want and write it in the comment box before ordering.")


def load_products():
    """Parse js/shofar-products.js. Size ladders are bare identifiers, so they
    are quoted before the array is read as JSON."""
    js = (SITE / "js" / "shofar-products.js").read_text(encoding="utf-8")
    body = re.search(r"const PRODUCTS = \[\n(.*?)\n\];", js, re.S).group(1)
    quoted = re.sub(r": ([A-Z][A-Z_]+)(,?)$", r': "\1"\2', body, flags=re.M)
    return json.loads("[\n" + quoted + "\n]")


def page_ids(key, products):
    """Mirrors PAGE_GROUPS in js/shofar-products.js."""
    if key == "custom":
        return ["custom-shofar", "custom-kudu-shofar"]
    if key == "rams":
        return ["custom-shofar"] + [p["id"] for p in products if p["id"].startswith("rams-")]
    if key == "kudu":
        return ["custom-kudu-shofar"] + [p["id"] for p in products if p["id"].startswith("kudu-")]
    return [p["id"] for p in products]


def min_price(p):
    return SIZE_MIN[p["sizes"]] if p.get("sizes") else p["price_ils"]


def static_cards(items):
    out = []
    for p in items:
        ils = min_price(p)
        alt = html.escape(f'{p["name_en"]}, handmade shofar decorated in 925 silver from Sherman Art Works', quote=True)
        out.append(f'''    <article class="product-card">
      <div class="product-card-img-wrap">
        <img src="{CDN}/w_600,c_fit,q_auto,f_auto/{p["photos"][0]}.jpg" alt="{alt}" loading="lazy" />
      </div>
      <div class="product-card-body">
        <h3 class="product-card-name">{html.escape(p["name_en"])}</h3>
        <p class="product-card-desc">{html.escape(p["description_en"])}</p>
        <div class="product-card-meta">
          <span class="product-card-price">from &#8362;{ils:,} <span class="product-card-price-alt">≈ ${round(ils / USD_RATE)}</span></span>
        </div>
        <p class="product-color-note">{COLOR_NOTE}</p>
      </div>
    </article>''')
    return "\n".join(out)


def build(key, cfg, src, products):
    out = src
    ids = page_ids(key, products)
    by_id = {p["id"]: p for p in products}
    items = [by_id[i] for i in ids]

    def sub1(pattern, repl, label, flags=0):
        nonlocal out
        out, n = re.subn(pattern, lambda m: repl, out, flags=flags)
        assert n == 1, f"{cfg['file']}: {label} matched {n} times"

    url = f"{BASE}/{cfg['file']}"
    img = f"{CDN}/w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto/{cfg['image']}.jpg"

    # ── head ──
    sub1(r"<title>.*?</title>", f"<title>{html.escape(cfg['title'])}</title>", "title")
    sub1(r'<meta name="description" content=".*?" />',
         f'<meta name="description" content="{html.escape(cfg["desc"], quote=True)}" />', "description")
    sub1(r'<meta property="og:title" content=".*?" />',
         f'<meta property="og:title" content="{html.escape(cfg["og_title"], quote=True)}" />', "og:title")
    sub1(r'<meta property="og:description" content=".*?" />',
         f'<meta property="og:description" content="{html.escape(cfg["desc"], quote=True)}" />', "og:description")
    sub1(r'<meta property="og:image" content=".*?" />',
         f'<meta property="og:image" content="{img}" />', "og:image")
    sub1(r'<meta property="og:url" content=".*?" />',
         f'<meta property="og:url" content="{url}" />', "og:url")
    sub1(r'<link rel="canonical" href=".*?" />',
         f'<link rel="canonical" href="{url}" />', "canonical")
    sub1(r'<meta name="twitter:title" content=".*?" />',
         f'<meta name="twitter:title" content="{html.escape(cfg["og_title"], quote=True)}" />', "twitter:title")
    sub1(r'<meta name="twitter:description" content=".*?" />',
         f'<meta name="twitter:description" content="{html.escape(cfg["desc"], quote=True)}" />', "twitter:description")
    sub1(r'<meta name="twitter:image" content=".*?" />',
         f'<meta name="twitter:image" content="{img}" />', "twitter:image")

    # ── JSON-LD: this page's products, and a three-level breadcrumb ──
    ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    item_list = json.loads(ld_blocks[0])
    keep = {i: e for e in item_list["itemListElement"] for i in [e["item"]["sku"]]}
    item_list["itemListElement"] = [
        {**keep[i], "position": n} for n, i in enumerate(ids, start=1) if i in keep
    ]
    # Product urls stay on shofars.html#<id> - one canonical identity per product,
    # which is also what merchant-feed.xml and llms.txt link to.
    sub1(re.escape(f'<script type="application/ld+json">{ld_blocks[0]}</script>'),
         '<script type="application/ld+json">' + json.dumps(item_list, ensure_ascii=False, separators=(",", ":")) + '</script>',
         "ItemList")

    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sherman Art Works", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Shofars", "item": f"{BASE}/shofars.html"},
        {"@type": "ListItem", "position": 3, "name": cfg["bc"], "item": url},
    ]}
    sub1(re.escape(f'<script type="application/ld+json">{ld_blocks[1]}</script>'),
         '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False, separators=(",", ":")) + '</script>',
         "BreadcrumbList")

    # ── breadcrumb trail ──
    sub1(r'      <a href="index\.html#shop" data-t="bc_shop">Shop</a>\n'
         r'      <span class="breadcrumb-sep">·</span>\n'
         r'      <span data-t="bc_current">Shofars</span>',
         '      <a href="index.html#shop" data-t="bc_shop">Shop</a>\n'
         '      <span class="breadcrumb-sep">·</span>\n'
         '      <a href="shofars.html" data-t="bc_shofars">Shofars</a>\n'
         '      <span class="breadcrumb-sep">·</span>\n'
         f'      <span data-t="bc_current">{html.escape(cfg["bc"])}</span>', "breadcrumb")

    # ── hero copy (JS re-applies it per language; this is the no-JS view) ──
    sub1(r'<h1 class="page-headline" data-t="hero_headline">.*?</h1>',
         f'<h1 class="page-headline" data-t="hero_headline">{html.escape(cfg["hero_headline"])}</h1>', "h1")
    sub1(r'<p class="page-subtitle"  data-t="hero_subtitle">.*?</p>',
         f'<p class="page-subtitle"  data-t="hero_subtitle">{html.escape(cfg["hero_subtitle"])}</p>', "subtitle")
    sub1(r'<p class="page-body"      data-t="hero_body">.*?</p>',
         f'<p class="page-body"      data-t="hero_body">{html.escape(cfg["hero_body"])}</p>', "body")

    # ── switcher: move the active chip ──
    out = out.replace(' class="cat-switch-item active" aria-current="page"', ' class="cat-switch-item"')
    out = re.sub(rf'(<a href="{re.escape(cfg["file"])}"\s+)class="cat-switch-item"',
                 r'\1class="cat-switch-item active" aria-current="page"', out)
    assert out.count('cat-switch-item active') == 1, f"{cfg['file']}: switcher active chip"

    # ── static product cards ──
    grid = re.search(r'(<div class="products-grid" id="grid-all">\n'
                     r'  <!-- Static EN product cards for SEO \(replaced by JS on load\) -->\n)(.*?)(\n  </div>)', out, re.S)
    assert grid, f"{cfg['file']}: product grid"
    out = out[:grid.start(2)] + static_cards(items) + out[grid.end(2):]

    # ── ram's-horn plating notes, under the grid ──
    if cfg["notes"]:
        notes = ('\n  <aside class="section-notes" aria-labelledby="notesTitle">\n'
                 '    <div class="section-notes-title" id="notesTitle" data-t="notes_title">Notes</div>\n'
                 f'    <p class="section-notes-body" data-t="plating_note_section">{html.escape(PLATING_NOTE_EN)}</p>\n'
                 '  </aside>\n')
        close = out.index("</section>", out.index('id="grid-all"'))
        out = out[:close] + notes + out[close:]

    # ── page config ──
    sub1(r"const PAGE_KEY = 'all';", f"const PAGE_KEY = '{key}';", "PAGE_KEY")

    # ── generated-file banner ──
    out = out.replace("<!DOCTYPE html>",
                      "<!DOCTYPE html>\n<!-- GENERATED by _shofar_pages.py from shofars.html - do not edit directly. -->", 1)
    return out


def main():
    src = (SITE / "shofars.html").read_text(encoding="utf-8")
    products = load_products()
    for key, cfg in PAGES.items():
        (SITE / cfg["file"]).write_text(build(key, cfg, src, products), encoding="utf-8")
        print(f"wrote {cfg['file']} ({len(page_ids(key, products))} products)")


if __name__ == "__main__":
    main()
