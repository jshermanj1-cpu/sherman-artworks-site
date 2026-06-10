# Sherman Art Works — Product Task List

> Last updated: June 2026 (Sprint 18 in progress — shopping cart Phase A) | PM: Claude | Owner: Sherman Family
> Active file: `sherman-artworks-site/` | Repo: github.com/jshermanj1-cpu/sherman-artworks-site

---

## ⛔ COMMIT RULE

**NEVER commit or push without the owner's explicit "approve" or "approved".** No exceptions.

---

## Legend

| Symbol | Meaning |
|---|---|
| 🔴 | Blocker — launch cannot happen without this |
| 🟡 | Important — significantly affects conversion or trust |
| 🟢 | Nice to have — improves experience, not blocking |
| ✅ | Done |
| 🔜 | Not started |
| ⚠️ | Started but incomplete |
| 👤 | Requires owner/human input — not a dev task |

---

## MILESTONE 0 — Owner Inputs

| ID | Task | Owner | Blocking | Status |
|---|---|---|---|---|
| M0-1 | Confirm WhatsApp business number | Sherman | 🔴 Site-wide | ✅ `972523482278` confirmed as official business number |
| M0-2 | Domain name | Sherman | — | ✅ shermanartworks.com |
| M0-3 | Choose payment provider | Sherman | 🔴 M19 | 🔜 Stripe not available for Israel; alternatives: PayPal, Payoneer, Cardcom, PayMe |
| M0-4 | Confirm prices for remaining products | Sherman | 🟡 M9 | ⚠️ Live products have prices. Missing: dedicated kiddush cups, business gifts. Ram mezuzah ✅ ₪700 |
| M0-5 | Confirm candlestick color variants | Sherman | 🟡 M9 | 🔜 |
| M0-6 | Native Hebrew speaker for copy review | Sherman | 🟡 M10 | 🔜 |
| M0-7 | Purchase model decision | Sherman | — | ✅ WhatsApp-first |
| M0-8 | Hosting platform | Sherman | — | ✅ GitHub Pages |
| M0-9 | Contact form backend | Sherman | — | ✅ WhatsApp + mailto (no backend) |
| M0-10 | Free shipping threshold | Sherman | — | ✅ Free on all orders |
| M0-11 | Instagram + TikTok handles | Sherman | 🟡 M11 | ⚠️ Instagram ✅ shermanartworks. TikTok still missing. |

---

## MILESTONE 1 — Foundation ✅ COMPLETE
## MILESTONE 2 — Trust & Conversion ✅ COMPLETE
## MILESTONE 3 — Homepage Enhancements ✅ COMPLETE
*(3.3 Shop by Occasion, 3.5 Personalisation badge, 3.8.2 TikTok deferred)*

---

## MILESTONE 4 — Shop Section (homepage) ✅ COMPLETE

**Current categories (6):**
1. Candlesticks ✅ live with products
2. Shofars & Goblets ✅ live with products
3. Kiddush Cups ✅ live — goblets cross-listed; dedicated designs coming soon
4. Trays & Bowls ✅ live with products
5. Business Gifts ⏳ Coming Soon
6. Mezuzahs ✅ Ram Mezuzah live (₪700); more designs needed

All category cards show real product photos. "From ₪X / $X" prices shown on all live categories, updating on currency toggle.

---

## MILESTONE 5 — Category Pages ⚠️ PARTIAL (4 of 6 live)

### 5.2 — Product Catalogue
| Page | Products | Status |
|---|---|---|
| `candlesticks.html` | Glass Circle Candlesticks (4 photos, ₪775) | ✅ |
| `shofars-goblets.html` | Jerusalem Wine Horn (₪850), Lion of Judah Goblet (₪473), Menorah Goblet (₪473) | ✅ |
| `kiddush-cups.html` | Lion of Judah Goblet + Menorah Goblet (cross-listed) + more coming soon | ✅ |
| `trays-bowls.html` | Glass Decorative Bowl (4 photos, ₪1,190) | ✅ |
| `business-gifts.html` | 0 — Coming Soon stub | ⏳ |
| `mezuzahs.html` | Ram Mezuzah (4 photos, ₪700) | ✅ |

### 5.5 — When new photos arrive
1. Upload to Cloudinary
2. Open `/product-builder.html`, group photos, fill name/desc/measurements/price, export JSON
3. Paste JSON to dev → updates PRODUCTS array in relevant page
4. For Coming Soon → also replace cat-card-placeholder on index.html + update sitemap.xml lastmod

---

## MILESTONE 6 — Custom Orders Page ✅ COMPLETE
## MILESTONE 7 — About Page ✅ COMPLETE
## MILESTONE 8 — Contact Page ✅ COMPLETE

---

## MILESTONE 9 — Full Product Catalogue 🔜
*Blocked on owner providing new photos.*

| ID | Task | Notes |
|---|---|---|
| 9.1.1 | Dedicated Kiddush Cup photos + product cards | Owner photographs → product-builder |
| 9.1.2 | Decorative Tray product card | Owner photographs → product-builder |
| 9.1.3 | Business Gifts product cards | Owner photographs → product-builder |
| 9.1.4 | Mezuzah product cards | Owner photographs → product-builder |
| 9.1.5 | Remove Coming Soon placeholders (Business Gifts + Mezuzahs) | After photos exist |

---

## MILESTONE 10 — Hebrew Quality & Localisation 🔜

| ID | Task | Effort |
|---|---|---|
| 10.1 | Full Hebrew copy review by native speaker — all pages | M · 👤 Blocked M0-6 |
| 10.2 | Judaica-specific Hebrew terminology review | S |
| 10.3 | RTL layout test on real device (iOS Safari + Android Chrome) | S |
| 10.4 | Varela Round rendering check across EN + HE (single font for both) | XS |
| 10.5 | Add `hreflang` meta tags | XS |

---

## MILESTONE 11 — Marketing & Distribution ⚠️ TIER 1 COMPLETE

### 11.1 — Tier 1: Foundational ✅ COMPLETE (dev side)

| ID | Task | Status |
|---|---|---|
| 11.1.1 | GA4 `G-J55QNV6GF1` — page views + 5 conversion event types | ✅ Live on all 11 pages |
| 11.1.2 | Google Search Console verified + sitemap.xml submitted | ✅ Done |
| 11.1.3 | WhatsApp Business profile | 👤 Owner action — install WA Business app, configure profile alongside M0-1 number swap |

### 11.2 — Tier 2: Growth Channels 🔜

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.2.1 | Wire TikTok in footer | Provide TikTok handle (M0-11) | Update footer site-wide | XS |
| 11.2.2 | Email newsletter service | Sign up Brevo / Mailchimp | Wire embed | S |
| 11.2.3 | Newsletter signup bar on homepage | Approve copy | Build + wire | M |
| 11.2.4 | Pinterest "Pin It" on product cards | Confirm desired | Add pinit.js | XS |

### 11.3 — Tier 3: Strategic 🔜

| ID | Task | Notes |
|---|---|---|
| 11.3.1 | Etsy / Not on the High Street as parallel channel | Owner decision |

---

## MILESTONE 12 — Payments Integration 🔜
*Blocked on M0-3 (owner chooses payment provider; Stripe not available for Israel). Candidate: PayPal, Payoneer, Cardcom, PayMe.*

---

## MILESTONE 13 — Bug Bash & Security ⚠️ MOSTLY COMPLETE

### 13.1 — 🔴 Blockers

| ID | Task | Status |
|---|---|---|
| 13.1.1 | Rotate GitHub PAT (`ghp_pDwEnvm…` exposed in chat) | ✅ Old token revoked; fine-grained PAT in owner's password manager |
| 13.1.2 | Confirm real WA number + update all pages | ✅ `972523482278` confirmed official; already in all pages |

### 13.2 — 🟡 Important

| ID | Task | Status |
|---|---|---|
| 13.2.1 | Diversify OG images — 5 pages share same bowl photo | 🔜 👤 Owner picks photos |
| 13.2.2 | sitemap.xml | ✅ Done |
| 13.2.3 | robots.txt | ✅ Done |
| 13.2.4 | aria-label / text fallbacks on nav links | ✅ Done |

### 13.3 — 🟢 Polish

| ID | Task | Status |
|---|---|---|
| 13.3.1 | Remove bestseller_badge dead translation key | ✅ Done |
| 13.3.2 | Delete orphan glass-curate.html | ✅ Done |
| 13.3.3 | block product-builder.html via robots.txt | ✅ Done (in robots.txt Disallow) |
| 13.3.4 | Security headers (HSTS, CSP) | 🔜 Needs Cloudflare proxy — GitHub Pages limitation |

---

## MILESTONE 14 — UI/UX Overhaul ✅ COMPLETE

| Item | Status |
|---|---|
| Varela Round for all text (EN + HE), token-based via `--ff-body/--ff-disp` | ✅ |
| AA contrast (`--brown` #6a5530, `--footer-text` #a89678) | ✅ |
| SVG icons replace emoji on all Coming Soon placeholders | ✅ |
| Single hero CTA hierarchy, `.btn-link` secondary | ✅ |
| Shop nav dropdown (6 categories, desktop + mobile, RTL) | ✅ |
| Inline photo carousel on product cards (arrows + dots) | ✅ |
| Cross-category products: goblets in Kiddush Cups | ✅ |
| context.md onboarding doc with commit rule | ✅ |

---

## MILESTONE 15 — Polish & Analytics ✅ COMPLETE (Sprint 15)

| Item | Status |
|---|---|
| Branded 404.html — full nav, 3 CTAs, EN/HE, floating WA | ✅ |
| Favicon upgrade — PNG, c_fill square crop, 16/32/180px, apple-touch-icon | ✅ |
| "From ₪X / $X" prices on homepage category cards (live currency toggle) | ✅ |
| Kiddush Cups category card → real goblet photo (was SVG placeholder) | ✅ |
| Hero image preload (`rel="preload"` + `fetchpriority="high"`) for LCP | ✅ |
| GA4 event tracking — whatsapp_click, view_details, email_click, category_browse, commission_click | ✅ |
| sitemap.xml (10 URLs, priorities) + robots.txt (disallows internal tools) | ✅ |
| Google Search Console verified + sitemap submitted | ✅ |
| aria-label / text fallbacks on all nav links (12 per page) | ✅ |
| Dead code removed: bestseller_badge key, glass-curate.html | ✅ |

---

## OPEN: Items Needing Owner Input Only

| Priority | Task | Your action |
|---|---|---|
| 🔴 | **Choose payment provider** (M0-3) | Decide between PayPal, Payoneer, Cardcom, PayMe — create account → unblocks M19 |
| 🟡 | **WhatsApp Business profile** (M11.1.3) | Install WA Business app, set up logo/hours/away message |
| 🟡 | **New product photos** (M9) | Photograph kiddush cups, business gifts → upload to Cloudinary |
| 🟡 | **Product dimensions** (M5.2) | Measure 5 products that are missing dimensions (messaging each size) |
| 🟡 | **Native Hebrew reviewer** (M0-6) | Arrange review of all HE copy before marketing launch |
| 🟡 | **Testimonials** (M20) | Collect 3–5 short quotes from happy customers with first name + city |
| 🟡 | **Brevo / newsletter signup** (M11.2.2) | Sign up at brevo.com → I wire the embed |
| 🟡 | **TikTok handle** (M0-11) | Send handle → I add to footer site-wide |
| 🟡 | **Diversify OG images** (M13.2.1) | Pick better social-share photos for about/contact/custom-orders/index |
| 🟡 | **Business Gifts strategy** | Decide: custom branded sets? gift cards? consignment? → enables M9 stub removal |

---

## MILESTONE 16 — Shared Foundation & SEO ✅ COMPLETE (Sprint 17)

| Item | Status |
|---|---|
| `css/site.css` — 615-line shared stylesheet extracted from all 11 pages | ✅ |
| `js/site.js` — 285-line shared script: constants, translations, state, helpers, GA4, init | ✅ |
| `data/products.json` — 6 products with slugs, categories, ILS prices, Cloudinary photo arrays | ✅ |
| JSON-LD structured data injected in `<head>` (Organization, Product+Offer, BreadcrumbList) | ✅ |
| Static EN content baked into `data-t` elements for SEO crawlers | ✅ |
| Static product cards baked into category page grids for SEO fallback | ✅ |
| canonical, og:url, twitter:card added to all 11 pages | ✅ |
| og:image updated to `c_fill,g_auto` (was `c_fit`) | ✅ |
| T_PAGE regression fix: `${T[l].` → `${T_PAGE[l].` across 5 category pages | ✅ |
| `_sprint17.py` idempotent extraction script (excluded from repo via `.gitignore`) | ✅ |

---

## MILESTONE 17 — Shopping Cart Phase A 🔜 IN PROGRESS (Sprint 18)

**Goal:** WhatsApp-first cart — customers add items, review totals, then checkout via pre-filled WA message. No payment gateway needed for Phase A.

| Step | Task | Files | Status |
|---|---|---|---|
| 0 | Verify `data/products.json` has all required fields (slug, category, priceIls, photos) | `data/products.json` | ✅ Done (Sprint 17) |
| 1 | `js/cart.js` — cart store: `addItem()`, `removeItem()`, `updateQty()`, `getCart()`, `clearCart()`, localStorage key `sa_cart`, custom event `sa:cart-change` | `js/cart.js` | 🔜 |
| 2 | `css/cart.css` — drawer styles: slide-in panel, cart badge (on nav icon), item rows, qty stepper, totals line, checkout CTA button | `css/cart.css` | 🔜 |
| 3 | Cart drawer HTML — inject `#cart-drawer` + `#cart-overlay` into all 11 pages; nav badge `<span id="cart-count">` | all `.html` | 🔜 |
| 4 | "Add to Cart" button on product cards (category pages) + in product modal | category `.html` | 🔜 |
| 5 | `checkout.html` — order summary table, ILS/USD toggle, WhatsApp checkout CTA (builds itemised WA message from cart), empty-cart state, breadcrumb | `checkout.html` | 🔜 |
| 6 | GA4 ecommerce events — `add_to_cart`, `view_cart`, `begin_checkout` (WA click = purchase intent) | `js/site.js` + `js/cart.js` | 🔜 |
| 7 | Wire `<script src="js/cart.js">` into all 11 pages + `checkout.html` | all `.html` | 🔜 |
| 8 | QA: add items → adjust qty → remove item → checkout → empty cart → HE locale → mobile 375px | browser | 🔜 |

**Out of scope (Phase B / M19):** actual payment processing, stock tracking, order database, email receipts.

---

## MILESTONE 18 — Legal, Trust & Social Proof 🔜

| ID | Task | Priority |
|---|---|---|
| 18.1 | Privacy policy page (`privacy.html`) | 🔴 Required for GA4 + future payments |
| 18.2 | Testimonials section on homepage | 🟡 |
| 18.3 | Trust badges: secure checkout, handcrafted, shipped from Israel | 🟡 |
| 18.4 | Instagram feed embed or gallery strip | 🟢 |
| 18.5 | TikTok footer link (M0-11) | 🟢 |

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 8/11 done (WA + PAT resolved) |
| Sprint 1 | M1 | Foundation | ✅ |
| Sprint 2 | M2 | Trust & conversion | ✅ |
| Sprint 3 | M3 | Homepage enhancements | ✅ |
| Sprint 4 | M4 | Shop category hub | ✅ |
| Sprint 5 | M5 | Category pages | ✅ 5/6 live (mezuzahs now has Ram Mezuzah) |
| Sprint 6–8 | M6–M8 | Custom Orders, About, Contact pages | ✅ |
| Sprint 13 | M13 | Bug bash + security audit | ✅ Security blockers cleared |
| Sprint 14 | M14 | UI/UX overhaul, dropdown, carousel, cross-category | ✅ |
| Sprint 15 | M15 | 404, favicons, prices, GA4, Search Console, aria, cleanup | ✅ |
| Sprint 16 | M13 / M14 cleanup | Security lockdown, Varela Round fonts, exchange rate, localStorage, .gitignore | ✅ |
| Sprint 17 | M16 | Shared CSS/JS, products.json, SEO baking, JSON-LD, T_PAGE fix | ✅ |
| **→ Sprint 18** | **M17** | **Shopping Cart Phase A** (Steps 1–8) | **⚠️ Approved, in progress** |
| — | M9 | Full product catalogue | 🔜 Blocked: owner photos for kiddush cups, business gifts |
| — | M18 | Legal, trust, testimonials | 🔜 Blocked: collect quotes + Brevo |
| — | M11 Tier 2 | Newsletter, Pinterest, TikTok | 🔜 |
| — | M10 | Hebrew quality pass | 🔜 Blocked: native speaker |
| — | M19 (was M12) | Payments integration | 🔜 Blocked: M0-3 provider decision |
| **→ FULL LAUNCH** | — | Marketing push | 🔜 |

---

## Effort Key

| Size | Time |
|---|---|
| XS | < 30 min |
| S | 30 min – 2 hrs |
| M | 2–5 hrs |
| L | 5–10 hrs |

---

*Task list is a living document. Update after every sprint.*
