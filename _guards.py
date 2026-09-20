# -*- coding: utf-8 -*-
"""_guards.py - every invariant that has silently broken on this site, in one run.

Called by .githooks/pre-push, and runnable by hand at any time:

    python _guards.py            report, exit non-zero if anything is broken
    python _guards.py --quiet    only print failures

Each check here exists because the thing it checks actually went wrong, twice in
some cases, and nothing noticed until an audit. The pattern is always the same:
a product is added, the generator chain is not re-run, and the damage sits on
the live site looking fine in a browser because JavaScript papers over it.

What is NOT here: a full chain re-run compared against the tree. That is the
strongest possible check and takes about twenty seconds on top of these, which
is too slow for a hook people will otherwise disable. The checks below catch the
symptoms that chain staleness produces, which is nearly as good and much faster.
"""

import io
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).parent
BASE = "https://shermanartworks.com"
HEBREW = re.compile(u"[֐-׿]")
QUIET = "--quiet" in sys.argv

# Gitignored local helpers. A fresh clone will not have them, and a missing
# helper must not fail a push - it means "cannot check", not "broken".
try:
    from _usd import usd_from_ils
except Exception:
    usd_from_ils = None

# What shipping costs, imported rather than copied, because the copies are what
# drift: a retired sprint script kept its own pair and still believed shipping
# was free over 1100 ILS. _offer_schema.py is tracked, so this normally loads.
try:
    from _offer_schema import SHIPPING

    RATES = {}
    for _node in SHIPPING:
        _dest = _node["shippingDestination"]["addressCountry"]
        _rate = _node["shippingRate"]
        RATES["IL" if _dest in ("IL", ["IL"]) else "INTL"] = (
            float(_rate["value"]), _rate["currency"])
except Exception:
    RATES = None

results = []


def misrated_shipping(node):
    """Returns (got, want) as display strings if a shipping node misprices it.

    Returns None when the node prices correctly, and also when there is nothing
    to compare - a bare `@id` reference to a shared node carries no rate of its
    own, and the node it points at is checked where it is defined.
    """
    if not RATES:
        return None
    dest = (node.get("shippingDestination") or {}).get("addressCountry")
    rate = node.get("shippingRate") or {}
    if dest is None or "value" not in rate:
        return None
    want = RATES.get("IL" if dest in ("IL", ["IL"]) else "INTL")
    if not want:
        return None
    try:
        got = (float(rate["value"]), rate.get("currency"))
    except (TypeError, ValueError):
        got = (rate["value"], rate.get("currency"))
    if got == want:
        return None
    return (show_rate(got), show_rate(want))


def show_rate(pair):
    value, currency = pair
    return "%s %s" % ("%g" % value if isinstance(value, float) else value, currency)


def record(name, bad, detail="", skipped=False):
    results.append((name, bad, detail, skipped))


def pages():
    return sorted(SITE.glob("*.html")) + sorted((SITE / "he").glob("*.html"))


def rel(path):
    return path.name if path.parent == SITE else "he/" + path.name


def walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for v in node.values():
            walk(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk(v, fn)


def scan():
    """One parse pass over every page, collecting every structural invariant."""
    from bs4 import BeautifulSoup

    bare, eng_he, invisible, faq_orphans, ld_broken = [], [], [], [], []
    usd_wrong, no_a11y = [], []
    undated, thin, misrated = [], [], []
    price_pat = re.compile(
        r'&#8362;([\d,]+) <span class="product-card-price-alt">≈ \$(\d+)</span>')

    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    listed = set()
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
        p = loc.replace(BASE + "/", "")
        listed.add("index.html" if p == "" else ("he/index.html" if p == "he/" else p))

    noindexed, absent = [], []
    for name in sorted(listed):
        if not (SITE / name).exists():
            absent.append(name)

    for path in pages():
        src = path.read_text(encoding="utf-8")
        name = rel(path)
        soup = BeautifulSoup(src, "html.parser")
        robots = soup.find("meta", attrs={"name": "robots"})
        noindex = "noindex" in ((robots.get("content") if robots else "") or "")
        if noindex and name in listed:
            noindexed.append(name)

        if not noindex and "accessibility.html" not in src:
            no_a11y.append(name)

        visible = BeautifulSoup(src, "html.parser")
        for tag in visible(["script", "style", "noscript"]):
            tag.decompose()
        text = re.sub(r"\s+", " ", visible.get_text(" "))

        for block in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(block.string or "")
            except ValueError:
                ld_broken.append(name)
                continue

            def check(node):
                # Checked wherever it appears rather than through the offer,
                # because three landing pages hold one shared node per
                # destination in an @graph block and point at it by @id.
                if node.get("@type") == "OfferShippingDetails":
                    where = node.get("@id") or "inline"
                    if "deliveryTime" not in node:
                        undated.append((name, where))
                    # The copy rule below only searches for the words "free
                    # shipping", so a rate written as a bare number - which is
                    # how a generator states it - would otherwise pass unseen.
                    wrong = misrated_shipping(node)
                    if wrong:
                        misrated.append((name, where) + wrong)
                if node.get("@type") == "Product":
                    offers = node.get("offers")
                    offers = offers if isinstance(offers, list) else [offers]
                    for offer in offers:
                        if not isinstance(offer, dict):
                            continue
                        if ("shippingDetails" not in offer
                                or "hasMerchantReturnPolicy" not in offer):
                            bare.append((name, node.get("sku") or node.get("name")))
                    # Google needs the first three to show a merchant listing at
                    # all; the Havdalah landing page shipped without any of them
                    # for months. mpn is the identifier the feed has always sent
                    # as g:mpn - handmade pieces have no gtin, so the SKU is all
                    # there is, and the page has to name it too or the two
                    # surfaces identify the same product differently.
                    for key in ("description", "brand", "itemCondition", "mpn"):
                        if not node.get(key):
                            thin.append((name, node.get("sku") or node.get("name"), key))
                    for offer in offers:
                        if isinstance(offer, dict) and not offer.get("mpn"):
                            thin.append((name, offer.get("sku") or node.get("sku"), "offer mpn"))
                    label = node.get("name")
                    if label:
                        if name.startswith("he/") and not HEBREW.search(label):
                            eng_he.append((name, label))
                        if label not in text:
                            invisible.append((name, label))
                if node.get("@type") == "Question":
                    q = node.get("name")
                    if q and q not in text:
                        faq_orphans.append((name, q))

            walk(data, check)

        if usd_from_ils:
            for ils, dollars in price_pat.findall(src):
                want = usd_from_ils(int(ils.replace(",", "")))
                if int(dollars) != want:
                    usd_wrong.append((name, ils, dollars, want))

    record("Product offers declare shipping and returns", bare,
           "%s ..." % (bare[0][1] if bare else ""))
    record("Shipping details carry a delivery estimate", undated,
           "%s on %s" % (undated[0][1], undated[0][0]) if undated else "")
    if RATES:
        record("Shipping is charged at the declared rate", misrated,
               "%s says %s, not %s (%s)" % (misrated[0][0], misrated[0][2],
                                            misrated[0][3], misrated[0][1])
               if misrated else "")
    else:
        record("Shipping is charged at the declared rate", [],
               "_offer_schema.py did not load", skipped=True)
    record("Products declare description, brand, condition and mpn", thin,
           "%s has no %s on %s" % (thin[0][1], thin[0][2], thin[0][0]) if thin else "")
    record("Hebrew pages name products in Hebrew", eng_he,
           "%s on %s" % (eng_he[0][1], eng_he[0][0]) if eng_he else "")
    record("Structured-data names appear on the page", invisible,
           "%s on %s" % (invisible[0][1], invisible[0][0]) if invisible else "")
    record("FAQ answers are rendered, not only marked up", faq_orphans,
           faq_orphans[0][0] if faq_orphans else "")
    record("JSON-LD parses", ld_broken, ld_broken[0] if ld_broken else "")
    record("Sitemap lists no noindex page", noindexed,
           ", ".join(noindexed))
    record("Sitemap URLs all resolve", absent, ", ".join(absent))
    record("Indexable pages link the accessibility statement", no_a11y,
           ", ".join(no_a11y[:3]))
    if usd_from_ils:
        record("Card dollar figures match the charged price", usd_wrong,
               "%s: %s shows $%s, charges $%s" % usd_wrong[0] if usd_wrong else "")
    else:
        record("Card dollar figures match the charged price", [],
               "_usd.py not present", skipped=True)


def copy_rules():
    """The owner's standing copy rules, which regenerating can reintroduce."""
    long_dash, sterling, free_ship = [], [], []
    tracked = subprocess.run(["git", "ls-files"], cwd=str(SITE),
                             capture_output=True, text=True).stdout.split()
    for name in tracked:
        if not name.endswith((".html", ".txt", ".xml", ".json", ".js", ".py")):
            continue
        # This file necessarily contains every string it searches for.
        if name == os.path.basename(__file__):
            continue
        try:
            text = io.open(SITE / name, encoding="utf-8").read()
        except Exception:
            continue
        if u"—" in text or u"–" in text:
            long_dash.append(name)
        low = text.lower()
        if "sterling" in low or u"סטרלינג" in text:
            sterling.append(name)
        if "free shipping" in low or u"משלוח חינם" in text:
            free_ship.append(name)
    record("No em or en dashes (plain hyphens only)", long_dash, ", ".join(long_dash[:3]))
    record("The word 'sterling' never appears", sterling, ", ".join(sterling[:3]))
    record("Nothing claims free shipping", free_ship, ", ".join(free_ship[:3]))


def feed_prices():
    """Every feed item's price must exist as an Offer on its landing page.

    _validate_skus.py already checks that the feed and the JSON-LD name the
    same products, but it never compares what they cost, and that is the half
    that broke. Until 2026-09-20 the shofar ItemList carried one Offer per
    product priced at the bottom of its size ladder while the feed listed each
    size at its own price: 123 of 255 items disagreed with their own landing
    page, every guard passed, and Merchant Center would have read it as
    "Mismatched value (price)" on nearly half the catalogue.

    A shopper following an ad has to find the advertised price on the page it
    lands on, so this compares by URL fragment rather than by sku - that is the
    thing Google actually resolves.
    """
    import xml.etree.ElementTree as ET

    feed = SITE / "merchant-feed.xml"
    if not feed.exists():
        record("Feed prices match the landing page", [],
               "merchant-feed.xml not present", skipped=True)
        return
    ns = "{http://base.google.com/ns/1.0}"

    def price_of(offer):
        try:
            return float(offer["price"])
        except (KeyError, TypeError, ValueError):
            return None

    # Landing-page offers indexed by the fragment Google resolves them at.
    offered = {}
    for path in {
        (item.findtext(ns + "link") or "").split("#")[0].replace(BASE + "/", "")
        for item in ET.parse(str(feed)).getroot().findall("./channel/item")
    }:
        page = SITE / path
        if not page.exists():
            continue
        for raw in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>',
                page.read_text(encoding="utf-8"), re.S):
            try:
                data = json.loads(raw)
            except ValueError:
                continue  # "JSON-LD parses" already reports this

            def collect(node):
                if node.get("@type") != "Product":
                    return
                url = node.get("url") or ""
                if "#" not in url:
                    return
                offers = node.get("offers")
                offers = offers if isinstance(offers, list) else [offers]
                seen = offered.setdefault((path, url.split("#", 1)[1]), set())
                for offer in offers:
                    if isinstance(offer, dict) and price_of(offer) is not None:
                        seen.add(price_of(offer))

            walk(data, collect)

    missing, mismatched = [], []
    for item in ET.parse(str(feed)).getroot().findall("./channel/item"):
        item_id = item.findtext(ns + "id")
        link = item.findtext(ns + "link") or ""
        if "#" not in link:
            continue
        page, fragment = link.replace(BASE + "/", "").split("#", 1)
        try:
            want = float((item.findtext(ns + "price") or "").split()[0])
        except (IndexError, ValueError):
            continue
        found = offered.get((page, fragment))
        if found is None:
            missing.append((item_id, page, fragment))
        elif want not in found:
            mismatched.append((item_id, want, sorted(found)))

    record("Feed items resolve to a product on their landing page", missing,
           "%s -> %s#%s" % missing[0] if missing else "")
    record("Feed prices match the landing page", mismatched,
           "%s: feed %g, page %s" % (mismatched[0][0], mismatched[0][1],
                                     ", ".join("%g" % p for p in mismatched[0][2][:4]))
           if mismatched else "")


def external(label, argv, missing_helper=None):
    """Run one of the existing --check scripts."""
    if missing_helper and not (SITE / missing_helper).exists():
        record(label, [], "%s not present" % missing_helper, skipped=True)
        return
    proc = subprocess.run([sys.executable] + argv, cwd=str(SITE),
                          capture_output=True, text=True)
    if proc.returncode == 0:
        record(label, [], "")
    else:
        tail = [l for l in (proc.stdout or "").strip().split("\n") if l.strip()]
        record(label, ["failed"], tail[-1][:90] if tail else "exit %d" % proc.returncode)


def main():
    scan()
    copy_rules()
    feed_prices()
    external("Static cards match the catalogue", ["_static_cards.py", "--check"], "_usd.py")
    external("Shofar sizing table is current", ["_shofar_guide.py", "--check"])
    external("SKUs, JSON-LD and the feed agree", ["_validate_skus.py"], "_launch.py")

    failed = [r for r in results if r[1] and not r[3]]
    for name, bad, detail, skipped in results:
        if skipped:
            if not QUIET:
                print("  SKIP  %-52s %s" % (name, detail))
        elif bad:
            count = "" if bad == ["failed"] else " (%d)" % len(bad)
            print("  FAIL  %-52s %s%s" % (name, detail, count))
        elif not QUIET:
            print("  ok    %s" % name)

    if failed:
        print("\n%d guard(s) failed. Re-run the generator chain:" % len(failed))
        print("  python _static_cards.py && python _subcategory_pages.py && "
              "python _shofar_jsonld.py \\\n    && python _shofar_pages.py && "
              "python _bake_en.py && python _offer_schema.py \\\n    && "
              "python _he_pages.py && python _merchant_feed.py")
        return 1
    if not QUIET:
        print("\nall guards passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
