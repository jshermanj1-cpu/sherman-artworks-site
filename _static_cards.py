# -*- coding: utf-8 -*-
"""_static_cards.py - keep the no-JS product cards on the landing pages current.

Every category page renders its cards twice: once as static HTML for crawlers
and no-JS visitors, and again from the inline PRODUCTS array once the page runs.
Only the static copy is ever seen by GPTBot, PerplexityBot, ClaudeBot and CCBot,
none of which execute JavaScript.

That static copy went stale. `_sync_cards.py` was the tool for this, but it
still looks products up by their pre-2026-08-10 names ("Custom Ram's Horn
Shofar, Symbol & Text"), so it has raised KeyError - and skipped every page -
since the 925 rename. The result on 2026-09-01: candlesticks.html carried 17
cards for 24 products, kiddush-cups.html 9 for 19, trays-bowls.html 12 for 23,
and the names still read "Blue-Green Tall Glass Cup" where the catalogue says
"925 Silver-Plated Tall Blue-Green Glass Kiddush Cup". The entire gold-plated
line was invisible to any crawler that does not run JS.

What this does, per landing page:

  * joins each existing card to its product by the Cloudinary photo id in the
    <img src>, which survives every rename, then refreshes the heading, the alt
    prefix, the description and the price from data/products.json;
  * appends a card for any product on that page that has none;
  * leaves the hand-written half of the alt text ("- handmade deep burgundy
    glass candle holders") alone, and leaves cards it cannot join alone, so the
    JS template card at the end of a grid is never touched.

Idempotent - a second run reports no changes.

    python _static_cards.py           fix in place
    python _static_cards.py --check   report only, exit 1 if anything is stale

The "≈ $" figure is the pinned dollar price from _usd.py - the same figure the
page shows once JS has run and the same one the card is charged. It used to be a
separate round(ils/3.117) approximation that understated every entry by $6-$22.
"""

import html
import io
import json
import re
import sys
from pathlib import Path

# Pinned dollar list - never a live conversion. See _usd.py.
from _usd import usd_from_ils

SITE = Path(__file__).parent
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"
COLOR_NOTE = ("* Colors and measurements may appear slightly different in person, "
              "as each item is handmade.")

# Landing pages that own a static grid, with the phrase used for a new card's
# alt text. Subcategory and shofar pages are generated elsewhere and excluded.
PAGES = {
    "candlesticks.html": "handmade glass candlesticks",
    "kiddush-cups.html": "handmade glass kiddush cup",
    "trays-bowls.html": "handmade glass tray",
    "mezuzahs.html": "handmade mezuzah case",
    "horn-goblets.html": "handmade horn goblet",
}

CARD = re.compile(r'<article class="product-card"[^>]*>.*?</article>', re.S)
# Not [A-Za-z0-9_-]: one Cloudinary id carries Hebrew characters, and excluding
# them silently failed to join that card, so every run re-added it as missing.
PHOTO = re.compile(r'/upload/[^/]*/([^/"]+?)\.(?:jpg|png|webp)')
CARD_ID = re.compile(r'<article class="product-card" id="([^"]+)"')


def load():
    data = json.loads((SITE / "data" / "products.json").read_text(encoding="utf-8"))
    return data["products"] if isinstance(data, dict) else data


def price_of(p):
    sizes = p.get("sizes") or []
    return min(s["price_ils"] for s in sizes) if sizes else p["price_ils"]


def price_html(p):
    ils = price_of(p)
    prefix = "from " if p.get("sizes") else ""
    # A literal ≈, not &#8776;: that is what the other generators emit and what
    # the existing cards carry, so an unchanged card stays byte-identical.
    return ('%s&#8362;%s <span class="product-card-price-alt">≈ $%d</span>'
            % (prefix, format(ils, ","), usd_from_ils(ils)))


def new_card(p, alt_phrase):
    return (
        '<article class="product-card" id="%s">\n'
        '      <div class="product-card-img-wrap">\n'
        '        <img src="%s/w_600,c_fit,q_auto,f_auto/%s.jpg" alt="%s - %s" loading="lazy" />\n'
        '      </div>\n'
        '      <div class="product-card-body">\n'
        '        <h2 class="product-card-name">%s</h2>\n'
        '        <p class="product-card-desc">%s</p>\n'
        '        <div class="product-card-meta">\n'
        '          <span class="product-card-price">%s</span>\n'
        '        </div>\n'
        '        <p class="product-color-note">%s</p>\n'
        '      </div>\n'
        '    </article>'
        % (html.escape(p["id"], quote=True), CDN, p["photos"][0],
           html.escape(p["name_en"], quote=True), alt_phrase,
           html.escape(p["name_en"]), html.escape(p.get("description_en", "")),
           price_html(p), COLOR_NOTE))


def refresh(card, p):
    """Rewrite one existing card's name, alt prefix, description and price."""
    out = card
    name = html.escape(p["name_en"])

    def sub(pattern, repl, text):
        return re.sub(pattern, lambda m: repl(m), text, count=1)

    out = sub(r'(<h[23] class="product-card-name">)(.*?)(</h[23]>)',
              lambda m: m.group(1) + name + m.group(3), out)
    out = sub(r'(<p class="product-card-desc">)(.*?)(</p>)',
              lambda m: m.group(1) + html.escape(p.get("description_en", "")) + m.group(3), out)
    out = sub(r'(<span class="product-card-price">)(.*?)(</span>\s*</div>)',
              lambda m: m.group(1) + price_html(p) + m.group(3), out)

    def fix_alt(m):
        alt = m.group(2)
        tail = alt.split(" - ", 1)[1] if " - " in alt else None
        new = html.escape(p["name_en"], quote=True)
        return m.group(1) + (new + " - " + tail if tail else new) + m.group(3)

    out = sub(r'(<img[^>]*alt=")([^"]*)(")', fix_alt, out)
    return out


GRID = re.compile(r'<div class="products-grid"[^>]*>')


def grid_region(src, page):
    """The static grid's inner span: (start, end) offsets.

    Everything happens inside this span. The page also builds cards at runtime
    from a JS template literal that contains its own <article class="product-
    card">, and that literal sits later in the file - so "the last card in the
    document" is a card inside <script>. Appending there injects markup into
    JavaScript: invisible to crawlers, and liable to break the template.
    """
    m = GRID.search(src)
    if not m:
        raise RuntimeError("%s: no static products grid found" % page)
    end = src.index("</section>", m.end())
    return m.end(), end


def process(page, alt_phrase, products, check):
    path = SITE / page
    src = path.read_text(encoding="utf-8")
    lo, hi = grid_region(src, page)
    byphoto = {}
    for p in products:
        for ph in (p.get("photos") or []):
            byphoto.setdefault(ph, p)

    mine = [p for p in products
            if page in (p.get("pages") or []) and p.get("active") is not False]
    byid = {p["id"]: p for p in products}
    seen, updated, dropped = set(), 0, 0
    out = src
    for card in CARD.findall(src[lo:hi]):
        # id first - it is exact and survives a shared or renamed photo. Photo
        # is the fallback for the hand-written cards, which carry no id.
        m = CARD_ID.match(card)
        p = byid.get(m.group(1)) if m else None
        if p is None:
            m = PHOTO.search(card)
            p = byphoto.get(m.group(1)) if m else None
        if not p or page not in (p.get("pages") or []):
            continue  # JS template card, or a photo shared with another page
        if p["id"] in seen:
            # A duplicate of a card already handled on this page: drop it.
            out = out.replace("\n    " + card, "", 1)
            dropped += 1
            continue
        seen.add(p["id"])
        fixed = refresh(card, p)
        if fixed != card:
            out = out.replace(card, fixed, 1)
            updated += 1

    added = [p for p in mine if p["id"] not in seen]
    if added and not check:
        # Re-locate the grid: the refresh pass above may have shifted offsets.
        lo2, hi2 = grid_region(out, page)
        cards = "\n    ".join(new_card(p, alt_phrase) for p in added)
        inner = list(CARD.finditer(out[lo2:hi2]))
        at = lo2 + inner[-1].end() if inner else lo2
        out = out[:at] + "\n    " + cards + out[at:]

    if not check and (updated or added or dropped):
        path.write_text(out, encoding="utf-8")
    return updated, added, dropped


def shofar_names():
    """Current shofar names from js/shofar-products.js (the catalogue that
    _shofar_pages.py builds the sub-pages from)."""
    js = (SITE / "js" / "shofar-products.js").read_text(encoding="utf-8")
    body = re.search(r"const PRODUCTS = \[\n(.*?)\n\];", js, re.S).group(1)
    quoted = re.sub(r": ([A-Z][A-Z_]+)(,?)$", r': "\1"\2', body, flags=re.M)
    return [p["name_en"] for p in json.loads("[\n" + quoted + "\n]") if p.get("name_en")]


# shofars.html and business-gifts.html hold hand-written cards for the shofar
# catalogue. The 2026-08-10 rename added a "925 Silver-Plated " prefix to every
# plated name, and the sub-pages picked it up because they are generated - these
# two did not, so their headings still read "Custom Kudu Shofar, Symbol & Text".
SHOFAR_PAGES = ["shofars.html", "business-gifts.html"]


def rename_shofar_cards(page, names, check):
    path = SITE / page
    src = path.read_text(encoding="utf-8")
    lo, hi = grid_region(src, page)
    byshort = {}
    for n in names:
        byshort[n] = n
        if n.startswith("925 Silver-Plated "):
            byshort[n[len("925 Silver-Plated "):]] = n
    out, fixed = src, []
    for card in CARD.findall(src[lo:hi]):
        m = re.search(r'<h[23] class="product-card-name">(.*?)</h[23]>', card, re.S)
        if not m:
            continue
        cur = html.unescape(m.group(1)).strip()
        want = byshort.get(cur)
        if not want or want == cur:
            continue
        # Splice on the match span, not card.replace(name, ...): the same text
        # appears earlier in the card's alt attribute, so a blind first-match
        # replace renamed the alt and left the heading untouched.
        new = card[:m.start(1)] + html.escape(want) + card[m.end(1):]
        am = re.search(r'(<img[^>]*alt=")([^"]*)(")', new)
        if am:
            alt = html.unescape(am.group(2))
            tail = alt.split(" - ", 1)[1] if " - " in alt else None
            repl = html.escape(want, quote=True) + (" - " + html.escape(tail, quote=True) if tail else "")
            new = new.replace(am.group(0), am.group(1) + repl + am.group(3), 1)
        out = out.replace(card, new, 1)
        fixed.append(want)
    if fixed and not check:
        path.write_text(out, encoding="utf-8")
    return fixed


# The "≈ $" beside a card's shekel price, on every page that has one.
ALT_PRICE = re.compile(r'(&#8362;([\d,]+) <span class="product-card-price-alt">≈ \$)(\d+)(</span>)')


def resync_alt_dollars(check):
    """Re-derive every card's dollar figure from the shekel figure beside it.

    Deliberately not a product lookup: the shekel price printed on the card is
    already authoritative, so converting it in place fixes pages no generator
    owns - shofars.html (its own cards, as opposed to the sub-pages it seeds),
    havdalah-sets.html, and any card whose photo could not be joined. Shekel
    figures are never touched.
    """
    fixed = {}
    for path in sorted(SITE.glob("*.html")) + sorted((SITE / "he").glob("*.html")):
        src = path.read_text(encoding="utf-8")
        hits = []

        def repl(m):
            want = usd_from_ils(int(m.group(2).replace(",", "")))
            if int(m.group(3)) == want:
                return m.group(0)
            hits.append((m.group(2), m.group(3), want))
            return m.group(1) + str(want) + m.group(4)

        out = ALT_PRICE.sub(repl, src)
        if hits:
            fixed[path.name if path.parent == SITE else "he/" + path.name] = hits
            if not check:
                path.write_text(out, encoding="utf-8")
    return fixed


def main():
    check = "--check" in sys.argv
    products = load()
    stale = 0
    for page, alt_phrase in PAGES.items():
        updated, added, dropped = process(page, alt_phrase, products, check)
        stale += updated + len(added) + dropped
        if updated or added or dropped:
            verb = "stale" if check else "refreshed"
            print("%-22s %d %s, %d missing card(s)%s%s"
                  % (page, updated, verb, len(added),
                     "" if check else " added",
                     ", %d duplicate(s) dropped" % dropped if dropped else ""))
            for p in added[:4]:
                print("      + %s" % p["name_en"])
            if len(added) > 4:
                print("      + ... and %d more" % (len(added) - 4))
    names = shofar_names()
    for page in SHOFAR_PAGES:
        fixed = rename_shofar_cards(page, names, check)
        if fixed:
            stale += len(fixed)
            print("%-22s %d shofar card name(s) %s"
                  % (page, len(fixed), "stale" if check else "renamed"))
            for n in fixed[:3]:
                print("      %s" % n)
            if len(fixed) > 3:
                print("      ... and %d more" % (len(fixed) - 3))

    dollars = resync_alt_dollars(check)
    if dollars:
        n = sum(len(v) for v in dollars.values())
        stale += n
        print("%-22s %d card dollar figure(s) %s"
              % ("(all pages)", n, "stale" if check else "resynced"))
        for page, hits in list(dollars.items())[:4]:
            ils, was, now = hits[0]
            print("      %-26s ILS %s  $%s -> $%s%s"
                  % (page, ils, was, now,
                     "  (+%d more)" % (len(hits) - 1) if len(hits) > 1 else ""))

    if not stale:
        print("every landing-page card matches data/products.json")
        return 0
    if check:
        print("\n%d card(s) stale or missing - run without --check to fix" % stale)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
