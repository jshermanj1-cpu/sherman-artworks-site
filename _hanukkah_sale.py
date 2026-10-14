"""Dated Hanukkah sale. Catalogue prices always stay regular."""
import math
import re
from datetime import datetime, timezone
from _usd import usd_from_ils

START = "2026-10-12T00:00:00+03:00"
END = "2026-12-05T00:00:00+02:00"
ELIGIBLE = re.compile(r"^(silver|gold)-tone-(pearl-white|blue|clear|emerald-green|light-blue|terracotta|turquoise|white-blue)-(half-moon|rectangular|trapezoid)-menorah$")

def active(slug, now=None):
    at = now or datetime.now(timezone.utc)
    return bool(ELIGIBLE.fullmatch(slug or "")) and datetime.fromisoformat(START) <= at < datetime.fromisoformat(END)

def sale(amount, slug, now=None):
    return math.floor(amount * .8 + .5) if active(slug, now) else amount

def price_html(product):
    regular = product["price_ils"]
    slug = product["id"]
    usd = usd_from_ils(regular)
    if not active(slug):
        return f'&#8362;{regular:,} <span class="product-card-price-alt">≈ ${usd}</span>'
    return (f'<span class="was-price">&#8362;{regular:,}</span> '
            f'<span class="now-price">&#8362;{sale(regular, slug):,}</span> '
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
