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

results = []


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
                if node.get("@type") == "Product":
                    offers = node.get("offers")
                    offers = offers if isinstance(offers, list) else [offers]
                    for offer in offers:
                        if not isinstance(offer, dict):
                            continue
                        if ("shippingDetails" not in offer
                                or "hasMerchantReturnPolicy" not in offer):
                            bare.append((name, node.get("sku") or node.get("name")))
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
              "python _shofar_pages.py \\\n    && python _bake_en.py && "
              "python _offer_schema.py && python _he_pages.py && python _merchant_feed.py")
        return 1
    if not QUIET:
        print("\nall guards passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
