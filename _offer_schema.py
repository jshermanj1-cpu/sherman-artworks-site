# -*- coding: utf-8 -*-
"""_offer_schema.py - keep every Product node complete for Google merchant listings.

Google drops the shipping and returns annotations from a merchant listing when
an Offer omits `shippingDetails` / `hasMerchantReturnPolicy`, and Search Console
reports them as missing fields. The landing pages have always carried both; what
drifts is anything added by hand afterwards. On 2026-09-01 the fourteen new
gold-plated kiddush cups and plates (SAW-KC-021..034) arrived on kiddush-cups
.html and trays-bowls.html without them, while the gold candlesticks added the
same day to candlesticks.html were complete - so this is a per-edit slip, not a
one-off, and it needs a guard rather than a single fix.

On 2026-09-20 the same Search Console report flagged three more gaps, so this
script now covers them too:

  deliveryTime   absent from every OfferShippingDetails on the site. Without it
                 Google cannot work out a delivery estimate, so the shipping
                 annotation stays blank even though the rate is declared.
  description    absent from the nine Havdalah sets in the ItemList block on
  brand          havdalah-sets.html, which was hand-authored and never picked up
  itemCondition  the fields the generated pages emit. Those same nine are what
                 the report counts under "missing description" and "no global
                 identifier" - Google takes sku + brand as the identifier, so
                 every product that has a brand goes unflagged.
  mpn            absent site-wide. Not flagged on its own once brand is there,
                 but merchant-feed.xml has always emitted the SKU as g:mpn, so
                 saying nothing on the page left the two surfaces naming the
                 product differently. Offers carry the size SKU, Products the
                 base one, exactly as the feed does.

The generated pages get their blocks from _subcategory_pages.py / _shofar_pages
.py, which now emit all of it. This script covers the hand-maintained landing
pages and doubles as the site-wide check.

    python _offer_schema.py            fix in place, report what changed
    python _offer_schema.py --check    report only, exit 1 if anything is missing

Raw-text edits: only a <script> block whose JSON actually changed is rewritten,
and only single-line (minified) blocks are ever rewritten, so diffs stay to one
line per block and hand-formatted blocks are left alone. deliveryTime is the one
exception - see add_delivery_time.
"""

import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).parent

INTL = ["US", "GB", "CA", "AU", "FR", "DE"]

# terms.html section 1 is the only authority for these numbers: we hand the order
# to the shipping company "within 14 business days" and state an official
# delivery timeframe of "up to 30 business days", so transit is the 16 business
# days left over. Google reads a bare DAY unit as a business day, which is what
# terms.html means by the phrase, so no businessDays block is needed.
DELIVERY = {
    "@type": "ShippingDeliveryTime",
    "handlingTime": {"@type": "QuantitativeValue",
                     "minValue": 1, "maxValue": 14, "unitCode": "DAY"},
    "transitTime": {"@type": "QuantitativeValue",
                    "minValue": 1, "maxValue": 16, "unitCode": "DAY"},
}
SHIPPING = [
    {"@type": "OfferShippingDetails",
     "deliveryTime": DELIVERY,
     "shippingRate": {"@type": "MonetaryAmount", "value": 35, "currency": "ILS"},
     "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IL"}},
    {"@type": "OfferShippingDetails",
     "deliveryTime": DELIVERY,
     "shippingRate": {"@type": "MonetaryAmount", "value": 45, "currency": "USD"},
     "shippingDestination": {"@type": "DefinedRegion", "addressCountry": INTL}},
]
RETURNS = {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": ["IL"] + INTL,
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 14,
    "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
}

# Fields every Product node needs. description has no safe default - inventing
# copy is worse than reporting the gap - so it is only ever copied from another
# node for the same sku on the same page, which keeps the Hebrew pages Hebrew.
BRAND = {"@type": "Brand", "name": "Sherman Art Works"}
CONDITION = "https://schema.org/NewCondition"
DEFAULTS = {"brand": BRAND, "itemCondition": CONDITION}
PRODUCT_FIELDS = ("description", "brand", "itemCondition")


def size_mpn():
    """Offer sku (the slug form) -> the formal sellable SKU, from products.json.

    A sized product carries one Offer per size, and its Offer sku is the
    id-with-suffix slug that the merchant feed uses as g:id - deliberately, so a
    feed item and its landing page resolve to the same variant. The feed's g:mpn
    is the formal SKU for that size, so this is the map that makes page and feed
    state the same identifier for the same sellable thing.
    """
    data = json.loads((SITE / "data" / "products.json").read_text(encoding="utf-8"))
    products = data["products"] if isinstance(data, dict) else data
    return {f"{p['id']}-{str(s['label']).lower()}": s["sku"]
            for p in products for s in (p.get("sizes") or [])}


MPN = size_mpn()

BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

# Every OfferShippingDetails node on the site is emitted minified and opens with
# this exact key, so a single anchor matches all of them.
SHIP_NODE = re.compile(r'\{"@type":"OfferShippingDetails",(?!"deliveryTime")')
DELIVERY_JSON = json.dumps(DELIVERY, ensure_ascii=False, separators=(",", ":"))


def add_delivery_time(src):
    """Insert deliveryTime into every OfferShippingDetails node. Returns (text, n).

    Done on the raw text rather than through the JSON round trip because three
    landing pages share their shipping nodes through `@id` references held in a
    hand-formatted `@graph` block, which the JSON path below refuses to rewrite.
    The negative lookahead makes a second run a no-op.
    """
    return SHIP_NODE.subn(
        '{"@type":"OfferShippingDetails","deliveryTime":' + DELIVERY_JSON + ",", src)


def collect_copy(node, copy):
    """Index sku -> the description/brand/itemCondition already present on a page.

    A bare ItemList entry and the rich ProductGroup variant for the same piece
    sit in different blocks of the same page, so a page nearly always already
    holds its own approved copy and nothing has to be written from scratch.
    """
    if isinstance(node, dict):
        if node.get("@type") == "Product" and node.get("sku"):
            have = copy.setdefault(node["sku"], {})
            for key in PRODUCT_FIELDS:
                if key not in have and node.get(key):
                    have[key] = node[key]
        for value in node.values():
            collect_copy(value, copy)
    elif isinstance(node, list):
        for value in node:
            collect_copy(value, copy)


def patch(node, copy, gaps):
    """Complete every Product and Offer under `node`. Returns True if changed."""
    changed = False
    if isinstance(node, dict):
        if node.get("@type") == "Product":
            name = node.get("name", "?")
            sku = node.get("sku") or "?"
            for key in PRODUCT_FIELDS:
                if node.get(key):
                    continue
                fill = copy.get(node.get("sku"), {}).get(key, DEFAULTS.get(key))
                gaps.append((name, sku, key, fill is not None))
                if fill is None:
                    continue
                node[key] = fill
                changed = True
            # These pieces are made one at a time and have no GTIN, so the SKU
            # is the only global identifier there will ever be. The feed has
            # said so as g:mpn all along; saying it on the page too means Google
            # matches a feed item to its landing page on the identifier rather
            # than on the link alone.
            if node.get("sku") and not node.get("mpn"):
                gaps.append((name, sku, "mpn", True))
                node["mpn"] = node["sku"]
                changed = True
            offers = node.get("offers")
            for offer in (offers if isinstance(offers, list) else [offers]):
                if not isinstance(offer, dict):
                    continue
                # A sized Offer carries its own size SKU, the same one the feed
                # emits for that size; anything else resells the base product.
                if node.get("sku") and not offer.get("mpn"):
                    gaps.append((name, offer.get("sku") or sku, "mpn", True))
                    offer["mpn"] = MPN.get(offer.get("sku"), node["sku"])
                    changed = True
                for key, value in (("shippingDetails", SHIPPING),
                                   ("hasMerchantReturnPolicy", RETURNS)):
                    if key in offer:
                        continue
                    gaps.append((name, offer.get("sku") or sku, key, True))
                    offer[key] = value
                    changed = True
        for value in node.values():
            changed |= patch(value, copy, gaps)
    elif isinstance(node, list):
        for value in node:
            changed |= patch(value, copy, gaps)
    return changed


def process(path, check):
    """Returns (delivery-node count, [(name, sku, field, fixable), ...])."""
    src = path.read_text(encoding="utf-8")
    out, delivered = add_delivery_time(src)
    gaps = []

    copy = {}
    for raw in BLOCK.findall(out):
        try:
            collect_copy(json.loads(raw), copy)
        except ValueError:
            pass

    for raw in BLOCK.findall(out):
        try:
            data = json.loads(raw)
        except ValueError:
            print(f"  ! {path.name}: a JSON-LD block does not parse, skipped")
            continue
        found = []
        rewrite = patch(data, copy, found)
        gaps.extend(found)
        if not rewrite or check:
            continue
        if "\n" in raw.strip():
            raise RuntimeError(f"{path.name}: a hand-formatted block is incomplete; fix it by hand")
        out = out.replace(
            f'<script type="application/ld+json">{raw}</script>',
            '<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "</script>", 1)
    if not check and out != src:
        path.write_text(out, encoding="utf-8")
    return delivered, gaps


def main():
    check = "--check" in sys.argv
    pages = sorted(SITE.glob("*.html")) + sorted((SITE / "he").glob("*.html"))
    total = 0
    stuck = 0
    for path in pages:
        delivered, gaps = process(path, check)
        if not delivered and not gaps:
            continue
        total += delivered + len(gaps)
        stuck += sum(1 for gap in gaps if not gap[3])
        verb = "missing" if check else "fixed"
        print(f"{path.relative_to(SITE)}: {delivered + len(gaps)} {verb}")
        if delivered:
            print(f"    deliveryTime             on {delivered} shipping nodes")
        for name, sku, key, fixable in gaps[:4]:
            note = "   <- no copy on the page, write it by hand" if not fixable else ""
            print(f"    {key:24s} {sku:16s} {name}{note}")
        if len(gaps) > 4:
            print(f"    ... and {len(gaps) - 4} more")
    if not total:
        print("all Product nodes are complete")
        return 0
    if check:
        print(f"\n{total} gaps - run without --check to fix")
        return 1
    print(f"\n{total} gaps closed")
    return 1 if stuck else 0


if __name__ == "__main__":
    sys.exit(main())
