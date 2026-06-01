# Sherman Art Works — Product Task List

> Last updated: June 2026 (Sprints 3, 4, 6, 7, 8 complete; Sprint 5 partial — 3 of 6 category pages built, 3 Coming Soon) | PM: Claude | Owner: Sherman Family
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

## MILESTONE 4 — Shop Landing Page ✅ COMPLETE

*Category-selection hub. Users arrive here and choose which type of piece to browse. Replaces the old flat "Glass page" concept. Extensible: add or remove categories by editing the card grid and this list.*

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
| 4.1.1 | Update nav link → `shop.html` (EN: "Shop", HE: "חנות") | ✅ |
| 4.1.2 | Remove old "Gallery" / "Judaica" nav references site-wide | ✅ |

### 4.2 — Landing Page Build
| ID | Task | Status |
|---|---|---|
| 4.2.1 | Create `shop.html` with shared header/footer | ✅ |
| 4.2.2 | Hero: "Explore Our Handmade Glass" — introductory headline + brand copy | ✅ |
| 4.2.3 | Category card grid — one card per category (photo + title + short description) | ✅ |
| 4.2.4 | Each card links to its category page (e.g., `candlesticks.html`) | ✅ |
| 4.2.5 | "Coming Soon" badge + dark placeholder for categories without photos yet | ✅ |
| 4.2.6 | Bottom "Don't see what you're after?" Custom Orders CTA | ✅ |

### 4.3 — Polish
| ID | Task | Status |
|---|---|---|
| 4.3.1 | Mobile responsive grid (2-col tablet, 1-col mobile) | ✅ |
| 4.3.2 | SEO meta: title, description, OG image for shop landing | ✅ |
| 4.3.3 | Translate all UI strings to Hebrew + RTL | ✅ |
| 4.3.4 | Update homepage hero CTA "Browse the Shop" → `shop.html` (was `#shop`) | ✅ |

---

## MILESTONE 5 — Category Pages ⚠️ PARTIAL (3 of 6 live with photos, 3 Coming Soon)

*One page per product category. All pages share the same template. To add a new category: create a new HTML file from the template and add a card to `shop.html`. To remove: delete the file and remove its card.*

### 5.1 — Shared Category Page Template
| ID | Task | Status |
|---|---|---|
| 5.1.1 | Build reusable category page template (hero, photo grid, lightbox, WhatsApp CTA, footer) | ✅ |
| 5.1.2 | Photo grid — Cloudinary photos for each category | ✅ for ready categories |
| 5.1.3 | Lightbox — click photo → full-screen view, Escape to close | ✅ |
| 5.1.4 | "Enquire about this piece" CTA per photo → WhatsApp with photo URL pre-filled | ✅ |
| 5.1.5 | "Commission a custom one" Custom Orders CTA on every page | ✅ |
| 5.1.6 | Breadcrumb (Shop → Category) on every page | ✅ |

### 5.2 — Shofars & Goblets: Design Picker (special case)
*This page is more than a grid — it's a configurator. Visitors pick a design (Jerusalem/Grapes/Crown for shofars, Lion/Menorah for goblets) and the WhatsApp CTA pre-fills with that design + an offer to customize the inscription.*

| ID | Task | Status |
|---|---|---|
| 5.2.1 | Two product sections on one page: Silver-Plated Shofars + Goblets | ✅ |
| 5.2.2 | Design cards per product type (4 shofars + 3 goblets) — photo + name + description | ✅ |
| 5.2.3 | "Order this design" CTA per card → WhatsApp with design name pre-filled | ✅ |
| 5.2.4 | Custom inscription example callout (using horn-grape-name photo) | ✅ |
| 5.2.5 | Click photo to enlarge in lightbox | ✅ |

### 5.3 — Per-Category Pages
| ID | Page | Photos | Status |
|---|---|---|---|
| 5.3.1 | `candlesticks.html` — Candlesticks | 4 | ✅ live |
| 5.3.2 | `shofars-goblets.html` — Shofars & Goblets (design picker) | 12 (7 used) | ✅ live |
| 5.3.3 | `kiddush-cups.html` — Kiddush Cups | 0 | ⏳ Coming Soon page live |
| 5.3.4 | `trays-bowls.html` — Glass Trays & Bowls | 4 bowls, 0 trays | ✅ live (Trays band Coming Soon) |
| 5.3.5 | `business-gifts.html` — Business Gifts | 0 | ⏳ Coming Soon page live |
| 5.3.6 | `mezuzahs.html` — Mezuzahs | 0 | ⏳ Coming Soon page live |

### 5.4 — Polish
| ID | Task | Status |
|---|---|---|
| 5.4.1 | Mobile responsive — all 6 pages | ✅ |
| 5.4.2 | SEO meta per page — category-specific titles + descriptions + OG | ✅ |
| 5.4.3 | Translate all UI strings to Hebrew — all 6 pages + RTL | ✅ |
| 5.4.4 | Wire category pages from `shop.html` cards | ✅ |
| 5.4.5 | "Browse other collections" link row on each Coming Soon page | ✅ |

### 5.5 — When new photos arrive
*To activate a Coming Soon category page: upload photos to Cloudinary, replace the hero+about content with the standard photo grid (see `candlesticks.html` as template), update the `cat-card-placeholder` on `shop.html` with a real `<img>`, and remove the `Coming Soon` badge.*

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

| ID | Task | Effort |
|---|---|---|
| 11.1 | Set up Google Analytics 4 | S |
| 11.2 | Set up Google Search Console + submit sitemap | S |
| 11.3 | Wire Instagram + TikTok links (handles from M0-11) | XS |
| 11.4 | Create WhatsApp Business profile | S |
| 11.5 | Set up email newsletter list (Mailchimp free / Brevo) | M |
| 11.6 | Add newsletter signup bar to homepage | S |
| 11.7 | Add Pinterest share button to product cards | XS |
| 11.8 | Explore Etsy / Not on the High Street as parallel channel | 👤 Owner |

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
| Sprint 11 | M11 | Marketing & analytics | 🔜 |
| Sprint 12 | M12 | Stripe checkout | 🔜 |
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
