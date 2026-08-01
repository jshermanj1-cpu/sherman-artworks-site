"""Generate merchant-feed.xml from data/products.json.

The product slug remains Google Merchant Center's stable g:id. The formal
sellable SKU is emitted separately as g:mpn: base SKU for single-configuration
products and the explicit size SKU for sized products.
"""

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from _launch import launch_active, sale_ils


ROOT = Path(__file__).parent
PRODUCTS_PATH = ROOT / "data" / "products.json"
OUTPUT_PATH = ROOT / "merchant-feed.xml"
BASE_URL = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"

CATEGORY_META = {
    "candlesticks": ("Candlesticks", "2784"),
    "horn-goblets": ("Horn Goblets", "97"),
    "kiddush-cups": ("Kiddush Cups", "97"),
    "trays-bowls": ("Trays & Bowls", "6457"),
    "mezuzahs": ("Mezuzahs", "97"),
    "shofars": ("Shofars", "97"),
    "havdalah-sets": ("Havdalah Sets", "97"),
}


def tag(name, value, indent=4):
    return " " * indent + f"<g:{name}>{escape(str(value))}</g:{name}>"


def size_slug(label):
    return re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-")


def product_link(product):
    page = product["pages"][0]
    return f"{BASE_URL}/{page}#{product['id']}"


def item_lines(product, size=None):
    product_type, google_category = CATEGORY_META[product["category"]]
    if size:
        item_id = f"{product['id']}-{size_slug(size['label'])}"
        size_text = f"{size['label']} ({size['range_cm']} cm)"
        title = f"{product['name_en']} - {size_text}"
        price = size["price_ils"]
        mpn = size["sku"]
    else:
        item_id = product["id"]
        size_text = None
        title = product["name_en"]
        price = product["price_ils"]
        mpn = product["sku"]

    lines = [
        "  <item>",
        tag("id", item_id),
        tag("title", title),
        tag("description", product["description_en"]),
        tag("link", product_link(product)),
        tag("image_link", f"{CDN}/w_1200,q_auto:good/{product['photos'][0]}.jpg"),
    ]
    for photo in product["photos"][1:]:
        lines.append(tag("additional_image_link", f"{CDN}/w_1200,q_auto:good/{photo}.jpg"))

    lines.extend(
        [
            tag("availability", "in_stock"),
            # g:price stays the regular catalogue price; the launch sale is
            # expressed with g:sale_price so Google Shopping shows the markdown
            # (struck regular + sale) rather than just a lower price.
            tag("price", f"{price:.2f} ILS"),
        ]
    )
    if launch_active():
        lines.append(tag("sale_price", f"{sale_ils(price):.2f} ILS"))
    lines.extend(
        [
            tag("condition", "new"),
            tag("brand", "Sherman Art Works"),
            tag("mpn", mpn),
        ]
    )

    group_id = product.get("family_id") or (product["id"] if size else None)
    if group_id:
        lines.append(tag("item_group_id", group_id))
    if size_text:
        lines.append(tag("size", size_text))
    if product.get("color_en"):
        lines.append(tag("color", product["color_en"]))

    lines.extend(
        [
            tag("product_type", product_type),
            tag("google_product_category", google_category),
            "    <g:shipping>",
            tag("country", "IL", indent=6),
            tag("price", "35.00 ILS", indent=6),
            "    </g:shipping>",
            "  </item>",
        ]
    )
    return lines


def validate(products):
    product_skus = [product.get("sku") for product in products]
    if any(not sku for sku in product_skus):
        raise ValueError("Every product must have a nonblank base sku")
    if len(product_skus) != len(set(product_skus)):
        raise ValueError("Duplicate base sku in data/products.json")

    sellable = []
    for product in products:
        sizes = product.get("sizes") or []
        if sizes:
            for size in sizes:
                expected = f"{product['sku']}-{str(size['label']).upper()}"
                if size.get("sku") != expected:
                    raise ValueError(
                        f"{product['id']} size {size.get('label')}: "
                        f"expected sku {expected}, found {size.get('sku')}"
                    )
                sellable.append(size["sku"])
        else:
            sellable.append(product["sku"])
    if len(sellable) != len(set(sellable)):
        raise ValueError("Duplicate sellable sku in data/products.json")


def main():
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    validate(products)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        "<channel>",
        "  <title>Sherman Art Works</title>",
        "  <link>https://shermanartworks.com/</link>",
        "  <description>Handmade glass art and Judaica from Israel - candlesticks, Kiddush cups, horn goblets, shofars, mezuzahs, trays and bowls, and Havdalah sets.</description>",
    ]

    count = 0
    for product in products:
        if product.get("active") is False:
            continue
        if product.get("category") == "horn-goblets":
            continue
        sizes = product.get("sizes") or []
        for size in sizes or [None]:
            lines.extend(item_lines(product, size))
            count += 1

    lines.extend(["</channel>", "</rss>", ""])
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {OUTPUT_PATH.name}: {count} items")


if __name__ == "__main__":
    main()
