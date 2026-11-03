# -*- coding: utf-8 -*-
"""_share_page.py - the unlisted page family uses to send clients product links.

Why this exists
---------------
Old clients still message a family member's phone to buy, and he answers with
photos from his gallery, so the order never reaches the shop. This page lets him
answer with a link instead: every live product with its photo, name and price,
and a button that opens WhatsApp with a ready message and the product page's
link already written. He picks the client and sends. WhatsApp shows the link as
the product photo (every product page carries og:image), so for him it is the
same as sending a picture, and the client lands on a page with Add to Cart.

Every link it sends carries ?ref=share. js/site.js notes that in the client's
browser (sa_shared), the checkout sends it with a card order and a WhatsApp
order names it in its message, so the studio can see which orders the links
brought (privacy.html describes sa_shared).

The page is not in the sitemap, not linked from anywhere and carries noindex.
It is deliberately not listed in robots.txt either, which every bot reads and
which would only advertise it. Nothing on it is private: it holds public
product links and prices. It names no person (the owner's rule for the site).
It loads none of the site's scripts, so it shows no cookie banner, counts no
cart activity and sends nothing to GA4.

What it reads
-------------
  data/products.json   the products, in shop order (live ones with a page)
  js/site.js           the sale functions, copied verbatim, so a sale shown on
                       the site is the sale shown here
  js/site.js T_SITE    the category names, in both languages

The chain runs it after _product_pages.py, since it links those pages.

    python _share_page.py           write share.html
    python _share_page.py --check   report only, exit 1 if share.html is stale
"""

import html
import json
import re
import sys
from pathlib import Path

from _hanukkah_page import BASE, image
from _he_pages import T_SITE_EN, T_SITE_HE
from _static_cards import has_page, price_of
from _usd import usd_from_ils

SITE = Path(__file__).parent
OUT = SITE / "share.html"
REF = "share"

# Category order on the page, with the T_SITE key that names each one.
CATEGORIES = [
    ("candlesticks", "cat1_title"),
    ("kiddush-cups", "cat3_title"),
    ("hanukkah-menorahs", "cat9_title"),
    ("shofars", "cat7_title"),
    ("havdalah-sets", "cat8_title"),
    ("trays-bowls", "cat4_title"),
    ("mezuzahs", "cat6_title"),
]

# The sale code the page runs, by name, exactly as js/site.js has it.
SALE_CONSTS = ["LAUNCH_DISCOUNT", "HANUKKAH_SALE_START", "HANUKKAH_SALE_END",
               "SHOPPINGIL_SALE_START", "SHOPPINGIL_SALE_END", "SHOPPINGIL_DISCOUNT"]
SALE_FUNCS = ["hanukkahSaleActive", "isHanukkahMenorah", "shoppingilSaleActive", "productDiscount"]

# Every visible string. Messages are written as the sender, about the studio,
# so they read right from someone who is not the studio himself. Plain hyphens,
# American English, and shipping stated as the site states it (sherman-copy-rules).
TEXT = {
    "he": {
        "title": "שליחת קישורים ללקוחות",
        "intro": "מוצאים את הפריט, לוחצים על \"שליחה בוואטסאפ\", בוחרים את הלקוח ושולחים. "
                 "הלקוח יקבל את התמונה עם קישור לדף שבו אפשר להזמין.",
        "tip": "כדאי לשמור את הדף במסך הבית: בתפריט הדפדפן בוחרים \"הוספה למסך הבית\".",
        "ready": "הודעות מוכנות",
        "products": "פריטים",
        "search": "חיפוש לפי שם או צבע",
        "all": "הכל",
        "send": "שליחה בוואטסאפ",
        "copy": "העתקה",
        "copied": "הועתק",
        "view": "צפייה",
        "from": "החל מ-",
        "none": "לא נמצא פריט. נסו מילה אחרת.",
        "sale": "יש מבצע באתר עכשיו, והמחירים כאן כבר אחרי ההנחה.",
        "collection": "שליחת כל הקולקציה",
        "footer": "המחירים והפריטים מתעדכנים יחד עם האתר. קישורים שנשלחים מהדף הזה מסומנים, "
                  "כדי שהסטודיו יוכל לראות אילו הזמנות הגיעו דרכם.",
        "other": "English",
        "m_shop": "כל האתר",
        "m_order": "איך מזמינים",
        "m_custom": "הזמנה אישית",
        "msg_product": "שלום! הנה {name} של שרמן ארט וורקס 👇\n{url}\n"
                       "בקישור יש תמונות, מידות ומחיר, ואפשר להזמין ישירות באתר. "
                       "משלוח בישראל ₪35 (לחו\"ל $45), או איסוף עצמי מהגלריה בקרני שומרון.",
        "msg_collection": "שלום! כאן אפשר לראות את כל קולקציית {name} של שרמן ארט וורקס 👇\n{url}\n"
                          "בכל פריט יש תמונות ומחיר, ואפשר להזמין ישירות באתר.",
        "msg_shop": "שלום! כל העבודות של שרמן ארט וורקס נמצאות עכשיו באתר, עם תמונות ומחירים, "
                    "ואפשר להזמין ישירות 👇\n{url}",
        "msg_order": "איך מזמינים? בוחרים פריט באתר, מוסיפים לעגלה ומשלמים בכרטיס אשראי, "
                     "או שולחים את ההזמנה בוואטסאפ ישירות מהעגלה. "
                     "משלוח בישראל ₪35 (לחו\"ל $45), או איסוף עצמי מהגלריה בקרני שומרון.\n{url}",
        "msg_custom": "לעבודה בהזמנה אישית אפשר לספר לסטודיו כאן מה חשוב לכם, "
                      "ויחזרו אליכם עם הצעה 👇\n{url}",
    },
    "en": {
        "title": "Send links to clients",
        "intro": "Find the piece, tap \"Send on WhatsApp\", pick the client and send. "
                 "They get the photo with a link to a page where they can order.",
        "tip": "Tip: save this page to your home screen. In the browser menu, choose \"Add to Home screen\".",
        "ready": "Ready messages",
        "products": "pieces",
        "search": "Search by name or color",
        "all": "All",
        "send": "Send on WhatsApp",
        "copy": "Copy",
        "copied": "Copied",
        "view": "View",
        "from": "From ",
        "none": "Nothing found. Try another word.",
        "sale": "There is a sale on the site right now, and the prices here already include it.",
        "collection": "Send the whole collection",
        "footer": "Prices and pieces update with the site. Links sent from this page are tagged "
                  "so the studio can see which orders came through them.",
        "other": "עברית",
        "m_shop": "The whole shop",
        "m_order": "How to order",
        "m_custom": "Custom piece",
        "msg_product": "Hi! Here's a link to the {name} from Sherman Art Works:\n{url}\n"
                       "The link has the photos, sizes and price, and you can order right there on the site. "
                       "Shipping is ₪35 in Israel and $45 abroad, or you can pick it up at the gallery in Karnei Shomron.",
        "msg_collection": "Hi! Here's the whole {name} collection from Sherman Art Works:\n{url}\n"
                          "Every piece has photos and a price, and you can order right on the site.",
        "msg_shop": "Hi! All of Sherman Art Works' pieces are on the website now, with photos and prices, "
                    "and you can order right there:\n{url}",
        "msg_order": "How to order: pick a piece on the site, add it to the cart and pay by card, "
                     "or send the order on WhatsApp straight from the cart. "
                     "Shipping is ₪35 in Israel and $45 abroad, or you can pick it up at the gallery in Karnei Shomron.\n{url}",
        "msg_custom": "For a custom piece, tell the studio what you have in mind here and they'll get back to you "
                      "with a quote:\n{url}",
    },
}

# The ready messages and the page each one links (relative to the language root).
READY = [("m_shop", "msg_shop", ""),
         ("m_order", "msg_order", ""),
         ("m_custom", "msg_custom", "custom-orders.html")]

CSS = """
:root{--bg:#faf7f2;--card:#fff;--ink:#202020;--muted:#5f5a52;--line:#e4dccd;--gold:#d4b572;--gold-ink:#7d5a00;--wa:#0f6e4f;--wa-ink:#fff}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Varela Round',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;font-size:17px;line-height:1.5}
.wrap{max-width:1100px;margin:0 auto;padding:16px}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:8px}
header>div{min-width:0}
h1{font-size:1.3rem;margin:0}
h2{font-size:1.1rem;margin:22px 0 10px}
.brand{color:var(--gold-ink);font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 2px}
.lang{border:1px solid var(--ink);background:none;color:var(--ink);border-radius:999px;padding:8px 16px;font:inherit;font-size:.95rem;cursor:pointer;min-height:44px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:10px 0}
.intro p{margin:0 0 6px}.intro p:last-child{margin:0;color:var(--muted);font-size:.92rem}
.sale{background:#f3e6c4;border-radius:10px;padding:10px 14px;margin:10px 0;font-size:.95rem}
.ready{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.msg{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:8px}
.msg strong{font-size:1rem}
.pair{display:flex;gap:6px}.pair .send{flex:2}.pair .ghost{flex:1}
.chips{display:flex;gap:8px;overflow-x:auto;padding:2px 0 8px;margin:0 -16px;padding-inline:16px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:9px 16px;font:inherit;font-size:.95rem;cursor:pointer;min-height:44px}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
.search{width:100%;font:inherit;font-size:1rem;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);margin:4px 0 10px;min-height:48px}
.bar{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px;color:var(--muted);font-size:.92rem}
.grid{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media (min-width:700px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1000px){.grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.card img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;background:#f1ece3}
.card .body{padding:10px 10px 12px;display:flex;flex-direction:column;gap:8px;flex:1}
.name{font-size:.95rem;line-height:1.35;margin:0}
.price{font-size:.95rem;color:var(--gold-ink);margin:0;margin-top:auto}
.price s{color:var(--muted);font-size:.85em}
.btn{display:flex;align-items:center;justify-content:center;gap:6px;text-align:center;text-decoration:none;font:inherit;font-size:.95rem;border-radius:8px;padding:10px 12px;min-height:44px;cursor:pointer;border:1px solid transparent}
.send{background:var(--wa);color:var(--wa-ink)}
.row{display:flex;gap:6px}
.ghost{background:none;border-color:var(--line);color:var(--ink)}
.row .btn{flex:1;font-size:.9rem;padding:8px}
.btn.done{border-color:var(--wa);color:var(--wa)}
.btn:focus-visible,.chip:focus-visible,.lang:focus-visible,.search:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.empty{grid-column:1/-1;text-align:center;color:var(--muted);padding:30px 0}
footer{color:var(--muted);font-size:.85rem;margin:28px 0 10px;border-top:1px solid var(--line);padding-top:14px}
@media (max-width:420px){body{font-size:16px}.card .body{padding:8px 8px 10px}.btn{font-size:.88rem;padding:9px 6px}}
"""

SCRIPT = """
var DATA = %(data)s;
var CATS = %(cats)s;
var TEXT = %(text)s;
var READY = %(ready)s;
var BASE = %(base)s, REF = %(ref)s;

// Copied from js/site.js by _share_page.py, so the sale is the site's own.
%(sale)s

var lang = 'he', cat = '', query = '';
try { lang = localStorage.getItem('sa_lang') === 'en' ? 'en' : 'he'; } catch (e) {}

function $(id) { return document.getElementById(id); }
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function root(l) { return BASE + (l === 'he' ? '/he/' : '/'); }
function link(rel) { return root(lang) + rel + '?ref=' + REF; }
function view(rel) { return root(lang) + rel; }
function fill(tpl, name, url) { return tpl.replace('{name}', name).replace('{url}', url); }
function wa(msg) { return 'https://wa.me/?text=' + encodeURIComponent(msg); }
function nis(n) { return '\\u20aa' + Number(n).toLocaleString('en-IL'); }

function price(p) {
  var t = TEXT[lang], d = productDiscount(p.id);
  var reg = p.ils, now = d > 0 ? Math.round(reg * (1 - d)) : reg;
  var usd = d > 0 ? Math.round(p.usd * (1 - d)) : p.usd;
  // Sale price first, struck regular price after it, so the two read in the
  // same order in Hebrew and English.
  var main = (p.multi ? t.from : '') + nis(now) + (now !== reg ? ' <s>' + nis(reg) + '</s>' : '');
  return lang === 'en' ? main + ' / $' + usd : main;
}

// A product gets Send, then Copy and View under it; a ready message (no page of
// its own) gets Send and Copy on one line, so the products start higher up.
function buttons(msg, rel) {
  var t = TEXT[lang];
  var send = '<a class="btn send" href="' + esc(wa(msg)) + '" target="_blank" rel="noopener">' + esc(t.send) + '</a>';
  var copyBtn = '<button type="button" class="btn ghost" data-copy="' + esc(msg) + '">' + esc(t.copy) + '</button>';
  if (!rel) return '<div class="pair">' + send + copyBtn + '</div>';
  return send + '<div class="row">' + copyBtn +
    '<a class="btn ghost" href="' + esc(view(rel)) + '" target="_blank" rel="noopener">' + esc(t.view) + '</a></div>';
}

function render() {
  var t = TEXT[lang];
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === 'he' ? 'rtl' : 'ltr';
  document.title = t.title + ' | Sherman Art Works';
  ['title', 'intro', 'tip', 'ready', 'footer', 'other'].forEach(function (k) { $('t-' + k).textContent = t[k]; });
  $('search').placeholder = t.search;
  $('search').setAttribute('aria-label', t.search);
  $('sale').hidden = !DATA.some(function (p) { return productDiscount(p.id) > 0; });
  $('sale').textContent = t.sale;

  $('ready').innerHTML = READY.map(function (r) {
    return '<div class="msg"><strong>' + esc(t[r[0]]) + '</strong>' + buttons(fill(t[r[1]], '', link(r[2]))) + '</div>';
  }).join('');

  $('chips').innerHTML = [['', t.all]].concat(CATS.map(function (c) { return [c.id, c[lang]]; })).map(function (c) {
    return '<button type="button" class="chip" data-cat="' + c[0] + '" aria-pressed="' + (c[0] === cat) + '">' + esc(c[1]) + '</button>';
  }).join('');
  list();
}

function list() {
  var t = TEXT[lang], q = query.trim().toLowerCase();
  var shown = DATA.filter(function (p) {
    return (!cat || p.c === cat) && (!q || (p.he + ' ' + p.en).toLowerCase().indexOf(q) !== -1);
  });
  var c = CATS.filter(function (x) { return x.id === cat; })[0];
  $('count').textContent = shown.length + ' ' + t.products;
  $('collection').innerHTML = c ? buttonsCollection(c) : '';
  $('grid').innerHTML = shown.length ? shown.map(function (p) {
    var name = p[lang], rel = 'products/' + p.id + '.html';
    return '<article class="card"><img src="' + esc(p.img) + '" alt="' + esc(name) + '" loading="lazy" width="400" height="400">' +
      '<div class="body"><p class="name">' + esc(name) + '</p><p class="price">' + price(p) + '</p>' +
      buttons(fill(t.msg_product, name, link(rel)), rel) + '</div></article>';
  }).join('') : '<p class="empty">' + esc(t.none) + '</p>';
}

function buttonsCollection(c) {
  var t = TEXT[lang], msg = fill(t.msg_collection, c[lang], link(c.page));
  return '<a class="btn send" href="' + esc(wa(msg)) + '" target="_blank" rel="noopener">' + esc(t.collection) + '</a>';
}

function copy(text, btn) {
  function done() {
    var t = TEXT[lang];
    btn.textContent = t.copied + ' \\u2713';
    btn.classList.add('done');
    setTimeout(function () { btn.textContent = t.copy; btn.classList.remove('done'); }, 1800);
  }
  function fallback() {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }
  if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
  else fallback();
}

document.addEventListener('click', function (e) {
  var b = e.target.closest('[data-copy]');
  if (b) { copy(b.getAttribute('data-copy'), b); return; }
  var c = e.target.closest('[data-cat]');
  if (c) { cat = c.getAttribute('data-cat'); render(); }
});
$('search').addEventListener('input', function () { query = this.value; list(); });
$('lang').addEventListener('click', function () {
  lang = lang === 'he' ? 'en' : 'he';
  try { localStorage.setItem('sa_lang', lang); } catch (e) {}
  render();
});
render();
"""

PAGE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<!-- Unlisted on purpose: see _share_page.py. Generated, do not edit by hand. -->
<meta name="robots" content="noindex, nofollow" />
<title>%(title)s | Sherman Art Works</title>
<meta name="apple-mobile-web-app-title" content="Sherman" />
<link rel="icon" type="image/png" sizes="32x32" href="https://res.cloudinary.com/doesupaf9/image/upload/w_32,h_32,c_fill,g_auto,q_auto,f_png/WhatsApp_Image_2026-05-23_at_14.51.54_xv8lbd.jpg" />
<link rel="apple-touch-icon" sizes="180x180" href="https://res.cloudinary.com/doesupaf9/image/upload/w_180,h_180,c_fill,g_auto,q_auto,f_png/WhatsApp_Image_2026-05-23_at_14.51.54_xv8lbd.jpg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet" />
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
<header>
  <div><p class="brand">Sherman Art Works</p><h1 id="t-title">%(title)s</h1></div>
  <button type="button" class="lang" id="lang"><span id="t-other">English</span></button>
</header>
<div class="intro"><p id="t-intro"></p><p id="t-tip"></p></div>
<p class="sale" id="sale" hidden></p>
<h2 id="t-ready"></h2>
<div class="ready" id="ready"></div>
<div class="chips" id="chips" role="group"></div>
<input type="search" class="search" id="search" autocomplete="off" />
<div class="bar"><span id="count"></span><span id="collection"></span></div>
<div class="grid" id="grid"></div>
<footer id="t-footer"></footer>
</div>
<noscript>This page needs JavaScript.</noscript>
<script>%(script)s</script>
</body>
</html>
"""


def site_js():
    return (SITE / "js" / "site.js").read_text(encoding="utf-8")


def sale_code(src):
    """The site's own sale code: its constants and top-level functions, verbatim."""
    parts = []
    for name in SALE_CONSTS:
        m = re.search(r"^const %s = .*?;$" % name, src, re.M)
        if not m:
            raise RuntimeError(f"js/site.js: no const {name}")
        parts.append(m.group(0))
    for name in SALE_FUNCS:
        m = re.search(r"^function %s\(.*?^}$" % name, src, re.M | re.S)
        if not m:
            raise RuntimeError(f"js/site.js: no function {name}")
        parts.append(m.group(0))
    return "\n".join(parts)


def products():
    catalog = json.loads((SITE / "data" / "products.json").read_text(encoding="utf-8"))
    known = {c for c, _ in CATEGORIES}
    out = []
    for p in catalog:
        if not has_page(p):
            continue
        if p["category"] not in known:
            raise RuntimeError(f"{p['id']}: category {p['category']} has no place on the share page")
        ils = price_of(p)
        out.append({
            "id": p["id"], "c": p["category"], "en": p["name_en"], "he": p["name_he"],
            "img": image(p["photos"][0], "w_400,h_400,c_pad,b_rgb:faf7f2,q_auto,f_auto"),
            "ils": ils, "usd": usd_from_ils(ils), "multi": bool(p.get("sizes")),
        })
    order = {c: i for i, (c, _) in enumerate(CATEGORIES)}
    out.sort(key=lambda p: order[p["c"]])  # stable: shop order within a category
    return out


def categories(items, catalog_pages):
    used = {p["c"] for p in items}
    return [{"id": c, "en": T_SITE_EN[key], "he": T_SITE_HE[key], "page": catalog_pages[c]}
            for c, key in CATEGORIES if c in used]


def build():
    catalog = json.loads((SITE / "data" / "products.json").read_text(encoding="utf-8"))
    pages = {}
    for p in catalog:
        pages.setdefault(p["category"], p["pages"][0])
    items = products()
    for p in items:
        for prefix in ("", "he/"):
            if not (SITE / prefix / "products" / f"{p['id']}.html").exists():
                raise RuntimeError(f"{prefix}products/{p['id']}.html does not exist: run _product_pages.py first")
    dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    script = SCRIPT % {
        "data": dump(items), "cats": dump(categories(items, pages)), "text": dump(TEXT),
        "ready": dump(READY), "base": dump(BASE), "ref": dump(REF), "sale": sale_code(site_js()),
    }
    return PAGE % {"title": html.escape(TEXT["he"]["title"]), "css": CSS.strip(), "script": script}


def main():
    check = "--check" in sys.argv
    out = build()
    if OUT.exists() and OUT.read_text(encoding="utf-8") == out:
        print("share.html is current")
        return 0
    if check:
        print("share.html is stale: run python _share_page.py")
        return 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    print("wrote share.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
