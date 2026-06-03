# Sherman Art Works — Product Task List

> Last updated: June 2026 (Sprint 14 complete — UI/UX overhaul, Shop dropdown, inline photo carousel, cross-category products, Kiddush Cups upgraded) | PM: Claude | Owner: Sherman Family
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
| M0-1 | Provide real WhatsApp number for `wa.me/972XXXXXXXXX` | Sherman | 🔴 Site-wide | ⚠️ Temp number +972523482278 active — replace with official business number |
| M0-2 | Decide on domain name and register it | Sherman | 🔴 Launch | ✅ shermanartworks.com |
| M0-3 | Create Stripe account (stripe.com) | Sherman | 🔴 M12 | 🔜 |
| M0-4 | Confirm prices for unlisted products | Sherman | 🟡 M9 | ⚠️ Done: candlesticks ₪775, shofar ₪850, goblets ₪473, bowl ₪1,190. Missing: dedicated kiddush cups, mezuzahs, business gifts |
| M0-5 | Confirm candlestick color variants (if any) | Sherman | 🟡 M9 | 🔜 |
| M0-6 | Identify a native Hebrew speaker to review all copy | Sherman | 🟡 M10 | 🔜 |
| M0-7 | Decide: direct purchase, inquiry only, or both? | Sherman | — | ✅ WhatsApp-first chosen |
| M0-8 | Choose hosting platform | Sherman | — | ✅ GitHub Pages (gh-pages branch + .nojekyll) |
| M0-9 | Contact form backend | Sherman | — | ✅ Replaced with WhatsApp + mailto (no backend needed) |
| M0-10 | Confirm free shipping threshold (for announcement bar) | Sherman | 🟡 M3 | ✅ Free on all orders |
| M0-11 | Confirm Instagram + TikTok handles | Sherman | 🟡 M3 | ⚠️ Instagram ✅ shermanartworks. TikTok handle still missing. |

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
| 1.1.6 | Test on iPhone SE (375px), iPhone 14 (390px), Android (360px) | 🔜 Manual QA on real device |

### 1.2 — Dead Links & CTAs
| ID | Task | Status |
|---|---|---|
| 1.2.1–4 | All nav, hero, footer CTAs wired correctly | ✅ |

### 1.3 — Image Performance
| ID | Task | Status |
|---|---|---|
| 1.3.1–8 | Cloudinary CDN, lazy loading, width/height attrs, c_fit | ✅ |

---

## MILESTONE 2 — Trust & Conversion ✅ COMPLETE

| ID | Task | Status |
|---|---|---|
| 2.1–2.4 | Contact section, WhatsApp flow, live currency, SEO meta | ✅ (WA number needs real number — M0-1) |

---

## MILESTONE 3 — Homepage Enhancements ✅ COMPLETE

| ID | Task | Status |
|---|---|---|
| 3.1–3.8 | Announcement bar, free shipping, best sellers, founder story, corporate CTA, Instagram footer | ✅ |
| 3.3 | "Shop by Occasion" / "Shop by Price" | 🔜 Deferred |
| 3.5 | Personalisation badge on product cards | 🔜 Deferred |
| 3.8.2 | TikTok footer link | 🔜 Blocked on M0-11 |

---

## MILESTONE 4 — Shop Section (homepage) ✅ COMPLETE

**Current categories (6):**
1. Candlesticks ✅ live with products
2. Shofars & Goblets ✅ live with products
3. Kiddush Cups ✅ live — shows goblets as cross-category products; dedicated designs coming soon
4. Trays & Bowls ✅ live with products
5. Business Gifts ⏳ Coming Soon
6. Mezuzahs ⏳ Coming Soon

| ID | Task | Status |
|---|---|---|
| 4.1–4.3 | Category grid, Coming Soon placeholders, nav, Hebrew, hero CTA | ✅ |
| NEW | Shop nav item → dropdown with all 6 categories (desktop + mobile) | ✅ Sprint 14 |
| NEW | Category cards: SVG icons instead of emoji on Coming Soon items | ✅ Sprint 14 |

---

## MILESTONE 5 — Category Pages ⚠️ PARTIAL (4 of 6 live, 2 Coming Soon)

*Product cards with photo carousel, price, measurements, View Details modal, Order on WhatsApp.*

### 5.1 — Product Card System ✅
| ID | Task | Status |
|---|---|---|
| 5.1.1–5.1.12 | All card + modal + currency features | ✅ |
| NEW 5.1.13 | Inline photo carousel on card (prev/next arrows + dots, no modal needed) | ✅ Sprint 14 |
| NEW 5.1.14 | Cross-category products — same product appears in multiple categories | ✅ Sprint 14 (goblets → kiddush-cups) |

### 5.2 — Per-Category Product Catalogue
| ID | Page | Products | Status |
|---|---|---|---|
| 5.2.1 | `candlesticks.html` | Glass Circle Candlesticks (4 photos, ₪775) | ✅ live |
| 5.2.2 | `shofars-goblets.html` | Jerusalem Wine Horn (5 photos, ₪850), Lion of Judah Goblet (4 photos, ₪473), Menorah Goblet (3 photos, ₪473) | ✅ live |
| 5.2.3 | `kiddush-cups.html` | Lion of Judah Goblet + Menorah Goblet (cross-listed from shofars) + "more coming soon" | ✅ live |
| 5.2.4 | `trays-bowls.html` | Glass Decorative Bowl (4 photos, ₪1,190) | ✅ live |
| 5.2.5 | `business-gifts.html` | 0 — Coming Soon stub | ⏳ |
| 5.2.6 | `mezuzahs.html` | 0 — Coming Soon stub | ⏳ |

### 5.3 — Polish ✅
| ID | Task | Status |
|---|---|---|
| 5.3.1–5.3.6 | Mobile, SEO, Hebrew, nav wiring, coming-soon rows, floating WA | ✅ |

### 5.4 — Product Builder Tool ✅
| ID | Task | Status |
|---|---|---|
| 5.4.1–5.4.2 | `/product-builder.html` — photo grouping, JSON export, localStorage | ✅ |

### 5.5 — When new photos arrive
*To add new products or activate a Coming Soon category:*
1. Upload photos to Cloudinary
2. Open `/product-builder.html`, group photos, fill in name/desc/measurements/price, generate JSON
3. Paste JSON to dev; dev updates the `PRODUCTS` array in the relevant `*.html` file
4. For a previously-Coming-Soon category: replace the `cat-card-placeholder` on `index.html#shop` with a real `<img>` and remove the Coming Soon badge

---

## MILESTONE 6 — Custom Orders Page ✅ COMPLETE

| ID | Task | Status |
|---|---|---|
| 6.1–6.2 | Custom orders page, WhatsApp form, how-it-works, mobile, Hebrew | ✅ |
| 6.1.8 | Gallery of past custom pieces | 🔜 Waiting on new photos |

---

## MILESTONE 7 — About Page ✅ COMPLETE

| ID | Task | Status |
|---|---|---|
| 7.1–7.2 | About page, 3-generations story, values, mobile, Hebrew | ✅ |
| 7.1.8 | Studio/family photos | 🔜 New photos pending |

---

## MILESTONE 8 — Contact Page ✅ COMPLETE

| ID | Task | Status |
|---|---|---|
| 8.1–8.2 | Contact page, WhatsApp/email/Instagram cards, FAQ accordion, mobile, Hebrew | ✅ |

---

## MILESTONE 9 — Full Product Catalogue 🔜
*Blocked on owner providing new photos.*

### 9.1 — Remaining Products 🟡
| ID | Task | Notes |
|---|---|---|
| 9.1.1 | Add dedicated Kiddush Cup photos + product cards | Owner photographs → uses product-builder.html |
| 9.1.2 | Add Decorative Tray product card (separate from bowl) | Owner photographs → product-builder |
| 9.1.3 | Add Business Gift product cards | Owner photographs → product-builder |
| 9.1.4 | Add Mezuzah product cards | Owner photographs → product-builder |
| 9.1.5 | Replace Coming Soon placeholder on Business Gifts + Mezuzahs category cards (index.html) | Once photos exist |
| 9.1.6 | Expand photo count — more angles per product | Improves conversion |

---

## MILESTONE 10 — Hebrew Quality & Localisation 🔜

| ID | Task | Effort |
|---|---|---|
| 10.1 | Full Hebrew copy review by native speaker — all pages | M · 👤 Blocked M0-6 |
| 10.2 | Review Judaica-specific Hebrew terminology | S |
| 10.3 | Test full RTL layout on real device (iOS Safari + Android Chrome) | S |
| 10.4 | Verify Frank Ruhl Libre + Heebo renders correctly in Hebrew | XS |
| 10.5 | Add `hreflang` meta tags for Hebrew/English SEO | XS |

---

## MILESTONE 11 — Marketing & Distribution 🔜

*Three tiers. Do Tier 1 before any marketing push — without it you can't measure anything.*

### 11.1 — Tier 1: Foundational (install first, all free)

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.1.1 | Google Analytics 4 (GA4) | Create property at analytics.google.com. Send `G-XXXXXXX` Measurement ID to dev. | Inject snippet into all 10 pages | S |
| 11.1.2 | Google Search Console + sitemap.xml | Verify ownership of shermanartworks.com. Submit sitemap. | Generate sitemap.xml + robots.txt (see M13.2.2–3) | S |
| 11.1.3 | WhatsApp Business profile | Install WA Business app, configure logo/hours/away message. Pair with M0-1 number swap. | None | S · 👤 |

### 11.2 — Tier 2: Growth Channels

| ID | Task | Owner action | Dev action | Effort |
|---|---|---|---|---|
| 11.2.1 | Wire TikTok in footer | Provide TikTok handle (M0-11) | Add TikTok social icon to footer site-wide | XS |
| 11.2.2 | Email newsletter service | Sign up Brevo / Mailchimp / Buttondown | Wire embed | S |
| 11.2.3 | Newsletter signup bar on homepage | Approve copy | Build inline form + connect to provider | M |
| 11.2.4 | Pinterest "Pin It" on product cards | Confirm desired | Add pinit.js to product cards | XS |

### 11.3 — Tier 3: Strategic

| ID | Task | Notes |
|---|---|---|
| 11.3.1 | Etsy / Not on the High Street as parallel sales channel | 10-12% fees but built-in traffic; owner decision |

---

## MILESTONE 12 — Stripe Checkout (Revenue) 🔜

*Can soft-launch without Stripe — WhatsApp is the purchase path today.*

| ID | Task | Effort |
|---|---|---|
| 12.1.1 | Create + verify Stripe account | 👤 Owner |
| 12.1.2 | Create Stripe Payment Links per product | S |
| 12.1.3 | Wire Payment Links into product cards | S |
| 12.1.4–6 | Test + go live | S |

---

## MILESTONE 13 — Bug Bash & Security Review ⚠️ IN PROGRESS

*Full audit run June 2026. Most issues resolved in Sprint 14. Outstanding items below.*

### 13.1 — 🔴 Blockers

| ID | Task | Status |
|---|---|---|
| 13.1.1 | Rotate GitHub PAT (`ghp_pDwEnvm…` exposed in chat — NOT in git history) | 🔜 👤 Owner: revoke at github.com/settings/tokens |
| 13.1.2 | Replace temp WA number `+972523482278` (20× across pages) | 🔜 Covered by M0-1 |

### 13.2 — 🟡 Important

| ID | Task | Status |
|---|---|---|
| 13.2.1 | Diversify OG images — 5 pages share the same bowl photo | 🔜 👤 Owner picks photos |
| 13.2.2 | Add `sitemap.xml` listing all 10 customer URLs | 🔜 Dev: ~15 min |
| 13.2.3 | Add `robots.txt` (points to sitemap, blocks product-builder.html) | 🔜 Dev: ~15 min |
| 13.2.4 | Add `aria-label` fallbacks on JS-populated nav links | 🔜 Dev: single Python sweep |

### 13.3 — 🟢 Polish

| ID | Task | Status |
|---|---|---|
| 13.3.1 | Remove unused `bestseller_badge` key from index.html translations | 🔜 XS |
| 13.3.2 | Delete orphan `glass-curate.html` | 🔜 XS |
| 13.3.3 | Block `product-builder.html` via robots.txt | Covered by 13.2.3 |
| 13.3.4 | Security headers (HSTS, CSP) | 🔜 GitHub Pages limitation — needs Cloudflare proxy |

### 13.4 — ✅ Resolved in Sprint 14

| Item | Fix |
|---|---|
| Emoji structural icons (🍷🎁✡) | Replaced with custom SVG line drawings |
| WCAG AA contrast failures | `--brown` darkened #8a6f40→#6a5530; footer text tokens upgraded |
| Competing dual hero CTAs | Secondary demoted to `.btn-link` text style |
| 24+ font-size values | `--fs-*` scale tokens defined |
| Italic Cormorant on small brown text | Limited to hero subtitle only |
| Hebrew system font fallback | Frank Ruhl Libre (headlines) + Heebo (body) added |
| Letter-spacing 0.28em on tiny labels | Reduced to 0.18em site-wide |
| Text `→` arrow in cat cards | Replaced with inline SVG, RTL-aware |
| Stale brown hex in placeholder gradient | Updated to use `--dark` token |
| Duplicate ornament on Coming Soon pages | Removed second `✦ ✦ ✦` |

---

## MILESTONE 14 — UI/UX Overhaul ✅ COMPLETE (Sprint 14)

*Applied ui-ux-pro-max skill audit findings across all 10 pages.*

| ID | Task | Status |
|---|---|---|
| 14.1 | Install ui-ux-pro-max skill globally | ✅ `C:\Users\User\.claude\skills\` |
| 14.2 | Typography: Cinzel→Fraunces, Arial→Inter, Hebrew: Frank Ruhl Libre + Heebo | ✅ |
| 14.3 | Contrast: `--brown` upgraded to AA-compliant #6a5530; footer text token | ✅ |
| 14.4 | SVG icons replace emoji on all Coming Soon placeholders | ✅ |
| 14.5 | Hero CTA hierarchy: single primary; secondary demoted to text link | ✅ |
| 14.6 | Shop nav → dropdown with all 6 categories, desktop + mobile | ✅ |
| 14.7 | Inline photo carousel on product cards (arrows + dots, no modal needed) | ✅ |
| 14.8 | Cross-category products: goblets appear in both Shofars & Goblets and Kiddush Cups | ✅ |
| 14.9 | Kiddush Cups upgraded from Coming Soon stub to live product page | ✅ |
| 14.10 | `context.md` created — full onboarding doc for new chat sessions | ✅ |

---

## MISSING / NOT YET TRACKED — Important gaps

### 🔴 Should do before launch

| ID | Task | Why |
|---|---|---|
| NEW-1 | **Replace temp WhatsApp number** (M0-1 / 13.1.2) | Every single enquiry and order goes to the wrong number |
| NEW-2 | **Custom branded 404 page** (`404.html`) | GitHub Pages shows a generic GitHub 404 if someone hits a bad URL — hurts credibility |
| NEW-3 | **Favicon upgrade** — currently a JPEG photo thumbnail | Should be a proper square icon (the logo mark cropped square) for tabs + bookmarks |

### 🟡 Should do soon

| ID | Task | Why |
|---|---|---|
| NEW-4 | **"From ₪X" price on homepage category cards** | Visitors can't see price range before clicking through — one of the top conversion improvements for e-commerce |
| NEW-5 | **Real device QA** (iPhone + Android) — 1.1.6 | The mobile layout has never been tested on a physical device; the hamburger, carousels, and modals especially need checking |
| NEW-6 | **Performance audit (Lighthouse)** | Category pages load 4–5 Cloudinary images; no audit has been done for Core Web Vitals or LCP |
| NEW-7 | **"Also in Shofars & Goblets" cross-link** on kiddush-cups goblet cards | Visitors don't know these items also live in the Shofars & Goblets section — a small note or tag would help |

### 🟢 Nice to have

| ID | Task | Why |
|---|---|---|
| NEW-8 | **Proper favicon SVG** — extract logo mark as SVG for `<link rel="icon" type="image/svg+xml">` | Crisper at all sizes, especially on retina displays |
| NEW-9 | **"Share this" / copy link** on product cards | Useful for gift buyers — they want to send a link to the product |
| NEW-10 | **WhatsApp pre-order message includes photo link** | Currently the WA message just says the product name; including a Cloudinary link to the main photo helps the owner see what the customer is interested in |
| NEW-11 | **Scroll-to-top button** on long product pages | Shofars & Goblets has 2 sections; once you've scrolled to goblets it's a long scroll back |

---

## Sprint Summary

| Sprint | Milestone | Goal | Status |
|---|---|---|---|
| Sprint 0 | M0 | Collect owner inputs | ⚠️ 6/11 done (WA number + TikTok handle + prices still pending) |
| Sprint 1 | M1 | Foundation: mobile, links, images | ✅ Done |
| Sprint 2 | M2 | Trust: contact, SEO, currency | ✅ Done |
| **→ SOFT LAUNCH** | — | Wire real WhatsApp number, enable custom domain | ⚠️ Temp WA number active, custom domain live |
| Sprint 3 | M3 | Homepage enhancements | ✅ Done (3.3 + 3.5 deferred) |
| Sprint 4 | M4 | Shop landing page (category hub) | ✅ Done |
| Sprint 5 | M5 | Category pages × 6 | ✅ Done (4/6 with real products; 2 Coming Soon) |
| Sprint 6 | M6 | Custom Orders page | ✅ Done |
| Sprint 7 | M7 | About page | ✅ Done |
| Sprint 8 | M8 | Contact page | ✅ Done |
| Sprint 13 | M13 | Bug bash & security review — findings logged | ✅ Logged |
| **Sprint 14** | M14 | UI/UX overhaul (font, contrast, icons, nav dropdown, carousel, cross-category, Kiddush Cups) | ✅ Done |
| **→ Sprint 15** | M9 | Full product catalogue (photos needed) | 🔜 **NEXT** — blocked on owner photo shoot |
| Sprint 16 | M11 Tier 1 | GA4 + Search Console + WA Business | 🔜 Fully unblocked — owner action needed |
| Sprint 17 | M10 | Hebrew quality pass | 🔜 Blocked on M0-6 |
| Sprint 18 | M11 Tier 2 | Newsletter, Pinterest, TikTok | 🔜 |
| Sprint 19 | M12 | Stripe checkout | 🔜 Blocked on M0-3 |
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
