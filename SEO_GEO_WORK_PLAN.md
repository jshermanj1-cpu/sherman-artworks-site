# SEO / GEO Work Plan — shermanartworks.com

> Created: 2026-07-07 | Source: SEO/GEO report run 2026-07-07 20:05 | PM: Claude | Owner: Sherman Family
> Companion to: LAUNCH_PLAN.md (referenced as L-x.x), FIX_PLAN.md, TASK_LIST.md
> ⛔ Commit rule applies: no commits/pushes without owner approval.

---

## 0. Report verification — read this first

The report was checked against the repo **and the live site** before planning. A large part of it is stale or wrong; do **not** redo these:

| Report claim | Reality (verified 2026-07-07) |
|---|---|
| "No sitemap.xml / robots.txt" | Both live and serving 200. robots.txt references the sitemap; sitemap lists all 14 pages |
| "No JSON-LD structured data" | Product + Offer + Brand + Organization + BreadcrumbList + ItemList live on all pages |
| "No llms.txt" | Live (3.6 KB) |
| "Register Google Search Console + submit sitemap" | Done — GSC verified, sitemap submitted (context.md, LAUNCH_PLAN) |
| "store-page.html serves an empty page" | Returns 404 (branded 404 page) |
| "Add hreflang tags" | Present on all pages (en / he / x-default) |
| "No FAQ content" | FAQ accordion exists on contact.html; expansion already planned (L-2.6) |
| "No shipping/returns policy anywhere" | Full policy exists in terms.html (processing times, returns, international shipping) — but it IS buried; see W7 |

**What survives from the report as genuinely actionable:** the site doesn't rank for its own brand name (the one critical finding), third-party listings are inconsistent, and a handful of small on-site gaps (H1, USD prices in HTML, tagline copy, artisan attribution, per-product URLs).

---

## Phase 1 — Brand visibility & indexing (this week) 🔴

The site is invisible in Google for "Sherman Art Works" while a dead legacy URL and third-party retailers rank. GSC is already set up, so this is diagnosis + nudging, not setup.

| ID | Task | Who | Effort | Status |
|---|---|---|---|---|
| W1 | **GSC coverage check** — open Search Console → Pages report. Confirm the 14 sitemap URLs are "Indexed"; note every legacy URL (e.g. `/store-page.html`) Google still holds | 👤 Owner (15 min) | XS | ⚠️ 2026-07-07: only 1 page indexed; owner clicked "Validate fix" (אימות). W2 (per-URL Request Indexing) still needed |
| W2 | **Request indexing** — URL Inspection → "Request indexing" for the homepage + 7 category pages + about. This is the fastest lever for a new site Google is slow to pick up | 👤 Owner (20 min) | XS | 🔜 |
| W3 | **Legacy URL redirect stubs** — GitHub Pages can't do server 301s. Create a real `store-page.html` containing `<meta http-equiv="refresh" content="0; url=/">` + `<link rel="canonical" href="https://shermanartworks.com/">` + a plain link, so Google consolidates the old URL into the new homepage instead of keeping a 404 in the index. Repeat for any other legacy URLs found in W1 | 💻 Dev | S | ✅ dev done 2026-07-07 for store-page.html (uncommitted); repeat for other URLs W1 finds |
| W4 | **Google Business Profile** — already planned as L-3.1; the report confirms it's the biggest single free win for brand-name searches. Do it in this phase, not later | 👤 Owner (15 min) | S | 🔜 owner scheduled for week of 2026-07-13 |

---

## Phase 2 — Third-party listing alignment (this week, owner outreach) 🔴

New work — in no existing plan. Google and AI assistants currently describe the business via Israel Cart ("Sherman Judaica", Jerusalem), Shalom House, The Aesthetic Sense, and Facebook ("Ginot Shomron") — with three different names and locations and no link to the site. Consistent third-party corroboration is the strongest GEO lever available.

| ID | Task | Who | Effort | Status |
|---|---|---|---|---|
| W5 | **Contact each listing** (Israel Cart, Shalom House, The Aesthetic Sense) and request: (a) name shown as **"Sherman Art Works"**, (b) one consistent location, (c) a link to shermanartworks.com | 👤 Owner | M | 🔜 |
| W5a | **Decide the canonical location string first** (Karnei Shomron? Ginot Shomron?) and use it everywhere — site JSON-LD, GBP (W4), all listings, Facebook | 👤 Owner | XS | ✅ 2026-07-07: **"Karnei Shomron, Israel"** — use this string everywhere |
| W6 | **Facebook page** — rename/align to "Sherman Art Works", set website field to shermanartworks.com, match the W5a location | 👤 Owner | S | 🔜 |
| W6a | **Israel Bookshop** already sells Sherman-made pieces and outranks us for candlestick queries — ask them to credit/link "Sherman Art Works" on those product pages | 👤 Owner | S | 🟢 nice-to-have |

---

## Phase 3 — On-site quick wins (one dev sprint) 🟡

| ID | Task | Who | Effort | Status |
|---|---|---|---|---|
| W7 | **Surface shipping/returns near the buy flow** — policy exists in terms.html but neither buyers nor the report's crawler found it. Add a one-line summary (processing time, free shipping, returns for custom orders) + link to terms.html on product modals/cards and checkout.html | 💻 Dev | S | ✅ dev done 2026-07-07 (uncommitted) — note added to product modal on all 7 pages + dispatch time added to checkout note |
| W8 | **Bake USD prices into static HTML** — visible USD is currently JS-only (`≈ ${usdStr}`); search engines and AI see ILS only. Bake "≈ $X" into the card markup (products.json already has the data) and consider a second USD `Offer` (or `AggregateOffer`) per product in JSON-LD | 💻 Dev | S | ✅ dev done 2026-07-07 (uncommitted) — "≈ $X" baked into all static cards + homepage category cards at fallback rate; JSON-LD deliberately left ILS-only (approximate USD would risk wrong prices in rich results) |
| W9 | **Homepage H1** — currently sr-only "Sherman Art Works" (index.html:396). Change to keyword-bearing: "Handmade Glass Judaica from Israel — Sherman Art Works" | 💻 Dev | XS | ✅ dev done 2026-07-07 (uncommitted) |
| W10 | **Tagline copy fix** — "Handcrafted in Israel · Since Generations" → "· For Three Generations" (index.html:537 + translation dict at :729; grep other pages for the same string) | 💻 Dev | XS | ✅ dev done 2026-07-07 (uncommitted) — EN only; Hebrew "מסורת דורות" already reads well |
| W11 | **FAQ expansion** (= L-2.6) — add WhatsApp-common questions (shipping times/costs, kosher status of shofars, custom order process, materials) + `FAQPage` schema. Report confirms FAQ content is exactly what AI answers quote | 👤 Owner lists → 💻 Dev | S | 🔜 |

---

## Phase 4 — GEO depth (next 2–4 weeks) 🟢

| ID | Task | Who | Effort | Status |
|---|---|---|---|---|
| W12 | **Name an artisan** — "The Sherman Family" is anonymous, so AI can't attribute the work to a citable person. Owner picks at least one named artisan + short bio for about.html; dev adds `Person` schema linked from `Organization` | 👤 Owner decides → 💻 Dev | S | 🔜 |
| W13 | **Testimonials** (= L-2.1 / FIX 5.5, Sprint 20) — report independently confirms zero social proof is the top conversion + GEO gap. No new work, but raise priority | 👤 + 💻 | M | already planned |
| W14 | **Per-product URLs — decide** — products live as cards + modal, so no product can rank on its own. Option A: generate per-product pages from products.json (best for SEO, effort M). Option B: stable `#anchors` per product now (effort XS) and revisit A after Phase 1 shows indexing results. Recommend B now, A later | 💻 Dev after 👤 decision | XS→M | 🔜 Option B planned as **TASK_LIST 22.5** (Sprint 22, 2026-07-08) |
| W15 | **Content pages** (= L-3.4) — buyer-intent queries the site is invisible for ("shofar buying guide", "handmade Shabbat candlesticks from Israel", …). Already planned; the report's competitor list (Judaica Web Store, Nadav Art, Etsy, ProShofar…) tells us which queries to target first | 💻 Dev drafts → 👤 Owner reviews | M each | already planned |

---

## Monitoring loop

- **+2 weeks:** re-run the report's visibility checks ("Sherman Art Works", "shermanartworks.com", the three buyer queries). Success gate for Phase 1: site ranks #1 for its own domain name and appears for its brand name.
- **Monthly:** GSC queries + coverage review (fits the L-6.4 analytics ritual).
- **Next report run:** section 0 above lists false findings — check them against the live site before acting.

## Suggested order of attack

1. W1 → W2 (owner, ~35 min, unblocks everything)
2. W5a → W4 → W5/W6 (owner outreach batch, one consistent identity everywhere)
3. W3 + W7–W10 as one small dev sprint (awaiting owner approval to commit)
4. W11–W14 as the following sprint, W15 ongoing
