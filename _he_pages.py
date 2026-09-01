# -*- coding: utf-8 -*-
"""
_he_pages.py - generate static Hebrew /he/ versions of the shop pages.

Why this exists
---------------
The site's i18n is runtime-JS only: every page ships English in the markup and
setLang('he') swaps [data-t] text + re-renders product cards in the browser.
Search engines (and GPTBot/ClaudeBot/PerplexityBot, which don't run JS) therefore
only ever index English, so the entire Hebrew market is invisible. The 2026-07-20
SEO/GEO audit flagged this as "the single biggest untapped SEO opportunity."

This script bakes the Hebrew the site already contains into real static pages
under /he/, with proper lang="he" dir="rtl", Hebrew <title>/description,
self-canonicals, and bidirectional hreflang. It reuses the EXISTING translation
data (T_SITE in js/site.js, per-page T_PAGE, and product name_he/description_he)
so nothing is re-translated by hand - the Hebrew stays a single source of truth.

Output: /he/<page>.html for each PAGES entry. English pages are left to a
separate, minimal edit (hreflang + toggle link); this script only writes /he/.
"""

import os
import re
import json
import datetime
from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.abspath(__file__))
HE_DIR = os.path.join(ROOT, "he")

# Shop pages: homepage, 8 shop categories, 3 shofar sub-category pages. These are
# the pages with product cards (used by build_product_records).
SHOP_PAGES = [
    "index.html",
    "candlesticks.html",
    "candlesticks-silver-plated.html",
    "candlesticks-gold-plated.html",
    "candlesticks-artisanal.html",
    "horn-goblets.html",
    "kiddush-cups.html",
    "kiddush-cups-silver-plated.html",
    "kiddush-cups-gold-plated.html",
    "havdalah-sets.html",
    "mezuzahs.html",
    "trays-bowls.html",
    "business-gifts.html",
    "shofars.html",
    "shofars-custom.html",
    "shofars-rams.html",
    "shofars-kudu.html",
]

# Studio + policy pages. about/custom-orders/contact are data-t driven; the three
# policy pages build their legal body via a JS render fn (replicated below).
STUDIO_PAGES = [
    "about.html",
    "custom-orders.html",
    "contact.html",
    "faq.html",
    "terms.html",
    "privacy.html",
    "accessibility.html",
]

# Every page that gets a Hebrew twin.
PAGES = SHOP_PAGES + STUDIO_PAGES
TRANSLATED = set(PAGES)

# Policy pages whose <main> body is assembled by a JS render fn from T_PAGE keys.
# We replicate that render in Hebrew so the no-JS/crawler view has the legal text.
POLICY = {
    "terms.html": {"container": "terms-content", "kind": "terms"},
    "privacy.html": {"container": "privacy-content", "kind": "privacy"},
    "accessibility.html": {"container": "a11y-content", "kind": "a11y"},
}

# Extra JS files to mine for product name_he/description_he (shofar catalogue).
PRODUCT_JS = ["js/shofar-products.js", "js/havdalah-sets.js"]

# setLang() uses innerHTML (not textContent) only for these rich-text keys.
RICH_KEYS = {"story_body", "craft_body"}

# Keys some pages reference via data-t but forgot to define in their own T_PAGE
# (a latent gap the site's JS toggle shares). Filled as a last resort so no
# label is left English on a Hebrew page. Values taken from the shofar pages.
FALLBACK_HE = {
    "spec_size": "מידה",
}

# Static strings the shared header/footer/hero carry WITHOUT a data-t hook, so
# neither setLang() nor the data-t sweep touches them. The site's JS Hebrew view
# leaves some of these English too (a latent i18n gap in the shared chrome) - but
# on a dedicated /he/ page the crawler should see Hebrew, so we translate them by
# exact match. Keyed by CSS selector → {english: hebrew}.
SUPP = {
    ".logo-sub": {"Handcrafted Glass & Judaica": "זכוכית ויודאיקה בעבודת יד"},
    "h1.sr-only": {
        "Handmade Glass Judaica from Israel - Sherman Art Works":
            "יודאיקה וזכוכית בעבודת יד מישראל - שרמן ארט וורקס"
    },
    ".story-sig": {"The Sherman Family": "משפחת שרמן"},
    ".logo-mark": {},  # img alt handled below
}
# Exact-match Hebrew for notable image alt texts (brand/hero) that aren't product
# names. Product-card alts are set to the Hebrew product name (matching buildCard).
ALT_SUPP = {
    "Sherman Art Works logo": "הלוגו של שרמן ארט וורקס",
    "Handmade glass decorative bowl by Sherman Art Works":
        "קערת זכוכית דקורטיבית בעבודת יד מאת שרמן ארט וורקס",
    # about.html studio/craft photos
    "Sherman Art Works handmade glass piece": "יצירת זכוכית בעבודת יד של שרמן ארט וורקס",
    "Handcrafted glass art detail": "פרט מתוך יצירת אמנות בזכוכית בעבודת יד",
    "Sherman Art Works collection": "הקולקציה של שרמן ארט וורקס",
    "Sherman Art Works glass craft": "אומנות הזכוכית של שרמן ארט וורקס",
    "Handmade glass detail": "פרט מזכוכית בעבודת יד",
    "Sherman glass art": "אמנות הזכוכית של שרמן",
    # faq.html kashrut certificate
    "Kosher certificate for the Sherman Art Works shofar supplier, issued by the Chief Rabbinate of Tel Aviv-Yafo for 2025/26":
        "אישור כשרות של ספק השופרות של שרמן ארט וורקס, מטעם הרבנות הראשית תל אביב-יפו לשנת 2025/26",
}

# Hebrew <title> + meta description per page (authored; concise, <60 / <155 chars).
META = {
    "index.html": (
        "שרמן ארט וורקס | יודאיקה וזכוכית בעבודת יד מישראל",
        "יודאיקה וזכוכית בעבודת יד מישראל - פמוטים, כוסות קידוש, שופרות, מזוזות, גביעי קרן וקערות. משלוח לכל העולם. הזמנות בהתאמה אישית מתקבלות בברכה.",
    ),
    "candlesticks.html": (
        "פמוטים מזכוכית בעבודת יד | שרמן ארט וורקס",
        "פמוטי זכוכית בעבודת יד לנרות שבת, בשיטה המשפחתית המסורתית. מגוון צבעים, מיוצר בישראל ונשלח לכל העולם.",
    ),
    "candlesticks-silver-plated.html": (
        "פמוטי זכוכית בציפוי כסף 925 | שרמן ארט וורקס",
        "פמוטי זכוכית בעבודת יד בגימור כסף 925. שבעה צבעים, שלושה גבהים ואפשרות למגש תואם, מיוצרים בישראל.",
    ),
    "candlesticks-gold-plated.html": (
        "פמוטי זכוכית בציפוי זהב | שרמן ארט וורקס",
        "פמוטי זכוכית בעבודת יד בגימור זהב. שלושה גבהים ואפשרות למגש תואם, מיוצרים בישראל.",
    ),
    "candlesticks-artisanal.html": (
        "פמוטי זכוכית אומנותיים בעבודת יד | שרמן ארט וורקס",
        "פמוטי זכוכית אומנותיים בעבודת יד מישראל במבחר עיצובים צבעוניים, מפוספסים, מנוקדים, שקופים ובסגנון מוראנו.",
    ),
    "horn-goblets.html": (
        "גביעי קרן בציפוי כסף 925 בעבודת יד | שרמן ארט וורקס",
        "גביעי קרן שתייה בציפוי כסף 925 בעבודת יד - עיצובי יודאיקה קלאסיים. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "kiddush-cups.html": (
        "כוסות קידוש בעבודת יד | שרמן ארט וורקס",
        "כוסות וגביעי קידוש בעבודת יד במגוון סגנונות - כוסות זכוכית, כוס קרמיקה וסטים של כוס וצלחת. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "trays-bowls.html": (
        "מגשים וקערות זכוכית בעבודת יד | שרמן ארט וורקס",
        "קערות ומגשים דקורטיביים מזכוכית בעבודת יד למרכז השולחן ולבית. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "kiddush-cups-silver-plated.html": (
        "כוסות קידוש בציפוי כסף 925 | שרמן ארט וורקס",
        "כוסות קידוש בעבודת יד בגימור כסף 925, במבחר צבעים ועם אפשרות לצלחת תואמת. מיוצר בישראל.",
    ),
    "kiddush-cups-gold-plated.html": (
        "כוסות קידוש בציפוי זהב | שרמן ארט וורקס",
        "כוסות קידוש בעבודת יד בגימור זהב, במבחר צבעים ועם אפשרות לצלחת תואמת. מיוצר בישראל.",
    ),
    "havdalah-sets.html": (
        "סטים להבדלה בעבודת יד | שרמן ארט וורקס",
        "סטים להבדלה בעבודת יד בצבעים שחור, כחול, לבן וכתום. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "business-gifts.html": (
        "מתנות לעסקים ולאירועים | שרמן ארט וורקס",
        "מתנות לעסקים, לבתי כנסת, לבר ובת מצווה ולאירועים - שופרות מותאמים אישית וסטי מתנה בעבודת יד מישראל.",
    ),
    "mezuzahs.html": (
        "מזוזות ובתי מזוזה בעבודת יד | שרמן ארט וורקס",
        "בתי מזוזה בעבודת יד במגוון סגנונות - זכוכית וקרן טבעית בציפוי כסף 925. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "shofars.html": (
        "שופרות בעבודת יד עם עיצוב אישי | שרמן ארט וורקס",
        "שופרות בעבודת יד עם אפשרות לעיצוב אישי - סמל וכיתוב לבחירתכם (עברית/English). שופר איל ושופר קודו, מיוצר בישראל.",
    ),
    "shofars-custom.html": (
        "שופרות בהתאמה אישית | שרמן ארט וורקס",
        "שופרות מותאמים אישית - בחרו סמל וכיתוב (עברית/English). שופר איל ושופר קודו בעבודת יד, מיוצר בישראל.",
    ),
    "shofars-rams.html": (
        "שופר איל בעבודת יד | שרמן ארט וורקס",
        "שופרות איל בעבודת יד, עם אפשרות לציפוי כסף 925 ולעיצוב אישי. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "shofars-kudu.html": (
        "שופר קודו בעבודת יד | שרמן ארט וורקס",
        "שופרות קודו גדולים בעבודת יד, עם אפשרות לעיצוב אישי. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "about.html": (
        "אודות | שרמן ארט וורקס",
        "הסיפור של שרמן ארט וורקס - סטודיו משפחתי ליודאיקה וזכוכית בעבודת יד בישראל, מסורת של שלושה דורות של אומנים.",
    ),
    "custom-orders.html": (
        "הזמנות בהתאמה אישית | שרמן ארט וורקס",
        "הזמנות בהתאמה אישית של יודאיקה וזכוכית בעבודת יד - פמוטים, כוסות קידוש, שופרות ומתנות. עיצוב אישי, מיוצר בישראל.",
    ),
    "contact.html": (
        "צור קשר | שרמן ארט וורקס",
        "צרו קשר עם שרמן ארט וורקס - שאלות על מוצרים, הזמנות בהתאמה אישית ומשלוחים. מענה בוואטסאפ או במייל תוך 24 שעות.",
    ),
    "faq.html": (
        "שאלות ותשובות | שרמן ארט וורקס",
        "תשובות לשאלות הנפוצות - זמני משלוח ועלויות, זמני ייצור להזמנה אישית, תשלום, החזרות והאם השופרות כשרים.",
    ),
    "terms.html": (
        "תקנון ומדיניות משלוחים | שרמן ארט וורקס",
        "תקנון האתר, תנאי השימוש ומדיניות המשלוחים וההחזרות של שרמן ארט וורקס.",
    ),
    "privacy.html": (
        "מדיניות פרטיות | שרמן ארט וורקס",
        "מדיניות הפרטיות של שרמן ארט וורקס - איזה מידע נאסף, כיצד הוא משמש וכיצד אנו שומרים עליו.",
    ),
    "accessibility.html": (
        "הצהרת נגישות | שרמן ארט וורקס",
        "הצהרת הנגישות של אתר שרמן ארט וורקס - המחויבות שלנו לנגישות לכלל המשתמשים.",
    ),
}

# sitemap priority per Hebrew page (mirrors the English sitemap).
SITEMAP_PRIORITY = {
    "index.html": "0.9", "custom-orders.html": "0.8", "about.html": "0.7",
    "contact.html": "0.7", "faq.html": "0.6", "terms.html": "0.3", "privacy.html": "0.3",
    "accessibility.html": "0.3",
}

BASE = "https://shermanartworks.com"


# ── helpers ────────────────────────────────────────────────────────────────
def read(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


def he_url(page):
    return BASE + "/he/" if page == "index.html" else BASE + "/he/" + page


def en_url(page):
    return BASE + "/" if page == "index.html" else BASE + "/" + page


def en_href(page):
    """Root-relative href to the English twin (for the EN toggle button)."""
    return "/" if page == "index.html" else "/" + page


def _match_brace_block(text, open_idx):
    """Return substring inside the { } starting at open_idx (index of '{'),
    string-literal aware so braces inside quotes don't confuse the counter."""
    depth = 0
    i = open_idx
    quote = None
    esc = False
    while i < len(text):
        c = text[i]
        if quote:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                quote = None
        else:
            if c in "'\"`":
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[open_idx + 1:i]
        i += 1
    return ""


_UNESC = {"\\'": "'", '\\"': '"', "\\\\": "\\", "\\n": "\n", "\\t": "\t", "\\/": "/"}


def _unescape(s):
    return re.sub(r"\\['\"\\nt/]", lambda m: _UNESC[m.group(0)], s)


def parse_he_dict(text, obj_marker, lang="he"):
    """Extract the `<lang>: { ... }` sub-block of the object introduced by
    obj_marker (e.g. 'const T_SITE' or 'T_PAGE') and return {key: value}.
    Defaults to Hebrew; the English branch is needed to build the EN→HE map
    used when localizing JSON-LD."""
    start = text.find(obj_marker)
    if start < 0:
        return {}
    obj_open = text.find("{", start)
    if obj_open < 0:
        return {}
    obj_body = _match_brace_block(text, obj_open)
    m = re.search(r"\b%s\s*:\s*\{" % lang, obj_body)
    if not m:
        return {}
    he_open = obj_body.find("{", m.start())
    he_body = _match_brace_block(obj_body, he_open)
    # Values may be single-quoted, double-quoted, or a backtick template literal
    # (the site uses backticks for multi-paragraph HTML copy).
    pairs = re.findall(
        r"(\w+)\s*:\s*(?:'((?:[^'\\]|\\.)*)'"
        r"|\"((?:[^\"\\]|\\.)*)\""
        r"|`((?:[^`\\]|\\.)*)`)",
        he_body,
        re.S,
    )
    out = {}
    for key, sq, dq, bt in pairs:
        out[key] = _unescape(sq or dq or bt)
    return out


def _field_values(blob, field):
    """All values of a JS/JSON object field in document order, tolerant of both
    "field": "val"  (JSON) and  field: 'val'  (JS literal) styles."""
    pat = re.compile(
        r'["\']?' + re.escape(field) + r'["\']?\s*:\s*'
        r'(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')'
    )
    return [_unescape(a if a is not None and a != "" else b) for a, b in
            ((m.group(1), m.group(2)) for m in pat.finditer(blob))]


def norm(s):
    """Collapse whitespace so a static card's text matches the source string even
    if the card builder normalised spaces/newlines."""
    return re.sub(r"\s+", " ", s or "").strip()


def esc_html(s):
    """Mirror site.js escapeHtml() - & < > only."""
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_sections(src):
    """Read the page's `var SECTIONS = [...]` list."""
    m = re.search(r"SECTIONS\s*=\s*\[([^\]]*)\]", src)
    if not m:
        return []
    return re.findall(r"'([^']+)'|\"([^\"]+)\"", m.group(1)) and [
        a or b for a, b in re.findall(r"'([^']+)'|\"([^\"]+)\"", m.group(1))
    ]


def render_policy(kind, t, sections):
    """Replicate renderTerms / renderPrivacy / renderA11y in Hebrew.

    Headings/meta go through escapeHtml (text); callout/intro/section bodies are
    raw HTML in the dictionary and are inserted verbatim - exactly as the JS does.
    """
    if kind == "terms":
        html = "<h1>%s</h1>" % esc_html(t.get("terms_h1", ""))
        if t.get("terms_subtitle"):
            html += '<p class="legal-subtitle">%s</p>' % esc_html(t["terms_subtitle"])
        html += '<p class="legal-meta">%s</p>' % esc_html(t.get("terms_updated", ""))
        html += '<div class="terms-callout">%s</div>' % t.get("terms_callout", "")
        for s in sections:
            html += "<h2>%s</h2><div>%s</div>" % (
                esc_html(t.get(s + "_h", "")), t.get(s + "_b", ""))
        return html

    if kind == "privacy":
        html = "<h1>%s</h1>" % esc_html(t.get("privacy_h1", ""))
        html += '<p class="privacy-meta">%s</p>' % esc_html(t.get("privacy_updated", ""))
        html += "<div>%s</div>" % t.get("privacy_intro", "")
        for s in sections:
            html += "<h2>%s</h2><div>%s</div>" % (
                esc_html(t.get(s + "_h", "")), t.get(s + "_b", ""))
        return html

    # a11y
    html = "<h1>%s</h1>" % esc_html(t.get("a11y_h1", ""))
    html += '<p class="legal-meta">%s</p>' % esc_html(t.get("a11y_updated", ""))
    for s in sections:
        html += "<h2>%s</h2><div>%s</div>" % (
            esc_html(t.get("a11y_%s_h" % s, "")), t.get("a11y_%s_b" % s, ""))
    return html


def _first(blob, field):
    v = _field_values(blob, field)
    return v[0] if v else ""


def build_product_records():
    """Map norm(name_en) → {name_he, desc_he} for every product across the inline
    PRODUCTS arrays (JSON *and* single-quoted JS literals) and the shofar
    catalogue. Keyed on the English NAME (stable), not the description - the
    pre-rendered static card descriptions have drifted from the source PRODUCTS
    (see the products-data-sync caveat), so text-matching descriptions is
    unreliable; the name is the safe join key and PRODUCTS is the source of
    truth for the Hebrew copy."""
    recs = {}
    for src_path in SHOP_PAGES + PRODUCT_JS:
        blob = read(os.path.join(ROOT, src_path))
        for m in re.finditer(r'["\']?name_en["\']?\s*:', blob):
            window = blob[m.start(): m.start() + 4000]
            name_en = _first(window, "name_en")
            if not name_en:
                continue
            recs[norm(name_en)] = {
                "name_he": _first(window, "name_he"),
                "desc_he": _first(window, "description_he"),
                "color_he": _first(window, "color_he"),
            }
    return recs


T_SITE_HE = parse_he_dict(read(os.path.join(ROOT, "js/site.js")), "const T_SITE")
T_SITE_EN = parse_he_dict(read(os.path.join(ROOT, "js/site.js")), "const T_SITE", "en")

# ProductGroup headings are page-level copy, not product copy, so they have no
# name_he/description_he to borrow from PRODUCTS. Keyed by productGroupID.
PRODUCT_GROUP_HE = {
    "silver-plated-glass-candlesticks": {
        "name": "פמוטי זכוכית בציפוי כסף 925",
        "description": "זוג פמוטי זכוכית בעבודת יד בציפוי כסף 925, "
                       "זמין בשבעה צבעים ובשלושה גבהים.",
    },
    "gold-plated-glass-candlesticks": {
        "name": "פמוטי זכוכית בציפוי זהב",
        "description": "זוג פמוטי זכוכית בעבודת יד בציפוי זהב, "
                       "זמין בשבעה צבעים ובשלושה גבהים.",
    },
    "silver-plated-glass-trays": {
        "name": "מגשי זכוכית בציפוי כסף 925",
        "description": "מגשי זכוכית בעבודת יד בציפוי כסף 925, "
                       "בשישה עיצובים מתואמים.",
    },
    "gold-plated-glass-trays": {
        "name": "מגשי זכוכית בציפוי זהב",
        "description": "מגשי זכוכית בעבודת יד בציפוי זהב, "
                       "בשבעה עיצובים מתואמים.",
    },
    "classic-havdalah-sets": {
        "name": "סטים להבדלה קלאסיים",
        "description": "סטים להבדלה בעבודת יד בצבעים שחור, כחול ולבן, "
                       "מיוצרים בסטודיו שלנו בישראל.",
    },
}


def he_units(value):
    """cm → ס״מ inside a schema size string ("30 × 18 cm", "S (14-18 cm)")."""
    if isinstance(value, list):
        return [he_units(v) for v in value]
    if isinstance(value, str):
        return re.sub(r"(\d)\s*cm\b", "\\1 ס״מ", value)
    return value


def localize_jsonld(txt, en2he):
    """Translate the FAQPage answers and HowTo steps inside a JSON-LD block.

    A /he/ page renders Hebrew but inherited its parent's English JSON-LD, so
    the markup described content the Hebrew reader never sees - the same
    visible/schema mismatch the English pages were fixed for, just one language
    over. Values are matched by exact English string rather than by position,
    so a reordered or extended FAQ cannot silently mis-pair questions with
    answers; anything without a Hebrew counterpart is left in English rather
    than guessed at."""
    try:
        data = json.loads(txt)
    except ValueError:
        return txt, 0

    hits = [0]

    def tr(s):
        if isinstance(s, str) and s in en2he and en2he[s]:
            hits[0] += 1
            return en2he[s]
        return s

    def tr_variant(node):
        """A ProductGroup variant describes a product the Hebrew reader sees in
        Hebrew, so its name/description/color come from PRODUCTS rather than
        being left in English. Joined on the English name, same key as the
        static cards. Offers are left alone - prices and the seller/shipping/
        return @id refs are language-neutral, so the /he/ page inherits the
        English page's full merchant-listing shape for free."""
        rec = PRODUCTS_HE.get(norm(node.get("name")))
        if not rec:
            return
        if rec.get("name_he"):
            node["name"] = rec["name_he"]
            hits[0] += 1
        if rec.get("desc_he"):
            node["description"] = rec["desc_he"]
        if rec.get("color_he") and node.get("color"):
            node["color"] = rec["color_he"]
        if node.get("size"):
            node["size"] = he_units(node["size"])

    def walk(node):
        if isinstance(node, dict):
            ty = node.get("@type")
            if ty == "Question":
                node["name"] = tr(node.get("name"))
            elif ty == "Answer":
                node["text"] = tr(node.get("text"))
            elif ty == "HowToStep":
                node["name"] = tr(node.get("name"))
                node["text"] = tr(node.get("text"))
            elif ty in ("FAQPage", "HowTo"):
                node["inLanguage"] = "he"
            elif ty == "ProductGroup":
                group = PRODUCT_GROUP_HE.get(node.get("productGroupID"))
                if group:
                    node["name"] = group["name"]
                    node["description"] = group["description"]
                    node["inLanguage"] = "he"
                    hits[0] += 1
                for variant in node.get("hasVariant", []):
                    tr_variant(variant)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data)
    if not hits[0]:
        return txt, 0
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")), hits[0]
PRODUCTS_HE = build_product_records()


# ── link / asset rewriting ─────────────────────────────────────────────────
SKIP_PREFIXES = ("http://", "https://", "//", "#", "mailto:", "tel:", "javascript:", "data:")


def rewrite_url(url):
    """Fix a relative href/src for a page that now lives under /he/."""
    if not url or url.startswith(SKIP_PREFIXES):
        return url
    if url.startswith("/"):
        # Root-absolute already. Send home + English-only pages sensibly.
        if url in ("/", "/index.html"):
            return "/he/"
        return url
    # relative
    frag = ""
    if "#" in url:
        url, frag = url.split("#", 1)
        frag = "#" + frag
    if url == "" or url == "./":  # pure in-page anchor like "#shop" handled above
        return url + frag
    url = url[2:] if url.startswith("./") else url
    if url.endswith(".html"):
        if url in TRANSLATED:
            return url + frag          # stays inside /he/
        return "/" + url + frag        # English-only page → root
    # asset (css/…, js/…, sitemap.xml, images …) → root-absolute
    return "/" + url + frag


def rewrite_links(soup):
    for tag, attr in (("a", "href"), ("link", "href"), ("script", "src"), ("img", "src")):
        for el in soup.find_all(tag):
            if el.has_attr(attr):
                el[attr] = rewrite_url(el[attr])
        # srcset / data-src style attrs are absolute Cloudinary URLs → untouched


# ── the transform ──────────────────────────────────────────────────────────
def translate_page(page):
    src = read(os.path.join(ROOT, page))
    soup = BeautifulSoup(src, "html.parser")

    page_he = parse_he_dict(src, "T_PAGE")
    dict_he = dict(FALLBACK_HE)          # lowest priority: fills keys a page's
    dict_he.update(T_SITE_HE)            # own dict forgot to define
    dict_he.update(page_he)

    # 0) Shofar pages alias generic hero keys from a page-specific key at runtime
    #    (t.hero_subtitle = t['hero_'+PAGE_KEY+'_subtitle']). Replicate so the
    #    static [data-t="hero_subtitle"] etc. resolve to the right Hebrew copy.
    mkey = re.search(r"const PAGE_KEY\s*=\s*'(\w+)'", src)
    if mkey:
        pk = mkey.group(1)
        for base in ("hero_headline", "hero_subtitle", "hero_body"):
            alias = base.replace("hero_", "hero_%s_" % pk)
            if dict_he.get(alias):
                dict_he[base] = dict_he[alias]
        if dict_he.get("bc_%s" % pk):
            dict_he["bc_current"] = dict_he["bc_%s" % pk]

    # 1) [data-t] swaps - mirror setLang() exactly.
    for el in soup.select("[data-t]"):
        key = el.get("data-t")
        if key not in dict_he:
            continue
        val = dict_he[key]
        el.clear()
        if key in RICH_KEYS:
            for node in list(BeautifulSoup(val, "html.parser").contents):
                el.append(node)
        else:
            el.append(val)

    # 1a) policy pages: rebuild the legal <main> body in Hebrew, replicating the
    #     page's JS render fn so the no-JS/crawler view carries the legal text.
    if page in POLICY:
        cfg = POLICY[page]
        container = soup.find(id=cfg["container"])
        if container is not None:
            body_html = render_policy(cfg["kind"], dict_he, parse_sections(src))
            container.clear()
            # list() is required: append() detaches the node from the temp soup,
            # so iterating .contents directly would mutate it and skip elements.
            for node in list(BeautifulSoup(body_html, "html.parser").contents):
                container.append(node)

    # 2) product cards - join each card to its product by NAME (stable), then take
    #    Hebrew name + first-line description straight from PRODUCTS (source of
    #    truth). Also set img alt to the Hebrew name, matching buildCard().
    for card in soup.select(".product-card"):
        name_el = card.select_one(".product-card-name")
        if not name_el:
            continue
        rec = PRODUCTS_HE.get(norm(name_el.get_text()))
        if not rec:
            continue
        if rec["name_he"]:
            name_el.clear()
            name_el.append(rec["name_he"])
        desc_el = card.select_one(".product-card-desc")
        if desc_el and rec["desc_he"]:
            desc_el.clear()
            desc_el.append(rec["desc_he"].split("\n")[0].strip())
        img = card.select_one(".product-card-img-wrap img") or card.select_one("img")
        if img and img.has_attr("alt") and rec["name_he"]:
            img["alt"] = rec["name_he"]

    # 2-price) shofar cards show "from ₪…" (size ladders) with no data-t hook.
    #    Localise the leading label to the Hebrew price_from ("החל מ־").
    pf = dict_he.get("price_from") or "החל מ־"
    for el in soup.select(".product-card-price"):
        for node in el.contents:
            if isinstance(node, NavigableString):
                s = str(node)
                if s.lstrip().lower().startswith("from "):
                    lead = s[: len(s) - len(s.lstrip())]
                    node.replace_with(lead + pf + " " + s.lstrip()[5:])
                break

    # 2a) per-card color note (no data-t in static markup) → Hebrew.
    note_he = T_SITE_HE.get("color_note")
    if note_he:
        for el in soup.select(".product-card-color-note, .product-color-note"):
            el.clear()
            el.append(note_he)

    # 2b) homepage category-card image alt → the (now-Hebrew) category title.
    for card in soup.select(".cat-card"):
        title_el = card.select_one(".cat-card-title")
        img = card.select_one("img")
        if title_el and img and img.has_attr("alt"):
            img["alt"] = title_el.get_text().strip()

    # 2c) static header/footer/hero strings with no data-t hook → Hebrew.
    for sel, mapping in SUPP.items():
        for el in soup.select(sel):
            t = el.get_text().strip()
            if t in mapping:
                el.clear()
                el.append(mapping[t])
    for img in soup.find_all("img"):
        if img.get("alt", "").strip() in ALT_SUPP:
            img["alt"] = ALT_SUPP[img["alt"].strip()]

    # 3) homepage "from ₪…" cards: localise the leading label.
    for el in soup.select(".cat-card-from"):
        txt = el.get_text()
        if txt.strip().lower().startswith("from "):
            el.string = "מ-" + txt.strip()[5:]

    # 4) <html lang/dir>
    html = soup.find("html")
    html["lang"] = "he"
    html["dir"] = "rtl"

    # 5) head: title, description, canonical, hreflang, og.
    title_he, desc_he = META[page]
    if soup.title:
        soup.title.string = title_he
    head = soup.find("head")

    def set_meta(attr, key, value):
        m = soup.find("meta", attrs={attr: key})
        if m:
            m["content"] = value
        else:
            m = soup.new_tag("meta")
            m[attr] = key
            m["content"] = value
            head.append(m)
        return m

    set_meta("name", "description", desc_he)
    set_meta("property", "og:title", title_he)
    set_meta("property", "og:description", desc_he)
    set_meta("property", "og:locale", "he_IL")
    set_meta("property", "og:url", he_url(page))

    can = soup.find("link", attrs={"rel": "canonical"})
    if can:
        can["href"] = he_url(page)

    # bidirectional hreflang (drop any pre-existing alternates first)
    for alt in soup.find_all("link", attrs={"rel": "alternate"}):
        if alt.get("hreflang"):
            alt.decompose()
    anchor = can or soup.title
    for hl, href in (("en", en_url(page)), ("he-IL", he_url(page)), ("x-default", en_url(page))):
        link = soup.new_tag("link", rel="alternate", hreflang=hl, href=href)
        anchor.insert_after(link)

    # 6) force Hebrew at runtime (before site.js init reads it).
    guard = soup.new_tag("script")
    guard.string = "window.__SA_LANG='he';"
    head.insert(0, guard)

    # 7) language toggle: EN button navigates to the English twin (keeping
    #    localStorage in sync); HE button marked active.
    btn_en = soup.find(id="btnEN")
    if btn_en:
        btn_en["onclick"] = (
            "localStorage.setItem('sa_lang','en');location.href='%s'" % en_href(page)
        )
    btn_he = soup.find(id="btnHE")
    if btn_he:
        cls = btn_he.get("class", [])
        if "active" not in cls:
            cls.append("active")
        btn_he["class"] = cls

    # 8) rewrite relative asset + cross-page URLs for the /he/ subdirectory.
    rewrite_links(soup)

    # 9) point JSON-LD self-URLs at the /he/ page, and translate the FAQ/HowTo
    #    content so the markup describes the Hebrew the reader actually sees.
    en2he = {}
    page_en = parse_he_dict(src, "T_PAGE", "en")
    for en_dict, he_dict in ((T_SITE_EN, T_SITE_HE), (page_en, page_he)):
        for k, en_val in en_dict.items():
            if he_dict.get(k):
                en2he[en_val] = he_dict[k]

    en_page_url = en_url(page)
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if not s.string:
            continue
        txt = s.string.replace(en_page_url, he_url(page))
        txt, _ = localize_jsonld(txt, en2he)
        s.string = txt

    return str(soup)


def he_href(page):
    return "/he/" if page == "index.html" else "/he/" + page


def patch_category_navigation():
    """Place Havdalah Sets between Kiddush Cups and Mezuzahs in shop menus.

    Shared navigation is duplicated in the static pages. Keeping this raw-text
    and line-based preserves the hand-authored markup. Footer lists are left
    unchanged because they do not contain the full ordered category list.
    """
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        out = []
        for line in lines:
            is_menu_line = 'role="menuitem"' in line or 'onclick="closeMobileNav()"' in line
            if not is_menu_line:
                out.append(line)
                continue

            # The Havdalah page keeps menu anchors on one compact line.
            if line.count("<a") > 1:
                line = re.sub(
                    r'<a href="havdalah-sets\.html"[^>]*(?:role="menuitem"|onclick="closeMobileNav\(\)")[^>]*>.*?</a>',
                    "",
                    line,
                )

                def add_havdalah_after_kiddush(match):
                    anchor = match.group(0)
                    new = anchor.replace('href="kiddush-cups.html"', 'href="havdalah-sets.html"', 1)
                    new = re.sub(r'data-t="[^"]+"', 'data-t="cat8_title"', new, count=1)
                    new = re.sub(r'(<a\b[^>]*>).*?(</a>)', r'\1Havdalah Sets\2', new, count=1)
                    return anchor + new

                line = re.sub(
                    r'<a href="kiddush-cups\.html"[^>]*(?:role="menuitem"|onclick="closeMobileNav\(\)")[^>]*>.*?</a>',
                    add_havdalah_after_kiddush,
                    line,
                )
                out.append(line)
                continue

            if 'href="havdalah-sets.html"' in line:
                continue

            out.append(line)
            if 'href="kiddush-cups.html"' in line:
                new = line.replace('href="kiddush-cups.html"', 'href="havdalah-sets.html"', 1)
                new = re.sub(r'data-t="[^"]+"', 'data-t="cat8_title"', new, count=1)
                new = re.sub(r'(<a\b[^>]*>).*?(</a>)', r'\1Havdalah Sets\2', new, count=1)
                out.append(new)

        if out != lines:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.writelines(out)
            print("ordered Havdalah Sets navigation in %s" % name)


def patch_english_pages():
    """Surgical raw-text edits on the live English pages (no bs4 re-serialization,
    so diffs stay minimal): add bidirectional hreflang after the canonical link,
    and route the עברית toggle to the /he/ twin. Idempotent."""
    for page in PAGES:
        path = os.path.join(ROOT, page)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        orig = txt
        en, he = en_url(page), he_url(page)

        if 'hreflang="he-IL"' not in txt:
            block = (
                '\n  <link rel="alternate" hreflang="en" href="%s" />'
                '\n  <link rel="alternate" hreflang="he-IL" href="%s" />'
                '\n  <link rel="alternate" hreflang="x-default" href="%s" />'
            ) % (en, he, en)
            txt = re.sub(
                r'(<link rel="canonical" href="[^"]*" />)',
                lambda m: m.group(1) + block,
                txt,
                count=1,
            )

        # Route the Hebrew toggle to the indexable /he/ page (keeps localStorage
        # in sync so the choice persists) instead of an in-place JS swap.
        txt = txt.replace(
            '<button id="btnHE" class="toggle-btn" onclick="setLang(\'he\')">',
            "<button id=\"btnHE\" class=\"toggle-btn\" "
            "onclick=\"localStorage.setItem('sa_lang','he');location.href='%s'\">" % he_href(page),
        )

        if txt != orig:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(txt)
            print("patched %s" % page)


def _en_lastmods(xml):
    """Map English <loc> → <lastmod> from the current sitemap."""
    out = {}
    for block in re.findall(r"<url>.*?</url>", xml, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block, re.S)
        lm = re.search(r"<lastmod>(.*?)</lastmod>", block, re.S)
        if loc and lm and "/he/" not in loc.group(1):
            out[loc.group(1).strip()] = lm.group(1).strip()
    return out


def he_lastmod(page, en_map):
    """A Hebrew page is generated from its English counterpart, so it is only as
    fresh as that source. Mirroring the English <lastmod> keeps the value honest
    and stable - deriving it from the generated file's mtime would instead bump
    every Hebrew URL on every run, telling crawlers the page changed when it did
    not. Falls back to today only when the English URL carries no lastmod."""
    return en_map.get(en_url(page)) or datetime.date.today().isoformat()


def update_sitemap():
    """Ensure every /he/ URL is listed in sitemap.xml with a <lastmod>. Idempotent
    per URL, so it also backfills pages added after the first run, and backfills
    <lastmod> onto /he/ entries written before it was emitted."""
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        xml = f.read()
    en_map = _en_lastmods(xml)

    # Backfill <lastmod> on existing /he/ entries that predate this field.
    # Order matters: the sitemap schema wants loc, lastmod, changefreq, priority.
    backfilled = 0
    for page in PAGES:
        url = he_url(page)
        block_re = re.compile(
            r"(<url>\s*<loc>%s</loc>\s*)(<changefreq>)" % re.escape(url), re.S
        )
        if block_re.search(xml):
            xml = block_re.sub(
                lambda m: "%s<lastmod>%s</lastmod>\n    %s"
                % (m.group(1), he_lastmod(page, en_map), m.group(2)),
                xml,
            )
            backfilled += 1

    missing = [p for p in PAGES if "<loc>%s</loc>" % he_url(p) not in xml]
    entries = []
    if missing and "Hebrew (/he/) pages" not in xml:
        entries.append("\n  <!-- Hebrew (/he/) pages -->")
    for page in missing:
        pri = SITEMAP_PRIORITY.get(page, "0.8")
        freq = "yearly" if pri == "0.3" else "weekly"
        entries.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (he_url(page), he_lastmod(page, en_map), freq, pri)
        )
    if entries:
        xml = xml.replace("</urlset>", "\n".join(entries) + "\n\n</urlset>")

    if not missing and not backfilled:
        print("sitemap already lists all %d /he/ URLs with lastmod" % len(PAGES))
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    if missing:
        print("added %d /he/ URL(s) to sitemap.xml" % len(missing))
    if backfilled:
        print("backfilled <lastmod> on %d existing /he/ URL(s)" % backfilled)


def main():
    print("-- category navigation --")
    patch_category_navigation()
    os.makedirs(HE_DIR, exist_ok=True)
    for page in PAGES:
        out = translate_page(page)
        with open(os.path.join(HE_DIR, page), "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print("wrote he/%s" % page)
    print("\n%d Hebrew pages generated in %s" % (len(PAGES), HE_DIR))
    print("\n-- patching English pages --")
    patch_english_pages()
    print("\n-- sitemap --")
    update_sitemap()


if __name__ == "__main__":
    main()
