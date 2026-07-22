# Sherman Art Works — Project Specification

> Last updated: May 2026 (rev 3) | Active file: `sherman_artworks_v2.html` | Owner: Sherman Family

---

## 1. Brand Overview

| Field | Detail |
|---|---|
| **Business name** | Sherman Art Works |
| **Type** | Family-owned handmade glass art & Judaica studio |
| **Location** | Israel |
| **Founded** | Multi-generational family business |
| **Primary market** | International (diaspora Judaica buyers, collectors, gift buyers) |
| **Secondary market** | Israeli domestic |
| **Shipping** | Free international shipping on all orders |
| **Contact email** | shermanartworks@gmail.com |
| **WhatsApp** | ⚠️ `wa.me/972XXXXXXXXX` — **REPLACE WITH REAL NUMBER BEFORE LAUNCH** |
| **Domain** | ⚠️ TBD — needs to be registered and configured |

### Brand Voice
Warm, artisanal, heritage-driven. Rooted in Israeli craftsmanship and Jewish tradition. Speaks to collectors, gift buyers, and Judaica enthusiasts worldwide. Never clinical or e-commerce generic — every line should feel like it came from a family who has been doing this for generations.

### Positioning
Premium handmade Judaica and decorative glass art. Not mass-produced. Not a marketplace. A direct-from-artist studio store where every piece is unique.

---

## 2. Products

### 2a. Currently Live on Site

#### Glass Decorative Bowl
| Field | Detail |
|---|---|
| **Price** | ₪ 1,190 |
| **Description** | Handmade glossy, marbled finish decorative bowl in soft seafoam white tones |
| **Colors available** | Multiple (custom on request) — seafoam white is default |
| **Category** | Decorative Bowl |
| **Hebrew name** | קערה דקורטיבית |
| **Image key** | `hero` (main card), `cup_green` (secondary) |
| **Status** | ✅ Live |

#### Murano Style Glass Candlesticks
| Field | Detail |
|---|---|
| **Price** | ₪ 775 |
| **Description** | Handmade Murano Style Glass Candlesticks – Traditional Family Method. Elegant candle holders for Shabbat and the home |
| **Colors available** | TBD — clarify with owner |
| **Category** | Shabbat Candlesticks |
| **Hebrew name** | פמוטים לשבת |
| **Image key** | `platter_blue` (card), `candle_clr`, `candle_blue` (story) |
| **Status** | ✅ Live |

### 2b. Full Collection (copy references these — not yet individually listed as product cards)

| Product | Hebrew | Est. Price | Priority to add |
|---|---|---|---|
| Glass candlestick holders | פמוטי זכוכית | TBD | 🔴 High — already referenced in brand copy |
| Custom-designed glass bowls | קערות זכוכית | TBD | 🔴 High |
| Elegant glass goblets / Kiddush cups | גביעי קידוש | TBD | 🔴 High — explicitly Judaica |
| Unique decorative trays | מגשים דקורטיביים | TBD | 🟡 Medium |
| Silver-plated shofars | שופרות מצופות כסף | TBD | 🟡 Medium — high gift value |
| Silver-plated Judaica (various) | יודאיקה מצופה כסף | TBD | 🟢 Low — catchall |

> ⚠️ **Action required:** Confirm prices, availability, and assign product photos for each of the above before adding to grid.

### 2c. Product Card Requirements (per card)
Each product card must display:
- Product image (high quality, consistent background preferred)
- Category tag (EN + HE)
- Product name (EN + HE)
- Short description (EN + HE, max ~20 words)
- Price in active currency (ILS or USD)
- "Add to Cart" or "Inquire" button
- Color/variant note if applicable

---

## 3. Pricing & Currency

| Setting | Detail |
|---|---|
| **Base currency** | Israeli Shekel (₪ ILS) |
| **Secondary currency** | US Dollar ($ USD) |
| **Conversion rate source** | Live — `https://open.er-api.com/v6/latest/USD` |
| **Markup** | +2% applied on top of live rate |
| **Fallback rate** | 3.05 ILS/USD (if API blocked; set 2026-07-08, re-check quarterly) |
| **Rate display** | "Rate live · +2% margin" shown in top bar |
| **Default on load** | USD (primary market is international) |

> ⚠️ **Risk:** `open.er-api.com` free tier has no SLA. If the API fails, fallback activates silently — users may see stale prices. Add a visible "(estimated rate)" disclaimer when fallback is active.

**Conversion formula:**
```
usdRate = rawILSperUSD / 0.98
USD displayed = ILS price / usdRate
```

---

## 4. Site Structure

### 4a. Current Homepage Sections (top → bottom)

```
┌─────────────────────────────────────────────┐
│  TOP BAR                                    │
│  Language toggle (EN / עברית)               │
│  Currency toggle (₪ ILS / $ USD)            │
│  Live rate note                             │
├─────────────────────────────────────────────┤
│  NAVIGATION                                 │
│  Logo · Gallery · Judaica                  │
│  Custom Orders · About · Contact            │
│  ⚠️ All nav links dead (no sub-pages yet)   │
├─────────────────────────────────────────────┤
│  HERO SECTION                               │
│  Headline + subtitle + brand copy          │
│  [Explore Gallery] [Custom Orders] CTAs     │
│  3-image grid (product photos)              │
├─────────────────────────────────────────────┤
│  SHIPPING BANNER                            │
│  ✦ Custom Orders Are Welcome ✦              │
├─────────────────────────────────────────────┤
│  SHOP SECTION — "Featured Pieces"           │
│  ├── Glass Decorative Bowl card             │
│  ├── Murano Glass Candlesticks card         │
│  └── Coming Soon (dashed placeholder card)  │
├─────────────────────────────────────────────┤
│  STORY SECTION — "A Family of Artisans"     │
│  3 images + brand narrative                 │
├─────────────────────────────────────────────┤
│  CONTACT SECTION ⚠️ MISSING — needs to be added │
│  Email + WhatsApp + Custom Orders form      │
├─────────────────────────────────────────────┤
│  FOOTER                                     │
│  Logo · Copyright · Category tags          │
└─────────────────────────────────────────────┘
```

### 4b. Planned Sub-Pages

| Page | Nav Label | Status | Notes |
|---|---|---|---|
| Gallery | Gallery | 🔜 Not built | Full photo grid of all pieces |
| Judaica collection | Judaica | 🔜 Not built | Filtered view of Judaica products |
| Custom orders | Custom Orders | 🔜 Not built | Form or WhatsApp redirect |
| About | About | 🔜 Not built | Brand story + family history |
| Contact | Contact | 🔜 Not built | Email, WhatsApp, enquiry form |

---

## 5. Localisation / Language

### Supported Languages
| Code | Language | Direction | Status |
|---|---|---|---|
| `en` | English | LTR | ✅ Live |
| `he` | Hebrew (עברית) | RTL | ⚠️ Live but unreviewed |

### Translation Architecture
All UI copy lives in a JS object `T = { en: {...}, he: {...} }` and swaps at runtime via `setLang(l)`.

Elements translated: nav links, hero headline, hero body, button labels, product names, product descriptions, section titles, story text, footer copy, currency/language labels.

### RTL Overrides (when Hebrew active, `dir="rtl"`)
- Nav links reverse order
- Top bar reverses
- Footer right column aligns left
- Product footer reverses

> ⚠️ **Hebrew copy review required before launch.** All current Hebrew strings are machine-translated. Judaica terminology must be reviewed by a fluent native speaker — incorrect or unnatural Hebrew in a Judaica context damages credibility with the core Israeli and diaspora audience.

---

## 6. Design Tokens

| Token | Value | Usage |
|---|---|---|
| **Background** | `#faf7f2` | Page background (warm cream) |
| **Dark** | `#2a1f0e` | Primary text, dark buttons (deep espresso) |
| **Gold accent** | `#c9a85c` | CTAs, highlights, borders |
| **Warm brown** | `#8a6f40` | Secondary text |
| **Border** | `#ede5d8` | Dividers, card borders |
| **Body font** | Heebo (300, 400, 500) | Hebrew-compatible, Google Fonts |
| **Display serif** | Cinzel (400, 600) | Headlines, nav, buttons |
| **Italic serif** | Cormorant Garamond (400i, 600) | Subtitles, emphasis |

> Note: Heebo is chosen specifically because it supports both Latin and Hebrew scripts, enabling clean bilingual rendering without font-switching.

---

## 7. Component Inventory

| Component | ID / Class | Behaviour | Status |
|---|---|---|---|
| Language toggle | `#btnEN`, `#btnHE` | Toggle `active` class, calls `setLang()` | ✅ |
| Currency toggle | `#btnILS`, `#btnUSD` | Toggle `active` class, calls `setCurrency()` | ✅ |
| Live rate note | `#rateNote` | Updated after `fetchRate()` resolves | ✅ |
| Bowl product card | `#bowlImg`, `#b-price`, `#b-usd`, `#b-btn` | Add to Cart → `addToCart('bowl')` | ✅ (alert only) |
| Candles product card | `#candleImg`, `#c-price`, `#c-usd`, `#c-btn` | Add to Cart → `addToCart('candles')` | ✅ (alert only) |
| Coming Soon card | `.coming-soon` | Static placeholder | ✅ |
| Story images | `#sg1`, `#sg2`, `#sg3` | Pull from `IMGS` object | ✅ |
| Hero images | `#hi1`, `#hi2`, `#hi3` | Pull from `IMGS` object | ✅ |
| Logo | `#logoImg` | SVG/JPG from `IMGS.logo` | ✅ |
| Cart / Checkout | — | **Not built** | 🔜 |
| Contact form | — | **Not built** | 🔜 |
| Custom orders form | — | **Not built** | 🔜 |
| Mobile hamburger menu | — | **Not built** | 🔜 |

---

## 8. JavaScript Functions

| Function | Purpose | Status |
|---|---|---|
| `fetchRate()` | Hits open.er-api.com, sets `usdRate`, updates `#rateNote` | ✅ |
| `ilsToUsd(ils)` | Converts ILS → USD using live rate | ✅ |
| `fmtPrice(ils)` | Returns formatted price string in active currency | ✅ |
| `updatePrices()` | Refreshes all price displays on page | ✅ |
| `setCurrency(cur)` | Switches `'ILS'` ↔ `'USD'`, calls `updatePrices()` | ✅ |
| `setLang(l)` | Swaps all UI text `'en'` ↔ `'he'`, updates `dir` | ✅ |
| `addToCart(item)` | **Alert placeholder only** — real cart TBD | ⚠️ Stub |
| Init sequence | `fetchRate()` → `setLang('en')` on `DOMContentLoaded` | ✅ |
| `showFallbackDisclaimer()` | Show "(estimated rate)" when API fails | 🔜 Needed |

---

## 9. Images

### Hosting Strategy
Images must **not** be embedded as base64 data URIs. Base64 bloats the HTML to 10–50MB+, breaks browser caching, and kills page load performance.

**Decision:** Upload images to Cloudinary free tier (generous 25 GB storage, 25 GB bandwidth/month). Reference as plain `<img src="https://res.cloudinary.com/...">` tags.

### Current Image Map (7 of 45 photos used)

| Key | Used for | File |
|---|---|---|
| `hero` | Main hero image (glass bowl) | TBD from curation |
| `cup_green` | Hero secondary image | TBD |
| `cup_amber` | Story gallery 1 | TBD |
| `candle_clr` | Story gallery 2 | TBD |
| `candle_blue` | Story gallery 3 | TBD |
| `platter_blue` | Hero third image + candles product card | TBD |
| `logo` | Navbar logo | TBD |

### Photo Curation Required
45 source photos exist at `/mnt/project/WhatsApp_Image_20260523_at_14_*.jpeg`. Only ~7 are currently mapped.

**Curation criteria:**
- Consistent or neutral background preferred (white, marble, wood — no cluttered backdrops)
- Natural light or even studio light — avoid harsh shadows
- Multiple angles per product: hero shot, detail shot, lifestyle shot
- Select 3–5 images per product SKU
- Flag any that are too dark, blurry, or cluttered for web use

**Recommended allocation:**
- Bowl: 3–4 images (hero, color variant angles)
- Candlesticks: 3–4 images
- Story/brand section: 3 lifestyle images showing craft/studio
- Gallery page: all remaining curated images

---

## 10. User Flows & Conversion Funnel

```
AWARENESS
  └── Google / social media / referral
        └── Land on Homepage

ENGAGEMENT
  ├── Hero: read headline, see product photography
  ├── Shipping banner: custom-orders welcome message removes friction
  ├── Shop section: browse products, read descriptions
  └── Story section: brand trust, generational craftsmanship

INTENT SIGNALS
  ├── "Add to Cart" click → currently broken (alert only)
  ├── "Custom Orders" click → currently dead link
  └── "Explore Gallery" click → currently dead link

CONVERSION PATHS (target state)
  ├── Path A — Direct purchase: Add to Cart → Stripe checkout → order confirmation email
  ├── Path B — Inquiry purchase: WhatsApp / email → personal consultation → payment link
  └── Path C — Custom order: Custom Orders form → back-and-forth → payment link

POST-PURCHASE
  └── Order confirmation + shipping update (email — TBD)
```

### Key Drop-Off Risks (current state)
1. Mobile users: grid layout breaks — likely immediate bounce
2. "Custom Orders" CTA goes nowhere — highest-intent visitors hit a dead end
3. No contact section — trust signal missing for international buyers
4. No checkout — "Add to Cart" is a dummy alert, not a real purchase path

---

## 11. Technical Architecture

### Current
- Single HTML file (`sherman_artworks_v2.html`)
- Vanilla JS, no framework
- Google Fonts via CDN
- CSS variables for theming
- No backend, no database

### Target (launch-ready)
- Single HTML file or simple multi-page site (no build system required)
- Stripe Checkout (hosted) for payments — no PCI compliance burden
- Cloudinary for image hosting
- Optional: Formspree or similar for contact/custom orders form (no backend needed)
- Optional: WhatsApp Business API link for pre-purchase chat

### Hosting Options (recommended)
| Option | Cost | Notes |
|---|---|---|
| GitHub Pages | Free | Static HTML only, custom domain supported |
| Netlify | Free tier | Static + form handling built in, easy deploys |
| Vercel | Free tier | Fast CDN, custom domain, easy |

---

## 12. Copy Reference

### Hero (English)
- **Eyebrow:** Handcrafted in Israel · Since Generations
- **Headline:** Where Light Meets Glass
- **Subtitle:** Each piece, a singular creation
- **Body:** Sherman Art Works creates blown and fused glass Judaica and decorative art of rare beauty — kiddush cups, Shabbat candleholders, decorative bowls and sculptural trays, each one unique and unrepeatable.

### Hero (Hebrew)
- **Eyebrow:** עבודת יד מישראל · מסורת דורות
- **Headline:** כשאור פוגש זכוכית
- **Subtitle:** כל יצירה — בלתי ניתנת לחזרה
- **Body:** ⚠️ *Requires native speaker review*

### Brand Story (English)
At Sherman Art Works, we create a wide variety of handmade glass art, including glass candlestick holders, custom-designed glass bowls, elegant glass goblets, and unique decorative trays, each crafted with artistic vision and attention to detail. Our passion for creating glass art and silver-plated Judaica has been passed down through generations, combining tradition, craftsmanship, and timeless design. Our collection also includes silver-plated shofars, Kiddush cups, and a variety of meaningful Judaica pieces, proudly handcrafted by our family business in Israel.

### Shipping Banner
- **EN:** ✦ Custom Orders Are Welcome ✦
- **HE:** ✦ הזמנות בהתאמה אישית מתקבלות בשמחה ✦

### Contact Section (to be written)
- **EN headline:** Get in Touch
- **EN subhead:** We'd love to hear from you — whether you're shopping for a gift, planning a custom piece, or just curious about our craft.
- **CTA:** WhatsApp Us · Email Us · Send a Message

---

## 13. File History

| File | Notes |
|---|---|
| `sherman_artworks_homepage.html` | Version 1 — initial design |
| `sherman_artworks_homepage_1.html` | Version 1 variant |
| `sherman_artworks_homepage_2.html` | Version 1 variant 2 |
| `sherman_artworks_v2.html` | **Current active version** — bilingual, currency toggle, 2 products, story section |
| `sherman_artworks_PROJECT_SPEC.md` | Spec rev 1–2 |
| `sherman_artworks_PROJECT_SPEC_v3.md` | **This file** — Spec rev 3, expanded |

---

## 14. Open Questions (need owner input)

| # | Question | Blocking |
|---|---|---|
| 1 | What is the real WhatsApp number? | 🔴 Launch-blocking |
| 2 | What domain name should be used? | 🔴 Launch-blocking |
| 3 | Has a Stripe account been created? | 🔴 Checkout-blocking |
| 4 | What are the prices for unlisted products (goblets, shofars, trays)? | 🟡 Needed for full catalogue |
| 5 | Are the candlesticks available in multiple colors? | 🟡 Product detail |
| 6 | Who will review Hebrew copy before launch? | 🟡 Pre-launch |
| 7 | Which hosting platform is preferred? | 🟡 Pre-launch |
| 8 | Is there a returns / refund policy to display? | 🟡 Trust signal |
| 9 | Are there any pieces currently out of stock or not for sale? | 🟡 Inventory management |
| 10 | Should the site support direct purchase, inquiry-only, or both? | 🔴 Affects checkout architecture |

---

## 15. Prioritized Task List

See separate `TASK_LIST.md` for the full sprint-by-sprint breakdown.

---

*This document reflects the full intended state of the Sherman Art Works website as of May 2026 (rev 3). Updated from rev 2 by expanding product catalogue, adding technical architecture, open questions, and linking to task list.*
