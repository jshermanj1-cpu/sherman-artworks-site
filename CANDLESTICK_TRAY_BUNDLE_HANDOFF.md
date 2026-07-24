# Candlestick and Matching Tray Work

## Status

The implementation is complete on the `candels` branch and is ready for owner review. It is not live on the production site until this branch is merged into `main` and GitHub Pages finishes deploying.

No Cloudinary API key or secret is stored in the repository. The site uses public Cloudinary image IDs only.

## What has been completed

### Candlestick products

- Added seven separate silver-plated glass candlestick products:
  - White / לבן
  - Red / אדום
  - Blue / כחול
  - Green / ירוק
  - Black / שחור
  - Blue-Green / כחול-ירוק
  - Earth / אדמה
- Grouped the separate products into one color family in the product modal.
- Added image thumbnails with color names. Choosing a color opens that color's separate product and changes the gallery.
- Added three required height choices with the same prices for every color:
  - S: 14–18 cm — ₪561
  - M: 19–22 cm — ₪623
  - L: 23–25 cm — ₪712
- Clarified in the English and Hebrew descriptions that the metal finish is 925 sterling-silver plating.
- Kept each item defined as a pair of candlesticks.

### Matching tray add-on

- Added an optional matching tray selector to every candlestick product.
- The tray is not selected by default.
- The selected tray automatically follows the chosen candlestick color.
- Tray details shown in the selector:
  - 30 × 18 cm
  - Glass with 925 sterling-silver plating
  - Regular price: ₪510
  - Price with candlesticks: ₪406
  - Savings: ₪104
- Selecting the tray changes the main product image to the matching candlestick-and-tray photograph.
- The combined set totals are:
  - S + tray: ₪967
  - M + tray: ₪1,029
  - L + tray: ₪1,118
- The cart keeps bundled and non-bundled candlesticks as distinct line items.
- Cart, checkout, WhatsApp, and email order details include the selected height, color, tray, tray measurements, discount, and combined price.

### Standalone tray products

- Added seven standalone tray products to the English and Hebrew Trays & Bowls pages at the regular price of ₪510.
- Grouped them into one color family with thumbnail-based color switching.
- Added their dimensions, 925 sterling-silver plating descriptions, images, product URLs, and cart routing.
- The Earth candlesticks use the provided round white tray image and product mapping.

### Product data and discovery surfaces

- Updated the English and Hebrew category pages.
- Updated `data/products.json`.
- Updated product structured data (JSON-LD).
- Regenerated `merchant-feed.xml`.
- Updated `llms.txt`.
- Updated the affected dates in `sitemap.xml`.
- Added responsive and keyboard-focus styling for the tray add-on.

## Cloudinary image mapping used

| Color | Candlesticks with tray | Tray alone |
|---|---|---|
| White | `White_pamotim2_s4579d` | `White_tray_o1npai` |
| Red | `Red_pamotim2_q6o2z4` | `Red_tray_zhqmoo` |
| Blue | `Blue_pamotim2_g7hkzr` | `Blue_tray_jvaf8d` |
| Green | `Green_pamotim2_dik7y4` | `Green_tray_ylui7h` |
| Black | `Black_pamotim2_druayt` | `Black_tray_cqaohw` |
| Blue-Green | `Blue_green_pamotim2_kpo6io` | `Vibrant_blue_tray_pyqqto` |
| Earth | `Adama_pamotim_2_nop3ln` | `White_round_tray_udmwyk` |

## Validation completed

- Parsed `data/products.json`: 62 products total, including seven candlestick variants and seven tray variants.
- Parsed all modified inline scripts and JSON-LD blocks without syntax errors.
- Checked `js/cart.js` syntax successfully.
- Regenerated and parsed the merchant feed:
  - 199 feed items
  - Seven standalone trays
  - All seven trays share the `silver-plated-glass-trays` item group.
- Render-tested the English candlestick page at a 390 px mobile viewport:
  - 17 cards
  - Seven color choices
  - Three height choices
  - Optional tray initially unchecked
  - No horizontal overflow
  - M + tray correctly totals ₪1,029
  - Switching from Red to Blue keeps the tray selected and switches to the Blue set image.
  - Cart data correctly stores the Blue set at ₪1,029 with ₪104 savings metadata.
- Render-tested the English tray page:
  - Nine cards total
  - Seven tray color choices
  - Price correctly remains ₪510
  - Color switching updates the product, image, and URL hash.
- Render-tested the Hebrew candlestick page in RTL:
  - Hebrew labels and descriptions
  - Seven color choices
  - Three height choices
  - L + tray correctly totals ₪1,118
  - No horizontal overflow.
- Visually checked the supplied tray-only and candlestick-with-tray image mappings.
- Ran `git diff --check` successfully.

## What is left to do

There are no known implementation blockers. The remaining work is release review:

1. Review the `candels` branch or open a pull request against `main`.
2. Confirm that the Earth color should intentionally use the provided round white tray.
3. After approval, merge into `main` and wait for the GitHub Pages deployment.
4. On the live site, perform a short production check with the real Cloudinary CDN:
   - Open one candlestick product in each language.
   - Select a height, color, and tray.
   - Add the set to the cart.
   - Check the checkout, WhatsApp, and email order summaries.
5. After deployment, let Google Merchant Center fetch the updated 199-item feed and review any diagnostics.

## Deliberately excluded

`SEO_GEO_ACTION_PLAN_2026-07-09.md` is an unrelated untracked file and is not part of this branch's product work.
