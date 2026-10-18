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

The Israeli feed speaks Hebrew. Merchant Center declares that source Hebrew,
and until 2026-10-14 it carried English titles linking to English pages, so it
barely matched Hebrew searches (107 impressions, 0 clicks in 28 days to 5 Oct).
Its titles, descriptions, colours, materials and highlights now come from the
Hebrew catalogue fields, and its links go to the /he/ twin of each page, which
also always shows shekels. g:product_type stays English in both feeds: shoppers
never see it, and Shopping campaigns subdivide by it, so one value per product
keeps the two campaigns' product groups identical.

g:custom_label_0 tells ready-to-ship menorahs apart from made-to-order ones for
the Hanukkah ads (data/ready-to-ship.json, updated from the studio's stock).
g:custom_label_1 is "menorah" on every menorah, so a campaign inventory filter
(one value per condition, no OR) can pick out all of them at once.
"""

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from _hanukkah_sale import active as hanukkah_active, sale as hanukkah_sale, START as HANUKKAH_START, END as HANUKKAH_END
from _launch import launch_active, sale_ils
from _usd import sale_usd, usd_from_ils


ROOT = Path(__file__).parent
PRODUCTS_PATH = ROOT / "data" / "products.json"
READY_PATH = ROOT / "data" / "ready-to-ship.json"
BASE_URL = "https://shermanartworks.com"
CDN = "https://res.cloudinary.com/doesupaf9/image/upload"


class Market:
    """One target country: where the feed goes, what money and language it speaks."""

    def __init__(self, filename, country, currency, shipping, price, sale, lang):
        self.filename = filename
        self.country = country
        self.currency = currency
        self.shipping = shipping  # "35.00 ILS", already in this market's money
        self._price = price
        self._sale = sale
        self.lang = lang  # "he" or "en": titles, descriptions and landing pages

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
           lambda ils: f"{sale_ils(ils):.2f} ILS",
           "he"),
    Market("merchant-feed-us.xml", "US", "USD", "45.00 USD",
           lambda ils: f"{usd_from_ils(ils):.2f} USD",
           lambda ils: f"{sale_usd(usd_from_ils(ils)):.2f} USD",
           "en"),
]

CATEGORY_META = {
    "candlesticks": ("Candlesticks", "2784"),
    "horn-goblets": ("Horn Goblets", "97"),
    "kiddush-cups": ("Kiddush Cups", "97"),
    "trays-bowls": ("Trays & Bowls", "6457"),
    "mezuzahs": ("Mezuzahs", "97"),
    "shofars": ("Shofars", "97"),
    "havdalah-sets": ("Havdalah Sets", "97"),
    "hanukkah-menorahs": ("Hanukkah Menorahs", "97"),
}

# Hanukkah menorahs are glass with silver-tone or gold-tone sockets and base -
# a finish, not plating - so they carry their own label rather than _finish()'s.
TONE = {"silver-tone": "Silver-Tone", "gold-tone": "Gold-Tone"}
# Each menorah shape is its own design; a new shape needs its label here.
SHAPE = {"half-moon": "Half-Moon", "rectangular": "Rectangular", "trapezoid": "Trapezoid"}


def tag(name, value, indent=4):
    return " " * indent + f"<g:{name}>{escape(str(value))}</g:{name}>"


def size_slug(label):
    return re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-")


def product_link(product, lang="en"):
    page = product["pages"][0]
    prefix = "he/" if lang == "he" else ""
    return f"{BASE_URL}/{prefix}{page}#{product['id']}"


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
    if cat == "candlesticks" and product.get("finish") in TONE:
        # Double-sided glass on silver-tone or gold-tone sockets and base: a
        # finish, not plating, labelled the same way as the menorahs.
        kind = "Double-Sided Glass Shabbat Candlesticks, Pair"
        desc = product["color_en"]
        plating = TONE[product["finish"]] + " Sockets & Base"
    elif cat == "candlesticks":
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
    elif cat == "hanukkah-menorahs":
        kind = "%s Glass Hanukkah Menorah" % SHAPE[product["shape"]]
        desc = product["color_en"]
        plating = TONE[product["finish"]] + " Sockets & Base"
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
    elif cat == "hanukkah-menorahs":
        line = SHAPE[product["shape"]] + " > " + TONE[product["finish"]]
    elif cat == "candlesticks" and product.get("finish") in TONE:
        line = "Double-Sided > " + TONE[product["finish"]]
    else:
        line = _finish(product) or "Artisanal"
    return " > ".join(x for x in ("Judaica", top, line) if x)


# Clear and pearl white glass is not "colorful"; every other menorah color is.
PLAIN_MENORAH_COLORS = {"Clear", "Pearl White"}


def feed_description(product, hebrew):
    """The catalogue description, plus for menorahs the facts and words shoppers
    search with (modern, colorful, hanukkiah, kosher layout, candles or oil)."""
    base = product["description_he" if hebrew else "description_en"]
    if product["category"] != "hanukkah-menorahs":
        return base
    colorful = product.get("color_en") not in PLAIN_MENORAH_COLORS
    if hebrew:
        lead = "חנוכייה מודרנית וצבעונית מזכוכית" if colorful else "חנוכייה מודרנית מזכוכית"
        extra = (f"{lead}: שמונה נרות בשורה ישרה ובגובה אחד, והשמש מופרד מהם. "
                 "מתאימה לנרות חנוכה רגילים, ואפשר להניח בקנים כוסיות שמן. "
                 "הבסיס עומד יציב גם על אדן חלון צר. כל חנוכיה נעשית בעבודת יד, ולכן אין שתיים זהות לגמרי.")
    else:
        lead = "A modern, colorful glass" if colorful else "A modern glass"
        extra = (f"{lead} Hanukkah menorah (hanukkiah, or Chanukah menorah): eight lights in a straight row "
                 "at one height, with the shamash set apart. It takes standard Hanukkah candles, or oil cups "
                 "in the sockets, and the base stands steadily on a narrow windowsill. Each piece is handmade, "
                 "so no two are exactly alike.")
    return base + " " + extra


def feed_highlights(product):
    """Plain facts for g:product_highlight (each under 150 characters, no promotional wording)."""
    name, cat = product["name_en"], product["category"]
    finish = _finish(product)
    # Some menorahs are in stock (data/ready-to-ship.json), so theirs does not say "to order".
    out = ["Handmade in our family studio in Israel" if cat == "hanukkah-menorahs"
           else "Handmade to order in our family studio in Israel"]
    if cat == "candlesticks":
        out.append("Sold as a pair")
        if product.get("finish") in TONE:
            out.append("Double-sided handmade glass, %s" % product["measurements"])
            out.append("%s sockets and base" % TONE[product["finish"]].capitalize())
        elif finish:
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
    elif cat == "hanukkah-menorahs":
        out.append("%s shape in double-sided handmade glass, %s (length × height × depth)"
                   % (SHAPE[product["shape"]], product["measurements"]))
        out.append("%s sockets and base" % TONE[product["finish"]].capitalize())
        out.append("Eight lights in a straight row at one height, with the shamash set apart")
        out.append("Takes standard Hanukkah candles, or oil cups in the sockets")
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


# ── Hebrew (the Israeli feed) ─────────────────────────────────────
# Hebrew names already lead with what the thing is ("חנוכיה חצי עיגול
# מזכוכית...", "זוג פמוטים מזכוכית..."), so the site's own name_he is the
# title; feed_title's reordering exists only because English names lead with
# the finish.

FEED_SUFFIX_HE = " | עבודת יד מישראל"

COLOR_HE = {
    "Black/White": "שחור/לבן", "Gold/Red": "זהב/אדום", "White/Blue": "לבן/כחול",
    "Blue-Green": "כחול-ירוק", "Multicolor": "צבעוני", "Red": "אדום",
    "Burgundy": "בורדו", "Clear": "שקוף", "Black": "שחור", "White": "לבן",
    "Blue": "כחול", "Green": "ירוק", "Orange": "כתום",
}

MATERIAL_HE = {
    "Glass": "זכוכית", "Ceramic": "קרמיקה", "Horn": "קרן",
    "Kudu horn": "קרן קודו", "Ram's horn": "קרן איל", "Oryx horn": "קרן ראם",
    "925 silver plating": "ציפוי כסף 925", "Gold plating": "ציפוי זהב",
}

SHAPE_HE = {"half-moon": "חצי עיגול", "rectangular": "מלבן", "trapezoid": "טרפז"}
TONE_HE = {"silver-tone": "בגוון כסף", "gold-tone": "בגוון זהב"}


def he_units(text):
    """cm -> ס״מ, as the /he/ pages write it ("33 × 27 × 3 ס״מ")."""
    return re.sub(r"(\d)\s*cm\b", "\\1 ס״מ", text)


def feed_title_he(product, size_text_he=None):
    return product["name_he"] + (" - מידה " + size_text_he if size_text_he else "") + FEED_SUFFIX_HE


def feed_color_he(product):
    if product.get("color_he"):
        return product["color_he"]
    color = feed_color(product)
    return COLOR_HE[color] if color else None


def feed_material_he(product):
    # A KeyError here means a new English material needs its Hebrew above;
    # failing beats shipping English into the Hebrew feed.
    return "/".join(MATERIAL_HE[part] for part in feed_material(product).split("/"))


def feed_highlights_he(product):
    """feed_highlights() in Hebrew, line for line."""
    name, cat = product["name_en"], product["category"]
    finish = _finish(product)
    plating = None
    if finish:
        plating = "ציפוי כסף 925" if finish.startswith("925") else "ציפוי זהב"
    out = ["נעשה בעבודת יד בסטודיו המשפחתי שלנו בישראל" if cat == "hanukkah-menorahs"
           else "נעשה בעבודת יד לפי הזמנה בסטודיו המשפחתי שלנו בישראל"]
    if cat == "candlesticks":
        out.append("נמכרים כזוג")
        if product.get("finish") in TONE_HE:
            out.append("זכוכית דו־צדדית בעבודת יד, %s" % he_units(product["measurements"]))
            out.append("קנים ובסיס %s" % TONE_HE[product["finish"]])
        elif finish:
            out.append("זכוכית ב%s" % plating)
            out.append("בשלושה גבהים: S (14-18 ס״מ), M (19-22 ס״מ) ו-L (23-25 ס״מ)")
        else:
            out.append("זכוכית בלבד, בשיטה המסורתית של המשפחה שלנו")
    elif cat == "kiddush-cups":
        rim = "ציפוי כסף 925" if finish and finish.startswith("925") else "ציפוי זהב"
        if name.endswith(" Plate"):
            out.append("תחתית זכוכית בקוטר 15 ס״מ עם שוליים ב%s" % rim)
            out.append("מותאמת לכוסות הקידוש שלנו בצבע ובגימור")
        else:
            out.append("כוס %s עם שפה ב%s" % ("קרמיקה" if "Ceramic" in name else "זכוכית", rim))
            if "Ceramic" not in name:
                out.append("יש תחתית זכוכית תואמת")
    elif cat == "havdalah-sets":
        out.append("ארבעה חלקים: כוס, קופסת בשמים, פמוט לנר ומגש")
        out.append("זכוכית ב%s" % ("ציפוי כסף 925" if finish and finish.startswith("925") else "ציפוי זהב"))
    elif cat == "trays-bowls":
        if finish:
            out.append("זכוכית ב%s" % plating)
    elif cat == "hanukkah-menorahs":
        out.append("צורת %s מזכוכית דו־צדדית בעבודת יד, %s (אורך × גובה × עומק)"
                   % (SHAPE_HE[product["shape"]], he_units(product["measurements"])))
        out.append("קנים ובסיס %s" % TONE_HE[product["finish"]])
        out.append("שמונה נרות בשורה ישרה ובגובה אחד, והשמש מופרד מהם")
        out.append("מתאימה לנרות חנוכה רגילים או לכוסיות שמן בקנים")
    elif cat == "shofars":
        out.append("%s טבעית בעיטור יד בציפוי כסף 925" % ("קרן קודו" if "Kudu" in name else "קרן איל"))
        if "Custom" in name:
            out.append("עם סמל לבחירתכם וכיתוב לבחירה בעברית או באנגלית")
    elif cat == "mezuzahs":
        out.append("בית מזוזה בלבד: הקלף נרכש בנפרד")
    if cat in ("shofars", "mezuzahs", "horn-goblets"):
        out.append("לשמור ביובש, לנגב את הציפוי במטלית רכה ויבשה ולא להשתמש בחומר לניקוי כסף")
    elif finish:
        out.append("לשטוף ביד בלבד ולא להשתמש בחומר לניקוי כסף על הציפוי")
    return out


def load_ready_to_ship(products):
    """Menorah ids the studio has in stock now (data/ready-to-ship.json)."""
    if not READY_PATH.exists():
        return set()
    ids = set(json.loads(READY_PATH.read_text(encoding="utf-8"))["ids"])
    known = {p["id"] for p in products if p["category"] == "hanukkah-menorahs"}
    unknown = sorted(ids - known)
    if unknown:
        raise ValueError(f"data/ready-to-ship.json names unknown menorah ids: {unknown}")
    return ids


READY = set()


def stock_label(product):
    """g:custom_label_0 for the Hanukkah ads: menorahs only."""
    if product["category"] != "hanukkah-menorahs":
        return None
    return "ready to ship" if product["id"] in READY else "made to order"


def item_lines(product, size, market):
    product_type, google_category = CATEGORY_META[product["category"]]
    hebrew = market.lang == "he"
    if size:
        item_id = f"{product['id']}-{size_slug(size['label'])}"
        size_text = (f"{size['label']} ({size['range_cm']} ס״מ)" if hebrew
                     else f"{size['label']} ({size['range_cm']} cm)")
        price = size["price_ils"]
        mpn = size["sku"]
    else:
        item_id = product["id"]
        size_text = None
        price = product["price_ils"]
        mpn = product["sku"]
    title = feed_title_he(product, size_text) if hebrew else feed_title(product, size_text)

    lines = [
        "  <item>",
        tag("id", item_id),
        tag("title", title),
        tag("description", feed_description(product, hebrew)),
        tag("link", product_link(product, market.lang)),
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
    if hanukkah_active(product["id"]):
        regular = price if market.currency == "ILS" else usd_from_ils(price)
        lines.append(tag("sale_price", f"{hanukkah_sale(regular, product['id']):.2f} {market.currency}"))
        lines.append(tag("sale_price_effective_date", HANUKKAH_START + "/" + HANUKKAH_END))
    elif launch_active():
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
    color = feed_color_he(product) if hebrew else feed_color(product)
    if color:
        lines.append(tag("color", color))
    lines.append(tag("material", feed_material_he(product) if hebrew else feed_material(product)))
    for highlight in (feed_highlights_he(product) if hebrew else feed_highlights(product)):
        lines.append(tag("product_highlight", highlight))
    label = stock_label(product)
    if label:
        lines.append(tag("custom_label_0", label))
        lines.append(tag("custom_label_1", "menorah"))

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
        "  <description>Handmade glass art and Judaica from Israel - candlesticks, Kiddush cups, horn goblets, shofars, mezuzahs, trays and bowls, Havdalah sets and Hanukkah menorahs.</description>",
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
    for product in products:
        if len(feed_highlights_he(product)) != len(feed_highlights(product)):
            raise ValueError(f"{product['id']}: Hebrew highlights out of step with the English ones")
    READY.update(load_ready_to_ship(products))
    for market in MARKETS:
        write_feed(products, market)


if __name__ == "__main__":
    main()
