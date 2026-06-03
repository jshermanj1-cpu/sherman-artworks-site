# Sherman Art Works — Product Task List

> Last updated: June 2026 (Sprint 15 complete — 404 page, favicon upgrade, from-prices, GA4, Search Console, sitemap, aria fallbacks, event tracking, cleanup) | PM: Claude | Owner: Sherman Family
> Active file: `sherman-artworks-site/index.html` | Repo: github.com/jshermanj1-cpu/sherman-artworks-site

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
| M0-1 | Provide real WhatsApp number | Sherman | 🔴 Site-wide | ⚠️ Temp +972523482278 active — **send real number ASAP** |
| M0-2 | Domain name | Sherman | — | ✅ shermanartworks.com |
| M0-3 | Create Stripe account | Sherman | 🔴 M12 | 🔜 |
| M0-4 | Confirm prices for remaining products | Sherman | 🟡 M9 | ⚠️ Live products have prices. Missing: dedicated kiddush cups, mezuzahs, business gifts |
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
6. Mezuzahs ⏳ Coming Soon

All category cards show real product photos. "From ₪X / $X" prices shown on all 4 live categories, updating on currency toggle.

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
| `mezuzahs.html` | 0 — Coming Soon stub | ⏳ |

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
| 10.4 | Frank Ruhl Libre + Heebo rendering check | XS |
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

## MILESTONE 12 — Stripe Checkout 🔜
*Blocked on M0-3 (owner creates Stripe account).*

---

## MILESTONE 13 — Bug Bash & Security ⚠️ MOSTLY COMPLETE

### 13.1 — 🔴 Blockers

| ID | Task | Status |
|---|---|---|
| 13.1.1 | Rotate GitHub PAT (`ghp_pDwEnvm…` exposed in chat) | 🔜 👤 Owner: revoke at github.com/settings/tokens |
| 13.1.2 | Replace temp WA number `+972523482278` (20× across pages) | 🔜 Covered by M0-1 |

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
| Fraunces + Inter fonts, Frank Ruhl Libre + Heebo for Hebrew | ✅ |
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
| 🔴 | **Replace temp WhatsApp number** (M0-1) | Send me the real business number → I update 20 occurrences in 5 min |
| 🔴 | **Rotate GitHub PAT** (M13.1.1) | Revoke at github.com/settings/tokens, generate new one |
| 🟡 | **WhatsApp Business profile** (M11.1.3) | Install WA Business app, set up logo/hours/away message |
| 🟡 | **New product photos** (M9) | Photograph kiddush cups, mezuzahs, business gifts → upload to Cloudinary |
| 🟡 | **Diversify OG images** (M13.2.1) | Pick better social-share photos for about/contact/custom-orders/index/mezuzahs |
| 🟡 | **TikTok handle** (M0-11) | Send handle → I add to footer site-wide |
| 🟡 | **GA4 property** (M11.1.1) | ✅ Done — check analytics.google.com for real-time data |

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 7/11 done |
| Sprint 1 | M1 | Foundation | ✅ |
| Sprint 2 | M2 | Trust & conversion | ✅ |
| Sprint 3 | M3 | Homepage enhancements | ✅ |
| Sprint 4 | M4 | Shop category hub | ✅ |
| Sprint 5 | M5 | Category pages | ✅ 4/6 live |
| Sprint 6–8 | M6–M8 | Custom Orders, About, Contact pages | ✅ |
| Sprint 13 | M13 | Bug bash + security audit | ✅ Mostly done |
| Sprint 14 | M14 | UI/UX overhaul, dropdown, carousel, cross-category | ✅ |
| **Sprint 15** | M15 | 404 page, favicons, prices, GA4, Search Console, aria, cleanup | ✅ **Done** |
| **→ Next** | M9 | Full product catalogue | 🔜 Blocked: owner photos |
| — | M11 Tier 2 | Newsletter, Pinterest, TikTok | 🔜 |
| — | M10 | Hebrew quality pass | 🔜 Blocked: native speaker |
| — | M12 | Stripe checkout | 🔜 Blocked: M0-3 |
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
