# -*- coding: utf-8 -*-
"""
_he_pages.py — generate static Hebrew /he/ versions of the shop pages.

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
so nothing is re-translated by hand — the Hebrew stays a single source of truth.

Output: /he/<page>.html for each SHOP_PAGES entry. English pages are left to a
separate, minimal edit (hreflang + toggle link); this script only writes /he/.
"""

import os
import re
import json
from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.abspath(__file__))
HE_DIR = os.path.join(ROOT, "he")

# Pages that get a Hebrew twin. Order = homepage, then the 7 shop categories,
# then the 3 shofar sub-category pages (same template, shared catalogue).
SHOP_PAGES = [
    "index.html",
    "candlesticks.html",
    "horn-goblets.html",
    "kiddush-cups.html",
    "trays-bowls.html",
    "business-gifts.html",
    "mezuzahs.html",
    "shofars.html",
    "shofars-custom.html",
    "shofars-rams.html",
    "shofars-kudu.html",
]
TRANSLATED = set(SHOP_PAGES)

# Extra JS files to mine for product name_he/description_he (shofar catalogue).
PRODUCT_JS = ["js/shofar-products.js"]

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
# leaves some of these English too (a latent i18n gap in the shared chrome) — but
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
}

# Hebrew <title> + meta description per page (authored; concise, <60 / <155 chars).
META = {
    "index.html": (
        "שרמן ארט וורקס | יודאיקה וזכוכית בעבודת יד מישראל",
        "יודאיקה וזכוכית בעבודת יד מישראל — פמוטים, כוסות קידוש, שופרות, מזוזות, גביעי קרן וקערות. משלוח לכל העולם. הזמנות בהתאמה אישית מתקבלות בברכה.",
    ),
    "candlesticks.html": (
        "פמוטים מזכוכית בעבודת יד | שרמן ארט וורקס",
        "פמוטי זכוכית בעבודת יד לנרות שבת, בשיטה המשפחתית המסורתית. מגוון צבעים, מיוצר בישראל ונשלח לכל העולם.",
    ),
    "horn-goblets.html": (
        "גביעי קרן בציפוי כסף בעבודת יד | שרמן ארט וורקס",
        "גביעי קרן שתייה בציפוי כסף בעבודת יד — עיצובי יודאיקה קלאסיים. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "kiddush-cups.html": (
        "כוסות קידוש בעבודת יד | שרמן ארט וורקס",
        "כוסות וגביעי קידוש בעבודת יד במגוון סגנונות — כוסות זכוכית, כוס קרמיקה וסטים של כוס וצלחת. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "trays-bowls.html": (
        "מגשים וקערות זכוכית בעבודת יד | שרמן ארט וורקס",
        "קערות ומגשים דקורטיביים מזכוכית בעבודת יד למרכז השולחן ולבית. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "business-gifts.html": (
        "מתנות לעסקים ולאירועים | שרמן ארט וורקס",
        "מתנות לעסקים, לבתי כנסת, לבר ובת מצווה ולאירועים — שופרות מותאמים אישית וסטי מתנה בעבודת יד מישראל.",
    ),
    "mezuzahs.html": (
        "מזוזות ובתי מזוזה בעבודת יד | שרמן ארט וורקס",
        "בתי מזוזה בעבודת יד במגוון סגנונות — זכוכית וקרן טבעית בציפוי כסף. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "shofars.html": (
        "שופרות בעבודת יד עם עיצוב אישי | שרמן ארט וורקס",
        "שופרות בעבודת יד עם אפשרות לעיצוב אישי — סמל וכיתוב לבחירתכם (עברית/English). שופר איל ושופר קודו, מיוצר בישראל.",
    ),
    "shofars-custom.html": (
        "שופרות בהתאמה אישית | שרמן ארט וורקס",
        "שופרות מותאמים אישית — בחרו סמל וכיתוב (עברית/English). שופר איל ושופר קודו בעבודת יד, מיוצר בישראל.",
    ),
    "shofars-rams.html": (
        "שופר איל בעבודת יד | שרמן ארט וורקס",
        "שופרות איל בעבודת יד, עם אפשרות לציפוי כסף ולעיצוב אישי. מיוצר בישראל, משלוח לכל העולם.",
    ),
    "shofars-kudu.html": (
        "שופר קודו בעבודת יד | שרמן ארט וורקס",
        "שופרות קודו גדולים בעבודת יד, עם אפשרות לעיצוב אישי. מיוצר בישראל, משלוח לכל העולם.",
    ),
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


def parse_he_dict(text, obj_marker):
    """Extract the `he: { ... }` sub-block of the object introduced by obj_marker
    (e.g. 'const T_SITE' or 'T_PAGE') and return {key: value} for Hebrew."""
    start = text.find(obj_marker)
    if start < 0:
        return {}
    obj_open = text.find("{", start)
    if obj_open < 0:
        return {}
    obj_body = _match_brace_block(text, obj_open)
    m = re.search(r"\bhe\s*:\s*\{", obj_body)
    if not m:
        return {}
    he_open = obj_body.find("{", m.start())
    he_body = _match_brace_block(obj_body, he_open)
    pairs = re.findall(
        r"(\w+)\s*:\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")",
        he_body,
    )
    out = {}
    for key, sq, dq in pairs:
        out[key] = _unescape(sq if sq else dq)
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


def _first(blob, field):
    v = _field_values(blob, field)
    return v[0] if v else ""


def build_product_records():
    """Map norm(name_en) → {name_he, desc_he} for every product across the inline
    PRODUCTS arrays (JSON *and* single-quoted JS literals) and the shofar
    catalogue. Keyed on the English NAME (stable), not the description — the
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
            }
    return recs


T_SITE_HE = parse_he_dict(read(os.path.join(ROOT, "js/site.js")), "const T_SITE")
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

    # 1) [data-t] swaps — mirror setLang() exactly.
    for el in soup.select("[data-t]"):
        key = el.get("data-t")
        if key not in dict_he:
            continue
        val = dict_he[key]
        el.clear()
        if key in RICH_KEYS:
            for node in BeautifulSoup(val, "html.parser").contents:
                el.append(node)
        else:
            el.append(val)

    # 2) product cards — join each card to its product by NAME (stable), then take
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
    for hl, href in (("en", en_url(page)), ("he", he_url(page)), ("x-default", en_url(page))):
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

    # 9) point JSON-LD self-URLs at the /he/ page + tag inLanguage he.
    en_page_url = en_url(page)
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if not s.string:
            continue
        txt = s.string.replace(en_page_url, he_url(page))
        s.string = txt

    return str(soup)


def he_href(page):
    return "/he/" if page == "index.html" else "/he/" + page


def patch_english_pages():
    """Surgical raw-text edits on the live English pages (no bs4 re-serialization,
    so diffs stay minimal): add bidirectional hreflang after the canonical link,
    and route the עברית toggle to the /he/ twin. Idempotent."""
    for page in SHOP_PAGES:
        path = os.path.join(ROOT, page)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        orig = txt
        en, he = en_url(page), he_url(page)

        if 'hreflang="he"' not in txt:
            block = (
                '\n  <link rel="alternate" hreflang="en" href="%s" />'
                '\n  <link rel="alternate" hreflang="he" href="%s" />'
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


def update_sitemap():
    """Add the /he/ URLs to sitemap.xml (idempotent)."""
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        xml = f.read()
    if "/he/" in xml:
        print("sitemap already has /he/ URLs — skipped")
        return
    entries = ["\n  <!-- Hebrew (/he/) pages -->"]
    for page in SHOP_PAGES:
        loc = he_url(page)
        pri = "0.9" if page == "index.html" else "0.8"
        entries.append(
            "  <url>\n    <loc>%s</loc>\n    <changefreq>weekly</changefreq>\n"
            "    <priority>%s</priority>\n  </url>" % (loc, pri)
        )
    block = "\n".join(entries) + "\n\n"
    xml = xml.replace("</urlset>", block + "</urlset>")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print("added %d /he/ URLs to sitemap.xml" % len(SHOP_PAGES))


def main():
    os.makedirs(HE_DIR, exist_ok=True)
    for page in SHOP_PAGES:
        out = translate_page(page)
        with open(os.path.join(HE_DIR, page), "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print("wrote he/%s" % page)
    print("\n%d Hebrew pages generated in %s" % (len(SHOP_PAGES), HE_DIR))
    print("\n-- patching English pages --")
    patch_english_pages()
    print("\n-- sitemap --")
    update_sitemap()


if __name__ == "__main__":
    main()
