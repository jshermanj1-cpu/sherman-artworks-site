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

## MILESTONE 0 — Owner Inputs (must collect before dev work)
*These are not dev tasks — they block everything downstream.*

| ID | Task | Owner | Blocking | Status |
|---|---|---|---|---|
| M0-1 | Provide real WhatsApp number for `wa.me/972XXXXXXXXX` | Sherman | 🔴 M1, M2, M3 | 🔜 |
| M0-2 | Decide on domain name and register it | Sherman | 🔴 Launch | 🔜 |
| M0-3 | Create Stripe account (stripe.com) | Sherman | 🔴 M3 | 🔜 |
| M0-4 | Confirm prices for unlisted products (goblets, shofars, trays, Kiddush cups) | Sherman | 🟡 M4 | 🔜 |
| M0-5 | Confirm candlestick color variants (if any) | Sherman | 🟡 M4 | 🔜 |
| M0-6 | Identify a native Hebrew speaker to review all copy | Sherman | 🟡 Pre-launch | 🔜 |
| M0-7 | Decide: direct purchase, inquiry only, or both? | Sherman | 🔴 M3 | ✅ WhatsApp-first chosen |
| M0-8 | Choose hosting platform | Sherman | 🟡 Launch | ✅ GitHub Pages (repo live) |

---

## MILESTONE 1 — Fix It Before Anyone Sees It ✅ COMPLETE

### 1.1 — Mobile Responsiveness 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 1.1.1 | Fix product grid: `repeat(auto-fit, minmax(280px, 1fr))` | XS | ✅ |
| 1.1.2 | Fix hero layout: stacks vertically on mobile | S | ✅ |
| 1.1.3 | Fix story section layout: stacks vertically on mobile | S | ✅ |
| 1.1.4 | All buttons minimum 44px tall | XS | ✅ |
| 1.1.5 | Add hamburger menu for mobile nav | M | ✅ |
| 1.1.6 | Test on: iPhone SE (375px), iPhone 14 (390px), Android (360px) | S | 🔜 Manual QA needed |

### 1.2 — Dead Links & Broken CTAs 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 1.2.1 | "Custom Orders" nav link → `#contact` | XS | ✅ |
| 1.2.2 | "Explore Gallery" hero button → `#shop` | XS | ✅ |
| 1.2.3 | "Custom Orders" hero button → `#contact` | XS | ✅ |
| 1.2.4 | Footer nav links → scroll targets | XS | ✅ |

### 1.3 — Image Performance 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 1.3.1 | Confirm no base64 images | XS | ✅ Built clean from scratch |
| 1.3.2 | Set up Cloudinary free account | XS | ✅ Owner did this |
| 1.3.3 | Upload all 45 source photos to Cloudinary | S | ✅ Owner uploaded 105 images |
| 1.3.4 | Curate best 7 photos for current mapped image keys | M | ✅ Curated via interactive tool |
| 1.3.5 | Replace placeholder src values with Cloudinary URLs | S | ✅ All 8 slots + OG image |
| 1.3.6 | Add `loading="lazy"` to all non-hero images | XS | ✅ |
| 1.3.7 | Add `width` + `height` attributes to all `<img>` tags | XS | ✅ |

---

## MILESTONE 2 — Trust & Conversion Signals ⚠️ MOSTLY DONE

### 2.1 — Contact Section 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 2.1.1 | Design and build Contact section above footer | M | ✅ |
| 2.1.2 | Add WhatsApp button | XS | ⚠️ Built — needs real number (M0-1) |
| 2.1.3 | Add email link: `mailto:shermanartwork@gmail.com` | XS | ✅ |
| 2.1.4 | Add simple enquiry form via Formspree | S | ⚠️ Built — needs real Formspree ID |
| 2.1.5 | Wire nav "Contact" link to `#contact` | XS | ✅ |
| 2.1.6 | Add contact email to footer | XS | ✅ |
| 2.1.7 | Translate Contact section to Hebrew | S | ✅ |

### 2.2 — Custom Orders Flow 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 2.2.1 | Decide: Custom Orders form vs. WhatsApp-first flow | 👤 | ✅ WhatsApp-first chosen |
| 2.2.2 | Wire "Custom Orders" CTA to `wa.me/` with pre-filled message | XS | ⚠️ Done — needs real number (M0-1) |
| 2.2.3 | Build Custom Orders form | M | N/A — WhatsApp chosen |
| 2.2.4 | Add Custom Orders section to site | M | ✅ Folded into Contact section |

### 2.3 — Currency API Fallback Disclaimer 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 2.3.1 | Add `showFallbackDisclaimer()` function | XS | ✅ |
| 2.3.2 | Display "(estimated rate · may not be exact)" on fallback | XS | ✅ |

### 2.4 — SEO & Meta 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 2.4.1 | Verify title tag | XS | ✅ |
| 2.4.2 | Verify meta description | XS | ✅ |
| 2.4.3 | Add Open Graph tags | S | ✅ Including real product photo for og:image |
| 2.4.4 | Add `lang="en"` / `lang="he"` switching | XS | ✅ |
| 2.4.5 | Add favicon | XS | ✅ Inline SVG favicon |

---

## MILESTONE 3 — Checkout (Revenue-Enabling) 🔜

### 3.1 — Stripe Integration 🔴
| ID | Task | Effort | Status |
|---|---|---|---|
| 3.1.1 | Create Stripe account, verify identity | 👤 Owner | 🔜 |
| 3.1.2 | Create Stripe Payment Links for each product | S | 🔜 |
| 3.1.3 | Wire "Add to Cart" → Stripe Payment Link | XS | 🔜 Currently opens WhatsApp as interim |
| 3.1.4 | Test full purchase flow end-to-end | S | 🔜 |
| 3.1.5 | Add order confirmation email in Stripe dashboard | S | 🔜 |
| 3.1.6 | Switch Stripe from test to live mode | XS | 🔜 |

### 3.2 — Cart UX (V2)
| ID | Task | Effort | Status |
|---|---|---|---|
| 3.2.1 | Slide-out mini-cart panel | L | 🔜 V2 |
| 3.2.2 | Multi-item Stripe Cart session | L | 🔜 V2 |

---

## MILESTONE 4 — Full Catalogue & Gallery 🔜

### 4.1 — Additional Product Cards 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 4.1.1 | Add Kiddush Cup product card | M | 🔜 Needs price + images from owner |
| 4.1.2 | Add Glass Goblets product card | M | 🔜 |
| 4.1.3 | Add Decorative Tray product card | M | 🔜 |
| 4.1.4 | Add Silver-plated Shofar product card | M | 🔜 |
| 4.1.5 | Add color picker/swatch to Bowl card | M | 🔜 |
| 4.1.6 | Remove "Coming Soon" placeholder | XS | 🔜 Once real cards added |
| 4.1.7 | Expand photo curation to 25+ images | L | 🔜 105 photos in Cloudinary ready to use |

### 4.2 — Gallery Page 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 4.2.1 | Create `gallery.html` with masonry/grid layout | L | 🔜 |
| 4.2.2 | Add lightbox / full-screen image viewer | M | 🔜 |
| 4.2.3 | Filter by category | M | 🔜 |
| 4.2.4 | Wire nav "Gallery" link to `gallery.html` | XS | 🔜 Currently → #shop |
| 4.2.5 | Translate gallery page to Hebrew | S | 🔜 |

### 4.3 — Judaica Page 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 4.3.1 | Create `judaica.html` | M | 🔜 |
| 4.3.2 | Add Judaica-specific copy | S | 🔜 |
| 4.3.3 | Wire nav "Judaica" link | XS | 🔜 Currently → #shop |

---

## MILESTONE 5 — Brand Depth Pages 🔜

### 5.1 — About Page 🟢
| ID | Task | Effort | Status |
|---|---|---|---|
| 5.1.1 | Create `about.html` | L | 🔜 |
| 5.1.2 | Include studio/craft photos | S | 🔜 |
| 5.1.3 | Add "Meet the Family" section | M | 🔜 |
| 5.1.4 | Wire nav "About" link | XS | 🔜 Currently → #story |

### 5.2 — Trust Signals 🟡
| ID | Task | Effort | Status |
|---|---|---|---|
| 5.2.1 | Add Shipping & Returns policy | S | 🔜 |
| 5.2.2 | Add "Handcrafted in Israel" badge | XS | ✅ In footer |
| 5.2.3 | Add customer testimonials section | M | 🔜 |
| 5.2.4 | Mention gift packaging option | S | 🔜 |

---

## MILESTONE 6 — Hebrew Quality & Localisation 🔜

| ID | Task | Effort | Status |
|---|---|---|---|
| 6.1 | Full Hebrew copy review by native speaker | M | 🔜 👤 Human task |
| 6.2 | Review Judaica-specific Hebrew terminology | S | 🔜 👤 Human task |
| 6.3 | Test full RTL layout on real device | S | 🔜 |
| 6.4 | Verify Heebo font renders correctly in Hebrew | XS | 🔜 |
| 6.5 | Add `hreflang` meta tags | XS | 🔜 |

---

## MILESTONE 7 — Marketing & Distribution 🔜

| ID | Task | Effort | Status |
|---|---|---|---|
| 7.1 | Set up Google Analytics 4 | S | 🔜 |
| 7.2 | Set up Google Search Console + submit sitemap | S | 🔜 |
| 7.3 | Add Instagram feed embed or link | S | 🔜 |
| 7.4 | Create WhatsApp Business profile | S | 🔜 |
| 7.5 | Set up email list (Mailchimp / Brevo) | M | 🔜 |
| 7.6 | Add Pinterest share button to product cards | XS | 🔜 |
| 7.7 | Explore Etsy / Not on the High Street | 👤 Owner | 🔜 |

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 2/8 done |
| Sprint 1 | M1 | Fix mobile, dead links, images | ✅ Done (manual device QA pending) |
| Sprint 2 | M2 | Contact, Custom Orders, SEO | ✅ Done (WhatsApp # + Formspree ID needed) |
| Sprint 3 | M3 | Stripe checkout live | 🔜 Blocked on Stripe account |
| **→ SOFT LAUNCH** | — | Share link, gather feedback | 🔜 Ready once WhatsApp + Formspree wired |
| Sprint 4 | M4 | Full catalogue + Gallery page | 🔜 |
| Sprint 5 | M5 | About page, trust signals | 🔜 |
| Sprint 6 | M6 | Hebrew quality pass | 🔜 |
| Sprint 7 | M7 | Marketing & analytics | 🔜 |
| **→ FULL LAUNCH** | — | Marketing push | 🔜 |

---

*Last updated May 2026 after Sprint 1 + 2 completion.*
