# -*- coding: utf-8 -*-
"""
_sync_cards.py — resync the static English product cards to the inline PRODUCTS
source of truth, and fix two latent gaps QA found:

  1. Description drift — 9 static .product-card-desc paragraphs (horn-goblets,
     kiddush-cups ×3, trays-bowls, mezuzahs ×4) carry an older/edited wording
     than the current PRODUCTS description_en ("Made to order in Israel." vs
     "…in our studio in Israel."). The static (no-JS/crawler) view therefore
     disagreed with the JS-rendered view. Resynced to the source first line.

  2. business-gifts.html carried ONE generic "Custom Shofar" SEO card, but the
     catalogue now has TWO products (custom-shofar, custom-kudu-shofar). The
     static grid is rebuilt to the two real cards so crawlers see both.

  3. business-gifts.html was missing the spec_size key in its T_PAGE dict, so the
     modal "Size" label stayed English even in the site's own Hebrew toggle.
     Added spec_size to the en + he dictionaries.

Raw-text edits only (no bs4 re-serialisation) so the live English pages keep
minimal, reviewable diffs. Idempotent. Re-run js/_he_pages.py afterwards to
regenerate the Hebrew twins from the corrected English source.
"""

import os
import re
import html
import importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))

# Reuse the extractor + normaliser from the Hebrew generator.
_spec = importlib.util.spec_from_file_location("hegen", os.path.join(ROOT, "_he_pages.py"))
hegen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hegen)
norm, first, field_values = hegen.norm, hegen._first, hegen._field_values

SHOP_PAGES = hegen.SHOP_PAGES
PRODUCT_JS = hegen.PRODUCT_JS


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def esc(s):
    """Escape for HTML text content (leave quotes/apostrophes literal)."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── source records: norm(name_en) → description_en first line ────────────────
DESC_EN = {}
for src in SHOP_PAGES + PRODUCT_JS:
    blob = read(src)
    for m in re.finditer(r'["\']?name_en["\']?\s*:', blob):
        w = blob[m.start(): m.start() + 4000]
        ne, de = first(w, "name_en"), first(w, "description_en")
        if ne and de:
            DESC_EN[norm(ne)] = de.split("\n")[0].strip()


# ── 1) resync drifted descriptions (all pages except the business-gifts grid,
#       which is rebuilt wholesale below) ─────────────────────────────────────
def sync_descriptions():
    from bs4 import BeautifulSoup
    for page in SHOP_PAGES:
        if page == "business-gifts.html":
            continue
        raw = read(page)
        soup = BeautifulSoup(raw, "html.parser")
        # map: norm(current desc text) → correct source first line, for cards
        # whose static desc drifted from source.
        fixes = {}
        for card in soup.select(".product-card"):
            n = card.select_one(".product-card-name")
            d = card.select_one(".product-card-desc")
            if not (n and d):
                continue
            want = DESC_EN.get(norm(n.get_text()))
            if want and norm(d.get_text()) != norm(want):
                fixes[norm(d.get_text())] = want
        if not fixes:
            continue

        def repl(mm):
            inner = mm.group(1)
            want = fixes.get(norm(html.unescape(inner)))
            return '<p class="product-card-desc">%s</p>' % esc(want) if want else mm.group(0)

        new = re.sub(r'<p class="product-card-desc">(.*?)</p>', repl, raw, flags=re.S)
        if new != raw:
            write(page, new)
            print("  synced %d description(s) in %s" % (len(fixes), page))


# ── 2) rebuild business-gifts static grid to the two catalogue products ──────
def _bg_card(photo, name_en, desc_en, from_ils, usd):
    name = esc(name_en)
    return (
        '    <article class="product-card">\n'
        '      <div class="product-card-img-wrap">\n'
        '        <img src="https://res.cloudinary.com/doesupaf9/image/upload/'
        'w_600,c_fit,q_auto,f_auto/%s.jpg" alt="%s" loading="lazy" />\n'
        '      </div>\n'
        '      <div class="product-card-body">\n'
        '        <h3 class="product-card-name">%s</h3>\n'
        '        <p class="product-card-desc">%s</p>\n'
        '        <div class="product-card-meta">\n'
        '          <span class="product-card-price">from &#8362;%s '
        '<span class="product-card-price-alt">&#8776; $%s</span></span>\n'
        '        </div>\n'
        '        <p class="product-color-note">* Colors may appear slightly different '
        'in person, as each item is handmade.</p>\n'
        '      </div>\n'
        '    </article>'
    ) % (photo, name, name, esc(desc_en.split("\n")[0].strip()), from_ils, usd)


def rebuild_business_gifts_grid():
    page = "business-gifts.html"
    raw = read(page)
    cards = [
        _bg_card("Chabad_shofar_o1sgb7", "Custom Ram's Horn Shofar, Symbol & Text",
                 DESC_EN[norm("Custom Ram's Horn Shofar, Symbol & Text")], "742", "238"),
        _bg_card("Name_kudu_shofar_hqdju6", "Custom Kudu Shofar, Symbol & Text",
                 DESC_EN[norm("Custom Kudu Shofar, Symbol & Text")], "1,297", "416"),
    ]
    new_block = "\n".join(cards)
    # Replace the single static SEO article with the two real cards. Consume the
    # article's own leading indent so the replacement isn't double-indented.
    m = re.search(r'[ \t]*<article class="product-card">.*?</article>', raw, re.S)
    if not m:
        print("  business-gifts: no static article found (already rebuilt?)")
        return
    if raw.count('<article class="product-card">') != 1:
        print("  business-gifts: expected exactly 1 static article — SKIPPED for safety")
        return
    raw = raw[:m.start()] + new_block + raw[m.end():]
    write(page, raw)
    print("  rebuilt business-gifts grid → 2 product cards")


# ── 3) add the missing spec_size key to business-gifts T_PAGE ────────────────
def add_spec_size():
    page = "business-gifts.html"
    raw = read(page)
    if re.search(r'\bspec_size\s*:', raw):
        print("  business-gifts: spec_size already defined")
        return
    raw = raw.replace("      spec_measurements: 'Measurements',",
                      "      spec_size:      'Size',\n      spec_measurements: 'Measurements',", 1)
    raw = raw.replace("      spec_measurements: 'מידות',",
                      "      spec_size:      'מידה',\n      spec_measurements: 'מידות',", 1)
    write(page, raw)
    print("  added spec_size to business-gifts T_PAGE (en + he)")


def main():
    print("-- description resync --")
    sync_descriptions()
    print("-- business-gifts grid --")
    rebuild_business_gifts_grid()
    print("-- spec_size --")
    add_spec_size()


if __name__ == "__main__":
    main()
