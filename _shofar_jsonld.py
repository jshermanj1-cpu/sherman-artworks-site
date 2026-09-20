# -*- coding: utf-8 -*-
"""_shofar_jsonld.py - give every shofar size its own Offer in the landing JSON-LD.

Every other category emits one Offer per purchasable size, built by
_subcategory_pages.item_list. The shofars never went through that engine: their
ItemList on shofars.html carries a single Offer per product priced at the
bottom of the size ladder, because the block predates offers_for() and nothing
regenerates it.

merchant-feed.xml, meanwhile, lists each size as its own item at its own price
(145 shofar items across 22 families). So for every size above the smallest,
the price Google reads from the feed and the price it reads from the landing
page disagree - 123 of the 255 items in the feed on 2026-09-20, all of them
shofars, and none anywhere else. That is the shape Merchant Center reports as
"Mismatched value (price)" and it is why the larger sizes cannot be listed at
all: the ladder above the minimum is invisible in the structured data.

This script rebuilds the ItemList block on shofars.html through the same
item_list() the other categories use, so a shofar node comes out identical in
shape to a candlestick node: one Offer per size, each carrying the per-size sku
that merchant-feed.xml uses as its g:id, plus the size array.

Run it BEFORE _shofar_pages.py, which copies this block onto the three
sub-category pages:

    python _shofar_jsonld.py            rewrite, report what changed
    python _shofar_jsonld.py --check    report only, exit 1 if stale

The size ladders live in js/shofar-options.js and the catalogue in
js/shofar-products.js, which references the ladders by bare identifier - so the
ladders are parsed here and spliced in before the products are handed over.
"""

import json
import re
import sys
from pathlib import Path

from _shofar_pages import load_products
from _subcategory_pages import item_list

SITE = Path(__file__).parent
LANDING = "shofars.html"

# A ladder entry is a one-line JS object literal with unquoted keys, e.g.
#   { label: 'S',  range_cm: '70-79',   range_in: '28-31', price_ils: 1336 },
LADDER = re.compile(r"const ([A-Z][A-Z_]*_SIZES) = \[(.*?)\];", re.S)
ENTRY = re.compile(
    r"\{\s*label:\s*'([^']*)',\s*"
    r"range_cm:\s*'([^']*)',\s*"
    r"range_in:\s*'([^']*)',\s*"
    r"price_ils:\s*(\d+)\s*,?\s*\}")
BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def load_ladders():
    """Parse the four size ladders out of js/shofar-options.js."""
    js = (SITE / "js" / "shofar-options.js").read_text(encoding="utf-8")
    ladders = {}
    for name, body in LADDER.findall(js):
        ladders[name] = [
            {"label": label, "range_cm": cm, "range_in": inches,
             "price_ils": int(price)}
            for label, cm, inches, price in ENTRY.findall(body)
        ]
        if not ladders[name]:
            raise RuntimeError(f"{name}: no size entries parsed")
    if not ladders:
        raise RuntimeError("js/shofar-options.js: no size ladders found")
    return ladders


def resolve(products, ladders):
    """Swap each product's bare ladder name for the ladder itself.

    load_products() quotes the identifiers so the array parses as JSON, which
    leaves p["sizes"] as the string "RAMS_SIZES" rather than the seven sizes it
    names. offers_for() needs the real list.

    A ladder is shared by every product that sells in it, so it carries no sku
    of its own; the per-size sku is the base sku plus the upper-cased label.
    That is the same rule _merchant_feed.validate() enforces against
    data/products.json, so a drift here fails the existing guard rather than
    reaching the feed.
    """
    out = []
    for p in products:
        name = p.get("sizes")
        if not name:
            out.append(p)
            continue
        if name not in ladders:
            raise RuntimeError(f"{p['id']}: unknown size ladder {name}")
        sizes = [{**s, "sku": f"{p['sku']}-{s['label'].upper()}"}
                 for s in ladders[name]]
        out.append({**p, "sizes": sizes})
    return out


def build():
    """The ItemList block shofars.html should carry, as compact JSON."""
    products = resolve(load_products(), load_ladders())
    data = item_list({"landing": LANDING}, products)
    return data, json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def offer_count(data):
    """Offers across the whole list. The block being replaced holds a bare dict
    per product rather than a list, so len() on it would count its keys."""
    total = 0
    for entry in data["itemListElement"]:
        offers = entry["item"].get("offers")
        total += len(offers) if isinstance(offers, list) else 1
    return total


def main():
    check = "--check" in sys.argv
    path = SITE / LANDING
    src = path.read_text(encoding="utf-8")

    match = BLOCK.search(src)
    if not match:
        raise RuntimeError(f"{LANDING}: no JSON-LD block found")
    current = json.loads(match.group(2))
    if current.get("@type") != "ItemList":
        raise RuntimeError(f"{LANDING}: first JSON-LD block is "
                           f"{current.get('@type')}, expected ItemList")

    data, compact = build()
    was = offer_count(current)
    now = offer_count(data)

    if json.dumps(current, ensure_ascii=False, separators=(",", ":")) == compact:
        print(f"{LANDING}: ItemList current "
              f"({len(data['itemListElement'])} products, {now} offers)")
        return 0
    if check:
        print(f"{LANDING}: ItemList stale - {was} offers on the page, "
              f"{now} in the catalogue")
        print("  run without --check to rewrite, then rerun _shofar_pages.py")
        return 1

    out = src[:match.start()] + match.group(1) + compact + match.group(3) + src[match.end():]
    path.write_text(out, encoding="utf-8")
    print(f"{LANDING}: ItemList rewritten - "
          f"{len(data['itemListElement'])} products, {was} offers -> {now}")
    print("  now rerun _shofar_pages.py to copy it onto the sub-category pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
