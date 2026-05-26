# Sherman Art Works — Product Task List

> Last updated: May 2026 | PM: Claude | Owner: Sherman Family
> Active file: `sherman_artworks_v2.html`

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

## MILESTONE 0 — Owner Inputs (must collect before dev work)
*These are not dev tasks — they block everything downstream.*

| ID | Task | Owner | Blocking |
|---|---|---|---|
| M0-1 | Provide real WhatsApp number for `wa.me/972XXXXXXXXX` | Sherman | 🔴 M1, M2, M3 |
| M0-2 | Decide on domain name and register it | Sherman | 🔴 Launch |
| M0-3 | Create Stripe account (stripe.com) | Sherman | 🔴 M3 |
| M0-4 | Confirm prices for unlisted products (goblets, shofars, trays, Kiddush cups) | Sherman | 🟡 M4 |
| M0-5 | Confirm candlestick color variants (if any) | Sherman | 🟡 M4 |
| M0-6 | Identify a native Hebrew speaker to review all copy | Sherman | 🟡 Pre-launch |
| M0-7 | Decide: direct purchase, inquiry only, or both? | Sherman | 🔴 M3 |
| M0-8 | Choose hosting platform (GitHub Pages / Netlify / Vercel recommended) | Sherman | 🟡 Launch |

---

## MILESTONE 1 — Fix It Before Anyone Sees It
*These are bugs or broken experiences that would cause immediate bounce or distrust. Ship nothing publicly until M1 is done.*

### 1.1 — Mobile Responsiveness 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 1.1.1 | Fix product grid: replace `grid-template-columns: 1fr 1fr 1fr` with `repeat(auto-fit, minmax(280px, 1fr))` | XS | One CSS line change |
| 1.1.2 | Fix hero layout: stacks vertically on mobile (image below text) | S | CSS media query |
| 1.1.3 | Fix story section layout: stacks vertically on mobile | S | CSS media query |
| 1.1.4 | All buttons must be minimum 44px tall (iOS touch target requirement) | XS | CSS |
| 1.1.5 | Add hamburger menu for mobile nav (nav collapses to burger icon) | M | JS + CSS |
| 1.1.6 | Test on: iPhone SE (375px), iPhone 14 (390px), Android (360px) | S | Manual QA |

### 1.2 — Dead Links & Broken CTAs 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 1.2.1 | "Custom Orders" nav link → scroll to contact section (interim) | XS | `href="#contact"` |
| 1.2.2 | "Explore Gallery" hero button → scroll to shop section (interim) | XS | `href="#shop"` |
| 1.2.3 | "Custom Orders" hero button → scroll to contact section (interim) | XS | `href="#contact"` |
| 1.2.4 | Footer nav links → same interim scroll targets | XS | — |

### 1.3 — Image Performance 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 1.3.1 | Audit current HTML — confirm whether images are base64 or URLs | XS | View source |
| 1.3.2 | If base64: set up Cloudinary free account (cloudinary.com) | XS | Owner does this |
| 1.3.3 | Upload all 45 source photos to Cloudinary | S | Organize by product folder |
| 1.3.4 | Curate best 7 photos for current mapped image keys (see spec §9) | M | Judgment call on quality |
| 1.3.5 | Replace any base64 src values with Cloudinary URLs | S | — |
| 1.3.6 | Add `loading="lazy"` to all non-hero images | XS | Performance |
| 1.3.7 | Add `width` + `height` attributes to all `<img>` tags | XS | Prevents layout shift |

---

## MILESTONE 2 — Trust & Conversion Signals
*The site works, but won't convert without these. Ship before sharing any links publicly.*

### 2.1 — Contact Section 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 2.1.1 | Design and build Contact section above footer | M | EN + HE, email + WhatsApp |
| 2.1.2 | Add WhatsApp button: `wa.me/972XXXXXXXXX` (replace with real number) | XS | Opens WhatsApp chat |
| 2.1.3 | Add email link: `mailto:shermanartwork@gmail.com` | XS | — |
| 2.1.4 | Add simple enquiry form (name, email, message) via Formspree | S | Free tier, no backend |
| 2.1.5 | Wire nav "Contact" link to `#contact` section | XS | — |
| 2.1.6 | Add contact email to footer (currently missing) | XS | — |
| 2.1.7 | Translate Contact section to Hebrew | S | Native review required |

### 2.2 — Custom Orders Flow 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 2.2.1 | Decide: Custom Orders form vs. WhatsApp-first flow | 👤 Owner | S — form; XS — WhatsApp |
| 2.2.2 | If WhatsApp: wire "Custom Orders" CTA to `wa.me/` link with pre-filled message | XS | "Hi, I'm interested in a custom order" |
| 2.2.3 | If form: build Custom Orders form (product type, size, color, budget, message) | M | Formspree or similar |
| 2.2.4 | Add Custom Orders section to site (below Story, above Contact) | M | EN + HE |

### 2.3 — Currency API Fallback Disclaimer 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 2.3.1 | Add `showFallbackDisclaimer()` function | XS | Show "(estimated rate)" when API call fails |
| 2.3.2 | Display "(estimated rate · may not be exact)" in `#rateNote` on fallback | XS | — |

### 2.4 — SEO & Meta 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 2.4.1 | Verify title tag: "Sherman Art Works — Handmade Glass Judaica from Israel" | XS | Currently present, verify |
| 2.4.2 | Verify meta description (150 chars, includes: glass art, Judaica, Israel, handmade) | XS | — |
| 2.4.3 | Add Open Graph tags (og:title, og:description, og:image) for social sharing | S | Use best hero photo as og:image |
| 2.4.4 | Add `lang="en"` attribute (switches to `lang="he"` when Hebrew active) | XS | Accessibility + SEO |
| 2.4.5 | Add favicon | XS | Use logo mark |

---

## MILESTONE 3 — Checkout (Revenue-Enabling)
*Can soft-launch as inquiry-only without this, but real revenue requires it.*

### 3.1 — Stripe Integration 🔴
| ID | Task | Effort | Notes |
|---|---|---|---|
| 3.1.1 | Create Stripe account, verify identity (owner task) | 👤 Owner | Required before any dev |
| 3.1.2 | Create Stripe Payment Links for each product (no-code, hosted by Stripe) | S | Fastest path: no custom checkout code |
| 3.1.3 | Wire "Add to Cart" → Stripe Payment Link (new tab) | XS | Interim: no cart UI needed |
| 3.1.4 | Test full purchase flow end-to-end (test card: 4242 4242...) | S | Verify amount in ILS and USD |
| 3.1.5 | Add order confirmation email in Stripe dashboard | S | Customer-facing receipt |
| 3.1.6 | Go live: switch Stripe from test to live mode | XS | Requires owner approval |

> **Architecture note:** Use Stripe Payment Links (hosted checkout) for V1. Do NOT build a custom checkout — it adds weeks of work and PCI compliance burden. Payment Links take ~30 minutes to set up.

### 3.2 — Cart UX (optional V2 upgrade)
| ID | Task | Effort | Notes |
|---|---|---|---|
| 3.2.1 | Replace `addToCart()` alert with a slide-out mini-cart panel | L | V2 — not needed for launch |
| 3.2.2 | Multi-item checkout via Stripe Cart session | L | V2 |

---

## MILESTONE 4 — Full Catalogue & Gallery
*Expand beyond 2 products.*

### 4.1 — Additional Product Cards 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 4.1.1 | Add Kiddush Cup product card (price + images from owner) | M | High Judaica demand |
| 4.1.2 | Add Glass Goblets product card | M | — |
| 4.1.3 | Add Decorative Tray product card | M | — |
| 4.1.4 | Add Silver-plated Shofar product card | M | Seasonal/gift — high value |
| 4.1.5 | Add color picker / color swatch to Bowl card | M | Multiple colors available |
| 4.1.6 | Remove "Coming Soon" placeholder once real product cards are added | XS | — |
| 4.1.7 | Expand product photo curation from 7 → 25+ images across all products | L | Quality check required |

### 4.2 — Gallery Page 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 4.2.1 | Create `gallery.html` with masonry or grid photo layout | L | All curated product photos |
| 4.2.2 | Add lightbox / full-screen image viewer | M | CSS-only or lightweight JS |
| 4.2.3 | Filter by category (Bowls / Candlesticks / Judaica / All) | M | — |
| 4.2.4 | Wire nav "Gallery" link to `gallery.html` | XS | — |
| 4.2.5 | Translate gallery page to Hebrew | S | — |

### 4.3 — Judaica Page 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 4.3.1 | Create `judaica.html` — filtered view of Judaica-category products | M | Candlesticks, Kiddush cups, shofars |
| 4.3.2 | Add Judaica-specific copy (Shabbat, holidays, gift-giving angle) | S | EN + HE |
| 4.3.3 | Wire nav "Judaica" link to `judaica.html` | XS | — |

---

## MILESTONE 5 — Brand Depth Pages
*Builds long-term trust and SEO.*

### 5.1 — About Page 🟢
| ID | Task | Effort | Notes |
|---|---|---|---|
| 5.1.1 | Create `about.html` — full brand story, family history, craft process | L | EN + HE |
| 5.1.2 | Include studio/craft photos (select from 45-photo pool) | S | — |
| 5.1.3 | Add a "Meet the Family" section (with owner permission) | M | Humanises the brand |
| 5.1.4 | Wire nav "About" link to `about.html` | XS | — |

### 5.2 — Trust Signals 🟡
| ID | Task | Effort | Notes |
|---|---|---|---|
| 5.2.1 | Add Shipping & Returns policy section or page | S | Key for international buyers |
| 5.2.2 | Add "Handcrafted in Israel" badge/seal in footer or product cards | XS | Visual trust cue |
| 5.2.3 | Add customer testimonials section (if available) | M | Social proof |
| 5.2.4 | Add gift packaging / gift message option mention | S | High relevance for Judaica buyers |

---

## MILESTONE 6 — Hebrew Quality & Localisation
*Required before targeting Israeli-speaking audience seriously.*

| ID | Task | Effort | Notes |
|---|---|---|---|
| 6.1 | Full Hebrew copy review by native speaker | M | 👤 Human task — all `T.he` strings |
| 6.2 | Review all Judaica-specific terminology in Hebrew | S | Critical — wrong terms are embarrassing |
| 6.3 | Test full RTL layout on real device | S | iOS Safari + Android Chrome |
| 6.4 | Verify Heebo font renders correctly in Hebrew at all sizes | XS | — |
| 6.5 | Add `hreflang` meta tags for Hebrew/English SEO | XS | — |

---

## MILESTONE 7 — Marketing & Distribution
*Post-launch, drives traffic.*

| ID | Task | Effort | Notes |
|---|---|---|---|
| 7.1 | Set up Google Analytics 4 | S | Free, privacy-compliant |
| 7.2 | Set up Google Search Console + submit sitemap | S | SEO visibility |
| 7.3 | Add Instagram feed embed or link (if account exists) | S | Visual social proof |
| 7.4 | Create WhatsApp Business profile | S | More professional than personal number |
| 7.5 | Set up basic email list (Mailchimp free or Brevo) for launch announcement | M | 🟢 Optional |
| 7.6 | Add Pinterest share button to product cards | XS | High-intent channel for Judaica/decor |
| 7.7 | Explore Etsy / Not on the High Street as parallel channel | 👤 Owner | 🟢 Business decision |

---

## Sprint Summary

| Sprint | Milestone | Goal | Est. Effort |
|---|---|---|---|
| Sprint 0 | M0 | Collect all owner inputs | 1–2 days (owner) |
| Sprint 1 | M1 | Fix mobile, dead links, image hosting | 3–5 dev days |
| Sprint 2 | M2 | Contact section, Custom Orders, SEO | 3–4 dev days |
| Sprint 3 | M3 | Stripe checkout live | 1–2 dev days |
| **→ SOFT LAUNCH** | — | Share link, gather feedback | — |
| Sprint 4 | M4 | Full catalogue + Gallery page | 5–7 dev days |
| Sprint 5 | M5 | About page, trust signals | 3–4 dev days |
| Sprint 6 | M6 | Hebrew quality pass | 2–3 days (human + dev) |
| Sprint 7 | M7 | Marketing & analytics | 2–3 dev days |
| **→ FULL LAUNCH** | — | Marketing push | — |

---

## Effort Key

| Size | Time |
|---|---|
| XS | < 30 min |
| S | 30 min – 2 hrs |
| M | 2–5 hrs |
| L | 5–10 hrs |
| XL | 10+ hrs |

---

*Task list is a living document. Update status as tasks are completed. Re-prioritize after Sprint 0 inputs are received.*
