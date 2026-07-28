"""Generate candlestick subcategory pages from candlesticks.html.

The landing page remains the source of truth for product data, card behaviour,
checkout, and shared layout. Run this after editing candlesticks.html or
data/products.json.
"""

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).parent
BASE = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"
USD_RATE = 3.117

SILVER_FAMILY = "silver-plated-glass-candlesticks"

PAGES = {
    "silver": {
        "file": "candlesticks-silver-plated.html",
        "title": "925 Silver-Plated Glass Candlesticks | Sherman Art Works",
        "desc": "Shop handmade glass candlesticks finished with 925 sterling-silver plating. Seven colours, three heights, and optional matching trays, made in Israel.",
        "headline": "Silver-Plated Candlesticks",
        "subtitle": "Handmade glass finished with 925 sterling silver.",
        "body": "Choose from seven colours and three heights, with an optional matching glass tray.",
        "bc": "Silver-Plated Candlesticks",
        "image": "White_pamotim_lrdkha",
        "he": {
            "headline": "פמוטים בציפוי כסף",
            "subtitle": "זכוכית בעבודת יד בגימור כסף סטרלינג 925.",
            "body": "בחרו מתוך שבעה צבעים ושלושה גבהים, עם אפשרות למגש זכוכית תואם.",
            "bc": "פמוטים בציפוי כסף",
        },
    },
    "artisanal": {
        "file": "candlesticks-artisanal.html",
        "title": "Artisanal Handmade Glass Candlesticks | Sherman Art Works",
        "desc": "Shop artisanal glass candlesticks shaped and finished by hand in Israel, including colourful, striped, dotted, clear and Murano-style designs.",
        "headline": "Artisanal Candlesticks",
        "subtitle": "Expressive glasswork, shaped and finished by hand.",
        "body": "Explore colourful, striped, dotted, clear and Murano-style candlesticks made in our family studio.",
        "bc": "Artisanal Candlesticks",
        "image": "Gold_colorful_pamotim_white_background_tlbsyf",
        "he": {
            "headline": "פמוטים אומנותיים",
            "subtitle": "עבודת זכוכית ייחודית, מעוצבת ומוגמרת ביד.",
            "body": "גלו פמוטים צבעוניים, מפוספסים, מנוקדים, שקופים ובסגנון מוראנו מהסטודיו המשפחתי שלנו.",
            "bc": "פמוטים אומנותיים",
        },
    },
}

SWITCHER_EN = """<nav class="cat-switch" aria-label="Candlestick categories">
  <a href="candlesticks.html" class="cat-switch-item active" aria-current="page" data-t="switch_candles_all">All Candlesticks</a>
  <a href="candlesticks-silver-plated.html" class="cat-switch-item" data-t="switch_candles_silver">Silver-Plated Candlesticks</a>
  <a href="candlesticks-artisanal.html" class="cat-switch-item" data-t="switch_candles_artisanal">Artisanal Candlesticks</a>
</nav>"""


def products():
    data = json.loads((SITE / "data/products.json").read_text(encoding="utf-8"))
    return [p for p in data if p.get("category") == "candlesticks"]


def page_products(kind, items):
    if kind == "silver":
        return [p for p in items if p.get("family_id") == SILVER_FAMILY]
    return [p for p in items if p.get("family_id") != SILVER_FAMILY]


def price(p):
    sizes = p.get("sizes") or []
    if sizes:
        return min(s["price_ils"] for s in sizes)
    return p["price_ils"]


def static_cards(items):
    cards = []
    for p in items:
        ils = price(p)
        prefix = "from " if p.get("sizes") else ""
        cards.append(f"""    <article class="product-card" id="{html.escape(p['id'])}">
      <div class="product-card-img-wrap">
        <img src="{CDN}/w_600,c_fit,q_auto,f_auto/{p['photos'][0]}.jpg" alt="{html.escape(p['name_en'], quote=True)} - handmade glass candlesticks" loading="lazy" />
      </div>
      <div class="product-card-body">
        <h2 class="product-card-name">{html.escape(p['name_en'])}</h2>
        <p class="product-card-desc">{html.escape(p['description_en'])}</p>
        <div class="product-card-meta">
          <span class="product-card-price">{prefix}&#8362;{ils:,} <span class="product-card-price-alt">≈ ${round(ils / USD_RATE)}</span></span>
        </div>
        <p class="product-color-note">* Colors may appear slightly different in person, as each item is handmade.</p>
      </div>
    </article>""")
    return "\n".join(cards)


def replace_one(src, pattern, replacement, label, flags=0):
    out, count = re.subn(pattern, replacement, src, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return out


def item_list(items):
    elements = []
    for position, p in enumerate(items, 1):
        ils = price(p)
        elements.append({
            "@type": "ListItem",
            "position": position,
            "item": {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": p["name_en"],
                "url": f"{BASE}/candlesticks.html#{p['id']}",
                "description": p["description_en"],
                "image": [f"{CDN}/w_800,q_auto,f_auto/{photo}.jpg" for photo in p["photos"]],
                "brand": {"@type": "Brand", "name": "Sherman Art Works"},
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "ILS",
                    "price": str(ils),
                    "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "Sherman Art Works"},
                },
                "sku": p["sku"],
                "itemCondition": "https://schema.org/NewCondition",
            },
        })
    return {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": elements}


def ensure_landing_switcher(src):
    if 'aria-label="Candlestick categories"' not in src:
        marker = "</div>\n\n<section class=\"products-section\">"
        src = src.replace(marker, "</div>\n\n" + SWITCHER_EN + "\n\n<section class=\"products-section\">", 1)
    keys = """      switch_candles_all: 'All Candlesticks',
      switch_candles_silver: 'Silver-Plated Candlesticks',
      switch_candles_artisanal: 'Artisanal Candlesticks',
"""
    if "switch_candles_all:" not in src:
        src = src.replace("      bc_shop:        'Shop',", keys + "\n      bc_shop:        'Shop',", 1)
        he_keys = """      switch_candles_all: 'כל הפמוטים',
      switch_candles_silver: 'פמוטים בציפוי כסף',
      switch_candles_artisanal: 'פמוטים אומנותיים',
"""
        second = src.find("      bc_shop:", src.find("      bc_shop:") + 1)
        src = src[:second] + he_keys + "\n" + src[second:]
    return src


def ensure_mobile_navigation():
    """Add the candlestick children wherever the shared mobile shop menu exists."""
    anchor = ('          <a href="candlesticks.html" onclick="closeMobileNav()" '
              'data-t="cat1_title">Candlesticks</a>')
    children = anchor + """
          <a href="candlesticks-silver-plated.html" class="mobile-shop-sub" onclick="closeMobileNav()" data-t="switch_candles_silver">Silver-Plated Candlesticks</a>
          <a href="candlesticks-artisanal.html" class="mobile-shop-sub" onclick="closeMobileNav()" data-t="switch_candles_artisanal">Artisanal Candlesticks</a>"""
    for path in SITE.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        if anchor in text and 'href="candlesticks-silver-plated.html" class="mobile-shop-sub"' not in text:
            path.write_text(text.replace(anchor, children, 1), encoding="utf-8")


def build(kind, cfg, source, all_items):
    items = page_products(kind, all_items)
    ids = [p["id"] for p in items]
    out = source
    url = f"{BASE}/{cfg['file']}"
    he_url = f"{BASE}/he/{cfg['file']}"
    image = f"{CDN}/w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto/{cfg['image']}.jpg"

    replacements = [
        (r"<title>.*?</title>", f"<title>{html.escape(cfg['title'])}</title>", "title"),
        (r'<meta name="description" content=".*?" />', f'<meta name="description" content="{html.escape(cfg["desc"], quote=True)}" />', "description"),
        (r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{html.escape(cfg["headline"], quote=True)} | Sherman Art Works" />', "og title"),
        (r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{html.escape(cfg["desc"], quote=True)}" />', "og description"),
        (r'<meta property="og:image" content=".*?" />', f'<meta property="og:image" content="{image}" />', "og image"),
        (r'<meta property="og:url" content=".*?" />', f'<meta property="og:url" content="{url}" />', "og url"),
        (r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{url}" />', "canonical"),
        (r'<link rel="alternate" hreflang="en" href=".*?" />', f'<link rel="alternate" hreflang="en" href="{url}" />', "alternate en"),
        (r'<link rel="alternate" hreflang="he" href=".*?" />', f'<link rel="alternate" hreflang="he" href="{he_url}" />', "alternate he"),
        (r'<link rel="alternate" hreflang="x-default" href=".*?" />', f'<link rel="alternate" hreflang="x-default" href="{url}" />', "alternate default"),
        (r'<meta name="twitter:title" content=".*?" />', f'<meta name="twitter:title" content="{html.escape(cfg["headline"], quote=True)} | Sherman Art Works" />', "twitter title"),
        (r'<meta name="twitter:description" content=".*?" />', f'<meta name="twitter:description" content="{html.escape(cfg["desc"], quote=True)}" />', "twitter description"),
        (r'<meta name="twitter:image" content=".*?" />', f'<meta name="twitter:image" content="{image}" />', "twitter image"),
    ]
    for pattern, replacement, label in replacements:
        out = replace_one(out, pattern, replacement, label)

    out = replace_one(out, r"location\.href='/he/candlesticks\.html'", f"location.href='/he/{cfg['file']}'", "language toggle")

    new_list = json.dumps(item_list(items), ensure_ascii=False, separators=(",", ":"))
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sherman Art Works", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Candlesticks", "item": f"{BASE}/candlesticks.html"},
        {"@type": "ListItem", "position": 3, "name": cfg["bc"], "item": url},
    ]}
    out = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", out, flags=re.S)
    structured = (
        f'  <script type="application/ld+json">{new_list}</script>\n'
        '  <script type="application/ld+json">' +
        json.dumps(crumbs, separators=(",", ":")) + '</script>\n  '
    )
    out = replace_one(out, r'  <link rel="canonical"', structured + '<link rel="canonical"', "structured data anchor")

    breadcrumb = f"""      <a href="index.html#shop" data-t="bc_shop">Shop</a>
      <span class="breadcrumb-sep">·</span>
      <a href="candlesticks.html" data-t="cat1_title">Candlesticks</a>
      <span class="breadcrumb-sep">·</span>
      <span data-t="bc_current">{html.escape(cfg['bc'])}</span>"""
    out = replace_one(out, r'      <a href="index\.html#shop" data-t="bc_shop">Shop</a>.*?<span data-t="bc_current">Candlesticks</span>',
                      breadcrumb, "visible breadcrumb", re.S)

    for key, value in (("hero_headline", cfg["headline"]), ("hero_subtitle", cfg["subtitle"]), ("hero_body", cfg["body"])):
        out = replace_one(out, rf'(<[^>]+data-t="{key}"[^>]*>).*?(</[^>]+>)', rf'\1{html.escape(value)}\2', f"visible {key}")

    switcher = SWITCHER_EN.replace(' class="cat-switch-item active" aria-current="page"', ' class="cat-switch-item"', 1)
    switcher = switcher.replace(f'href="{cfg["file"]}" class="cat-switch-item"',
                                f'href="{cfg["file"]}" class="cat-switch-item active" aria-current="page"')
    out = replace_one(out, r'<nav class="cat-switch" aria-label="Candlestick categories">.*?</nav>',
                      switcher, "switcher", re.S)

    grid = static_cards(items)
    out = replace_one(out, r'(<div class="products-grid" id="grid-products">\n).*?(\n</div>\n</section>)',
                      r'\1  <!-- Static EN product cards for SEO -->\n' + grid + r'\2', "static grid", re.S)
    out = replace_one(out, r'"products": \[[^\]]*\],',
                      '"products": ' + json.dumps(ids) + ',', "product ids")

    # Runtime translations must match the subcategory page rather than reset it
    # to the landing-page copy when setLang() runs.
    for key, en_value, he_value in (
        ("bc_current", cfg["bc"], cfg["he"]["bc"]),
        ("hero_headline", cfg["headline"], cfg["he"]["headline"]),
        ("hero_subtitle", cfg["subtitle"], cfg["he"]["subtitle"]),
        ("hero_body", cfg["body"], cfg["he"]["body"]),
    ):
        matches = list(re.finditer(rf"({key}:\s+)'[^']*'", out))
        if len(matches) != 2:
            raise RuntimeError(f"{cfg['file']} {key}: expected two language values")
        for match, value in reversed(list(zip(matches, (en_value, he_value)))):
            out = out[:match.start()] + match.group(1) + repr(value) + out[match.end():]

    out = re.sub(r"[ \t]+$", "", out, flags=re.M)
    (SITE / cfg["file"]).write_text(out, encoding="utf-8")
    print(f"{cfg['file']}: {len(items)} products")


def main():
    ensure_mobile_navigation()
    source_path = SITE / "candlesticks.html"
    source = ensure_landing_switcher(source_path.read_text(encoding="utf-8"))
    source_path.write_text(source, encoding="utf-8")
    items = products()
    for kind, cfg in PAGES.items():
        build(kind, cfg, source, items)


if __name__ == "__main__":
    main()
