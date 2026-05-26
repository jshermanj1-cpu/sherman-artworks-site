# Sherman Art Works — Product Task List

> Last updated: May 2026 (Sprint 3 complete) | PM: Claude | Owner: Sherman Family
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
| M0-1 | Provide real WhatsApp number for `wa.me/972XXXXXXXXX` | Sherman | 🔴 Site-wide | 🔜 |
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

## MILESTONE 4 — Glass Page 🔜

*Rename "Gallery" → "Glass" throughout the site. Full photo showcase of all pieces.*

### 4.1 — Nav & Naming
| ID | Task | Effort |
|---|---|---|
| 4.1.1 | Rename nav link "Gallery" → "Glass" (EN) and "גלריה זכוכית" (HE) in translations | XS |
| 4.1.2 | Update all internal links pointing to gallery → `glass.html` | XS |

### 4.2 — Page Build
| ID | Task | Effort |
|---|---|---|
| 4.2.1 | Create `glass.html` with shared header/footer matching homepage | M |
| 4.2.2 | Uniform photo grid — all 105 Cloudinary photos, curated best ~40 | L |
| 4.2.3 | Category filter tabs: All · Bowls · Candlesticks · Judaica · Decorative | M |
| 4.2.4 | Lightbox — click any photo to open full-screen with prev/next | M |
| 4.2.5 | Each photo card: image + category tag + optional caption | S |
| 4.2.6 | "Enquire about this piece" CTA per photo → WhatsApp with photo name pre-filled | S |

### 4.3 — Polish
| ID | Task | Effort |
|---|---|---|
| 4.3.1 | Mobile responsive grid (2-col on tablet, 1-col on small mobile) | S |
| 4.3.2 | SEO meta: title, description, OG image for glass page | XS |
| 4.3.3 | Translate all UI strings to Hebrew | S |

---

## MILESTONE 5 — Judaica Page 🔜

*Filtered collection page for Judaica buyers — Shabbat, holidays, gifting angle.*

### 5.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 5.1.1 | Create `judaica.html` with shared header/footer | M |
| 5.1.2 | Hero section: Judaica-specific headline + copy (Shabbat, holidays, meaningful gifts) | S |
| 5.1.3 | Product grid showing Judaica items: candlesticks, Kiddush cups, shofars | M |
| 5.1.4 | "Gift for every occasion" section — Shabbat, bar/bat mitzvah, holidays, home | S |
| 5.1.5 | WhatsApp CTA: "Looking for a specific Judaica piece? Ask us." | XS |

### 5.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 5.2.1 | Mobile responsive | S |
| 5.2.2 | SEO meta — target "handmade Judaica Israel", "glass Kiddush cup" keywords | S |
| 5.2.3 | Translate to Hebrew | S |
| 5.2.4 | Wire nav "Judaica" link to `judaica.html` | XS |

---

## MILESTONE 6 — Custom Orders Page 🔜

*Dedicated page for bespoke commissions — makes the custom offer feel premium.*

### 6.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 6.1.1 | Create `custom-orders.html` with shared header/footer | M |
| 6.1.2 | Hero: "Commission a One-of-a-Kind Piece" — headline + brand copy | S |
| 6.1.3 | How It Works section — 3–4 steps (enquire → design → craft → deliver) | M |
| 6.1.4 | What can be customised: size, color, shape, inscription, gift packaging | S |
| 6.1.5 | Primary CTA: WhatsApp button with pre-filled "I'd like to commission a piece" | XS |
| 6.1.6 | Custom order enquiry form: product type, size, color preference, budget, deadline, message | M |
| 6.1.7 | Timeline/expectations copy: typical lead time, what happens next | S |
| 6.1.8 | Gallery of past custom pieces (pull from Cloudinary) | M |

### 6.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 6.2.1 | Mobile responsive | S |
| 6.2.2 | SEO meta — "custom glass art Israel", "bespoke Judaica gift" | S |
| 6.2.3 | Translate to Hebrew | S |
| 6.2.4 | Wire nav "Custom Orders" link to `custom-orders.html` | XS |

---

## MILESTONE 7 — About Page 🔜

*Builds brand trust and emotional connection — critical for premium pricing.*

### 7.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 7.1.1 | Create `about.html` with shared header/footer | M |
| 7.1.2 | Hero: studio/workshop photo + "The Sherman Family" headline | S |
| 7.1.3 | Full brand story: family history, how it started, generations of craft | M |
| 7.1.4 | Our Craft section: glass-blowing process, techniques, what makes each piece unique | M |
| 7.1.5 | Meet the Family section: names, roles, photo (with owner permission) | M |
| 7.1.6 | Studio photos gallery — 6–8 behind-the-scenes images from Cloudinary | S |
| 7.1.7 | "Made in Israel" values section: heritage, pride, craftsmanship | S |
| 7.1.8 | CTA at bottom → "Explore the Collection" + "Get in Touch" | XS |

### 7.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 7.2.1 | Mobile responsive | S |
| 7.2.2 | SEO meta — "handmade glass art Israel family studio" | S |
| 7.2.3 | Translate to Hebrew | S |
| 7.2.4 | Wire nav "About" link to `about.html` | XS |

---

## MILESTONE 8 — Contact Page 🔜

*Standalone contact page — more detailed than the homepage section.*

### 8.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 8.1.1 | Create `contact.html` with shared header/footer | M |
| 8.1.2 | Hero: "We'd love to hear from you" — warm, personal copy | S |
| 8.1.3 | WhatsApp button (primary) + Email button | XS |
| 8.1.4 | Full enquiry form: name, email, subject (dropdown: order / custom / general), message | S |
| 8.1.5 | FAQ section: shipping times, custom order lead time, returns, payment methods | M |
| 8.1.6 | "Based in Israel, shipping worldwide" trust line + free shipping reminder | XS |

### 8.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 8.2.1 | Mobile responsive | S |
| 8.2.2 | SEO meta | XS |
| 8.2.3 | Translate to Hebrew | S |
| 8.2.4 | Wire nav "Contact" link to `contact.html` (currently → #contact section) | XS |

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
| **→ SOFT LAUNCH** | — | Wire real WhatsApp number, enable custom domain | 🔜 1 input away (M0-1) |
| Sprint 3 | M3 | Homepage enhancements (announcement bar, best sellers, corporate CTA, Instagram) | ✅ Done (3.3 + 3.5 deferred) |
| **→ Sprint 4** | M4 | Glass page | 🔜 **CURRENT** |
| Sprint 5 | M5 | Judaica page | 🔜 |
| Sprint 6 | M6 | Custom Orders page | 🔜 |
| Sprint 7 | M7 | About page | 🔜 |
| Sprint 8 | M8 | Contact page | 🔜 |
| Sprint 9 | M9 | Full product catalogue | 🔜 |
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
