"""Launch-promotion discount, shared by every generator.

Single source of truth for the site-wide launch sale on the Python side. It must
stay in lock-step with:

  * js/site.js         - LAUNCH_DISCOUNT / saleIls() (display + cart + checkout)
  * sherman-payments   - src/pricing.js LAUNCH_DISCOUNT / saleIls() (card charge)

Everything except shipping is sold at (1 - LAUNCH_DISCOUNT) of its catalogue
price, rounded to the nearest whole shekel on the per-item price. data/products.json
keeps the REGULAR prices - it is what the payments Worker reprices from, so it
must never carry discounted numbers or card orders would be discounted twice.

The launch promotion ended on 1 September 2026. Keep LAUNCH_DISCOUNT at 0 here
and in the two JavaScript copies unless a future promotion deliberately reuses
this mechanism, then re-run the generator chain.
"""

import math

LAUNCH_DISCOUNT = 0


def launch_active():
    return LAUNCH_DISCOUNT > 0


def sale_ils(ils):
    """Discounted price for one item, nearest whole shekel.

    Uses floor(x + 0.5) so it rounds half up exactly like JavaScript's
    Math.round in js/site.js and the payments Worker - never Python's
    round-half-to-even - so the three never disagree by a shekel.
    """
    if not launch_active():
        return ils
    return math.floor(ils * (1 - LAUNCH_DISCOUNT) + 0.5)
