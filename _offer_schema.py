# -*- coding: utf-8 -*-
"""_offer_schema.py - guarantee every Product offer declares shipping and returns.

Google drops the shipping and returns annotations from a merchant listing when
an Offer omits `shippingDetails` / `hasMerchantReturnPolicy`, and Search Console
reports them as missing fields. The landing pages have always carried both; what
drifts is anything added by hand afterwards. On 2026-09-01 the fourteen new
gold-plated kiddush cups and plates (SAW-KC-021..034) arrived on kiddush-cups
.html and trays-bowls.html without them, while the gold candlesticks added the
same day to candlesticks.html were complete - so this is a per-edit slip, not a
one-off, and it needs a guard rather than a single fix.

The generated pages get their blocks from _subcategory_pages.py / _shofar_pages
.py, which now emit both. This script covers the hand-maintained landing pages
and doubles as the site-wide check.

    python _offer_schema.py            fix in place, report what changed
    python _offer_schema.py --check    report only, exit 1 if anything is missing

Raw-text edits: only a <script> block whose JSON actually changed is rewritten,
and only single-line (minified) blocks are ever rewritten, so diffs stay to one
line per block and hand-formatted blocks are left alone.
"""

import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).parent

INTL = ["US", "GB", "CA", "AU", "FR", "DE"]
SHIPPING = [
    {"@type": "OfferShippingDetails",
     "shippingRate": {"@type": "MonetaryAmount", "value": 35, "currency": "ILS"},
     "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IL"}},
    {"@type": "OfferShippingDetails",
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

BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def patch(node, missing):
    """Add the two blocks to every Offer under `node`. Returns True if changed."""
    changed = False
    if isinstance(node, dict):
        if node.get("@type") == "Product":
            offers = node.get("offers")
            for offer in (offers if isinstance(offers, list) else [offers]):
                if not isinstance(offer, dict):
                    continue
                gap = [k for k in ("shippingDetails", "hasMerchantReturnPolicy") if k not in offer]
                if gap:
                    missing.append((node.get("name", "?"), offer.get("sku") or node.get("sku") or "?"))
                    offer.setdefault("shippingDetails", SHIPPING)
                    offer.setdefault("hasMerchantReturnPolicy", RETURNS)
                    changed = True
        for value in node.values():
            changed |= patch(value, missing)
    elif isinstance(node, list):
        for value in node:
            changed |= patch(value, missing)
    return changed


def process(path, check):
    src = path.read_text(encoding="utf-8")
    out = src
    missing = []
    for raw in BLOCK.findall(src):
        try:
            data = json.loads(raw)
        except ValueError:
            print(f"  ! {path.name}: a JSON-LD block does not parse, skipped")
            continue
        found = []
        if not patch(data, found):
            continue
        missing.extend(found)
        if check:
            continue
        if "\n" in raw.strip():
            raise RuntimeError(f"{path.name}: a hand-formatted block needs offers; fix it by hand")
        out = out.replace(
            f'<script type="application/ld+json">{raw}</script>',
            '<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "</script>", 1)
    if missing and not check:
        path.write_text(out, encoding="utf-8")
    return missing


def main():
    check = "--check" in sys.argv
    pages = sorted(SITE.glob("*.html")) + sorted((SITE / "he").glob("*.html"))
    total = 0
    for path in pages:
        missing = process(path, check)
        if missing:
            total += len(missing)
            verb = "missing" if check else "fixed"
            print(f"{path.relative_to(SITE)}: {len(missing)} {verb}")
            for name, sku in missing[:4]:
                print(f"    {sku}  {name}")
            if len(missing) > 4:
                print(f"    ... and {len(missing) - 4} more")
    if not total:
        print("all Product offers declare shipping and returns")
        return 0
    if check:
        print(f"\n{total} offers missing shipping/returns - run without --check to fix")
        return 1
    print(f"\n{total} offers completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
