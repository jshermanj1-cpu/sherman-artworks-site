# Sherman Art Works — Product Task List

> Last updated: May 2026 | PM: Claude | Owner: Sherman Family
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
| M0-2 | Decide on domain name and register it | Sherman | 🔴 Launch | 🔜 |
| M0-3 | Create Stripe account (stripe.com) | Sherman | 🔴 M10 | 🔜 |
| M0-4 | Confirm prices for unlisted products (goblets, shofars, trays, Kiddush cups) | Sherman | 🟡 M8 | 🔜 |
| M0-5 | Confirm candlestick color variants (if any) | Sherman | 🟡 M8 | 🔜 |
| M0-6 | Identify a native Hebrew speaker to review all copy | Sherman | 🟡 M9 | 🔜 |
| M0-7 | Decide: direct purchase, inquiry only, or both? | Sherman | — | ✅ WhatsApp-first chosen |
| M0-8 | Choose hosting platform | Sherman | — | ✅ GitHub Pages |
| M0-9 | Provide Formspree account ID for contact form | Sherman | 🟡 M2 | 🔜 |

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
| 2.1.4 | Enquiry form via Formspree | ⚠️ Built — needs Formspree ID (M0-9) |
| 2.1.5–7 | Nav wired, email in footer, Hebrew translation | ✅ |

### 2.2 — Custom Orders Flow
| ID | Task | Status |
|---|---|---|
| 2.2.1 | WhatsApp-first flow chosen | ✅ |
| 2.2.2 | "Custom Orders" CTA → WhatsApp with pre-filled message | ⚠️ Done — needs real number |

### 2.3 — Currency
| ID | Task | Status |
|---|---|---|
| 2.3.1–2 | Fallback disclaimer (`showFallbackDisclaimer`) | ✅ |

### 2.4 — SEO & Meta
| ID | Task | Status |
|---|---|---|
| 2.4.1–5 | Title, meta description, OG tags, lang attr, favicon | ✅ |

---

## MILESTONE 3 — Glass Page 🔜

*Rename "Gallery" → "Glass" throughout the site. Full photo showcase of all pieces.*

### 3.1 — Nav & Naming
| ID | Task | Effort |
|---|---|---|
| 3.1.1 | Rename nav link "Gallery" → "Glass" (EN) and "גלריה זכוכית" (HE) in translations | XS |
| 3.1.2 | Update all internal links pointing to gallery → `glass.html` | XS |

### 3.2 — Page Build
| ID | Task | Effort |
|---|---|---|
| 3.2.1 | Create `glass.html` with shared header/footer matching homepage | M |
| 3.2.2 | Uniform photo grid — all 105 Cloudinary photos, curated best ~40 | L |
| 3.2.3 | Category filter tabs: All · Bowls · Candlesticks · Judaica · Decorative | M |
| 3.2.4 | Lightbox — click any photo to open full-screen with prev/next | M |
| 3.2.5 | Each photo card: image + category tag + optional caption | S |
| 3.2.6 | "Enquire about this piece" CTA per photo → WhatsApp with photo name pre-filled | S |

### 3.3 — Polish
| ID | Task | Effort |
|---|---|---|
| 3.3.1 | Mobile responsive grid (2-col on tablet, 1-col on small mobile) | S |
| 3.3.2 | SEO meta: title, description, OG image for glass page | XS |
| 3.3.3 | Translate all UI strings to Hebrew | S |

---

## MILESTONE 4 — Judaica Page 🔜

*Filtered collection page for Judaica buyers — Shabbat, holidays, gifting angle.*

### 4.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 4.1.1 | Create `judaica.html` with shared header/footer | M |
| 4.1.2 | Hero section: Judaica-specific headline + copy (Shabbat, holidays, meaningful gifts) | S |
| 4.1.3 | Product grid showing Judaica items: candlesticks, Kiddush cups, shofars | M |
| 4.1.4 | "Gift for every occasion" section — Shabbat, bar/bat mitzvah, holidays, home | S |
| 4.1.5 | WhatsApp CTA: "Looking for a specific Judaica piece? Ask us." | XS |

### 4.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 4.2.1 | Mobile responsive | S |
| 4.2.2 | SEO meta — target "handmade Judaica Israel", "glass Kiddush cup" keywords | S |
| 4.2.3 | Translate to Hebrew | S |
| 4.2.4 | Wire nav "Judaica" link to `judaica.html` | XS |

---

## MILESTONE 5 — Custom Orders Page 🔜

*Dedicated page for bespoke commissions — makes the custom offer feel premium.*

### 5.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 5.1.1 | Create `custom-orders.html` with shared header/footer | M |
| 5.1.2 | Hero: "Commission a One-of-a-Kind Piece" — headline + brand copy | S |
| 5.1.3 | How It Works section — 3–4 steps (enquire → design → craft → deliver) | M |
| 5.1.4 | What can be customised: size, color, shape, inscription, gift packaging | S |
| 5.1.5 | Primary CTA: WhatsApp button with pre-filled "I'd like to commission a piece" | XS |
| 5.1.6 | Custom order enquiry form: product type, size, color preference, budget, deadline, message | M |
| 5.1.7 | Timeline/expectations copy: typical lead time, what happens next | S |
| 5.1.8 | Gallery of past custom pieces (pull from Cloudinary) | M |

### 5.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 5.2.1 | Mobile responsive | S |
| 5.2.2 | SEO meta — "custom glass art Israel", "bespoke Judaica gift" | S |
| 5.2.3 | Translate to Hebrew | S |
| 5.2.4 | Wire nav "Custom Orders" link to `custom-orders.html` | XS |

---

## MILESTONE 6 — About Page 🔜

*Builds brand trust and emotional connection — critical for premium pricing.*

### 6.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 6.1.1 | Create `about.html` with shared header/footer | M |
| 6.1.2 | Hero: studio/workshop photo + "The Sherman Family" headline | S |
| 6.1.3 | Full brand story: family history, how it started, generations of craft | M |
| 6.1.4 | Our Craft section: glass-blowing process, techniques, what makes each piece unique | M |
| 6.1.5 | Meet the Family section: names, roles, photo (with owner permission) | M |
| 6.1.6 | Studio photos gallery — 6–8 behind-the-scenes images from Cloudinary | S |
| 6.1.7 | "Made in Israel" values section: heritage, pride, craftsmanship | S |
| 6.1.8 | CTA at bottom → "Explore the Collection" + "Get in Touch" | XS |

### 6.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 6.2.1 | Mobile responsive | S |
| 6.2.2 | SEO meta — "handmade glass art Israel family studio" | S |
| 6.2.3 | Translate to Hebrew | S |
| 6.2.4 | Wire nav "About" link to `about.html` | XS |

---

## MILESTONE 7 — Contact Page 🔜

*Standalone contact page — more detailed than the homepage section.*

### 7.1 — Page Build
| ID | Task | Effort |
|---|---|---|
| 7.1.1 | Create `contact.html` with shared header/footer | M |
| 7.1.2 | Hero: "We'd love to hear from you" — warm, personal copy | S |
| 7.1.3 | WhatsApp button (primary) + Email button | XS |
| 7.1.4 | Full enquiry form: name, email, subject (dropdown: order / custom / general), message | S |
| 7.1.5 | FAQ section: shipping times, custom order lead time, returns, payment methods | M |
| 7.1.6 | "Based in Israel, shipping worldwide" trust line + free shipping reminder | XS |

### 7.2 — Polish
| ID | Task | Effort |
|---|---|---|
| 7.2.1 | Mobile responsive | S |
| 7.2.2 | SEO meta | XS |
| 7.2.3 | Translate to Hebrew | S |
| 7.2.4 | Wire nav "Contact" link to `contact.html` (currently → #contact section) | XS |

---

## MILESTONE 8 — Full Product Catalogue 🔜

### 8.1 — Additional Product Cards 🟡
| ID | Task | Effort |
|---|---|---|
| 8.1.1 | Add Kiddush Cup product card (price + images from owner) | M |
| 8.1.2 | Add Glass Goblets product card | M |
| 8.1.3 | Add Decorative Tray product card | M |
| 8.1.4 | Add Silver-plated Shofar product card | M |
| 8.1.5 | Add color picker/swatch to Bowl card | M |
| 8.1.6 | Remove "Coming Soon" placeholder | XS |
| 8.1.7 | Expand photo curation to 25+ images across all products | L |

---

## MILESTONE 9 — Hebrew Quality & Localisation 🔜

| ID | Task | Effort |
|---|---|---|
| 9.1 | Full Hebrew copy review by native speaker — all pages | M |
| 9.2 | Review Judaica-specific Hebrew terminology | S |
| 9.3 | Test full RTL layout on real device (iOS Safari + Android Chrome) | S |
| 9.4 | Verify Heebo font renders correctly in Hebrew at all sizes | XS |
| 9.5 | Add `hreflang` meta tags for Hebrew/English SEO | XS |

---

## MILESTONE 10 — Marketing & Distribution 🔜

| ID | Task | Effort |
|---|---|---|
| 10.1 | Set up Google Analytics 4 | S |
| 10.2 | Set up Google Search Console + submit sitemap | S |
| 10.3 | Add Instagram feed embed or link | S |
| 10.4 | Create WhatsApp Business profile | S |
| 10.5 | Set up email list (Mailchimp free / Brevo) | M |
| 10.6 | Add Pinterest share button to product cards | XS |
| 10.7 | Explore Etsy / Not on the High Street as parallel channel | 👤 Owner |

---

## MILESTONE 11 — Stripe Checkout (Revenue) 🔜

*Can soft-launch without this using WhatsApp as the purchase path.*

### 11.1 — Stripe Integration
| ID | Task | Effort |
|---|---|---|
| 11.1.1 | Create Stripe account, verify identity | 👤 Owner |
| 11.1.2 | Create Stripe Payment Links for each product | S |
| 11.1.3 | Replace "Add to Cart" WhatsApp fallback → Stripe Payment Link | XS |
| 11.1.4 | Test full purchase flow end-to-end (test card: 4242 4242...) | S |
| 11.1.5 | Add order confirmation email in Stripe dashboard | S |
| 11.1.6 | Switch Stripe from test to live mode | XS |

### 11.2 — Cart UX (V2 after launch)
| ID | Task | Effort |
|---|---|---|
| 11.2.1 | Slide-out mini-cart panel | L |
| 11.2.2 | Multi-item Stripe Cart session | L |

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 3/9 done |
| Sprint 1 | M1 | Foundation: mobile, links, images | ✅ Done |
| Sprint 2 | M2 | Trust: contact, SEO, currency | ✅ Done |
| **→ SOFT LAUNCH** | — | Wire WhatsApp + Formspree, enable GitHub Pages | 🔜 2 inputs away |
| Sprint 3 | M3 | Glass page | 🔜 |
| Sprint 4 | M4 | Judaica page | 🔜 |
| Sprint 5 | M5 | Custom Orders page | 🔜 |
| Sprint 6 | M6 | About page | 🔜 |
| Sprint 7 | M7 | Contact page | 🔜 |
| Sprint 8 | M8 | Full product catalogue | 🔜 |
| Sprint 9 | M9 | Hebrew quality pass | 🔜 |
| Sprint 10 | M10 | Marketing & analytics | 🔜 |
| Sprint 11 | M11 | Stripe checkout | 🔜 |
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
