"""Generate subcategory pages from a category's landing page.

The landing page stays the source of truth for product data, card behaviour,
checkout and shared layout; each subcategory page is that same page with its
metadata, breadcrumb, hero copy, switcher, static cards and section registry
rewritten for a subset of the products.

Candlesticks and kiddush cups are the same shape, so they share one engine and
differ only in the CATEGORIES table below. Run after editing either landing page
or data/products.json.
"""

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).parent
BASE = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"
USD_RATE = 3.117

CANDLE_SILVER = "silver-plated-glass-candlesticks"
CANDLE_GOLD = "gold-plated-glass-candlesticks"


def family_is(*names):
    return lambda p: p.get("family_id") in names


def finish_is(name):
    return lambda p: p.get("finish") == name


# Each page's "match" selects its products. Exactly one page per category may
# use None, meaning "everything the others did not claim"; without one, a
# product matching nothing appears only on the landing page and is reported.
CATEGORIES = {
    "candlesticks": {
        "category": "candlesticks",
        "landing": "candlesticks.html",
        "landing_label": "Candlesticks",
        "landing_key": "cat1_title",
        "aria": "Candlestick categories",
        "prefix": "switch_candles_",
        "card_alt": "handmade glass candlesticks",
        "all_label": ("All Candlesticks", "כל הפמוטים"),
        "pages": {
            "silver": {
                "file": "candlesticks-silver-plated.html",
                "match": family_is(CANDLE_SILVER),
                "title": "925 Silver-Plated Glass Candlesticks | Sherman Art Works",
                "desc": "Shop handmade glass candlesticks finished with 925 silver plating. Seven colours, three heights, and optional matching trays, made in Israel.",
                "headline": "Silver-Plated Candlesticks",
                "subtitle": "Handmade glass finished with 925 silver.",
                "body": "Choose from seven colours and three heights, with an optional matching glass tray.",
                "bc": "Silver-Plated Candlesticks",
                "image": "White_pamotim_lrdkha",
                "he": {
                    "headline": "פמוטים בציפוי כסף",
                    "subtitle": "זכוכית בעבודת יד בגימור כסף 925.",
                    "body": "בחרו מתוך שבעה צבעים ושלושה גבהים, עם אפשרות למגש זכוכית תואם.",
                    "bc": "פמוטים בציפוי כסף",
                },
            },
            "gold": {
                "file": "candlesticks-gold-plated.html",
                "match": family_is(CANDLE_GOLD),
                "title": "Gold-Plated Glass Candlesticks | Sherman Art Works",
                "desc": "Shop handmade glass candlesticks finished with gold plating. Seven colours, three heights, and optional matching trays, made in Israel.",
                "headline": "Gold-Plated Candlesticks",
                "subtitle": "Handmade glass finished with gold.",
                "body": "Choose from seven colours and three heights, with an optional matching glass tray.",
                "bc": "Gold-Plated Candlesticks",
                "guide": {
                    "guide_q2": ("Are the gold-plated candlesticks solid gold?",
                                 "האם הפמוטים המצופים עשויים זהב מלא?"),
                    "guide_a2": ("No. They are handmade glass finished with gold plating, which gives the look and weight of gold at a lower price than solid gold.",
                                 "לא. אלה פמוטי זכוכית בעבודת יד עם ציפוי זהב, שמעניק את המראה והמשקל של זהב במחיר נמוך מזהב מלא."),
                },
                "image": "Blue_Pamotim_gold_1_kdduli",
                "he": {
                    "headline": "פמוטים בציפוי זהב",
                    "subtitle": "זכוכית בעבודת יד בגימור זהב.",
                    "body": "בחרו מתוך שבעה צבעים ושלושה גבהים, עם אפשרות למגש זכוכית תואם.",
                    "bc": "פמוטים בציפוי זהב",
                },
            },
            "artisanal": {
                "file": "candlesticks-artisanal.html",
                "match": None,
                "title": "Artisanal Handmade Glass Candlesticks | Sherman Art Works",
                "desc": "Shop artisanal glass candlesticks shaped and finished by hand in Israel, including colourful, striped, dotted, clear and Murano-style designs.",
                "headline": "Artisanal Candlesticks",
                "subtitle": "Expressive glasswork, shaped and finished by hand.",
                "body": "Explore colourful, striped, dotted, clear and Murano-style candlesticks made in our family studio.",
                "bc": "Artisanal Candlesticks",
                "guide": {
                    "guide_q2": ("Will my candlesticks look exactly like the photos?",
                                 "האם הפמוטים שאקבל ייראו בדיוק כמו בתמונות?"),
                    "guide_a2": ("Not exactly. Every pair is shaped and finished by hand, so colours, patterns and measurements vary a little from one pair to the next. The photographs show a representative pair rather than the exact one you will receive.",
                                 "לא בדיוק. כל זוג מעוצב ומוגמר בעבודת יד, ולכן הצבעים, הדוגמאות והמידות משתנים מעט מזוג לזוג. התמונות מציגות זוג לדוגמה ולא בדיוק את הזוג שתקבלו."),
                },
                "image": "Gold_colorful_pamotim_white_background_tlbsyf",
                "he": {
                    "headline": "פמוטים אומנותיים",
                    "subtitle": "עבודת זכוכית ייחודית, מעוצבת ומוגמרת ביד.",
                    "body": "גלו פמוטים צבעוניים, מפוספסים, מנוקדים, שקופים ובסגנון מוראנו מהסטודיו המשפחתי שלנו.",
                    "bc": "פמוטים אומנותיים",
                },
            },
        },
    },
    "kiddush-cups": {
        "category": "kiddush-cups",
        "landing": "kiddush-cups.html",
        "landing_label": "Kiddush Cups",
        "landing_key": "cat3_title",
        "aria": "Kiddush cup categories",
        "prefix": "switch_cups_",
        "card_alt": "handmade glass kiddush cup",
        "all_label": ("All Kiddush Cups", "כל כוסות הקידוש"),
        "pages": {
            "silver": {
                "file": "kiddush-cups-silver-plated.html",
                "match": None,
                "title": "925 Silver-Plated Kiddush Cups | Sherman Art Works",
                "desc": "Shop handmade kiddush cups finished with 925 silver plating, in a range of colours with optional matching plates, made in Israel.",
                "headline": "Silver-Plated Kiddush Cups",
                "subtitle": "Handmade glass and ceramic finished with 925 silver.",
                "body": "Choose your colour, with an optional matching plate at a set price.",
                "bc": "Silver-Plated Kiddush Cups",
                "image": "Blue_high_cup_fxhkep",
                "he": {
                    "headline": "כוסות קידוש בציפוי כסף",
                    "subtitle": "זכוכית וקרמיקה בעבודת יד בגימור כסף 925.",
                    "body": "בחרו את הצבע, עם אפשרות לצלחת תואמת במחיר מוזל.",
                    "bc": "כוסות קידוש בציפוי כסף",
                },
            },
            "gold": {
                "file": "kiddush-cups-gold-plated.html",
                "match": finish_is("gold-plated"),
                "title": "Gold-Plated Kiddush Cups | Sherman Art Works",
                "desc": "Shop handmade kiddush cups finished with gold plating, in a range of colours with optional matching plates, made in Israel.",
                "headline": "Gold-Plated Kiddush Cups",
                "subtitle": "Handmade glass finished with gold.",
                "body": "Choose your colour, with an optional matching plate at a set price.",
                "bc": "Gold-Plated Kiddush Cups",
                "guide": {
                    "guide_q2": ("Are the gold-plated kiddush cups solid gold?",
                                 "האם כוסות הקידוש המצופות עשויות זהב מלא?"),
                    "guide_a2": ("No. They are handmade glass finished with gold plating, which gives the look and weight of gold at a lower price than solid gold.",
                                 "לא. אלה כוסות זכוכית בעבודת יד עם ציפוי זהב, שמעניק את המראה והמשקל של זהב במחיר נמוך מזהב מלא."),
                },
                "image": "Blue_high_cup_fxhkep",
                "he": {
                    "headline": "כוסות קידוש בציפוי זהב",
                    "subtitle": "זכוכית בעבודת יד בגימור זהב.",
                    "body": "בחרו את הצבע, עם אפשרות לצלחת תואמת במחיר מוזל.",
                    "bc": "כוסות קידוש בציפוי זהב",
                },
            },
        },
    },
}


def replace_one(src, pattern, replacement, label, flags=0):
    out, count = re.subn(pattern, replacement, src, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return out


def products(cat):
    """Active products that actually appear on this landing page.

    Category alone is not enough: the kiddush cup plates are category
    kiddush-cups but sell on trays-bowls.html, so "pages" is the real test of
    what belongs here. Retired products keep active: False and belong on no
    page, the way the feed already treats them.
    """
    data = json.loads((SITE / "data/products.json").read_text(encoding="utf-8"))
    return [p for p in data
            if p.get("category") == cat["category"]
            and cat["landing"] in (p.get("pages") or [])
            and p.get("active") is not False]


def split(cat, items):
    """Map each page kind to its products, and report anything unclaimed."""
    pages = cat["pages"]
    claimed, buckets = set(), {}
    for kind, cfg in pages.items():
        if cfg["match"] is None:
            continue
        buckets[kind] = [p for p in items if cfg["match"](p)]
        claimed.update(p["id"] for p in buckets[kind])
    rest = [kind for kind, cfg in pages.items() if cfg["match"] is None]
    if len(rest) > 1:
        raise RuntimeError(f"{cat['landing']}: more than one catch-all page")
    if rest:
        buckets[rest[0]] = [p for p in items if p["id"] not in claimed]
    else:
        orphans = [p["id"] for p in items if p["id"] not in claimed]
        if orphans:
            print(f"  ! {cat['landing']}: on no subcategory page: {', '.join(orphans)}")
    return {kind: buckets.get(kind, []) for kind in pages}


def price(p):
    sizes = p.get("sizes") or []
    if sizes:
        return min(s["price_ils"] for s in sizes)
    return p["price_ils"]


def static_cards(cat, items):
    cards = []
    for p in items:
        ils = price(p)
        prefix = "from " if p.get("sizes") else ""
        cards.append(f"""    <article class="product-card" id="{html.escape(p['id'])}">
      <div class="product-card-img-wrap">
        <img src="{CDN}/w_600,c_fit,q_auto,f_auto/{p['photos'][0]}.jpg" alt="{html.escape(p['name_en'], quote=True)} - {cat['card_alt']}" loading="lazy" />
      </div>
      <div class="product-card-body">
        <h2 class="product-card-name">{html.escape(p['name_en'])}</h2>
        <p class="product-card-desc">{html.escape(p['description_en'])}</p>
        <div class="product-card-meta">
          <span class="product-card-price">{prefix}&#8362;{ils:,} <span class="product-card-price-alt">≈ ${round(ils / USD_RATE)}</span></span>
        </div>
        <p class="product-color-note">* Colors and measurements may appear slightly different in person, as each item is handmade.</p>
      </div>
    </article>""")
    return "\n".join(cards)


def item_list(cat, items):
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
                "url": f"{BASE}/{cat['landing']}#{p['id']}",
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


def switcher(cat):
    """The category pill row, with the landing page marked current."""
    lines = [f'<nav class="cat-switch" aria-label="{cat["aria"]}">',
             f'  <a href="{cat["landing"]}" class="cat-switch-item active" aria-current="page" '
             f'data-t="{cat["prefix"]}all">{cat["all_label"][0]}</a>']
    for kind, cfg in cat["pages"].items():
        lines.append(f'  <a href="{cfg["file"]}" class="cat-switch-item" '
                     f'data-t="{cat["prefix"]}{kind}">{cfg["headline"]}</a>')
    lines.append("</nav>")
    return "\n".join(lines)


def switch_keys(cat, lang):
    """The T_PAGE block for one language. Nav labels are the page headlines, so
    a renamed subcategory renames its pill without a second edit."""
    label = lambda cfg: cfg["headline"] if lang == "en" else cfg["he"]["headline"]
    out = [f"      {cat['prefix']}all: {(cat['all_label'][0] if lang == 'en' else cat['all_label'][1])!r},"]
    for kind, cfg in cat["pages"].items():
        out.append(f"      {cat['prefix']}{kind}: {label(cfg)!r},")
    return "\n".join(out) + "\n"


def ensure_landing_switcher(cat, src):
    """Install the switcher and its translation keys on the landing page.

    Both halves rewrite whatever is already there rather than bailing once a
    switcher exists, so adding a subcategory is only an edit to CATEGORIES. An
    earlier version skipped any page that already had an older set, which would
    have left every page a category behind.
    """
    nav = switcher(cat)
    if f'aria-label="{cat["aria"]}"' in src:
        src = replace_one(src, rf'<nav class="cat-switch" aria-label="{re.escape(cat["aria"])}">.*?</nav>',
                          lambda m: nav, "landing switcher", re.S)
    else:
        # Matched as a prefix: candlesticks.html opens the section bare while
        # kiddush-cups.html carries an id on it.
        marker = "</div>\n\n<section class=\"products-section\""
        if marker not in src:
            raise RuntimeError(f"{cat['landing']}: no anchor for the switcher")
        src = src.replace(marker, "</div>\n\n" + nav + "\n\n<section class=\"products-section\"", 1)

    last = list(cat["pages"])[-1]
    block_re = rf"      {cat['prefix']}all:.*?{cat['prefix']}{last}:[^\n]*\n"
    blocks = list(re.finditer(block_re, src, re.S))
    if blocks:
        if len(blocks) != 2:
            raise RuntimeError(f"{cat['landing']} switcher keys: expected two language blocks, found {len(blocks)}")
        for block, lang in reversed(list(zip(blocks, ("en", "he")))):
            src = src[:block.start()] + switch_keys(cat, lang) + src[block.end():]
    else:
        src = src.replace("      bc_shop:        'Shop',", switch_keys(cat, "en") + "\n      bc_shop:        'Shop',", 1)
        second = src.find("      bc_shop:", src.find("      bc_shop:") + 1)
        src = src[:second] + switch_keys(cat, "he") + "\n" + src[second:]
    return src


def ensure_mobile_navigation(cat):
    """Keep this category's children in the shared mobile shop menu in sync.

    Rewrites the sub-links already present rather than only inserting when there
    are none, so a new subcategory reaches every English page carrying the menu
    instead of only the ones that never had it.
    """
    anchor = (f'<a href="{cat["landing"]}" onclick="closeMobileNav()" '
              f'data-t="{cat["landing_key"]}">{cat["landing_label"]}</a>')
    sublinks = tuple(
        f'<a href="{cfg["file"]}" class="mobile-shop-sub" onclick="closeMobileNav()" '
        f'data-t="{cat["prefix"]}{kind}">{cfg["headline"]}</a>'
        for kind, cfg in cat["pages"].items())
    stem = cat["landing"][:-len(".html")]
    menu_re = re.compile(
        r'(?P<indent>[ \t]*)' + re.escape(anchor) +
        rf'(?:\s*<a href="{re.escape(stem)}-[^"]*" class="mobile-shop-sub"[^>]*>.*?</a>)*')

    def render(match):
        indent = match.group("indent")
        # Most pages pretty-print the menu one link per line; havdalah-sets.html
        # ships it minified on a single line, so follow whatever the page does
        # rather than injecting newlines into the middle of a minified tag run.
        if indent and match.string[:match.start()].endswith("\n"):
            joiner = "\n" + indent
            return indent + anchor + joiner + joiner.join(sublinks)
        return indent + anchor + "".join(sublinks)

    for path in SITE.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        if anchor not in text:
            continue
        updated = menu_re.sub(render, text, count=1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def build(cat, kind, cfg, source, items):
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
        (r'<link rel="alternate" hreflang="he-IL" href=".*?" />', f'<link rel="alternate" hreflang="he-IL" href="{he_url}" />', "alternate he"),
        (r'<link rel="alternate" hreflang="x-default" href=".*?" />', f'<link rel="alternate" hreflang="x-default" href="{url}" />', "alternate default"),
        (r'<meta name="twitter:title" content=".*?" />', f'<meta name="twitter:title" content="{html.escape(cfg["headline"], quote=True)} | Sherman Art Works" />', "twitter title"),
        (r'<meta name="twitter:description" content=".*?" />', f'<meta name="twitter:description" content="{html.escape(cfg["desc"], quote=True)}" />', "twitter description"),
        (r'<meta name="twitter:image" content=".*?" />', f'<meta name="twitter:image" content="{image}" />', "twitter image"),
    ]
    for pattern, replacement, label in replacements:
        out = replace_one(out, pattern, replacement, label)

    out = replace_one(out, rf"location\.href='/he/{re.escape(cat['landing'])}'",
                      f"location.href='/he/{cfg['file']}'", "language toggle")

    new_list = json.dumps(item_list(cat, items), ensure_ascii=False, separators=(",", ":"))
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sherman Art Works", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": cat["landing_label"], "item": f"{BASE}/{cat['landing']}"},
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
      <a href="{cat['landing']}" data-t="{cat['landing_key']}">{cat['landing_label']}</a>
      <span class="breadcrumb-sep">·</span>
      <span data-t="bc_current">{html.escape(cfg['bc'])}</span>"""
    out = replace_one(out, rf'      <a href="index\.html#shop" data-t="bc_shop">Shop</a>.*?<span data-t="bc_current">{re.escape(cat["landing_label"])}</span>',
                      breadcrumb, "visible breadcrumb", re.S)

    overrides = [
        ("bc_current", cfg["bc"], cfg["he"]["bc"]),
        ("hero_headline", cfg["headline"], cfg["he"]["headline"]),
        ("hero_subtitle", cfg["subtitle"], cfg["he"]["subtitle"]),
        ("hero_body", cfg["body"], cfg["he"]["body"]),
    ]
    overrides += [(key, en, he) for key, (en, he) in sorted(cfg.get("guide", {}).items())]

    # bc_current is already written by the breadcrumb replacement above; the
    # rest own a single data-t element each.
    for key, value, _he in overrides[1:]:
        out = replace_one(out, rf'(<[^>]+data-t="{key}"[^>]*>).*?(</[^>]+>)', rf'\1{html.escape(value)}\2', f"visible {key}")

    nav = switcher(cat)
    nav = nav.replace(' class="cat-switch-item active" aria-current="page"', ' class="cat-switch-item"', 1)
    nav = nav.replace(f'href="{cfg["file"]}" class="cat-switch-item"',
                      f'href="{cfg["file"]}" class="cat-switch-item active" aria-current="page"')
    out = replace_one(out, rf'<nav class="cat-switch" aria-label="{re.escape(cat["aria"])}">.*?</nav>',
                      lambda m: nav, "switcher", re.S)

    grid = static_cards(cat, items)
    # candlesticks.html closes the grid at column 0, kiddush-cups.html indents it.
    out = replace_one(out, r'(<div class="products-grid" id="grid-products">\n).*?(\n[ \t]*</div>\n</section>)',
                      lambda m: m.group(1) + "  <!-- Static EN product cards for SEO -->\n" + grid + m.group(2),
                      "static grid", re.S)
    out = replace_one(out, r'"products": \[[^\]]*\],',
                      '"products": ' + json.dumps(ids) + ',', "product ids")

    # Runtime translations must match the subcategory page rather than reset it
    # to the landing-page copy when setLang() runs.
    for key, en_value, he_value in overrides:
        matches = list(re.finditer(rf"({key}:\s+)'[^']*'", out))
        if len(matches) != 2:
            raise RuntimeError(f"{cfg['file']} {key}: expected two language values")
        for match, value in reversed(list(zip(matches, (en_value, he_value)))):
            out = out[:match.start()] + match.group(1) + repr(value) + out[match.end():]

    out = re.sub(r"[ \t]+$", "", out, flags=re.M)
    (SITE / cfg["file"]).write_text(out, encoding="utf-8")
    print(f"{cfg['file']}: {len(items)} products")


def main():
    for cat in CATEGORIES.values():
        ensure_mobile_navigation(cat)
        source_path = SITE / cat["landing"]
        source = ensure_landing_switcher(cat, source_path.read_text(encoding="utf-8"))
        source_path.write_text(source, encoding="utf-8")
        buckets = split(cat, products(cat))
        for kind, cfg in cat["pages"].items():
            build(cat, kind, cfg, source, buckets[kind])


if __name__ == "__main__":
    main()
