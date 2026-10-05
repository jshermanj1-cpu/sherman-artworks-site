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



# Colours as the name states them, for items without a catalogue color_en (kiddush cups and
# plates, artisanal candlesticks). Existing color_en values are kept as they are: inside an
# item group they are what tells the variants apart. Horn items get no colour.
_COLOR_RULES = [
    ("Black and White", "Black/White"), ("Gold and Red", "Gold/Red"), ("White and Blue", "White/Blue"),
    ("Blue-Green", "Blue-Green"), ("Gold Colorful", "Multicolor"), ("Colorful", "Multicolor"),
    ("Vibrant Red", "Red"), ("Burgundy", "Burgundy"), ("Clear", "Clear"), ("Black", "Black"),
    ("White", "White"), ("Blue", "Blue"), ("Green", "Green"), ("Red", "Red"), ("Orange", "Orange"),
]


def feed_color(product):
    if product.get("color_en"):
        return product["color_en"]
    if product["category"] not in ("kiddush-cups", "candlesticks", "trays-bowls"):
        return None
    name = product["name_en"].replace("Gold-Plated", "").replace("925 Silver-Plated", "")
    for needle, color in _COLOR_RULES:
        if needle in name:
            return color
    return None


def _finish(product):
    name = product["name_en"]
    return "925 Silver-Plated" if "925 Silver-Plated" in name else "Gold-Plated" if "Gold-Plated" in name else None


def feed_material(product):
    name, cat = product["name_en"], product["category"]
    plating = {"925 Silver-Plated": "925 silver plating", "Gold-Plated": "Gold plating"}.get(_finish(product))
    if cat == "shofars":
        base = "Kudu horn" if "Kudu" in name else "Ram's horn"
    elif cat == "mezuzahs":
        base = "Glass" if "Glass" in name else "%s horn" % name.replace("925 Silver-Plated", "").replace("Mezuzah", "").strip().replace("Ram", "Ram's")
    elif cat == "horn-goblets":
        base, plating = "Horn", "925 silver plating"
    elif "Ceramic" in name:
        base = "Ceramic"
    else:
        base = "Glass"
    return base + ("/" + plating if plating else "")


def feed_product_type(product):
    """Judaica > category > line, e.g. 'Judaica > Kiddush Cups > Gold-Plated'."""
    name, cat = product["name_en"], product["category"]
    top = CATEGORY_META[cat][0]
    if cat == "shofars":
        line = "Custom" if "Custom" in name else "Kudu" if "Kudu" in name else "Ram's Horn"
    elif cat == "mezuzahs":
        line = "Glass" if "Glass" in name else "Horn"
    elif cat == "horn-goblets":
        line = None
    else:
        line = _finish(product) or "Artisanal"
    return " > ".join(x for x in ("Judaica", top, line) if x)


def feed_highlights(product):
    """Plain facts for g:product_highlight (each under 150 characters, no promotional wording)."""
    name, cat = product["name_en"], product["category"]
    finish = _finish(product)
    out = ["Handmade to order in our family studio in Israel"]
    if cat == "candlesticks":
        out.append("Sold as a pair")
        if finish:
            out.append("Glass finished with %s" % ("925 silver plating" if finish.startswith("925") else "gold plating"))
            out.append("Available in three heights: S (14-18 cm), M (19-22 cm) and L (23-25 cm)")
        else:
            out.append("All glass, made with our family's traditional method")
    elif cat == "kiddush-cups":
        rim = "925 silver-plated" if finish and finish.startswith("925") else "gold-plated"
        if name.endswith(" Plate"):
            out.append("15 cm glass plate with a %s rim" % rim)
            out.append("Made to match our Kiddush cups in colour and finish")
        else:
            out.append(("Ceramic" if "Ceramic" in name else "Glass") + " cup with a %s rim" % rim)
            if "Ceramic" not in name:
                out.append("A matching glass plate is available")
    elif cat == "havdalah-sets":
        out.append("Four pieces: cup, spice box, candle holder and tray")
        out.append("Glass finished with %s" % ("925 silver plating" if finish and finish.startswith("925") else "gold plating"))
    elif cat == "trays-bowls":
        if finish:
            out.append("Glass finished with %s" % ("925 silver plating" if finish.startswith("925") else "gold plating"))
    elif cat == "shofars":
        out.append("Natural %s decorated by hand in 925 silver" % ("kudu horn" if "Kudu" in name else "ram's horn"))
        if "Custom" in name:
            out.append("Engraved with a symbol of your choice and an optional Hebrew or English inscription")
    elif cat == "mezuzahs":
        out.append("Mezuzah case only: the parchment (klaf) is bought separately")
    if cat in ("shofars", "mezuzahs", "horn-goblets"):
        out.append("Keep dry; wipe the plating with a soft dry cloth and do not use silver polish")
    elif finish:
        out.append("Wash by hand and do not use silver polish on the plating")
    return out


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
    color = feed_color(product)
    if color:
        lines.append(tag("color", color))
    lines.append(tag("material", feed_material(product)))
    for highlight in feed_highlights(product):
        lines.append(tag("product_highlight", highlight))

    lines.extend(
        [
            tag("product_type", feed_product_type(product)),
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
