# Sherman Art Works — New Chat Context Document
**Date:** June 2026 | **Repo:** github.com/jshermanj1-cpu/sherman-artworks-site | **Live:** shermanartworks.com (GitHub Pages, gh-pages branch)

---

## Project Overview

Sherman Art Works is a family-run handmade glass & Judaica business in Israel. The site is a **single-owner, vanilla HTML/CSS/JS site** (no framework, no backend, no build step) deployed to GitHub Pages. All pages are self-contained HTML files. There are two always-in-sync branches: `main` and `gh-pages`.

**The golden rule: never commit without the owner's explicit "approve" or "approved".**

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
| `shofars-goblets.html` | Category page — 3 products (2 sections: Shofars + Goblets) | ✅ Live |
| `trays-bowls.html` | Category page — 1 product (bowl, 4 photos, ₪1,190) | ✅ Live |
| `kiddush-cups.html` | Coming Soon stub — SVG chalice icon, commission CTAs | ✅ Live |
| `business-gifts.html` | Coming Soon stub — SVG gift-box icon, commission CTAs | ✅ Live |
| `mezuzahs.html` | Coming Soon stub — SVG mezuzah icon, commission CTAs | ✅ Live |
| `custom-orders.html` | Custom commissions page — 4-step flow + WhatsApp form | ✅ Live |
| `about.html` | Brand story — 3 generations, craft values, studio | ✅ Live |
| `contact.html` | Contact page — 3-method cards + form + FAQ accordion | ✅ Live |
| `product-builder.html` | Internal tool — photo grouping + JSON export for owner (not linked from site) | Tool only |
| `glass-curate.html` | Old curation tool — orphaned, never committed, never linked | Delete when ready |
| `TASK_LIST.md` | Full project roadmap (living doc) | Up to date |
| `context.md` | This file — full context for new chat sessions | Up to date |

---

## Product Catalogue (current)

### Candlesticks (`candlesticks.html`)
- **Glass Circle Candlesticks** — ₪775, 20cm × 25cm, "Handmade Murano-style glass candlesticks"
- Photos: `IMG_9845_wsxhug`, `WhatsApp_Image_2026-05-23_at_14.51.06_1_q8pfxh`, `WhatsApp_Image_2026-05-23_at_14.51.06_2_mmafna`, `WhatsApp_Image_2026-05-23_at_14.51.06_e7jg95`

### Shofars & Goblets (`shofars-goblets.html`) — 2 sections
- **Jerusalem Wine Horn** — ₪850, 5 photos: `horn-jerusalem`, `horn-grapes`, `horn-grape-name`, `horn-crown`, `horn-edge`
- **Lion of Judah Goblet** — ₪473, 4 photos: `goblet-lion` + variants
- **Menorah Goblet** — ₪473, 3 photos: `goblet-menorah`, `goblets-jerusalem-menorah`

### Trays & Bowls (`trays-bowls.html`)
- **Glass Decorative Bowl** — ₪1,190, 15cm × 30cm, long handcrafted description
- Photos: 4 × `WhatsApp_Image_2026-05-23_at_14.50.45_*` variants

---

## Navigation Structure (all 10 pages)

**Desktop nav** (4 items): Shop (dropdown) · Custom Orders · About · Contact

**Shop dropdown:**
- Candlesticks → `candlesticks.html`
- Shofars & Goblets → `shofars-goblets.html`
- Kiddush Cups `[Coming Soon]` → `kiddush-cups.html`
- Trays & Bowls → `trays-bowls.html`
- Business Gifts `[Coming Soon]` → `business-gifts.html`
- Mezuzahs `[Coming Soon]` → `mezuzahs.html`
- ─── All Collections → `index.html#shop`

**Mobile hamburger**: Same 4 items; Shop expands as an accordion, **categories shown by default (expanded)**, tap to collapse.

**Dropdown JS**: Self-contained `toggleShopDropdown()` + `toggleMobileShop()` functions injected into every page. Click-outside closes dropdown. Escape key closes. RTL-aware (menu anchors to right in Hebrew).

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
- Kiddush Cups: chalice SVG | Business Gifts: gift-box SVG | Mezuzahs: mezuzah-case SVG
- Each has: breadcrumb → eyebrow "Coming Soon" → headline → subtitle → body → 2 CTAs (Commission + WhatsApp)
- "Browse Our Other Collections" row at bottom (no second ornament)

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
| `f6715df` | Add Shop dropdown nav with 6 categories (desktop + mobile) |
| `98625de` | UI/UX overhaul: Fraunces + Inter, AA contrast, SVG icons, CTA hierarchy |
| `9518efb` | Add M13: bug bash & security review findings |
| `5c3d36c` | Expand M11 plan: 3 tiers, owner-vs-dev split, recommended order |
| `debc41d` | Shop merge + product card system with carousel & modal |
| `a1281e0` | Add floating WhatsApp + per-category OG + brighter gold + mobile headlines |
| `81ffa83` | Restyle: charcoal dark + Arial body font |
| `d5df83b` | M4-M5: shop landing + 6 category pages + nav rewire |
| `ad5bc54` | M8: add standalone contact page + wire nav links site-wide |

---

## Pending / Open Issues

### 🔴 Blockers
1. **Replace temp WhatsApp number** `+972523482278` — 20 occurrences across all pages. Owner provides official business number → single Python find-and-replace script.
2. **Rotate GitHub PAT** — was shown in chat. Owner revokes at github.com/settings/tokens, generates new one, sends to dev.

### 🟡 Important (fix soon)
3. **sitemap.xml + robots.txt** — needed for Google Search Console (M11.1.2). `robots.txt` should block `product-builder.html`.
4. **aria-label fallbacks** on JS-populated nav `<a data-t="...">` links — empty if JS fails to load.
5. **Diversify OG images** — 5 pages share the same bowl photo (index, about, contact, custom-orders, mezuzahs). Owner needs to pick better representative photos.

### 🟢 Polish
6. Remove unused `bestseller_badge` translation key from `index.html`
7. Delete orphaned `glass-curate.html` from working tree
8. Block `product-builder.html` via robots.txt (or accept it's publicly accessible — no security risk)

### 🔜 Major upcoming milestones
- **M9**: Full product catalogue — needs new photos for kiddush cups / trays / business gifts / mezuzahs. Use `product-builder.html` to group photos + export JSON, then paste JSON to dev to update `PRODUCTS` array in the relevant page.
- **M10**: Hebrew quality pass — needs native Hebrew speaker (M0-6)
- **M11**: Marketing — GA4, Google Search Console + sitemap, WhatsApp Business profile, Instagram/TikTok wiring, newsletter signup bar
- **M12**: Stripe checkout — owner creates Stripe account first (M0-3)
- **Full launch**: After M9 photos + M11 foundational tier (GA4 + Search Console + WA Business)

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

**Skill audit verdict for Sherman (June 2026):**
- Style: "Liquid Glass" / Artisan warmth direction chosen
- Typography: Fraunces + Inter (English), Frank Ruhl Libre + Heebo (Hebrew) — **already implemented**
- Contrast: `--brown` upgraded from #8a6f40 to #6a5530 (passes AA 4.5:1) — **already implemented**
- Icons: no emoji as structural icons — use inline SVG — **already implemented**
- CTA hierarchy: one primary per screen — **already implemented**

---

## Python Helper Scripts (site root)

All Python 3.8 compatible (no lowercase generic type hints). All already applied — safe to delete after confirming.

| Script | Purpose | Safe to delete? |
|---|---|---|
| `_uiux_overhaul.py` | Font/token/colour/Hebrew sweep | ✅ Yes |
| `_dedup_tokens.py` | Fixed double-insertion of token block | ✅ Yes |
| `_shop_dropdown.py` | Shop dropdown sweep | ✅ Yes |

---

*This file is the single source of truth for onboarding a new chat session. Update after every major sprint.*
