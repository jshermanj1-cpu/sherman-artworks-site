"""ShoppingIL by Google: 10% off every catalogue product, Wednesday and Thursday,
4-5 November 2026, Israel time. Catalogue prices always stay regular.

The identical window and rate live in js/site.js and the payments Worker
(sherman-payments/src/pricing.js). Menorahs keep their Hanukkah 20% instead
(_hanukkah_sale.py); the two never add up.
"""
import math
from datetime import datetime, timezone
from _hanukkah_sale import ELIGIBLE as MENORAH

START = "2026-11-04T00:00:00+02:00"
END = "2026-11-06T00:00:00+02:00"
DISCOUNT = 0.10


def upcoming(now=None):
    """Whether the sale has not ended yet. The feed states it ahead of time with
    its dates, so Merchant Center turns it on and off by itself."""
    at = now or datetime.now(timezone.utc)
    return at < datetime.fromisoformat(END)


def eligible(slug):
    return bool(slug) and not MENORAH.fullmatch(slug) and not slug.startswith("quote:")


def sale(amount):
    """Nearest whole unit, half up - Math.round in the site and the Worker."""
    return math.floor(amount * (1 - DISCOUNT) + .5)
