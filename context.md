# Sherman Art Works — New Chat Context Document
**Date:** June 2026 (Sprint 15 complete) | **Repo:** github.com/jshermanj1-cpu/sherman-artworks-site | **Live:** shermanartworks.com (GitHub Pages, gh-pages branch)

---

## ⛔ COMMIT RULE — READ THIS FIRST

**NEVER commit or push without the owner's explicit written approval.**

- Always stop after completing and previewing work.
- Show the owner what was done (screenshot + summary).
- Wait for the owner to reply with **"approve"** or **"approved"** before running any `git commit` or `git push`.
- This rule has no exceptions — not even for small fixes, typos, or "obvious" changes.
- Violating this rule has happened before. Do not repeat it.

The approval workflow:
1. Do the work
2. Preview + verify
3. Summarise what changed
4. **Wait for "approve"**
5. Only then: `git add … && git commit … && git push`

---

## Project Overview

Sherman Art Works is a family-run handmade glass & Judaica business in Israel. The site is a **single-owner, vanilla HTML/CSS/JS site** (no framework, no backend, no build step) deployed to GitHub Pages. All pages are self-contained HTML files. There are two always-in-sync branches: `main` and `gh-pages`.

---

## Technology Stack

- **HTML**: Self-contained per page (no shared JS/CSS files). Each page duplicates nav/footer/styles.
- **Hosting**: GitHub Pages from `gh-pages` branch. After each commit to `main`, we manually `git merge main` into `gh-pages` and push.
- **Fonts**: Fraunces (display/headlines, replaced Cinzel), Inter (body, replaced Arial), Cormorant Garamond (italic accents only). Hebrew: Frank Ruhl Libre (headlines), Heebo (body). All loaded via Google Fonts.
- **i18n**: Runtime EN/HE switching via `data-t` attributes + a `T = { en: {...}, he: {...} }` object in each page's inline `<script>`. RTL via `html[dir="rtl"]`. `setLang('he')` swaps all text and flips layout.
- **Currency**: Live ILS↔USD conversion via `open.er-api.com/v6/latest/USD` (GET-only, no user data sent). Fallback rate 3.75 ILS/USD with disclaimer. Conversion: `ils / usdRate`.
- **Contact/Orders**: WhatsApp-first (no backend). `wa.me/972523482278` — **⚠️ TEMP NUMBER, needs replacing with official business WhatsApp**.
- **Images**: Cloudinary CDN, cloud name `doesupaf9`. URL pattern: `https://res.cloudinary.com/doesupaf9/image/upload/{transformations}/{public_id}.jpg` — **folder names are NOT in URLs**, only the bare public_id.

---

## Design Tokens (current, in `:root`)

```css
--bg:        #faf7f2;   /* warm cream */
--dark:      #202020;   /* charcoal */
--gold:      #d4b572;   /* brand gold */
--brown:     #6a5530;   /* AA-compliant muted (was #8a6f40) */
--border:    #ede5d8;
--footer-text: #a89678; /* for text on --dark backgrounds, AA-compliant */
--green:     #25d366;   /* WhatsApp */
--ff-body:   'Inter', Arial, sans-serif;
--ff-disp:   'Fraunces', 'Cinzel', serif;
--ff-ital:   'Cormorant Garamond', serif;
--ff-body-he:'Heebo', 'Arial Hebrew', sans-serif;  /* [lang="he"] body */
--ff-disp-he:'Frank Ruhl Libre', 'David', serif;   /* [lang="he"] headlines */
--fs-xs: 0.75rem; --fs-sm: 0.875rem; --fs-base: 1rem;
--fs-lg: 1.125rem; --fs-xl: 1.5rem; --fs-2xl: 2.25rem; --fs-3xl: 3rem;
```

`WA_NUMBER = '972523482278'` (appears ~20× across all pages as a JS constant — needs replacing)

---

## File Map

| File | Purpose | Status |
|---|---|---|
| `index.html` | Homepage — hero + 6-category shop grid + story + contact + footer | ✅ Live |
| `candlesticks.html` | Category page — 1 product, 4 photos, ₪775 | ✅ Live |
| `shofars-goblets.html` | Category page — 3 products (Jerusalem Wine Horn + 2 goblets) | ✅ Live |
| `kiddush-cups.html` | Category page — 2 cross-listed goblets + "more coming soon" section | ✅ Live (upgraded from Coming Soon) |
| `trays-bowls.html` | Category page — 1 product (bowl, 4 photos, ₪1,190) | ✅ Live |
| `business-gifts.html` | Coming Soon stub — SVG gift-box icon, commission CTAs | ✅ Live |
| `mezuzahs.html` | Coming Soon stub — SVG mezuzah icon, commission CTAs | ✅ Live |
| `custom-orders.html` | Custom commissions page — 4-step flow + WhatsApp form | ✅ Live |
| `about.html` | Brand story — 3 generations, craft values, studio | ✅ Live |
| `contact.html` | Contact page — 3-method cards + form + FAQ accordion | ✅ Live |
| `404.html` | Branded 404 page — full nav, hero, 3 CTAs, EN/HE, floating WA | ✅ Live |
| `sitemap.xml` | 10 customer URLs, priorities (homepage 1.0 → coming soon 0.6) | ✅ Live |
| `robots.txt` | Allows all; disallows product-builder.html + glass-curate.html | ✅ Live |
| `product-builder.html` | Internal tool — photo grouping + JSON export for owner (not linked from site) | Tool only |
| `TASK_LIST.md` | Full project roadmap (living doc) | ✅ Up to date |
| `context.md` | This file — full context for new chat sessions | ✅ Up to date |

> `glass-curate.html` was an orphaned internal tool — deleted in Sprint 15.

---

## Product Catalogue (current)

### Candlesticks (`candlesticks.html`)
- **Glass Circle Candlesticks** — ₪775, 20cm × 25cm
- Photos: `IMG_9845_wsxhug`, `WhatsApp_Image_2026-05-23_at_14.51.06_1_q8pfxh`, `WhatsApp_Image_2026-05-23_at_14.51.06_2_mmafna`, `WhatsApp_Image_2026-05-23_at_14.51.06_e7jg95`

### Shofars & Goblets (`shofars-goblets.html`) — 2 sections
- **Jerusalem Wine Horn** — ₪850, 5 photos: `horn-jerusalem`, `horn-grapes`, `horn-grape-name`, `horn-crown`, `horn-edge`
- **Lion of Judah Goblet** — ₪473, 4 photos: `goblet-lion` + variants
- **Menorah Goblet** — ₪473, 3 photos: `goblet-menorah`, `goblets-jerusalem-menorah`

### Kiddush Cups (`kiddush-cups.html`) — cross-listed from Shofars & Goblets
- **Lion of Judah Goblet** — ₪473, 4 photos (same product, cross-listed)
- **Menorah Goblet** — ₪473, 3 photos (same product, cross-listed)
- "More designs coming soon" section with commission CTAs
- Cross-listing is manual: if goblet prices/photos change, update both pages.

### Trays & Bowls (`trays-bowls.html`)
- **Glass Decorative Bowl** — ₪1,190, 15cm × 30cm
- Photos: 4 × `WhatsApp_Image_2026-05-23_at_14.50.45_*` variants

---

## Homepage Category Cards (`index.html` — `.cat-card` grid)

All 4 live category cards use **square frames** (1:1 aspect ratio) with Cloudinary smart crop:

| Card | Cloudinary public_id | Transformation |
|---|---|---|
| Candlesticks | `WhatsApp_Image_2026-05-23_at_14.51.06_1_q8pfxh` | `w_600,h_600,c_fill,g_auto,q_auto,f_auto` |
| Shofars & Goblets | `horn-jerusalem_k5fryr` | `w_600,h_600,c_fill,g_auto,q_auto,f_auto` |
| Kiddush Cups | `goblet-menorah_va4q5g` | `w_600,h_600,c_fill,g_auto,q_auto,f_auto` |
| Trays & Bowls | `WhatsApp_Image_2026-05-23_at_14.50.45_2_lutcx6` | `w_600,h_600,c_fill,g_auto,q_auto,f_auto` |

Note: Shofars card uses `horn-jerusalem_k5fryr` (close-up horn photo) instead of the original panoramic goblets photo, because the wide panoramic (800×403) cropped badly to a square — the horn close-up crops dramatically and cleanly.

CSS:
```css
.cat-card-img-wrap { width: 100%; aspect-ratio: 1 / 1; overflow: hidden; background: #f5f0e8; }
.cat-card-img      { width: 100%; height: 100%; object-fit: cover; object-position: center; transition: transform 0.5s; }
```

Coming Soon cards (Business Gifts, Mezuzahs) use inline SVG placeholders in the same square frame.

"From ₪X / $Y" prices are shown on all 4 live cards. The min price is stored as `data-min-ils="XXX"` on `.cat-card-from` spans and populated by `updatePrices()` (respects the ₪/$ toggle).

---

## Navigation Structure (all 10 pages)

**Desktop nav** (4 items): Shop (dropdown) · Custom Orders · About · Contact

**Shop dropdown:**
- Candlesticks → `candlesticks.html`
- Shofars & Goblets → `shofars-goblets.html`
- Kiddush Cups → `kiddush-cups.html` (live product page — no "Coming Soon" badge in nav)
- Trays & Bowls → `trays-bowls.html`
- Business Gifts `[Coming Soon]` → `business-gifts.html`
- Mezuzahs `[Coming Soon]` → `mezuzahs.html`
- ─── All Collections → `index.html#shop`

**Mobile hamburger**: Same 4 items; Shop expands as an accordion, **categories shown by default (expanded)**, tap to collapse.

**Dropdown JS**: Self-contained `toggleShopDropdown()` + `toggleMobileShop()` functions injected into every page. Click-outside closes dropdown. Escape key closes. RTL-aware (menu anchors to right in Hebrew).

---

## GA4 Analytics (`G-J55QNV6GF1`)

Installed on all 11 pages (including 404.html). Each page has:
1. The GA4 `<script>` snippet immediately after the viewport `<meta>` tag.
2. A `trackGA4(eventName, params)` helper function.
3. A delegated `document.addEventListener('click', ...)` that fires these 5 event types:

| Event name | Trigger |
|---|---|
| `whatsapp_click` | Any `[href*="wa.me"]` link |
| `view_details` | Any `[data-action="view-details"]` button |
| `email_click` | Any `[href^="mailto:"]` link |
| `category_browse` | Any `[data-action="browse-category"]` link |
| `commission_click` | Any `[data-action="commission"]` link |

GA4 property verified in Google Search Console. Sitemap (`sitemap.xml`) submitted at Search Console.

---

## Key Patterns

### Product Card (on category pages)
```
.product-card
  .product-img-wrap  ← main photo, hover scale(1.03)
  .product-body
    .product-cats    ← cat tags
    .product-name
    .product-desc
    .product-footer
      .price-block   ← ₪X ≈ $Y live conversion
      .btn-cart      ← "Order on WhatsApp"
```
Photo badge `+N photos` when product has multiple images.

### Inline Photo Carousel
Scroll through product photos directly on the card (no modal needed). Arrows + dot indicators.
Dots update on scroll; arrows call `scrollCarousel(card, dir)`. Touch-swipe works via `scroll-snap-type`.

### View Details Modal
Split-screen (gallery left + info right on desktop, stacked on mobile).
- `#productModal` > `.modal-inner` > `.modal-gallery` + `.modal-info`
- Prev/next arrows, clickable thumbnail strip, keyboard ←/→/Esc nav, body scroll lock
- `escapeHtml()` / `escapeAttr()` used on all interpolated innerHTML (XSS safety)
- "Order on WhatsApp" CTA pre-fills product name. Email CTA fallback.

### Floating WhatsApp Button
Fixed bottom-right, 56px circle, green `#25d366`, on every page. `[dir="rtl"]` flips to bottom-left. `z-index: 998`.

### Page Structure (non-homepage pages)
1. `.shipping-banner` (top announcement bar — dark bg, gold text)
2. `.top-bar` (EN/HE + ₪/$ toggles)
3. `.nav-wrap` (sticky nav with Shop dropdown + hamburger)
4. `.page-hero` (dark bg, breadcrumb, headline, CTAs)
5. Content section(s)
6. `<footer>` (3-column, dark bg)
7. Floating WA button (`<a id="floatingWa">`)
8. `<script>` block (all JS inline — `WA_NUMBER`, `T = {en, he}`, `setLang()`, `toggleNav()`, `toggleShopDropdown()`, etc.)

### CTA Hierarchy Rule (ui-ux-pro-max)
- One `.btn-primary` per hero (dark bg, gold hover) — the single main action
- Secondary CTAs use `.btn-link` (text + SVG arrow, brown → gold on hover) — NOT a competing `.btn-outline`

### Coming Soon Pages
- Page hero uses inline SVG icon (NOT emoji — ui-ux-pro-max rule: no-emoji-icons)
- Kiddush Cups: now a real page. Business Gifts: gift-box SVG. Mezuzahs: mezuzah-case SVG.
- Each Coming Soon page has: breadcrumb → eyebrow "Coming Soon" → headline → subtitle → body → 2 CTAs (Commission + WhatsApp)
- "Browse Our Other Collections" row at bottom (no second ornament)

---

## Favicon

Three sizes, all served from Cloudinary as PNG with square smart crop:
- 16×16: `w_16,h_16,c_fill,g_auto,f_png`
- 32×32: `w_32,h_32,c_fill,g_auto,f_png`
- 180×180 (apple-touch-icon): `w_180,h_180,c_fill,g_auto,f_png`

Image used: `WhatsApp_Image_2026-05-23_at_14.51.06_1_q8pfxh` (candlestick close-up).

---

## LCP Optimisation

Homepage hero image has a `<link rel="preload" as="image" fetchpriority="high">` in `<head>` to improve Largest Contentful Paint. This is the only page with the preload — add to other pages if their hero image is identified as LCP element.

---

## Credentials & Secrets (NEVER commit)

| Item | Value | Status |
|---|---|---|
| GitHub PAT | `ghp_xxxx…` (redacted) | **⚠️ Was exposed in a previous chat session — owner must rotate at github.com/settings/tokens** |
| Cloudinary API Key | `REDACTED_KEY` | Not in git history — keep out |
| Cloudinary API Secret | `REDACTED_SECRET` | Not in git history — keep out |
| WA Number (temp) | `972523482278` | Replace with official business number |

---

## Recent Git History (latest first)

| Commit | Description |
|---|---|
| `10381e9` | Fix category card image display — square frames, smart crop, horn photo for Shofars |
| `036953a` | Fix category card images + update task list |
| `cc0cd2a` | Remove dead bestseller_badge keys + delete glass-curate.html |
| `4dcf51a` | Add aria fallbacks + GA4 event tracking to all 11 pages |
| `21ae72d` | Add GA4 analytics to all 11 pages (M11.1.1) |
| `9dbb996` | Add sitemap.xml + robots.txt (M11.1.2 dev work) |
| `22a2570` | Strengthen commit rule in context.md |
| `376b75a` | Add 404 page, upgrade favicons, add from-prices, fix Kiddush card, LCP preload |
| `7126208` | Update TASK_LIST.md: Sprint 14 complete |
| `cbfc25a` | Add goblets to Kiddush Cups; remove Coming Soon badge from nav |
| `8c51bac` | Add inline photo carousel to product cards |
| `cb31962` | Add context.md — full session onboarding document |
| `f6715df` | Add Shop dropdown nav with 6 categories (desktop + mobile) |
| `98625de` | UI/UX overhaul: Fraunces + Inter, AA contrast, SVG icons, CTA hierarchy |

---

## Pending / Open Issues

### 🔴 Blockers (owner action required)
1. **Replace temp WhatsApp number** `+972523482278` — ~20 occurrences across all pages. Owner provides official business number → single Python find-and-replace script, done in 5 min.
2. **Rotate GitHub PAT** — was shown in chat. Owner revokes at github.com/settings/tokens, generates new one.

### 🟡 Important (owner action required)
3. **WhatsApp Business profile** — install WA Business app, configure logo/hours/away message (M11.1.3)
4. **New product photos** (M9) — photograph kiddush cups, trays, business gifts, mezuzahs → upload to Cloudinary → use `product-builder.html` to group + export JSON → paste JSON to dev
5. **Diversify OG images** (M13.2.1) — 5 pages share the same bowl photo (index, about, contact, custom-orders, mezuzahs). Owner picks better photos.
6. **TikTok handle** (M0-11) — send handle → dev adds to footer site-wide (XS task)

### 🔜 Major upcoming milestones
- **M9**: Full product catalogue — needs new photos. Use `product-builder.html` to group photos + export JSON, then paste JSON to dev to update `PRODUCTS` array.
- **M10**: Hebrew quality pass — needs native Hebrew speaker (M0-6)
- **M11 Tier 2**: Newsletter bar, Pinterest "Pin It", TikTok footer link
- **M12**: Stripe checkout — owner creates Stripe account first (M0-3)
- **Full launch**: After M9 photos + M0-1 real WhatsApp number

---

## Deployment Workflow

```bash
# After changes + owner approval:
git add <specific files>     # never git add -A (risk of committing .env etc.)
git commit -m "..."
git push origin main

# Sync gh-pages:
git checkout gh-pages
git merge main --no-edit
git push origin gh-pages
git checkout main
```

GitHub Pages serves from `gh-pages` branch. `.nojekyll` file in root suppresses Jekyll. CDN propagation ~1 minute after push.

---

## ui-ux-pro-max Skill

Installed globally at `C:\Users\User\.claude\skills\` — 7 sub-skills: `ui-ux-pro-max`, `design`, `design-system`, `ui-styling`, `brand`, `banner-design`, `slides`. Requires session restart to activate. Python 3.8 available on this machine.

**Skill audit verdict for Sherman (June 2026) — all implemented:**
- Style: "Liquid Glass" / Artisan warmth direction
- Typography: Fraunces + Inter (English), Frank Ruhl Libre + Heebo (Hebrew)
- Contrast: `--brown` #6a5530 (passes AA 4.5:1), `--footer-text` #a89678 (AA on dark)
- Icons: no emoji as structural icons — inline SVG only
- CTA hierarchy: one primary per screen

---

## Python Helper Scripts (site root)

All Python 3.8 compatible (no lowercase generic type hints). All already applied — safe to delete.

| Script | Purpose | Safe to delete? |
|---|---|---|
| `_uiux_overhaul.py` | Font/token/colour/Hebrew sweep | ✅ Yes |
| `_dedup_tokens.py` | Fixed double-insertion of token block | ✅ Yes |
| `_shop_dropdown.py` | Shop dropdown sweep | ✅ Yes |

---

*This file is the single source of truth for onboarding a new chat session. Update after every major sprint.*
