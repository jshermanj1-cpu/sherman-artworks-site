# -*- coding: utf-8 -*-
"""_hanukkah_page.py - build the Hanukkah menorah page from data/products.json.

Every menorah exists twice over - seven glass colours, each with silver-tone or
gold-tone sockets and base - so the page carries fourteen products, and a
photo or a price lives on five surfaces of it at once: the runtime catalogue in
js/hanukkah-menorahs.js, the no-JS cards crawlers read, two ProductGroup blocks,
the share image, and the homepage category card. Hand-keeping five copies in
step is how every other category on this site drifted, so here data/products.json
is the only copy anyone edits and this script writes the rest.

What it owns, each between marker comments so nothing around it is touched:

  js/hanukkah-menorahs.js   the PRODUCTS array (all fourteen, photo or not)
  hanukkah-menorahs.html    static cards + ProductGroup JSON-LD + og/twitter image
  index.html                the Hanukkah category card's image

A menorah with no photo yet is held back: products.json marks it
"active": false, and it gets no static card, no JSON-LD and no feed item until
_menorah_photos.py (or a hand edit) gives it one. The runtime array keeps it, so
the page can be previewed while photos are still being shot.

    python _hanukkah_page.py           write in place
    python _hanukkah_page.py --check   report only, exit 1 if anything is stale
"""

import html
import json
import re
import sys
from pathlib import Path

from _usd import usd_from_ils

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
COVER = "silver-tone-blue-half-moon-menorah"

# One ProductGroup per family_id: a shape in one finish, its variants the glass
# colours. A new shape means new families here (and in _he_pages.py's
# PRODUCT_GROUP_HE), never a rename of these - productGroupID is what Google keys
# the variants on.
GROUPS = {
    "silver-tone-half-moon-hanukkah-menorahs": {
        "name": "Half-Moon Glass Hanukkah Menorahs with Silver-Tone Sockets",
        "description": "Handmade half-moon Hanukkah menorahs of double-sided glass in seven colours, "
                       "with silver-tone sockets and base, crafted in our studio in Israel."},
    "gold-tone-half-moon-hanukkah-menorahs": {
        "name": "Half-Moon Glass Hanukkah Menorahs with Gold-Tone Sockets",
        "description": "Handmade half-moon Hanukkah menorahs of double-sided glass in seven colours, "
                       "with gold-tone sockets and base, crafted in our studio in Israel."},
}

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
    ils = p["price_ils"]
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
        f'          <span class="product-card-price">&#8362;{ils:,} '
        f'<span class="product-card-price-alt">≈ ${usd_from_ils(ils)}</span></span>\n'
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


def cover(products):
    by_id = {p["id"]: p for p in products}
    if COVER in by_id:
        return by_id[COVER]["photos"][0]
    return products[0]["photos"][0] if products else None


def between(text, start, end, inner, label):
    """Replace what sits between two marker comments. Raises if they are missing."""
    pat = re.compile(re.escape(start) + r"\n.*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise RuntimeError(f"{label}: markers {start!r} ... {end!r} not found")
    body = (inner + "\n") if inner else ""
    return pat.sub(lambda m: start + "\n" + body + end, text, count=1)


def build_page(src, products):
    shown = live(products)
    indent = "  "
    out = between(src, "<!-- hanukkah:jsonld -->", indent + "<!-- /hanukkah:jsonld -->",
                  jsonld(shown), PAGE)
    out = between(out, "<!-- hanukkah:cards -->", "    <!-- /hanukkah:cards -->",
                  "\n".join(card(p) for p in shown), PAGE)
    photo = cover(shown)
    share = image(photo, "w_1200,h_630,c_pad,b_rgb:faf7f2,q_auto,f_auto") if photo else ""
    for attr, key in (("property", "og:image"), ("name", "twitter:image")):
        out = re.sub(rf'<meta {attr}="{key}" content="[^"]*" />',
                     f'<meta {attr}="{key}" content="{share}" />', out, count=1)
    return out


def build_index(src, products):
    photo = cover(live(products))
    src_attr = image(photo, "w_600,h_600,c_pad,b_rgb:faf7f2,q_auto,f_auto") if photo else "data:,"
    pat = re.compile(r'(<a href="hanukkah-menorahs\.html" class="cat-card">\s*'
                     r'<div class="cat-card-img-wrap">\s*<img [^>]*?src=")[^"]*(")', re.S)
    if not pat.search(src):
        raise RuntimeError("index.html: Hanukkah category card not found")
    return pat.sub(lambda m: m.group(1) + src_attr + m.group(2), src, count=1)


def build_js(src, products):
    return between(src, "// <generated by _hanukkah_page.py>", "// </generated>",
                   js_array(products), JS)


def main():
    check = "--check" in sys.argv
    products = load()
    if not products:
        raise SystemExit("no hanukkah-menorahs products in data/products.json")
    stale = []
    for rel, fn in ((PAGE, build_page), ("index.html", build_index), (JS, build_js)):
        path = SITE / rel
        src = path.read_text(encoding="utf-8")
        out = fn(src, products)
        if out != src:
            stale.append(rel)
            if not check:
                path.write_text(out, encoding="utf-8")
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
