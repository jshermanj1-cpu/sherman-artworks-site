# Sherman Art Works — Product Task List

> Last updated: 2026-07-08 (Sprint 22 planned — owner feedback round 2 + product anchors) | PM: Claude | Owner: Sherman Family
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
| M0-10 | Shipping policy | Sherman | — | ✅ Flat rate — International $45 · Israel ₪35 |
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

## MILESTONE 17 — Shopping Cart Phase A ✅ COMPLETE (Sprint 18)

**Goal:** WhatsApp-first cart — customers add items, review totals, then checkout via pre-filled WA message. No payment gateway needed for Phase A.

| Step | Task | Files | Status |
|---|---|---|---|
| 0 | Verify `data/products.json` has all required fields (slug, category, priceIls, photos) | `data/products.json` | ✅ |
| 1 | `js/cart.js` — cart store, WA message builder, slide-in drawer, nav badge, modal btn, GA4 events | `js/cart.js` | ✅ |
| 2 | `css/cart.css` — drawer, nav badge, card stacked layout, modal CTA, checkout page styles | `css/cart.css` | ✅ |
| 3 | Cart drawer + nav badge injected by cart.js (idempotent) on all 11 pages | all `.html` | ✅ |
| 4 | Gold "Add to Cart" button in all 5 category page `buildCard()` templates + modal btn | category `.html` | ✅ |
| 5 | `checkout.html` — order table, ILS/USD totals, WA CTA, empty state, bilingual, canonical, JSON-LD | `checkout.html` | ✅ |
| 6 | GA4 ecommerce: `add_to_cart`, `view_cart`, `begin_checkout` | `js/cart.js` | ✅ |
| 7 | `<script src="js/cart.js">` wired into all 11 pages + checkout.html | all `.html` | ✅ |
| 8 | QA: add items → qty adjust → remove → checkout → empty cart → HE locale → WA message verified | browser | ✅ |

**Bugs caught + fixed during QA:** `renderCheckout` not re-called on rate load or lang switch → added duck-typed hooks to `loadUsdRate()` and `setLang()` in site.js.

**Out of scope (Phase B / M19):** actual payment processing, stock tracking, order database, email receipts.

---

## MILESTONE 18 — Legal, Trust & Social Proof ⚠️ LEGAL CORE DONE (Sprint 19)

| ID | Task | Priority | Status |
|---|---|---|---|
| 18.1 | Privacy policy page (`privacy.html`) | 🔴 Required for GA4 + future payments | ✅ Live; static EN baked into HTML for SEO (Sprint 19) |
| 18.2 | Testimonials section on homepage | 🟡 | 🔜 Blocked: owner collects quotes |
| 18.3 | Trust badges: secure checkout, handcrafted, shipped from Israel | 🟡 | ✅ 2026-07-20 (Sprint 24) — `.trust-strip` on 10 conversion pages, EN+HE, 4 badges + SVG icons; uncommitted pending owner approval |
| 18.4 | Instagram feed embed or gallery strip | 🟢 | ⏸ Deferred — owner declined June 2026 |
| 18.5 | TikTok footer link (M0-11) | 🟢 | 🔜 Blocked: owner sends handle |
| 18.6 | Cookie consent banner gating GA4 — gtag.js loads only after Accept; `sa_consent` in localStorage; Decline = zero analytics | 🔴 EU-traffic prerequisite (FIX_PLAN 5.2) | ✅ Sprint 19 — `js/site.js` + `css/site.css`, applies to all 13 pages; hardcoded GA4 snippet removed from every `<head>` |
| 18.7 | `terms.html` — bilingual, 10 sections, static EN baked, BreadcrumbList JSON-LD | 🟡 (FIX_PLAN 5.3) | ✅ Sprint 19 |
| 18.8 | `shipping-returns.html` — bilingual, 9 sections, seeded from contact FAQ promises | 🔴 conversion-critical (FIX_PLAN 5.1) | ✅ Sprint 19 — **owner must approve policy decisions: buyer pays return shipping; customs = recipient's responsibility; refund ≤14 days after return received; custom non-cancellable once crafting begins** |
| 18.9 | Footer "Policies" block (Shipping & Returns / Privacy / Terms) on all 13 pages incl. checkout | 🟡 (FIX_PLAN 5.4) | ✅ Sprint 19 |
| 18.10 | `sitemap.xml`: + shipping-returns (0.5), privacy (0.3), terms (0.3) | 🟢 | ✅ Sprint 19 |
| 18.11 | contact.html FAQ: removed false "Stripe checkout coming soon" claim (Stripe unavailable in Israel) → "card checkout coming soon" EN+HE | 🟡 accuracy | ✅ Sprint 19 |
| 18.12 | **Official policy PDF integrated** (`complete_website_policy.pdf`, owner-supplied) — supersedes 18.8 drafted decisions. Applied to shipping-returns.html (dispatch ≤4 business days; delivery window ≤5 business days from dispatch; business days excl. Fri/Sat/holidays; damage = photo in original packaging within 48h; custom/made-to-order non-cancellable per consumer-protection law; customs incl. no-shipping-refund rule; NEW force-majeure section), terms.html (liability capped at amount paid; exclusive Israeli jurisdiction), contact FAQ 1+3 synced EN+HE | 🔴 | ✅ — ⚠️ PDF text layer was corrupted: "5 business days" + "48 hours" need owner confirmation; standard-piece 14-day return kept (PDF covers custom only); HE wording is dev translation pending M10 native pass |

**Sprint 19 QA (browser-verified):** fresh visit = banner + zero GA4 requests → Accept = gtag loads + page_view fires → Decline = no GA4, persists across reload. HE/RTL verified on both new pages incl. translated banner (אישור / לא תודה). checkout.html keeps `noindex` and is deliberately NOT in robots.txt (disallow would hide the noindex from Google).

**Found during QA (pre-existing, not fixed):** index.html requests 6 dead Cloudinary images (`…14.47.17/18/48/49…` variants, 404) — likely story/strip section. Needs owner to confirm correct public_ids.

---

## MILESTONE 19 — Owner Feedback Round (Sprint 20) ✅ COMPLETE (approved, pushed `2aa6f7c` + gift-wrap/4-day removal follow-up `0823fbc`)

Owner provided site + Hebrew wording feedback; implemented 2026-06-12.

| ID | Item | Status |
|---|---|---|
| 20.1 | HE nav label `הזמנות מיוחדות` → `הזמנות בהתאמה אישית` — all 16 files (site.js + 13 HTML pages + policy pages + 404) | ✅ |
| 20.2 | Cat1 HE rename: `פמוטים` → `פמוטי חן` (category title + footer + product name_he + description_he) | ✅ |
| 20.3 | Cat2 rename: EN `Shofars & Goblets` → `Shofars & Horn Goblets`; HE `שופרות וגביעים` → `שופרות וגביעי קרן` — all pages, static HTML, T_SITE, T_PAGE | ✅ |
| 20.4 | Cat5 HE `מתנות עסקיות` → `מתנות לעסקים` | ✅ |
| 20.5 | `עשוי ביד` → `עבודת יד` phrasing: footer_badge `עשוי ביד בישראל` → `עבודת יד מישראל`; footer_tagline; topbar_right | ✅ |
| 20.6 | Homepage restructure: shop category grid moved above hero banner — visitor sees shop immediately | ✅ |
| 20.7 | Candlesticks: `description_he` updated to owner-specified text (translucent-blue round glass, Shabbat/decorative); removed "custom candlesticks" `custom-band` section | ✅ |
| 20.8 | Shofars page: added handmade-variation disclaimer HE + EN (minor differences, each piece unique) to hero_body and section sub-header | ✅ |
| 20.9 | Jerusalem Wine Horn corrected: it is NOT a shofar — it's a wine goblet made of kudu horn. Updated `name_he`, `description_en`, `description_he`, section header, static SEO cards (shofars-goblets.html + kiddush-cups.html) | ✅ |
| 20.10 | Lion of Judah Goblet description: `description_he` → "סמל אריה על רקע ציפוי כסף 925"; `description_en` updated — both pages | ✅ |
| 20.11 | Menorah Goblet description: `description_he` → "מנורה בעלת שבעה קנים" only — both pages | ✅ |
| 20.12 | Mezuzahs intro: new `hero_body` HE (variety of styles, personal design, each unique, minor differences); `custom_title` HE → `הזמינו מזוזה מיוחדת` (removed "מותאמת אישית"); `description_he` updated to include `עבודת יד` + `עשוי בעבודת יד*` note | ✅ |
| 20.13 | About page: new HE `story_body` (grandfather saw more than raw material, three generations, same love, belief every creation tells a story) | ✅ |
| 20.14 | Email nowrap fix: `.footer-email { white-space: nowrap; }` in site.css | ✅ |
| 20.15 | Image buttons investigation: modal arrows confirmed working (all pages, desktop + mobile-width). In-card carousel was removed in Sprint 17 rebuild — not yet reinstated (separate work item) | 🔜 TBD |
| 20.16 | FAQ displays in Hebrew — confirmed working in previous session | ✅ No fix needed |

**Still pending owner decisions (not implemented):**
- 925 silver consistency pass across all products (need full list from owner)
- In-card carousel reinstatement (sprint 17 casualty — medium effort to rebuild)
- Shofars category split vs. rename (implemented rename only — "Shofars & Horn Goblets")

---

## MILESTONE 20 — SEO Hardening (Sprint 21)

On-page SEO audit + fixes; implemented 2026-06-12.

| ID | Item | Status |
|---|---|---|
| 21.1 | JSON-LD Product descriptions resynced with Sprint 20 copy: Jerusalem Wine Horn (kudu-horn goblet), Lion of Judah, Menorah — shofars-goblets.html (×3) + kiddush-cups.html (×2) | ✅ |
| 21.2 | shofars-goblets.html head metadata renamed: `<title>`, og:title, meta/og description, BreadcrumbList name → "Shofars & Horn Goblets" (missed in Sprint 20's visible-content rename) | ✅ |
| 21.3 | Static SEO card alt texts enriched on all 5 category pages (descriptive, keyword-bearing — e.g. "rams horn kiddush wine goblet with silver-plated lion emblem") | ✅ |
| 21.4 | FAQPage JSON-LD added to contact.html (6 EN Q&As, synced with current T_PAGE text incl. new shipping answer). NOTE: must be re-synced whenever FAQ copy changes | ✅ |
| 21.5 | Organization schema (index.html) enriched: `email`, `sameAs` → Instagram | ✅ |
| 21.6 | Verified: GSC verified + sitemap submitted in Sprint 15; robots.txt, canonicals, og tags, per-page titles/descriptions all present | ✅ No action |

**Known limitation:** JS card rendering overwrites enriched static alts with bare product names at runtime (`buildCard`). Static HTML (crawler first pass) carries the rich alts. Optional follow-up: enrich `buildCard` alt generation.

**Open SEO items (owner action / future sprints):**
- Google Business Profile (owner: business.google.com)
- Google Merchant Center free product listings (feed can be generated from PRODUCTS data)
- Hebrew SEO: HE exists only as JS toggle on same URLs — invisible to Google. Needs separate `/he/` pages + hreflang (L effort)
- Content pages targeting search queries (e.g. "What is a kiddush cup?")
- Backlinks: Judaica/artisan directories, marketplace profiles

---

## MILESTONE 21 — Owner Feedback Round 2 + Product Anchors (Sprint 22) 🔜

Owner feedback received 2026-07-08 (WhatsApp + screenshot of cropped mobile modal) + W14-B from SEO_GEO_WORK_PLAN. Planned 2026-07-08 — awaiting owner approval before commit.

**Recommended execution order: 22.3 → 22.2 → 22.4 → 22.1 → 22.5** (two quick fixes first, then descriptions, then the big split, anchors last since they depend on the final category structure).

### 22.1 — Category split: "Shofars & Horn Goblets" → "Horn Goblets" + separate "Shofars" 🔴 M

**Goal:** `shofars-goblets.html` becomes **Horn Goblets / גביעי קרן** (Jerusalem Wine Horn + Lion of Judah + Menorah goblets only). **Shofars / שופרות** becomes its own category containing the personalisation option (Custom Shofar builder).

**Recommended approach — no URL churn:** keep both existing filenames. `shofars-goblets.html` is renamed in place; `custom-shofars.html` (already in nav as "Custom Shofars" + in sitemap) is retitled to be THE Shofars category page. No new files, no redirect stubs, no sitemap URL changes — important while the W1/W2 indexing push is still in flight. *(Alternative rejected: new `horn-goblets.html`/`shofars.html` + meta-refresh stubs — cleaner slugs but URL churn mid-indexing and 2 extra stub pages.)*

| Step | Task | Files |
|---|---|---|
| 1 | 👤 Owner confirms: (a) naming above, (b) Jerusalem Wine Horn stays on Horn Goblets page (it's a drinking horn, NOT a shofar — per Sprint 20.9), (c) nav order (suggest Shofars directly after Horn Goblets) | — |
| 2 | `shofars-goblets.html` rename sweep EN+HE: `<title>`, meta/og/twitter description, page-hero H1 + breadcrumb, `T_PAGE` dict, JSON-LD (BreadcrumbList, ItemList name), static SEO card category tags. EN "Shofars & Horn Goblets"→"Horn Goblets", HE "שופרות וגביעי קרן"→"גביעי קרן" | `shofars-goblets.html` |
| 3 | Remove Custom Shofar product from `shofars-goblets.html`: PRODUCTS array entry, static SEO card, JSON-LD Product, its "custom" section markup + the now-dead personalisable form branch | `shofars-goblets.html` |
| 4 | `custom-shofars.html` retitle "Custom Shofars"→"Shofars / שופרות": `<title>`, meta/og, H1, breadcrumb, JSON-LD names. Keep builder + Custom Shofar card (this IS the "אופציה להתאמה אישית" inside the category); hero copy: category intro + "ready-made designs — contact us" line | `custom-shofars.html` |
| 5 | Site-wide nav sweep: `cat2_title` → "Horn Goblets"/"גביעי קרן", `cat7_title` → "Shofars"/"שופרות" in `T_SITE` (js/site.js) + hardcoded nav fallback text + mobile accordion in ALL HTML pages (~17 files; grep `cat2_title`/`cat7_title` + both old strings). Footer `footer_link_shofars` label likewise | all `.html`, `js/site.js` |
| 6 | Homepage category grid: card at index.html:428 → Horn Goblets (title/alt), card at :512 → Shofars (title/alt); verify `data-min-ils` prices still correct per card | `index.html` |
| 7 | `kiddush-cups.html` cross-listed goblets: category tag labels → "Horn Goblets" (8 old-name occurrences) | `kiddush-cups.html` |
| 8 | `data/products.json`: `category` 'shofars-goblets'→'horn-goblets' (3 goblets), custom-shofar `category`→'shofars' + drop 'shofars-goblets.html' from its `pages`. Grep all consumers of the category string (cart.js, GA4 params, product-builder.html) and sync | `data/products.json`, consumers |
| 9 | `llms.txt` category rename; `sitemap.xml` — URLs unchanged, bump `<lastmod>` on both pages + index | `llms.txt`, `sitemap.xml` |
| 10 | QA: EN/HE toggle on every touched page, Shop dropdown desktop + mobile + RTL, cart add-goblet→checkout, builder still works on custom-shofars.html + business-gifts.html, grep returns ZERO old-name occurrences (currently 119 across 19 files) | browser |

### 22.2 — Inscription hint: add "עברית/English" where missing 🟡 XS

`custom-shofars.html` already shows "(אופציונלי, עד 8 תווים, עברית/English)" — the same builder cloned on two other pages doesn't:

| Step | Task |
|---|---|
| 1 | `shofars-goblets.html:709` — append ", עברית/English" (HE) / ", Hebrew/English" (EN) to `l_hint_txt`. *(Becomes dead code after 22.1 step 3 — fix anyway in case 22.2 ships first)* |
| 2 | `business-gifts.html:387` (`custom_text_hint`) + `:605` (`l_hint_txt`) — same append, EN + HE |
| 3 | QA: open Custom Shofar modal on business-gifts.html in EN + HE → hint shows language note |

### 22.3 — Mobile modal: content clipped, can't scroll 🔴 XS–S (bug, screenshot 2026-07-08)

**Root cause:** `css/site.css:562` — at ≤800px `.modal-inner` is a single-column grid, `max-height: 96vh`, `overflow: hidden`; `.modal-info`'s `overflow-y: auto` never engages because its auto-sized grid row grows to full content height → anything past 96vh (e.g. the shofar order form) is clipped with no scroll.

| Step | Task |
|---|---|
| 1 | In the ≤800px block: `.modal-inner { overflow-y: auto; }` + `.modal-info { overflow-y: visible; }` — whole modal becomes ONE scroll container (gallery scrolls away as you read; standard mobile sheet pattern). Prefer `max-height: 96dvh` with 96vh fallback for iOS URL-bar resize |
| 2 | Keep close button reachable while scrolled: make `.modal-close` `position: sticky` (or fixed within modal) at top in the mobile block; verify RTL position |
| 3 | QA at 375px + real phone: long product (Custom Shofar form) scrolls fully, short product unaffected, body scroll-lock still works, Esc/backdrop close, RTL |

### 22.4 — FDA-approved epoxy coating note on horn + ceramic cups 🟡 S

**Products (👤 confirm list):** Jerusalem Wine Horn, Lion of Judah Goblet, Menorah Goblet (horn), Ceramic Kiddush Cup (ceramic). *(Owner said "all horn cups and all ceramic cups" — wine horn included as a horn drinking vessel.)*

**Text to append:** HE: `בציפוי אפוקסי קריסטל באישור ה-FDA.` *(owner wrote "הFDA" — suggest hyphenated ה-FDA, confirm)* · EN: `Coated with FDA-approved crystal epoxy.`

| Step | Task |
|---|---|
| 1 | `data/products.json` — append to `description_en` + `description_he` of the 4 products |
| 2 | Inline PRODUCTS arrays — same 4 products: `shofars-goblets.html` (wine horn, lion, menorah), `kiddush-cups.html` (lion, menorah, ceramic) — cross-listed goblets appear in BOTH files |
| 3 | Static SEO cards — same descriptions baked in HTML on both pages |
| 4 | JSON-LD `Product.description` in `<head>` of both pages |
| 5 | QA: open each of the 4 products' modals EN + HE on both pages → note visible; grep confirms all 4 sync points updated per product |

### 22.5 — Per-product anchor URLs (= SEO_GEO_WORK_PLAN W14 option B) 🟡 S–M

Products can't be linked/ranked individually (cards + modal only). Cheap first step before deciding on full per-product pages (W14-A).

| Step | Task |
|---|---|
| 1 | `buildCard()` on all category pages: set `id="{product.id}"` on `.product-card` (ids = products.json slugs, e.g. `#ceramic-kiddush-cup`); same id on the static SEO cards (JS render replaces them, so no duplicate ids at runtime) |
| 2 | On page load: if `location.hash` matches a product id → `scrollIntoView` + open its modal. On modal open, `history.replaceState` the hash; clear on close (no history spam, shareable URL) |
| 3 | JSON-LD: add `"url": "https://shermanartworks.com/{page}#{id}"` to every Product object + ItemList entries on all category pages |
| 4 | `llms.txt`: add per-product anchor URLs under each category |
| 5 | Share/copy affordance in modal (optional, owner call): small "copy link" icon next to product name |
| 6 | QA: direct-load each anchor URL (EN + HE + RTL + mobile), hash opens correct modal, no scroll-jump when opening without hash; after 22.1, anchors must use FINAL page assignments (custom-shofar → custom-shofars.html) |

**+2 weeks after deploy:** check GSC whether anchor URLs surface in queries; then decide W14-A (full product pages).

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
| Sprint 18 | M17 | Shopping Cart Phase A (Steps 1–8) | ✅ |
| Sprint 19 | M18 | Legal core: consent banner, terms, shipping-returns, footer policies, sitemap, privacy SEO bake (+ standalone mobile-breakpoints fix `dbbd00b`) | ✅ |
| Sprint 20 | M10 / M14 | Owner feedback round: Hebrew copy + product accuracy pass (`2aa6f7c`) + gift-wrap/4-day removal (`0823fbc`) | ✅ |
| Sprint 21 | M20 | SEO hardening: JSON-LD resync, shofars head rename, alt texts, FAQPage + Organization schema | ✅ Dev done — awaiting owner approval |
| **→ Sprint 22** | **M21** | **Owner feedback round 2: category split (Horn Goblets / Shofars), inscription hint, mobile modal scroll fix, FDA epoxy note, per-product anchors (W14-B)** | 🔜 Planned 2026-07-08 |
| Sprint 23 | M18 rest + M11.2 | Trust badges, testimonials, newsletter — per FIX_PLAN "Depth & launch" | ⚠️ Trust badges done in Sprint 24; testimonials/newsletter still blocked on owner |
| **Sprint 24** | M18.3 / M20 / launch prep | **2026-07-20 dev-side launch batch: trust strip (10 pages); products.json + llms.txt resynced (3 candlesticks were missing: white, clear-round, clear-rectangular); Google Merchant feed `merchant-feed.xml` (27 products) + `_merchant_feed.py` generator; sitemap lastmod bump ×9; WA quick replies drafted (`WHATSAPP_QUICK_REPLIES.md`); order tracker built (`Documents\Sherman_Art_Works_Order_Tracker.xlsx`). Browser QA: strip EN/HE/RTL/mobile, cart→checkout flow, zero console errors. UNCOMMITTED — awaiting owner approval** | ✅ dev done |
| — | M9 | Full product catalogue | 🔜 Blocked: owner photos for kiddush cups, business gifts |
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
