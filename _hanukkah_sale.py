"""Dated Hanukkah sale. Catalogue prices always stay regular."""
import math
import re
from datetime import datetime, timezone
from _usd import usd_from_ils

START = "2026-10-12T00:00:00+03:00"
END = "2026-12-05T00:00:00+02:00"
ELIGIBLE = re.compile(r"^(silver|gold)-tone-(pearl-white|blue|clear|emerald-green|light-blue|terracotta|turquoise|white-blue)-(half-moon|rectangular|trapezoid)-menorah$")

def running(now=None):
    """Whether the sale window is open, whatever the product."""
    at = now or datetime.now(timezone.utc)
    return datetime.fromisoformat(START) <= at < datetime.fromisoformat(END)

def active(slug, now=None):
    return bool(ELIGIBLE.fullmatch(slug or "")) and running(now)

def sale(amount, slug, now=None):
    return math.floor(amount * .8 + .5) if active(slug, now) else amount

def price_html(product):
    regular = product["price_ils"]
    slug = product["id"]
    usd = usd_from_ils(regular)
    if not active(slug):
        return f'&#8362;{regular:,} <span class="product-card-price-alt">≈ ${usd}</span>'
    # Crawlers read this without CSS, so the struck price is a real <s> and both
    # figures carry a hidden label; without them "₪1,250 ₪1,000" reads as 1,250.
    # The labels are data-t keys, so _he_pages.py puts the Hebrew in.
    return (f'<s class="was-price"><span class="sr-only" data-t="price_regular">Regular price</span> '
            f'&#8362;{regular:,}</s> '
            f'<span class="now-price"><span class="sr-only" data-t="price_hanukkah">Hanukkah price</span> '
            f'&#8362;{sale(regular, slug):,}</span> '
            f'<span class="product-card-price-alt">${sale(usd, slug)}</span>')

def offer_fields(product):
    if not active(product["id"]):
        return {}
    return {
        "price": str(sale(product["price_ils"], product["id"])),
        "priceValidUntil": "2026-12-04",
        "priceSpecification": {
            "@type": "UnitPriceSpecification",
            "priceType": "https://schema.org/StrikethroughPrice",
            "price": str(product["price_ils"]), "priceCurrency": "ILS"
        }
    }
