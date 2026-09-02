"""Pinned USD price list, shared by every generator.

Single source of truth for dollar prices on the Python side. It must stay in
lock-step with:

  * js/site.js         - USD_PIN_MID / usdFromIls() / saleUsd()  (display)
  * sherman-payments   - src/pricing.js, same three               (card charge)

International shoppers are quoted a FIXED dollar price, not a live conversion.
A figure that moves with the market between the shop page and the card is a
figure nobody actually quoted, and dividing by a live rate produces prices like
$138.72 that read as a currency widget rather than a price list.

So the dollar price is a pure function of the shekel price at a pinned rate,
rounded UP to the nearest $5: pinned so it moves only when somebody decides to
move it, up so a dollar figure never sits below the shekel one it came from.
The pin is the same mid and the same 2% margin the payments Worker's rates.js
quotes with, which makes re-pinning a judgement about the market rather than
about the formula.

To re-pin: change USD_PIN_MID in all three places, redeploy the Worker, and
re-run the generator chain. data/products.json keeps SHEKEL prices only - it is
what the Worker reprices from, and a second stored price list there would drift
from this one exactly the way products.json already drifts from the inline
PRODUCTS arrays.
"""

import math

from _launch import LAUNCH_DISCOUNT, launch_active

USD_PIN_MID = 3.06
USD_PIN_MARGIN = 0.02
USD_PIN_RATE = USD_PIN_MID * (1 - USD_PIN_MARGIN)  # 2.9988
USD_ROUND_TO = 5


def usd_from_ils(ils):
    """Catalogue dollar price for a shekel price, rounded up to the nearest $5."""
    return int(math.ceil((float(ils) / USD_PIN_RATE) / USD_ROUND_TO) * USD_ROUND_TO)


def sale_usd(usd):
    """Discounted dollar price, to the nearest whole dollar.

    Catalogue prices want round numbers; a sale price is derived from one and
    nobody expects it round. Rounding this to $5 as well would quietly turn
    "20% off" into 17.9% off, which any shopper with a calculator can see is
    not what the banner promises.

    Uses floor(x + 0.5) so it rounds half up exactly like JavaScript's
    Math.round in js/site.js and the payments Worker, never Python's
    round-half-to-even, so the three never disagree by a dollar.
    """
    if not launch_active():
        return usd
    return int(math.floor(usd * (1 - LAUNCH_DISCOUNT) + 0.5))
