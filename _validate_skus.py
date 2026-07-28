"""Validate SKU coverage and synchronization across the catalog.

Run before every product deployment:

    python _validate_skus.py
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent
GUIDE = ROOT / ".github" / "SKU_GUIDE.md"
PRODUCTS_PATH = ROOT / "data" / "products.json"
FEED_PATH = ROOT / "merchant-feed.xml"
G = "http://base.google.com/ns/1.0"

CATEGORY_CODES = {
    "candlesticks": ("Candlesticks", "CS"),
    "horn-goblets": ("Horn Goblets", "HG"),
    "kiddush-cups": ("Kiddush Cups", "KC"),
    "trays-bowls": ("Trays & Bowls", "TB"),
    "mezuzahs": ("Mezuzahs", "MZ"),
    "shofars": ("Shofars", "SH"),
    "havdalah-sets": ("Havdalah Sets", "HS"),
}


class Validation:
    def __init__(self):
        self.errors = []

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)

    def finish(self, products, sellable):
        if self.errors:
            print(f"SKU VALIDATION FAILED ({len(self.errors)} issue(s))")
            for error in self.errors:
                print(f"- {error}")
            return 1
        print(
            "SKU VALIDATION PASSED: "
            f"{len(products)} products, {len(sellable)} sellable SKUs, "
            "runtime objects, JSON-LD, cart ordering, and merchant feed synchronized"
        )
        return 0


def size_slug(label):
    return re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-")


def guide_assignments(validation):
    validation.check(GUIDE.exists(), ".github/SKU_GUIDE.md is missing")
    validation.check(
        not (ROOT / "SKU_GUIDE.md").exists(),
        "SKU_GUIDE.md must not be stored at the public site root",
    )
    if not GUIDE.exists():
        return {}, {}
    text = GUIDE.read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| `(SAW-[A-Z]{2}-\d{3})` \| `([^`]+)` \| .*? \| (.*?) \|$",
        text,
        flags=re.M,
    )
    assignments = {product_id: sku for sku, product_id, _ in rows}
    validation.check(len(assignments) == len(rows), "duplicate product ID in SKU guide")
    validation.check(
        len({sku for sku, _, _ in rows}) == len(rows),
        "duplicate base SKU in SKU guide",
    )

    next_numbers = {}
    for label, code in (value for value in CATEGORY_CODES.values()):
        match = re.search(
            rf"^\| {re.escape(label)} \| `{code}` \| `(\d{{3}})` \|$",
            text,
            flags=re.M,
        )
        validation.check(bool(match), f"missing next-number row for {label}")
        if match:
            next_numbers[code] = int(match.group(1))
    return assignments, next_numbers


def catalog(validation, assignments, next_numbers):
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    ids = [product.get("id") for product in products]
    validation.check(all(ids), "blank product id in data/products.json")
    validation.check(len(ids) == len(set(ids)), "duplicate product id in data/products.json")
    validation.check(
        set(ids) == set(assignments),
        "SKU guide product IDs do not exactly match data/products.json",
    )

    base_skus = []
    sellable = []
    expected_feed = {}
    highest_by_code = Counter()

    for product in products:
        product_id = product["id"]
        category = product.get("category")
        validation.check(category in CATEGORY_CODES, f"{product_id}: unknown category {category}")
        if category not in CATEGORY_CODES:
            continue
        _, code = CATEGORY_CODES[category]
        sku = product.get("sku")
        validation.check(
            bool(re.fullmatch(rf"SAW-{code}-\d{{3}}", sku or "")),
            f"{product_id}: invalid or missing base sku {sku!r}",
        )
        validation.check(
            assignments.get(product_id) == sku,
            f"{product_id}: catalog sku {sku!r} differs from SKU guide {assignments.get(product_id)!r}",
        )
        if sku:
            base_skus.append(sku)
            highest_by_code[code] = max(highest_by_code[code], int(sku.rsplit("-", 1)[-1]))

        sizes = product.get("sizes") or []
        if sizes:
            labels = [str(size.get("label", "")).upper() for size in sizes]
            validation.check(
                len(labels) == len(set(labels)),
                f"{product_id}: duplicate size label",
            )
            for size in sizes:
                expected_sku = f"{sku}-{str(size.get('label', '')).upper()}"
                actual_sku = size.get("sku")
                validation.check(
                    actual_sku == expected_sku,
                    f"{product_id} size {size.get('label')}: expected {expected_sku}, found {actual_sku!r}",
                )
                if actual_sku:
                    sellable.append(actual_sku)
                feed_id = f"{product_id}-{size_slug(size['label'])}"
                expected_feed[feed_id] = actual_sku
        else:
            if sku:
                sellable.append(sku)
            expected_feed[product_id] = sku

    validation.check(len(base_skus) == len(set(base_skus)), "duplicate catalog base SKU")
    validation.check(len(sellable) == len(set(sellable)), "duplicate sellable SKU")
    for _, code in CATEGORY_CODES.values():
        validation.check(
            next_numbers.get(code) == highest_by_code[code] + 1,
            f"{code}: next number should be {highest_by_code[code] + 1:03d}, "
            f"found {next_numbers.get(code)}",
        )
    return products, sellable, expected_feed


def runtime_objects(validation, assignments):
    paths = (
        list(ROOT.glob("*.html"))
        + list((ROOT / "he").glob("*.html"))
        + list((ROOT / "js").glob("*.js"))
    )
    seen = Counter()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for product_id, expected_sku in assignments.items():
            pattern = re.compile(
                rf"(?m)^(?P<indent>[ \t]*)(?:[\"']?id[\"']?)\s*:\s*[\"']"
                rf"{re.escape(product_id)}[\"']\s*,[ \t]*\r?\n"
                rf"(?P=indent)(?:[\"']?sku[\"']?)\s*:\s*[\"']"
                rf"{re.escape(expected_sku)}[\"']\s*,"
            )
            matches = pattern.findall(text)
            if matches:
                seen[product_id] += len(matches)

            id_only = re.findall(
                rf"(?m)^[ \t]*(?:[\"']?id[\"']?)\s*:\s*[\"']"
                rf"{re.escape(product_id)}[\"']\s*,",
                text,
            )
            if len(id_only) != len(matches):
                validation.errors.append(
                    f"{path.relative_to(ROOT)}: {product_id} runtime object missing or mismatching sku"
                )
    for product_id in assignments:
        validation.check(seen[product_id] > 0, f"{product_id}: no runtime product object found")


def jsonld(validation, assignments):
    product_nodes = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "he").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text,
            flags=re.I | re.S,
        ):
            try:
                payload = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                validation.errors.append(f"{path.relative_to(ROOT)}: invalid JSON-LD: {exc}")
                continue

            def walk(node):
                nonlocal product_nodes
                if isinstance(node, dict):
                    if node.get("@type") == "Product":
                        product_nodes += 1
                        url = node.get("url", "")
                        product_id = (
                            unquote(urlparse(url).fragment)
                            if isinstance(url, str) and "#" in url
                            else None
                        )
                        validation.check(
                            product_id in assignments,
                            f"{path.relative_to(ROOT)}: JSON-LD Product has unknown URL/id {url!r}",
                        )
                        if product_id in assignments:
                            validation.check(
                                node.get("sku") == assignments[product_id],
                                f"{path.relative_to(ROOT)}: {product_id} JSON-LD sku mismatch",
                            )
                    for value in node.values():
                        walk(value)
                elif isinstance(node, list):
                    for value in node:
                        walk(value)

            walk(payload)
    validation.check(product_nodes > 0, "no JSON-LD Product nodes found")


def add_on_skus(validation, products):
    sku_by_id = {product["id"]: product["sku"] for product in products}
    add_ons = 0
    for path in list(ROOT.glob("*.html")) + list((ROOT / "he").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for raw in re.findall(r'"tray_addon"\s*:\s*(\{[^\r\n]+\})', text):
            try:
                add_on = json.loads(raw)
            except json.JSONDecodeError as exc:
                validation.errors.append(
                    f"{path.relative_to(ROOT)}: invalid tray_addon object: {exc}"
                )
                continue
            add_ons += 1
            product_id = add_on.get("id")
            validation.check(
                product_id in sku_by_id,
                f"{path.relative_to(ROOT)}: unknown tray_addon id {product_id!r}",
            )
            if product_id in sku_by_id:
                validation.check(
                    add_on.get("sku") == sku_by_id[product_id],
                    f"{path.relative_to(ROOT)}: tray_addon {product_id} sku "
                    f"{add_on.get('sku')!r} should be {sku_by_id[product_id]!r}",
                )
    validation.check(add_ons > 0, "no SKU-bearing tray add-ons found")


def feed(validation, expected_feed):
    root = ET.parse(FEED_PATH).getroot()
    items = root.findall("./channel/item")
    ids = []
    mpns = []
    actual = {}
    for item in items:
        item_id = item.findtext(f"{{{G}}}id")
        mpn = item.findtext(f"{{{G}}}mpn")
        ids.append(item_id)
        mpns.append(mpn)
        actual[item_id] = mpn
        validation.check(
            item.find(f"{{{G}}}identifier_exists") is None,
            f"{item_id}: feed must not emit identifier_exists=no when MPN exists",
        )
    validation.check(len(ids) == len(set(ids)), "duplicate g:id in merchant feed")
    validation.check(all(mpns), "blank g:mpn in merchant feed")
    validation.check(len(mpns) == len(set(mpns)), "duplicate g:mpn in merchant feed")
    validation.check(
        actual == expected_feed,
        "merchant-feed g:id/g:mpn mapping differs from data/products.json",
    )


def cart_ordering(validation):
    text = (ROOT / "js" / "cart.js").read_text(encoding="utf-8")
    for required in (
        "function productSku(product, size)",
        "sku: sku || ''",
        "SKU: ' + item.sku",
        "tray_sku",
        "item_id: i.sku || i.slug",
    ):
        validation.check(required in text, f"cart ordering is missing required SKU logic: {required}")
    candlesticks = (ROOT / "candlesticks.html").read_text(encoding="utf-8")
    validation.check(
        "Matching tray SKU:" in candlesticks,
        "direct candlestick WhatsApp ordering is missing the matching tray SKU",
    )


def main():
    validation = Validation()
    assignments, next_numbers = guide_assignments(validation)
    products, sellable, expected_feed = catalog(validation, assignments, next_numbers)
    runtime_objects(validation, assignments)
    jsonld(validation, assignments)
    add_on_skus(validation, products)
    feed(validation, expected_feed)
    cart_ordering(validation)
    return validation.finish(products, sellable)


if __name__ == "__main__":
    sys.exit(main())
