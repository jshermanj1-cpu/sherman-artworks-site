"""Generate the Google Merchant Center feeds from data/products.json.

The product slug remains Google Merchant Center's stable g:id. The formal
sellable SKU is emitted separately as g:mpn: base SKU for single-configuration
products and the explicit size SKU for sized products. Both are the same in
every feed, because they identify the same piece wherever it is listed.

One feed per market, because a feed item carries exactly one price and Merchant
Center wants that price in the currency of the country it is targeted at:

    merchant-feed.xml       Israel, shekels, 35 ILS shipping
    merchant-feed-us.xml    United States, dollars, 45 USD shipping

Targeting the US off the shekel feed is not an option - ILS is not a currency
Google will take for a US listing - and a single feed with both shipping
countries would still quote Americans in shekels. The dollar figures are the
pinned ones from _usd.py, the same list js/site.js shows an English-language
shopper and the payments Worker charges from, so the feed, the page and the
card agree by construction rather than by conversion.

Shipping is authoritative in the currency it is quoted in (35 ILS at home, 45
USD abroad) and is never converted between them - see the same note in
js/cart.js, where converting 35 ILS of Israeli shipping would invent a "$15"
nobody charges.
"""

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from _launch import launch_active, sale_ils
from _usd import sale_usd, usd_from_ils


ROOT = Path(__file__).parent
PRODUCTS_PATH = ROOT / "data" / "products.json"
BASE_URL = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"


class Market:
    """One target country: where the feed goes, and what money it speaks."""

    def __init__(self, filename, country, currency, shipping, price, sale):
        self.filename = filename
        self.country = country
        self.currency = currency
        self.shipping = shipping  # "35.00 ILS", already in this market's money
        self._price = price
        self._sale = sale

    @property
    def path(self):
        return ROOT / self.filename

    def price(self, ils):
        """The catalogue price of a shekel-priced item, in this market."""
        return self._price(ils)

    def sale(self, ils):
        return self._sale(ils)


MARKETS = [
    Market("merchant-feed.xml", "IL", "ILS", "35.00 ILS",
           lambda ils: f"{ils:.2f} ILS",
           lambda ils: f"{sale_ils(ils):.2f} ILS"),
    Market("merchant-feed-us.xml", "US", "USD", "45.00 USD",
           lambda ils: f"{usd_from_ils(ils):.2f} USD",
           lambda ils: f"{sale_usd(usd_from_ils(ils)):.2f} USD"),
]

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


FEED_SUFFIX = " | Handmade in Israel"


def _strip(text, *words):
    for w in words:
        text = text.replace(w, " ")
    return re.sub(r"\s+", " ", text).strip(" ,-")


def feed_title(product, size_text=None):
    """Shopping title: what the thing is first (the words people search),
    then colour or design, finish and size. Product names on the site lead
    with the finish ("925 Silver-Plated Tall Blue Glass Kiddush Cup"), which
    pushes the product type past where Shopping truncates the title.
    The site's own names are untouched; this only shapes the feed."""
    name = product["name_en"]
    cat = product["category"]
    plating = ("925 Silver-Plated" if "925 Silver-Plated" in name
               else "Gold-Plated" if "Gold-Plated" in name else None)
    rest = _strip(name, "925 Silver-Plated", "Gold-Plated")
    if cat == "candlesticks":
        kind = "Glass Shabbat Candlesticks, Pair"
        desc = _strip(rest, "Glass Candlesticks", "Candlesticks")
        desc = re.sub(r"^Glass ", "", desc)
        if desc == "Circle":
            desc = "Circle Design"
    elif cat == "kiddush-cups":
        if "Plate" in rest:
            kind, desc = "Glass Kiddush Cup Plate", _strip(rest, "Kiddush Cup Plate")
        elif "Ceramic" in rest:
            kind, desc = "Ceramic Kiddush Cup", "Menorah Design"
        else:
            kind, desc = "Glass Kiddush Cup", _strip(rest, "Glass Kiddush Cup", "Glass Cup")
        desc = desc.replace(" with ", ", ").replace("Bore Pri Hagefen", "Bore Pri Hagefen Blessing")
        if plating:
            plating += " Rim"
    elif cat == "shofars":
        horn = "Kudu" if "Kudu" in rest else "Ram's Horn"
        if "Custom" in rest:
            kind, desc = "Custom Engraved %s Shofar" % horn, "Your Symbol & Text"
        else:
            kind = "Decorated %s Shofar" % horn
            desc = rest.split(" - ", 1)[1] if " - " in rest else ""
    elif cat == "havdalah-sets":
        kind, desc = "Glass Havdalah Set", _strip(rest, "Havdalah Set")
    elif cat == "mezuzahs":
        if "Glass" in rest:
            kind, desc = "Clear Glass Mezuzah Case", ""
        else:
            horn = _strip(rest, "Mezuzah")
            kind, desc = "%s Horn Mezuzah Case" % ("Ram's" if horn == "Ram" else horn), ""
    elif cat == "trays-bowls":
        if "Bowl" in rest:
            kind, desc = "Decorative Glass Bowl", ""
        else:
            kind, desc = "Glass Tray", _strip(rest, "Glass Tray")
    else:
        return name + (" - " + size_text if size_text else "")
    parts = [p for p in (desc, plating, size_text) if p]
    return kind + (" - " + ", ".join(parts) if parts else "") + FEED_SUFFIX


def item_lines(product, size, market):
    product_type, google_category = CATEGORY_META[product["category"]]
    if size:
        item_id = f"{product['id']}-{size_slug(size['label'])}"
        size_text = f"{size['label']} ({size['range_cm']} cm)"
        title = feed_title(product, size_text)
        price = size["price_ils"]
        mpn = size["sku"]
    else:
        item_id = product["id"]
        size_text = None
        title = feed_title(product)
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
            tag("price", market.price(price)),
        ]
    )
    if launch_active():
        lines.append(tag("sale_price", market.sale(price)))
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
            tag("country", market.country, indent=6),
            tag("price", market.shipping, indent=6),
            "    </g:shipping>",
            # The same window the JSON-LD deliveryTime states, and from the same
            # authority - terms.html section 1: handed to the courier within 14
            # business days, delivered within 30. Google reads both in business
            # days. Left off the feed, Merchant Center invents its own estimate
            # and contradicts the landing page it links to.
            tag("min_handling_time", 1),
            tag("max_handling_time", 14),
            tag("min_transit_time", 1),
            tag("max_transit_time", 16),
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


def write_feed(products, market):
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
        sizes = product.get("sizes") or []
        for size in sizes or [None]:
            lines.extend(item_lines(product, size, market))
            count += 1

    lines.extend(["</channel>", "</rss>", ""])
    with market.path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {market.filename}: {count} items ({market.country}, {market.currency})")


def main():
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    validate(products)
    for market in MARKETS:
        write_feed(products, market)


if __name__ == "__main__":
    main()
