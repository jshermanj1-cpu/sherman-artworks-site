# Sherman Art Works — Product Task List

> Last updated: June 2026 (Sprints 3, 4, 6, 7, 8 complete; Sprint 5 partial — 3 of 6 categories live as product cards, 3 Coming Soon. Shop lives on homepage; category pages use product-card system. Bug bash + security review run, findings logged as M13) | PM: Claude | Owner: Sherman Family
> Active file: `sherman-artworks-site/index.html` | Repo: github.com/jshermanj1-cpu/sherman-artworks-site

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
| M0-1 | Provide real WhatsApp number for `wa.me/972XXXXXXXXX` | Sherman | 🔴 Site-wide | ⚠️ Temp number set: +972523482278 — replace with official business number when ready |
| M0-2 | Decide on domain name and register it | Sherman | 🔴 Launch | ✅ shermanartworks.com |
| M0-3 | Create Stripe account (stripe.com) | Sherman | 🔴 M12 | 🔜 |
| M0-4 | Confirm prices for unlisted products (goblets, shofars, trays, Kiddush cups) | Sherman | 🟡 M9 | 🔜 |
| M0-5 | Confirm candlestick color variants (if any) | Sherman | 🟡 M9 | 🔜 |
| M0-6 | Identify a native Hebrew speaker to review all copy | Sherman | 🟡 M10 | 🔜 |
| M0-7 | Decide: direct purchase, inquiry only, or both? | Sherman | — | ✅ WhatsApp-first chosen |
| M0-8 | Choose hosting platform | Sherman | — | ✅ GitHub Pages (gh-pages branch + .nojekyll) |
| M0-9 | Contact form backend | Sherman | — | ✅ Replaced with WhatsApp + mailto (no backend needed) |
| M0-10 | Confirm free shipping threshold (for announcement bar) | Sherman | 🟡 M3 | ✅ Free on all orders |
| M0-11 | Confirm Instagram + TikTok handles | Sherman | 🟡 M3 | ✅ Instagram: shermanartworks |

---

## MILESTONE 1 — Foundation ✅ COMPLETE

### 1.1 — Mobile Responsiveness
| ID | Task | Status |
|---|---|---|
| 1.1.1 | Product grid: `repeat(auto-fit, minmax(280px, 1fr))` | ✅ |
| 1.1.2 | Hero layout stacks vertically on mobile | ✅ |
| 1.1.3 | Story section stacks vertically on mobile | ✅ |
| 1.1.4 | All buttons minimum 44px tall | ✅ |
| 1.1.5 | Hamburger menu for mobile nav | ✅ |
| 1.1.6 | Test on iPhone SE (375px), iPhone 14 (390px), Android (360px) | 🔜 Manual QA |

### 1.2 — Dead Links & CTAs
| ID | Task | Status |
|---|---|---|
| 1.2.1 | "Custom Orders" nav → `#contact` (interim) | ✅ |
| 1.2.2 | "Explore Gallery" button → `#shop` (interim) | ✅ |
| 1.2.3 | "Custom Orders" hero button → `#contact` (interim) | ✅ |
| 1.2.4 | Footer nav links → scroll targets | ✅ |

### 1.3 — Image Performance
| ID | Task | Status |
|---|---|---|
| 1.3.1–2 | No base64 images; Cloudinary account set up | ✅ |
| 1.3.3 | 105 photos uploaded to Cloudinary | ✅ Owner |
| 1.3.4 | Curate 7 photos for mapped slots | ✅ |
| 1.3.5 | All image slots + OG tag use Cloudinary URLs | ✅ |
| 1.3.6 | `loading="lazy"` on non-hero images | ✅ |
| 1.3.7 | `width` + `height` on all `<img>` tags | ✅ |
| 1.3.8 | Full product visible — no cropping (`c_fit` / `height: auto`) | ✅ |

---

## MILESTONE 2 — Trust & Conversion ✅ COMPLETE

### 2.1 — Contact Section (homepage)
| ID | Task | Status |
|---|---|---|
| 2.1.1 | Build Contact section above footer | ✅ |
| 2.1.2 | WhatsApp button | ⚠️ Built — needs real number (M0-1) |
| 2.1.3 | Email link: `mailto:shermanartwork@gmail.com` | ✅ |
| 2.1.4 | Enquiry form — WhatsApp primary, mailto fallback (no backend) | ✅ |
| 2.1.5–7 | Nav wired, email in footer, Hebrew translation | ✅ |

### 2.2 — Custom Orders Flow
| ID | Task | Status |
|---|---|---|
| 2.2.1 | WhatsApp-first flow chosen | ✅ |
| 2.2.2 | "Custom Orders" CTA → WhatsApp with pre-filled message | ⚠️ Done — needs real number (M0-1) |

### 2.3 — Currency
| ID | Task | Status |
|---|---|---|
| 2.3.1–2 | Live ILS↔USD conversion + fallback disclaimer | ✅ |

### 2.4 — SEO & Meta
| ID | Task | Status |
|---|---|---|
| 2.4.1–5 | Title, meta description, OG tags, lang attr, favicon | ✅ |

---

## MILESTONE 3 — Homepage Enhancements ✅ COMPLETE

*Competitor-inspired improvements to the homepage (based on Hazorfim analysis). Quick wins that strengthen trust and conversion — prioritised before new pages as they improve the site visitors already see.*

### 3.1 — Announcement Bar ✅
| ID | Task | Status |
|---|---|---|
| 3.1.1 | Announcement bar top of page: "✦ Free Worldwide Shipping on All Orders · Custom Orders Welcome ✦" | ✅ |
| 3.1.2 | Translated to Hebrew | ✅ |

### 3.2 — Free Shipping ✅
| ID | Task | Status |
|---|---|---|
| 3.2.1 | Free shipping confirmed (all orders, no threshold) | ✅ M0-10 |
| 3.2.2 | Bar copy updated to reflect "all orders" | ✅ |

### 3.3 — Shop by Occasion 🔜 *Deferred*
| ID | Task | Status |
|---|---|---|
| 3.3.1 | "Shop by Occasion" section — Wedding · Bar/Bat Mitzvah · Shabbat · Home Décor | 🔜 Deferred |
| 3.3.2 | "Shop by Price" row — Under $50 · $50–$150 · $150+ | 🔜 Deferred |

### 3.4 — Best Sellers Badges ✅
| ID | Task | Status |
|---|---|---|
| 3.4.1 | "Bestseller" gold badge added to both current product cards | ✅ |
| 3.4.2 | Translated to Hebrew | ✅ |

### 3.5 — Personalisation Badge 🔜 *Deferred*
| ID | Task | Status |
|---|---|---|
| 3.5.1 | "Personal inscription available" badge on product cards | 🔜 No current products support this yet |
| 3.5.2 | Custom Orders CTA note: Size · Colour · Shape · Inscription · Gift packaging | 🔜 Deferred |

### 3.6 — Founder Story Teaser ✅
| ID | Task | Status |
|---|---|---|
| 3.6.1 | "Read Our Full Story →" link added below story section, links to `about.html` | ✅ |

### 3.7 — Corporate & Bulk Gifts CTA ✅
| ID | Task | Status |
|---|---|---|
| 3.7.1 | Dark "Corporate & Events" band added with WhatsApp CTA pre-filled message | ✅ |
| 3.7.2 | Translated to Hebrew | ✅ |

### 3.8 — Social Media Links ✅
| ID | Task | Status |
|---|---|---|
| 3.8.1 | Instagram icon link added to footer → instagram.com/shermanartworks | ✅ |
| 3.8.2 | TikTok link — handle not provided yet | 🔜 M0-11 |

---

## MILESTONE 4 — Shop Section (merged into homepage) ✅ COMPLETE

*Originally built as a separate `shop.html` page. **Restructured: the shop section now lives directly on the homepage** (`index.html#shop`), so visitors land on the shop experience immediately. The old `shop.html` was deleted, and all "Shop" nav links across the site point to `index.html#shop`.*

**Current categories (6):**
1. Candlesticks ✅ photos
2. Shofars & Goblets ✅ photos
3. Kiddush Cups ⏳ Coming Soon
4. Glass Trays & Bowls ✅ bowls only (trays Coming Soon)
5. Business Gifts ⏳ Coming Soon
6. Mezuzahs ⏳ Coming Soon

### 4.1 — Nav & Naming
| ID | Task | Status |
|---|---|---|
| 4.1.1 | Update nav link → `index.html#shop` (EN: "Shop", HE: "חנות") | ✅ |
| 4.1.2 | Remove old "Gallery" / "Judaica" nav references site-wide | ✅ |

### 4.2 — Shop Section on Homepage
| ID | Task | Status |
|---|---|---|
| 4.2.1 | Replace the homepage's old "Featured Pieces" (2 hardcoded products) with the category card grid | ✅ |
| 4.2.2 | Category card grid — one card per category (photo + title + short description) | ✅ |
| 4.2.3 | Each card links to its category page (e.g., `candlesticks.html`) | ✅ |
| 4.2.4 | "Coming Soon" badge + dark placeholder for categories without photos yet | ✅ |
| 4.2.5 | Delete old `shop.html`, update Shop links to `index.html#shop` (or `#shop` when already on homepage) | ✅ |

### 4.3 — Polish
| ID | Task | Status |
|---|---|---|
| 4.3.1 | Mobile responsive grid (2-col tablet, 1-col mobile) | ✅ |
| 4.3.2 | Translate all UI strings to Hebrew + RTL | ✅ |
| 4.3.3 | Homepage hero CTA "Browse the Shop" scrolls to `#shop` section | ✅ |
| 4.3.4 | Remove dead `PRODUCTS`/`addToCart` JS from homepage (no longer needed) | ✅ |

---

## MILESTONE 5 — Category Pages (Product Cards) ⚠️ PARTIAL (3 of 6 live with real products, 3 Coming Soon)

*The 3 active category pages were **restructured from a flat photo grid to a true product catalog**. Each product card groups multiple photos of the same item, shows price + measurements + short description, and opens a full **View Details modal** with photo carousel, full description, and order CTA.*

### 5.1 — Product Card System (shared component)
| ID | Task | Status |
|---|---|---|
| 5.1.1 | Build product card component: photo + name + price + measurements + description + 2 buttons | ✅ |
| 5.1.2 | "+N photos" badge on cards when product has multiple photos | ✅ |
| 5.1.3 | Live ILS→USD conversion via open.er-api.com (shown as `₪X ≈ $Y`) | ✅ |
| 5.1.4 | View Details modal — split-screen layout with photo gallery left, info right | ✅ |
| 5.1.5 | Modal photo carousel: prev/next arrows, clickable thumbnail strip, ←/→ keyboard nav | ✅ |
| 5.1.6 | Modal "Order on WhatsApp" CTA with product name pre-filled | ✅ |
| 5.1.7 | Modal "Email" fallback CTA with product name in subject + body | ✅ |
| 5.1.8 | Esc to close, click outside to close, body scroll lock when open | ✅ |
| 5.1.9 | Mobile responsive: modal stacks gallery + info | ✅ |
| 5.1.10 | Full bilingual EN/HE with RTL — product names, descriptions, all UI strings | ✅ |
| 5.1.11 | Breadcrumb (Shop → Category) on every page | ✅ |
| 5.1.12 | "Commission a custom one" Custom Orders CTA band on every page | ✅ |

### 5.2 — Per-Category Product Catalogue
| ID | Page | Products | Status |
|---|---|---|---|
| 5.2.1 | `candlesticks.html` | 1 product (Glass Circle Candlesticks, 4 photos, ₪775) | ✅ live |
| 5.2.2 | `shofars-goblets.html` | 3 products: Jerusalem Wine Horn (5 photos, ₪850), Lion of Judah Goblet (4 photos, ₪473), Menorah Goblet (3 photos, ₪473) | ✅ live |
| 5.2.3 | `kiddush-cups.html` | 0 — Coming Soon stub | ⏳ |
| 5.2.4 | `trays-bowls.html` | 1 product (Glass Decorative Bowl, 4 photos, ₪1,190) | ✅ live |
| 5.2.5 | `business-gifts.html` | 0 — Coming Soon stub | ⏳ |
| 5.2.6 | `mezuzahs.html` | 0 — Coming Soon stub | ⏳ |

### 5.3 — Polish
| ID | Task | Status |
|---|---|---|
| 5.3.1 | Mobile responsive — all 6 pages | ✅ |
| 5.3.2 | SEO meta per page — category-specific titles + descriptions + OG | ✅ |
| 5.3.3 | Translate all UI strings to Hebrew — all 6 pages + RTL | ✅ |
| 5.3.4 | Wire category pages from homepage `#shop` cards | ✅ |
| 5.3.5 | "Browse other collections" link row on each Coming Soon page | ✅ |
| 5.3.6 | Floating WhatsApp button on every page | ✅ |

### 5.4 — Product Builder Tool
*Standalone tool at `/product-builder.html` (not linked from the site) for owner to update product data. Pre-fills with current products, supports adding/regrouping photos, outputs JSON to paste back to dev.*

| ID | Task | Status |
|---|---|---|
| 5.4.1 | Build `product-builder.html` with tabs per category, photo groupings, metadata forms, JSON export | ✅ |
| 5.4.2 | LocalStorage persistence so progress isn't lost on refresh | ✅ |

### 5.5 — When new photos arrive
*To add new products or activate a Coming Soon category:*
1. *Upload photos to Cloudinary*
2. *Open `/product-builder.html`, group the new photos, fill in name/description/measurements/price, generate JSON*
3. *Paste JSON to dev; dev updates the `PRODUCTS` array in the relevant `*.html` file*
4. *For a previously-Coming-Soon category: also replace the `cat-card-placeholder` on `index.html#shop` with a real `<img>` and remove the `Coming Soon` badge*

---

## MILESTONE 6 — Custom Orders Page ✅ COMPLETE

*Dedicated page for bespoke commissions — makes the custom offer feel premium.*

### 6.1 — Page Build
| ID | Task | Status |
|---|---|---|
| 6.1.1 | Create `custom-orders.html` with shared header/footer | ✅ |
| 6.1.2 | Hero: "Commission a One-of-a-Kind Piece" — headline + brand copy | ✅ |
| 6.1.3 | How It Works — 4 steps (enquire → design → craft → deliver) with arrows | ✅ |
| 6.1.4 | What can be customised: size, colour, inscription, gift packaging, quantity | ✅ |
| 6.1.5 | WhatsApp CTA button in hero with pre-filled message | ✅ |
| 6.1.6 | Enquiry form: name, email, piece type dropdown, vision textarea → WhatsApp | ✅ |
| 6.1.7 | Lead time copy: 2–4 weeks, reply within 24h | ✅ |
| 6.1.8 | Gallery of past custom pieces | 🔜 Deferred — waiting on new photos |

### 6.2 — Polish
| ID | Task | Status |
|---|---|---|
| 6.2.1 | Mobile responsive | ✅ |
| 6.2.2 | SEO meta — "custom glass art Israel", "bespoke Judaica gift" | ✅ |
| 6.2.3 | Translate to Hebrew | ✅ |
| 6.2.4 | Nav "Custom Orders" → `custom-orders.html` | ✅ |

---

## MILESTONE 7 — About Page ✅ COMPLETE

*Builds brand trust and emotional connection — critical for premium pricing.*

### 7.1 — Page Build
| ID | Task | Status |
|---|---|---|
| 7.1.1 | Create `about.html` with shared header/footer | ✅ |
| 7.1.2 | Hero: "Three Generations of Glass" dark headline | ✅ |
| 7.1.3 | Origin story: grandfather's passion, 3 generations narrative | ✅ |
| 7.1.4 | Our Craft section: unique methods, art-first philosophy | ✅ |
| 7.1.5 | Three Generations band (I · II · III cards, dark bg) | ✅ |
| 7.1.6 | Values: Entirely Handmade · Our Own Methods · Made in Israel | ✅ |
| 7.1.7 | CTA bottom → "Explore Gallery" + "Commission a Piece" | ✅ |
| 7.1.8 | Studio/family photos — update when reshoot complete | 🔜 New photos pending |

### 7.2 — Polish
| ID | Task | Status |
|---|---|---|
| 7.2.1 | Mobile responsive | ✅ |
| 7.2.2 | SEO meta — "handmade glass art Israel family studio" | ✅ |
| 7.2.3 | Translate to Hebrew | ✅ |
| 7.2.4 | Nav "About" → `about.html` | ✅ |

---

## MILESTONE 8 — Contact Page ✅ COMPLETE

*Standalone contact page — more detailed than the homepage section.*

### 8.1 — Page Build
| ID | Task | Status |
|---|---|---|
| 8.1.1 | Create `contact.html` with shared header/footer | ✅ |
| 8.1.2 | Hero: "We'd love to hear from you" — warm, personal copy | ✅ |
| 8.1.3 | WhatsApp button (primary) + Email button in hero | ✅ |
| 8.1.4 | Three-way methods band: WhatsApp · Email · Instagram cards | ✅ |
| 8.1.5 | Full enquiry form: name, email, subject (6 options), message → WhatsApp + email fallback | ✅ |
| 8.1.6 | FAQ accordion: shipping, custom lead time, damage, payment, worldwide, returns | ✅ |
| 8.1.7 | "Crafted in Israel, Sent With Care" trust band — Made in Israel · Free Worldwide · 24h reply | ✅ |

### 8.2 — Polish
| ID | Task | Status |
|---|---|---|
| 8.2.1 | Mobile responsive | ✅ |
| 8.2.2 | SEO meta (title, description, OG image) | ✅ |
| 8.2.3 | Translate to Hebrew (full bilingual + RTL) | ✅ |
| 8.2.4 | Wire nav "Contact" link to `contact.html` across index, about, custom-orders | ✅ |
| 8.2.5 | Fix homepage hero "Custom Orders" button → `custom-orders.html` (was → #contact) | ✅ |

---

## MILESTONE 9 — Full Product Catalogue 🔜

### 9.1 — Additional Product Cards 🟡
| ID | Task | Effort |
|---|---|---|
| 9.1.1 | Add Kiddush Cup product card (price + images from owner) | M |
| 9.1.2 | Add Glass Goblets product card | M |
| 9.1.3 | Add Decorative Tray product card | M |
| 9.1.4 | Add Silver-plated Shofar product card | M |
| 9.1.5 | Add color picker/swatch to Bowl card | M |
| 9.1.6 | Remove "Coming Soon" placeholder | XS |
| 9.1.7 | Expand photo curation to 25+ images across all products | L |

---

## MILESTONE 10 — Hebrew Quality & Localisation 🔜

| ID | Task | Effort |
|---|---|---|
| 10.1 | Full Hebrew copy review by native speaker — all pages | M |
| 10.2 | Review Judaica-specific Hebrew terminology | S |
| 10.3 | Test full RTL layout on real device (iOS Safari + Android Chrome) | S |
| 10.4 | Verify Heebo font renders correctly in Hebrew at all sizes | XS |
| 10.5 | Add `hreflang` meta tags for Hebrew/English SEO | XS |

---

## MILESTONE 11 — Marketing & Distribution 🔜

*Eight tasks in three tiers. Tier 1 = foundational, install before any marketing push so you can measure what's working. Tier 2 = growth channels. Tier 3 = strategic decision the owner leads.*

### 11.1 — Tier 1: Foundational (install first)

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.1.1 | Set up Google Analytics 4 (GA4) — tracks visitors, page views, CTA clicks, sources. Free. | Create a free GA4 property at analytics.google.com (~15 min, needs a Google account). Send the Measurement ID (looks like `G-XXXXXXX`) to dev. | Inject the GA4 snippet into every page via Python script. Verify events fire in real-time view. | S |
| 11.1.2 | Set up Google Search Console + sitemap.xml — gets pages indexed by Google, reports on queries that bring traffic. Free. | Verify ownership of shermanartworks.com in Search Console (~5 min, needs Google account). | Generate `sitemap.xml` with all URLs (auto). Add `robots.txt`. Submit sitemap from Search Console. | S |
| 11.1.3 | Upgrade to WhatsApp Business profile — adds business name, logo, hours, away message, quick replies. Visitors see "Sherman Art Works" not a personal number. Free app. | Install WhatsApp Business app. Configure profile (logo, hours, address, away-message template). Coordinate with replacing the temp WA number (M0-1). | None. | S |

### 11.2 — Tier 2: Growth Channels

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.2.1 | Wire real Instagram + TikTok handles in footer | Confirm Instagram handle is `shermanartworks`. Provide TikTok handle (M0-11). | Update the social-link URLs in the footer site-wide. | XS |
| 11.2.2 | Choose + set up email newsletter service (Brevo / Mailchimp / Buttondown). Free tiers exist. | Sign up, decide on a welcome email template. | Wire up the API key / embed if needed. | S |
| 11.2.3 | Add newsletter signup bar to homepage (after the shop section) | Approve copy + visual treatment. | Build inline form + connect to provider. Style to match. | M |
| 11.2.4 | Add Pinterest "Pin it" button to product cards — Pinterest is the highest-converting visual platform for handmade goods. | Confirm visual addition is desired. | Add Pinterest pinit.js to product cards. Each card becomes pinnable to user boards (= evergreen marketing). | XS |

### 11.3 — Tier 3: Strategic (owner-led)

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.3.1 | Evaluate Etsy / Not on the High Street / Aisle Society as parallel sales channel — ~10-12% fees but huge built-in traffic. | Decide whether to explore. If yes: register as a seller, list a few products via their own upload UI. | None initially. Later we may add "Also available on Etsy" badges to product pages. | 👤 Owner |

### 11.4 — Recommended Order

**Week 1 (do all 3 — foundational):**
1. GA4 install → start measuring from now (11.1.1)
2. Search Console + sitemap → get indexed by Google (11.1.2)
3. WhatsApp Business profile → upgrade the main contact channel (11.1.3) — pair with M0-1 number swap

**Week 2-3 (when time allows):**
4. Wire Instagram + TikTok (11.2.1) — quick, just need handles
5. Newsletter setup + signup bar (11.2.2 + 11.2.3) — biggest long-term ROI for repeat sales
6. Pinterest button (11.2.4) — visual platform, fits the brand

**Whenever (no urgency):**
7. Etsy evaluation (11.3.1)

### 11.5 — Dependencies

- **11.1.3** (WhatsApp Business) should happen *alongside* **M0-1** (replace temp WhatsApp number with official one) — don't upgrade twice
- **11.2.1** (social links) blocked on owner confirming handles (M0-11)
- **11.2.3** (signup bar on homepage) blocked on 11.2.2 (newsletter service chosen)

---

## MILESTONE 12 — Stripe Checkout (Revenue) 🔜

*Can soft-launch without this using WhatsApp as the purchase path.*

### 12.1 — Stripe Integration
| ID | Task | Effort |
|---|---|---|
| 12.1.1 | Create Stripe account, verify identity | 👤 Owner |
| 12.1.2 | Create Stripe Payment Links for each product | S |
| 12.1.3 | Replace "Add to Cart" WhatsApp fallback → Stripe Payment Link | XS |
| 12.1.4 | Test full purchase flow end-to-end (test card: 4242 4242...) | S |
| 12.1.5 | Add order confirmation email in Stripe dashboard | S |
| 12.1.6 | Switch Stripe from test to live mode | XS |

### 12.2 — Cart UX (V2 after launch)
| ID | Task | Effort |
|---|---|---|
| 12.2.1 | Slide-out mini-cart panel | L |
| 12.2.2 | Multi-item Stripe Cart session | L |

---

## MILESTONE 13 — Bug Bash & Polish 🔜

*Findings from a full bug bash + security review (June 2026). Pages tested: all 10 customer-facing pages. Grouped by severity.*

### 13.1 — 🔴 Blockers (security / launch-readiness)

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 13.1.1 | Rotate GitHub PAT — `ghp_pDwEnvm...` was shown in chat (not in git history, but chat logs are a leak vector) | Revoke at github.com/settings/tokens, generate a new one, send to dev | Update local push workflow to use new PAT | XS · 👤 Owner |
| 13.1.2 | Replace temp WhatsApp number `+972523482278` site-wide (20 occurrences) | Provide official business WhatsApp number | Single-line site-wide find-and-replace | XS — *covered by M0-1* |

### 13.2 — 🟡 Important (fix soon)

| ID | Task | Detail | Effort |
|---|---|---|---|
| 13.2.1 | Diversify OG (social-share) images — 6 pages currently use the same bowl image (index, about, contact, custom-orders, mezuzahs, trays-bowls). Visitors sharing different page links get identical previews. | trays-bowls correctly shows a bowl. Pick more representative photos for the other 5: about → studio shot, contact → workshop, custom-orders → handcrafting close-up, index → hero collection shot, mezuzahs → keep as fallback OR pick analogue (👤 owner picks) | S · 👤 Owner-dependent |
| 13.2.2 | Add `sitemap.xml` listing all 10 customer URLs | Required for M11.1.2 (Google Search Console submission) | XS |
| 13.2.3 | Add `robots.txt` pointing at sitemap, blocking `product-builder.html` and any other internal tools | Required for M11.1.2; also hides the internal tool from search engines | XS |
| 13.2.4 | Add `aria-label` fallback on JS-populated nav links — 17-20 empty `<a data-t="...">` per page have no accessible text if JS fails to load | Single Python script across all pages | S |

### 13.3 — 🟢 Nice-to-have polish

| ID | Task | Detail | Effort |
|---|---|---|---|
| 13.3.1 | Remove unused `bestseller_badge` translation key in index.html | Leftover from old "Best Seller" badges that were removed | XS |
| 13.3.2 | Delete orphan `glass-curate.html` from working tree | Old curation tool, never committed, never linked. Already not deployed. | XS |
| 13.3.3 | Consider blocking `product-builder.html` from public discovery | Internal tool currently accessible at shermanartworks.com/product-builder.html. Not a security risk (no live API), just clutter. Could exclude via robots.txt (covered by 13.2.3) or accept as-is. | XS |
| 13.3.4 | Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options) — NOT set | GitHub Pages doesn't expose response-header config. Would require Cloudflare proxy in front. HTTPS + 301 redirect already work, so the practical risk is low. Defer unless we move off GitHub Pages. | 👤 Decision |

### 13.4 — ✅ Verified clean (no action needed)

*For the record, these were checked and passed:*
- All 10 customer pages return HTTP 200, no broken internal links, no broken anchors
- Every `data-t` key has matching EN + HE translation
- All `<title>` and `<meta description>` unique
- `lang` + `dir` + viewport set on all customer pages
- Every `<img>` has an `alt` attribute
- All `target="_blank"` links use `rel="noopener noreferrer"` (no tabnabbing)
- No `eval` / `new Function` / dynamic code execution anywhere
- Product cards use `escapeHtml` / `escapeAttr` for all interpolated values (no XSS)
- Forms have no `action` attribute — all JS-handled via WhatsApp + mailto (no server POST)
- No sensitive input fields (password, card, SSN) anywhere
- No secrets in git history (no Cloudinary `api_secret`, no GitHub PAT, no API keys)
- Cloudinary delivery URLs use the public cloud name only — API credentials never appear in client HTML
- External resources load from only 3 trusted hosts: `fonts.googleapis.com`, `fonts.gstatic.com`, `res.cloudinary.com`
- Live currency API (`open.er-api.com`) is a GET-only call with no user data sent
- Modal interactions verified end-to-end (open, photo nav, close, body scroll lock, keyboard ←/→/Esc)
- Language toggle EN↔HE verified across all pages
- Floating WhatsApp button persists across language switches and scroll positions
- HTTPS works on the live site, HTTP→HTTPS 301 redirect confirmed

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 5/11 done |
| Sprint 1 | M1 | Foundation: mobile, links, images | ✅ Done |
| Sprint 2 | M2 | Trust: contact, SEO, currency | ✅ Done |
| **→ SOFT LAUNCH** | — | Wire real WhatsApp number, enable custom domain | ⚠️ Temp WA number active, custom domain live |
| Sprint 3 | M3 | Homepage enhancements (announcement bar, best sellers, corporate CTA, Instagram) | ✅ Done (3.3 + 3.5 deferred) |
| Sprint 4 | M4 | Shop landing page (category hub) | ✅ Done |
| Sprint 5 | M5 | Category pages × 6 (Candlesticks, Shofars & Goblets w/ picker, Trays & Bowls live; Kiddush, Business, Mezuzahs Coming Soon) | ⚠️ Partial (3/6 with photos) |
| Sprint 6 | M6 | Custom Orders page | ✅ Done |
| Sprint 7 | M7 | About page | ✅ Done |
| Sprint 8 | M8 | Contact page | ✅ Done |
| **→ Sprint 9** | M9 | Full product catalogue | 🔜 **NEXT** (blocked on photo reshoot) |
| Sprint 10 | M10 | Hebrew quality pass | 🔜 |
| Sprint 11 | M11 | Marketing & analytics (3 tiers — foundational / growth / strategic; full plan in §M11) | 🔜 fully unblocked |
| Sprint 12 | M12 | Stripe checkout | 🔜 |
| Sprint 13 | M13 | Bug bash & polish (2 blockers, 4 important, 4 polish — full list in §M13) | 🔜 |
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

*Task list is a living document. Update status as tasks complete.*
