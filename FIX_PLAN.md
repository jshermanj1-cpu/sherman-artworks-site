# Sherman Art Works — Remediation & Shopping Cart Plan
> Created: June 2026 (post-audit) | Status: AWAITING OWNER APPROVAL — nothing committed
> Companion to TASK_LIST.md. Once approved, tasks migrate into TASK_LIST.md as Sprints 16–20.

**Legend:** 👤 = Owner action · 💻 = Dev action · 🤝 = Both
**Effort:** XS < 30 min · S = 30 min–2 hrs · M = 2–5 hrs · L = 5–10 hrs

---

## WS0 — Corrections to the record 💻 XS

The WhatsApp number `+972523482278` is the **official business number** — not temporary.

| Task | What exactly |
|---|---|
| 0.1 💻 | Remove all "⚠️ temp number, replace" warnings from `context.md`, `TASK_LIST.md`, and the HTML comments (`index.html` has `// ⚠️ Replace with real WhatsApp number before launch`). Mark M0-1 ✅ and close M13.1.2. |
| 0.2 💻 | Fix other doc drift in `context.md`: mezuzahs is no longer a Coming Soon stub (has Ram Mezuzah product); fonts are currently Varela Round, not Fraunces/Inter; favicon image is the logo, not the candlestick. |

---

## WS1 — Security & Deployment (DO FIRST — this week)

### 1.1 👤 Rotate Cloudinary credentials — 10 min — CRITICAL
The API key + secret are in `context.md`, which is committed to a **public** repo (verified fetchable anonymously). With the secret, anyone can delete/replace every image on the site.

**Exact steps (Owner):**
1. Log in at console.cloudinary.com → ⚙️ Settings → **Access Keys**.
2. Click **Generate New Access Key** → save the new pair in a password manager (NOT in any repo file).
3. **Deactivate/delete the old key** (the exposed one — now rotated ✅ June 2026).
4. Tell dev it's done.

Site keeps working — public image delivery URLs don't use the secret. Only `product-builder`-style admin uploads need the new key, entered locally when used.

### 1.2 💻 Remove secret from repo + history — S
1. Delete the credentials table rows from `context.md` (replace with: "Credentials live in the owner's password manager — never in this repo").
2. Purge from git history with `git filter-repo --replace-text` (or BFG), force-push `main`.
3. Honest note: GitHub can cache old blobs; **rotation (1.1) is the real mitigation** — the purge is hygiene so scrapers don't harvest it later.

### 1.3 👤 Rotate GitHub PAT — 5 min
github.com/settings/tokens → revoke the exposed `ghp_…` token → create a **fine-grained** token scoped to only this repo (Contents: read/write). Store in password manager.

### 1.4 🤝 Fix the deployment pipeline — 15 min
The live site is currently **7 commits behind main** (mezuzah launch, font change, banner update are not live) because the manual main→gh-pages merge was skipped. Remove the failure mode entirely:

1. 👤 (or 💻 with repo admin): GitHub repo → Settings → Pages → Source: **Deploy from a branch** → branch **`main`** → `/ (root)` → Save.
2. 💻 Verify live site serves latest main (~1 min propagation), then delete the `gh-pages` branch (local + remote).
3. 💻 Update the deployment workflow section in `context.md` — push to main = deployed, no merge step.

### 1.5 💻 Repo hygiene — XS
- `.gitignore`: add `pics/`, `.claude/`, `_*.py` (13 MB of local photos are one `git add .` from bloating a public repo).
- Delete leftover `_card_carousel.py`.
- `robots.txt`: remove the `glass-curate.html` line (file was deleted in Sprint 15).

---

## WS2 — Kill the duplication (foundation for cart + ends the drift bugs)

Eleven self-contained pages each carry their own copy of nav/footer/CSS/translations. This is the **root cause** of the bugs found in the audit (banner drift, currency toggle on only 2 of 11 pages, two different exchange-rate formulas). GitHub Pages serves plain `.css`/`.js` files fine — no build step needed.

| Task | What exactly | Who | Effort |
|---|---|---|---|
| 2.1 | **Extract `css/site.css` + `js/site.js`.** Moves: tokens, reset, top bar, nav + dropdown, banner, footer, floating WA, modal/carousel CSS; `WA_NUMBER`, shared T-dictionary (nav/footer/banner/common), `setLang`, `setCurrency`, rate fetch, GA4 helper + delegated listener, nav toggles. Pages keep only page-specific T entries and their PRODUCTS rendering. **Acceptance: changing the banner text in ONE file changes all 11 pages.** Test all pages, EN/HE, mobile, RTL before approval. | 💻 | L |
| 2.2 | **`data/products.json` — single catalog.** One entry per product: `id, category, names, descriptions, price_ils, measurements, photos[], personalisable, lead_time`. Category pages fetch and filter it; the kiddush-cups cross-listing becomes a category tag instead of duplicated objects (ends that drift class). Also feeds: homepage from-prices, JSON-LD generation (WS3), and the cart (WS4). | 💻 | M |
| 2.3 | **Persist language + currency** in `localStorage` (`sa_lang`, `sa_cur`), read via a tiny inline `<head>` snippet before first paint (no flash). First visit: default from `navigator.language` (he → Hebrew + ILS, else English + USD). Can ship before 2.1. | 💻 | S |
| 2.4 | **One exchange-rate formula everywhere**: `usdRate = liveILSperUSD / 0.98` (+2% margin), whole-dollar rounding. Today the homepage applies the markup and category pages don't — same goblet shows two different $ prices. | 💻 | XS |
| 2.5 | **Copy sweep**: unify the shipping banner site-wide (owner confirms wording); rewrite the homepage Kiddush card description (currently says "Photos coming soon" next to a photo and a price); fix the two grammatically broken Hebrew banner variants. | 💻 + 👤 approves wording | XS |

---

## WS3 — SEO structural fixes

The site's growth depends on organic search, and right now every page is **nearly empty without JavaScript** (every `<h1>` is empty, all copy and products are JS-injected).

| Task | What exactly | Who | Effort |
|---|---|---|---|
| 3.1 | **Bake static English content into the HTML.** Every `data-t` element gets its EN text as real content; `setLang('he')` swaps, `setLang('en')` becomes a no-op on load. Product cards: pre-render static EN markup from `products.json` via a small Python generator script (keeps the no-build philosophy — script writes the HTML, dev pastes/commits), JS then enhances (carousel, modal, Hebrew). **Acceptance: View Source shows the full English page; with JS disabled the page is readable.** | 💻 | M–L |
| 3.2 | **JSON-LD structured data**, generated from `products.json` by the same script: `Organization` + `WebSite` (homepage), `Product` + `Offer` per product (priceCurrency ILS, availability, image array), `BreadcrumbList` on category pages. Validate with Google's Rich Results Test. This is what gets price + photo rich results in Google. | 💻 | S |
| 3.3 | **Head hygiene on all pages**: `rel=canonical` absolute URLs; `og:url`; `og:image` switched to `c_fill,w_1200,h_630,g_auto` (currently `c_fit` doesn't produce 1200×630); `twitter:card summary_large_image`; titles rewritten from "Candlesticks, Sherman Art Works" to "Candlesticks — Sherman Art Works | Handmade Glass Judaica" (≤60 chars); meta descriptions rewritten as real sentences (currently comma run-ons from the em-dash strip). | 💻 | S |
| 3.4 | **hreflang: deliberately deferred.** Honest call: hreflang pointing at a JS toggle is useless. Real Hebrew SEO needs `/he/` pages — schedule only after cart + catalog are done (the EN diaspora market is the priority per the spec). Documented as a Phase-2 decision. | — | — |
| 3.5 | **Distinct OG photos** for index/about/contact/custom-orders (5 pages currently share one bowl photo). | 👤 picks, 💻 applies | XS |

---

## WS4 — Payments & Shopping Cart ⭐ (the new feature)

**Principles:** charge currency is ILS; the site stays static on GitHub Pages; every order is reviewed by the owner anyway (handmade / made-to-order), so a lightweight flow is appropriate; WhatsApp stays a first-class channel, card checkout is added for everyone who doesn't use it.

### 4.1 👤 Provider selection (Owner — this week, in parallel with dev work)

Stripe doesn't onboard Israeli businesses. Realistic shortlist:

| Provider | Type | Why consider | Watch for |
|---|---|---|---|
| **PayPal Business (Israel)** | Global wallet + guest card checkout | Trusted by US/diaspora buyers; pure client-side JS integration possible → **no backend at all** | Highest fees (~4.4% + fixed intl); occasional fund holds |
| **Grow (Meshulam)** | Israeli processor | Bit + Apple/Google Pay + cards; cheap; popular with small IL businesses; hosted payment pages | Verify the checkout page has proper **English** for intl buyers |
| **PayPlus** | Israeli processor | Solid API, payment links, EN pages, auto-invoice | Link creation via API → needs the tiny worker (4.3 path 2) |
| **Tranzila** | Israeli veteran | Hosted iframe, multi-currency presentment | Dated docs/UX |
| **CardCom** | Israeli processor | Payment pages + built-in חשבונית invoicing | Same worker note |
| **Morning / GreenInvoice** | Invoicing + payment pages | If you already invoice there — unified bookkeeping | Underlying processor fees vary |

**Checklist to ask each provider (Owner):**
1. Hosted payment page (no card data touches our site — no PCI burden)?
2. Accepts foreign Visa/MC/Amex with 3-D Secure? English checkout page?
3. Charges in ILS; optional USD price display?
4. Payout to Israeli bank; auto receipt/חשבונית email?
5. Can a payment link with a **fixed amount** be created (a) in the dashboard and/or (b) via API?
6. Redirect-back / success URL support (needed for thank-you page + GA4 purchase tracking)? Webhooks?
7. Fees: per-transaction %, fixed fee, monthly fee, intl card surcharge.

**One architecture decision for Owner:** OK with a free Cloudflare Worker as the single piece of "backend glue" holding the provider's API key? (Recommended — see 4.3.) If no: checkout falls back to per-product fixed payment links, and the cart total is handled via WhatsApp instead.

### 4.2 💻 Cart — Phase A (no provider dependency; ships first) — L
*Depends on 2.1 (shared js) + 2.2 (products.json).*

**Data model**
- `localStorage` key `sa_cart`: `{v:1, ts:…, items:[{id, qty}]}`.
- **Prices are never stored in the cart** — always joined from `products.json` at render time (no stale/tampered prices).
- 30-day expiry via timestamp.

**UI — every page (lives in shared site.js/css)**
- Nav: bag icon button with count badge (`aria-live="polite"`), next to the hamburger on mobile.
- **Slide-over drawer** (from right; from left in RTL): Esc/overlay close, focus trap.
  - Line item: 64 px Cloudinary thumb (`w_128,h_128,c_fill`), lang-aware name, measurements, unit price, qty stepper (1–9 with "made to order" note), remove button.
  - Subtotal in ₪ + ≈$ (one shared formula from 2.4); "✓ Free worldwide shipping" reassurance line.
  - CTA primary: **Checkout** → `checkout.html`. CTA secondary: **Order via WhatsApp** → itemized message:
    `Hi! I'd like to order: • 1× Jerusalem Wine Horn (₪850) • 2× Menorah Goblet (₪946). Total: ₪1,796. My name is …`
  - Empty state: short message + "Browse the Shop" link.
- **Add to Cart**: product cards' primary button becomes "Add to Cart" (WhatsApp "Order" becomes secondary); modal gets the same pair. Toast "Added ✓", badge bump, drawer opens on first add.
- **checkout.html** (new page): order summary table + customer form (name, email, phone, shipping address, notes — proper `autocomplete` attributes). Phase A submit = WhatsApp handoff with full order + address (mailto fallback). Phase B swaps the submit for the provider redirect.
- **GA4: migrate to standard ecommerce events** with `items[]`: `view_item` (modal open), `add_to_cart`, `view_cart` (drawer), `begin_checkout`, `generate_lead` (WhatsApp handoff), `purchase` (Phase B thank-you page). Existing custom events stay.
- i18n: all new strings EN+HE in the shared T-dict; RTL drawer flip; keyboard accessible throughout.

**Edge cases:** product removed from catalog → line dropped with a notice; qty change recalculates; currency toggle re-renders drawer; multiple tabs (storage event listener).

### 4.3 💻 Cart — Phase B (card payment, once provider is chosen)

Three integration paths — pick by what the chosen provider supports:

1. **Dashboard/parameterized payment links** (no server): checkout page assembles the provider link, redirects; `thank-you.html` fires `purchase`. *Limitation: dynamic cart totals only if the provider signs/allows amount-in-URL — many don't.*
2. **Cloudflare Worker (recommended, works with any API provider)** — one free serverless endpoint, `create-payment`:
   - Receives `{items, customer}` → fetches `products.json` from the live site → **computes the total server-side** (client can't tamper) → calls the provider API with the secret key (stored as a Worker environment variable, **never in the repo**) → returns the hosted payment URL.
   - Success redirect → `thank-you.html?order=…`; optional webhook → order email.
   - 👤 creates the free Cloudflare account (or dev sets it up under the owner's email); 💻 implements. Effort M–L once provider docs are known.
3. **If PayPal is chosen**: PayPal JS SDK Smart Buttons directly on checkout.html — fully client-side, no worker. Mitigation for client-computed totals: owner cross-checks the paid amount against the order email before shipping (manual review already happens for every handmade order). Effort S–M.

### 4.4 👤 Order operations (Owner decides, dev documents in context.md)
What arrives per order (WhatsApp message / provider email / both), who replies, target response time, how lead time is communicated for made-to-order pieces.

---

## WS5 — Trust, legal & conversion

| Task | What exactly | Who | Effort |
|---|---|---|---|
| 5.1 | **`shipping-returns.html`.** Owner decides the actual policy: return window (14/30 days?), who pays return shipping, damage protocol (photos within 48 h → replacement/refund), customs/import duties responsibility, cancellation rules for made-to-order. Dev writes the page EN+HE seeded from the existing contact-page FAQ answers. **You promise "free worldwide shipping, 14 business days" — international buyers won't pay $300 without seeing the returns terms.** | 👤 decisions, 💻 page | S |
| 5.2 | **`privacy.html` + cookie consent banner.** Disclose GA4, Cloudinary, the exchange-rate API, WhatsApp handoff. Banner gates GA4: `gtag.js` loads only after "Accept"; choice stored (`sa_consent`); Decline = no analytics. Required for EU traffic (you ship worldwide) — must precede any marketing push. | 💻 | M |
| 5.3 | **`terms.html`** (light version: who you are, order acceptance, prices, IP). | 💻 | S |
| 5.4 | Footer "Policies" column on all pages — one edit after 2.1. | 💻 | XS |
| 5.5 | **Testimonials.** Owner mines WhatsApp/Instagram history for 3–5 short customer quotes (+ permission, ideally photos of pieces in customers' homes). Dev builds a testimonials section (homepage + category pages). Currently the site has **zero social proof** — for handmade goods this outweighs any design polish. | 👤 collect, 💻 build | S+S |
| 5.6 | Trust strip near hero/CTAs: "✓ Handmade in Israel · ✓ Free insured worldwide shipping · ✓ Secure card payment · ✓ Family studio, 3 generations" (card-payment item after WS4 ships). | 💻 | XS |
| 5.7 | **Newsletter capture** (every non-converting visitor is currently lost forever). Owner signs up for Brevo free tier; decides incentive (e.g., 10% first order — optional). Dev wires footer signup + post-add-to-cart prompt. | 👤 XS, 💻 S | |

---

## WS6 — Catalog & content depth (the real growth ceiling)

| Task | What exactly | Who | Effort |
|---|---|---|---|
| 6.1 | **Integrate the photos already sitting in `pics/`** (white bowl ×3, IMG_9845/46/52, Bowls IMG_9847/9851). Owner sends name + price + measurements per piece; dev uploads to Cloudinary and adds to `products.json`. These are finished photos going to waste. | 👤 details, 💻 integrate | S each |
| 6.2 | **Measurements for the 5 products missing them** (your own spec mandates dimensions per card; currently 5 of 7 are empty). Tape measure, 10 minutes. | 👤 → 💻 | XS |
| 6.3 | **Description upgrade**: 2–3 sentences per product — what it is, materials/technique, personalization options, lead time. Dev drafts all from existing knowledge; owner corrects facts. One-line descriptions don't sell $300 handmade pieces. | 💻 draft, 👤 approve | S |
| 6.4 | **Category strategy decision**: Business Gifts has zero products. Either (a) owner schedules the photo shoot, or (b) fold it into Custom Orders until products exist. An empty "Coming Soon" category at launch reads "abandoned," not "exclusive." | 👤 | — |
| 6.5 | TikTok handle for the footer (existing M0-11). | 👤 | XS |

---

## WS7 — Hebrew quality

| Task | What exactly | Who | Effort |
|---|---|---|---|
| 7.1 | **Immediate fixes** (dev now, native confirms later): both broken banner variants ("הזמנות מיוחדות בברוכים הבאים" / "בברוכות הבאות" — both wrong); "מסירה תוך 14 ימי עסקים" → "אספקה תוך…"; the awkward "בלתי ניתנת לחזרה" hero line. | 💻 | XS |
| 7.2 | **Full native pass** (existing M0-6): after 2.1, all Hebrew lives in ONE shared file instead of 11 — export strings to a doc, reviewer edits, dev applies. | 👤 find reviewer, 💻 apply | M |
| 7.3 | RTL device test after the cart ships (drawer, checkout form on real iOS Safari + Android Chrome). | 🤝 | S |

---

## WS8 — Brand typography decision

Commit `8a4d964` replaced the documented Fraunces + Inter pairing with **Varela Round for everything** — headlines and body. One rounded geometric font reads friendly-app, not heritage atelier, and flattens the hierarchy the premium copy works hard to build.

- 💻 Dev produces side-by-side homepage + category screenshots of three options: (a) current all-Varela-Round, (b) Fraunces headlines + Inter body (the documented design), (c) hybrid — Fraunces headlines + Varela Round body.
- 👤 Owner picks. Dev recommendation: (b) or (c).
- 💻 Applied via shared CSS (one edit after 2.1); docs updated.

---

## Proposed sprint sequence

| Sprint | Name | Contents | Owner's parallel homework |
|---|---|---|---|
| **16** | **Lockdown** | WS1 (security + deploy), WS0 (docs), 2.3 persistence, 2.4/2.5 sweeps, 3.3 head hygiene, 7.1 Hebrew quick fixes | 1.1 + 1.3 rotations (15 min total), Pages source switch |
| **17** | **Foundation** | 2.1 shared css/js, 2.2 products.json, 3.1 static EN content, 3.2 JSON-LD, WS8 font decision applied | 4.1 provider research, 5.1 policy decisions, 6.2 measurements |
| **18** | **Cart** | 4.2 Phase A complete (drawer + checkout.html + WhatsApp checkout + GA4 ecommerce) | 4.1 provider chosen, 5.5 collect testimonials |
| **19** | **Payments live** | 4.3 Phase B integration, thank-you + purchase tracking, 5.2/5.3/5.4 legal pages + consent banner | Test a real ₪1 transaction end-to-end |
| **20** | **Depth & launch** | 5.5 testimonials section, 5.6 trust strip, 5.7 newsletter, 6.1/6.3 catalog enrichment, 7.2 Hebrew pass | 6.4 category decision, 6.5 TikTok → then marketing push |

---

## Owner action summary (everything 👤 in one list)

| # | Action | Time | Blocking |
|---|---|---|---|
| 1 | Rotate Cloudinary access keys (1.1) | 10 min | 🔴 everything |
| 2 | Revoke + reissue GitHub PAT (1.3) | 5 min | 🔴 |
| 3 | Switch GitHub Pages source to `main` (1.4) | 2 min | 🔴 deploys |
| 4 | Research + choose payment provider (4.1 checklist) | 2–4 hrs | 🔴 Sprint 19 |
| 5 | Decide returns/shipping policy answers (5.1) | 30 min | 🟡 Sprint 19 |
| 6 | Measure the 5 products (6.2) | 10 min | 🟡 |
| 7 | Send names/prices for the pics/ photos (6.1) | 20 min | 🟡 |
| 8 | Pick OG photos (3.5) | 10 min | 🟢 |
| 9 | Collect 3–5 testimonials + permissions (5.5) | 1–2 hrs | 🟡 Sprint 20 |
| 10 | Font decision from screenshots (WS8) | 10 min | 🟡 Sprint 17 |
| 11 | Business Gifts: shoot or fold (6.4) | decision | 🟢 |
| 12 | Brevo signup + incentive decision (5.7) | 20 min | 🟢 |
| 13 | Find native Hebrew reviewer (7.2 / M0-6) | — | 🟢 |
| 14 | TikTok handle (6.5 / M0-11) | 1 min | 🟢 |

---

*Per the commit rule: this plan is uncommitted until the owner approves. On approval, Sprint 16 begins and TASK_LIST.md is updated to absorb these workstreams.*
