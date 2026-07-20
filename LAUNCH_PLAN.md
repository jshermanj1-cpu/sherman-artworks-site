# Sherman Art Works — Full Launch Plan

> Created: 2026-07-06 | Owner: Sherman Family | PM/Dev: Claude
> Scope: everything needed to launch **except payment integration** (M0-3 / M19 — tracked separately, slots in whenever the provider is chosen).
> Companion docs: `TASK_LIST.md` (sprint history), `FIX_PLAN.md`.

---

## Where we stand today

**Done and live:** 8 category pages with products, bilingual EN/HE, WhatsApp-first cart + checkout, GA4 with cookie consent, Google Search Console + sitemap, JSON-LD structured data on all pages, llms.txt, legal pages (terms/privacy/accessibility), branded 404, custom domain with HTTPS.

**The site is functionally launchable now.** What remains is: a handful of open fixes, content gaps that hurt conversion (testimonials, dimensions, Hebrew review), SEO work that compounds over time, and the marketing/sales machine around the site.

---

## PHASE 1 — Fix Open Issues (Week 1) 🔴

Everything here is either broken or was flagged in QA and never closed.

| # | Task | Who | Effort | Status |
|---|------|-----|--------|--------|
| 1.1 | **Swap פמוטי חן (candlesticks) photos** to new images | Owner sends photos → Dev | S | 🔜 Blocked on owner |
| 1.2 | **Dead Cloudinary images on index.html** — 6 requests 404 (`…14.47.17/18/48/49…` variants, found Sprint 19 QA). Remove or fix the public_ids | Dev (Owner confirms correct IDs) | XS | ✅ 2026-07-06 — verified no broken images remain; the dead references were removed in later sprints |
| 1.3 | **og:image on index.html** still uses `h_630 c_fill` crop of the portrait bowl photo — same cropping problem we just fixed in the hero. Re-crop or pick a landscape photo | Dev | XS | ✅ 2026-07-06 — all 11 pages switched to `c_pad` (never crops); kiddush-cups og:image updated to cup+plate hero |
| 1.4 | **Diversify OG images** — 3 pages (index/about/custom-orders/contact) share the same bowl photo for social shares. Each page should share its own photo | Owner picks → Dev | S | 🔜 Crop fixed (1.3); photo diversification still needs owner picks |
| 1.5 | **Product dimensions** — 5 products missing measurements (customers ask; each answer costs a WhatsApp round-trip) | Owner measures → Dev | S | 🔜 |
| 1.6 | **Full-site QA sweep** — every page, EN + HE, desktop + real mobile device (iOS Safari + Android Chrome): links, cart, modals, carousels, RTL layout, WhatsApp deep links | Dev | M | 🔜 |
| 1.7 | **Verify in-card photo carousel** works on every category page (Sprint 17 rebuild casualty, partially reinstated since) | Dev | XS | ✅ 2026-07-06 — arrows/dots present, click advances photo (verified on kiddush-cups) |
| 1.8 | **sitemap.xml lastmod refresh** — most dates say 2026-06-19; kiddush-cups/trays-bowls/index changed heavily since | Dev | XS | ✅ 2026-07-06 — all 14 URLs updated |

---

## PHASE 2 — Content & Trust (Week 1–2) 🟡

These directly move conversion. A visitor deciding whether to send ₪770 to a stranger over WhatsApp needs proof.

| # | Task | Who | Effort |
|---|------|-----|--------|
| 2.1 | **Testimonials** — collect 3–5 quotes from past customers (first name + city + product). Add a homepage strip + quotes on relevant category pages | Owner collects → Dev builds | M |
| 2.2 | **Trust badges row** — "Handcrafted in Israel · Three generations · Ships worldwide · Secure ordering" near cart/checkout CTAs | Dev | S — ✅ 2026-07-20 built (trust strip on 10 pages, EN+HE, uncommitted pending approval) |
| 2.3 | **Native Hebrew copy review** — all pages. HE copy is dev-translated; a native pass before marketing spend is essential | Owner arranges | 👤 |
| 2.4 | **Process/story photos** — workshop, hands shaping glass, packing. Humanizes the About page and feeds social content. Even phone photos work | Owner | 👤 |
| 2.5 | **Business Gifts page content** — decide the offer (branded sets? volume pricing? lead form?) and fill the page, or hide the category until ready. A "Coming Soon" at launch looks unfinished | Owner decides → Dev | M |
| 2.6 | **FAQ expansion** — add the questions customers actually ask on WhatsApp (lead time per product, gift wrapping, kashrut/ritual questions, cup capacity). Feeds FAQPage schema too | Owner lists → Dev | S |

---

## PHASE 3 — SEO & GEO Hardening (Week 2, compounds forever) 🟡

Search Console + sitemap + JSON-LD are done. What's left, in impact order:

| # | Task | Who | Effort |
|---|------|-----|--------|
| 3.1 | **Google Business Profile** (business.google.com) — free, high-intent local + brand searches, shows reviews. Biggest single free win | Owner (15 min) | 👤 |
| 3.2 | **Google Merchant Center free listings** — product feed generated from `data/products.json`; products appear in Google Shopping tab for free | Dev generates feed, Owner opens account | M — ✅ dev half 2026-07-20: `merchant-feed.xml` (27 products, regenerate via `_merchant_feed.py`); owner opens Merchant Center account + points it at https://shermanartworks.com/merchant-feed.xml |
| 3.3 | **Hebrew SEO** — HE currently exists only as a JS toggle on the same URLs, invisible to Google. Build `/he/` static pages + `hreflang` tags. Large effort but unlocks the entire Hebrew-speaking market on search | Dev | L |
| 3.4 | **Content pages** targeting buyer-intent queries: "What is a Kiddush cup?", "Jewish wedding gift ideas", "Shofar buying guide", "Bar Mitzvah gifts from Israel". 1 page every 1–2 weeks; each links to products | Dev drafts → Owner reviews | M each |
| 3.5 | **Backlinks / directories** — Judaica directories, Israeli artisan directories, Jewish community sites, synagogue gift-shop outreach. 5–10 quality listings | Owner + Dev list-building | M |
| 3.6 | **GEO (AI search) upkeep** — llms.txt exists; keep it and `data/products.json` in sync on every product change, keep FAQ/Product schema current. AI assistants (ChatGPT, Perplexity, Claude) increasingly answer "where to buy handmade Judaica" — structured data + llms.txt is how we appear | Dev (ongoing) | XS/change |
| 3.7 | **Image SEO** — descriptive Cloudinary public_ids for future uploads; keep enriching alt texts (incl. `buildCard` runtime alts, a known gap) | Dev | S |
| 3.8 | **Core Web Vitals check** — PageSpeed Insights on homepage + one category page post-launch; fix anything red (LCP preload already done) | Dev | S |

---

## PHASE 4 — Social Media Presence (Week 2–3, then ongoing) 🟡

Handmade glass is a *visual* product — social is the natural channel. The asset already exists: the workshop.

| # | Task | Who | Effort |
|---|------|-----|--------|
| 4.1 | **Instagram upgrade** — switch @shermanartworks to a Business account, complete bio (link, WhatsApp button), post the full catalogue as a grid foundation | Owner (Dev writes captions) | S |
| 4.2 | **Content engine** — 3 posts/week sustainable mix: process videos (glass being shaped = highest engagement), finished pieces, packing orders, family story. Batch-film once a week | Owner films, Dev helps captions/hashtags | 👤 ongoing |
| 4.3 | **TikTok** — register handle (M0-11, still missing), cross-post the process videos. Craft/making-of content is TikTok's sweet spot | Owner | 👤 |
| 4.4 | **Facebook page** — required for Instagram Shopping + WhatsApp Business API later; also where synagogue/community groups live | Owner | S |
| 4.5 | **Pinterest** — create account, pin all product photos with links. Judaica/wedding/holiday gift searches on Pinterest have long shelf-life. Add "Pin it" buttons (M11.2.4) | Owner + Dev | S |
| 4.6 | **Instagram Shopping tags** — after 4.1 + 4.4, tag products in posts so followers tap through to the site | Owner + Dev | M |
| 4.7 | **Social proof loop** — ask every happy customer for a photo of the piece in their home; repost. Free content + testimonials in one | Owner (ongoing) | 👤 |

---

## PHASE 5 — Client Reach & Marketing Channels (Week 3+) 🟢

| # | Task | Who | Effort |
|---|------|-----|--------|
| 5.1 | **Email newsletter** — sign up Brevo (free tier), Dev wires signup embed on homepage + checkout. Send monthly: new pieces, holiday gift guides (Rosh Hashana = shofar season, Hanukkah, Passover) | Owner signs up → Dev wires | M |
| 5.2 | **Holiday calendar marketing** — the Judaica buying year is seasonal: Rosh Hashana (shofars, Aug–Sep), Hanukkah (Nov–Dec), Passover (Kiddush cups, Mar–Apr), wedding season (May–Aug). Plan content + email 6 weeks ahead of each | Owner + Dev | S/season |
| 5.3 | **Etsy shop** as parallel channel (M11.3.1) — Judaica sells well there; buyers already have payment + trust. Listings link back to the brand. Decide: full catalogue or 3–4 hero products | Owner decides → both build | L |
| 5.4 | **WhatsApp Business app** — profile with logo, catalogue, hours, away message, quick replies (M11.1.3). The storefront's "cash register" — should look professional | Owner (30 min) | 👤 |
| 5.5 | **B2B outreach** — synagogue gift shops, Judaica retailers, Jewish community centers, hotel gift shops in Jerusalem/Tel Aviv. One-page wholesale PDF + email template | Dev drafts → Owner sends | M |
| 5.6 | **Paid ads (optional, post-launch)** — start tiny: ₪500/month Meta ads on best process video, targeted at Jewish diaspora (US/UK/FR). Only after testimonials + Instagram look alive. GA4 conversion events already wired for measurement | Owner budget → Dev sets up | M |
| 5.7 | **Press/blogs** — pitch the "three generations of glass artisans in Israel" story to Jewish lifestyle blogs, Times of Israel lifestyle, local craft features. Story > product | Owner + Dev draft pitch | S |

---

## PHASE 6 — Sales Management & Optimization (ongoing from launch)

The site is WhatsApp-first — orders arrive as chats. Without a system, orders get lost in the chat scroll.

| # | Task | Who | Effort |
|---|------|-----|--------|
| 6.1 | **Order tracking sheet** — Google Sheet (or Notion): date, customer, product, price, status (quoted → paid → crafting → shipped → delivered), tracking #, source. Dev builds the template with status dropdowns | Dev builds → Owner uses | S — ✅ 2026-07-20: `Documents\Sherman_Art_Works_Order_Tracker.xlsx` (status/paid/source dropdowns, colour-coded statuses, auto Summary tab; kept OUT of the repo so customer data never deploys). Import to Google Sheets if preferred |
| 6.2 | **WhatsApp quick replies** — templates for: price quote, payment instructions, "your order shipped" + tracking, review request. Consistent, fast, professional | Dev drafts EN+HE → Owner installs | S — ✅ 2026-07-20 drafted: `WHATSAPP_QUICK_REPLIES.md` (9 templates EN+HE; /pay placeholder until M0-3; HE needs M10 native pass) |
| 6.3 | **Post-sale flow** — day after delivery: "how does it look?" message → ask for photo + review → feeds testimonials (2.1) and social (4.7). This loop is the growth engine | Owner (ongoing) | 👤 |
| 6.4 | **Analytics review ritual** — monthly 30-min look at GA4 (which products get views/add-to-carts, where visitors come from, where they drop) + Search Console (which queries impress). Dev prepares a simple dashboard/report format | Dev sets up → both review | S |
| 6.5 | **Conversion experiments** — after ~1 month of data: test hero photo, category order, price display (₪ vs $ first for foreign traffic), CTA wording. One change at a time, measured via GA4 | Dev | ongoing |
| 6.6 | **Inventory/lead-time signals** — since everything is made-to-order, show honest lead times per product ("ships in ~10 business days"). Reduces WhatsApp friction and abandoned carts | Owner confirms times → Dev | S |
| 6.7 | **Ops checklist (owner-side)** — packaging supplies stocked, customs forms process for international ($45 tier), invoice/receipt process per Israeli requirements (חשבונית), returns handling per terms.html | Owner | 👤 |

---

## PHASE 7 — Technical Hardening (post-launch, low urgency) 🟢

| # | Task | Who | Effort |
|---|------|-----|--------|
| 7.1 | Security headers (HSTS, CSP) — requires Cloudflare proxy in front of GitHub Pages; also gives caching + analytics | Dev | M |
| 7.2 | Uptime monitor (UptimeRobot free) + broken-link check monthly | Dev | XS |
| 7.3 | Image audit — remove unused `pics/` folder files from repo (Cloudinary serves everything) | Dev | S |
| 7.4 | Repo cleanup — `_sprint*.py`, `_card_carousel.py` helper scripts out of the deployed site | Dev | XS |

---

## Suggested timeline

| Week | Focus | Launch gate |
|------|-------|-------------|
| **Week 1** | Phase 1 (all fixes) + start Phase 2 (owner collects testimonials, measures products, arranges Hebrew reviewer) | — |
| **Week 2** | Phase 2 complete + Phase 3 quick wins (3.1, 3.2, 3.8) + Phase 4 setup (4.1, 4.3, 4.4) | **SOFT LAUNCH** — site is "open", share with friends/family/existing customers, collect first feedback + orders |
| **Week 3** | Phase 5 setup (newsletter, WhatsApp Business, order sheet 6.1–6.2) + social posting rhythm begins | — |
| **Week 4** | **PUBLIC LAUNCH** — announcement post, email to contacts, press pitches out, directories submitted | Full marketing push |
| **Month 2+** | Phase 3 long plays (Hebrew pages, content pages), Phase 5 channels (Etsy, B2B), Phase 6 optimization loop | Payment integration slots in whenever provider is chosen |

**Rationale for soft-launching in Week 2:** the site already works — orders can flow via WhatsApp today. Real customer feedback in Week 2–3 is worth more than another week of polish, and the first testimonials/photos it produces are exactly what the public launch needs.

---

## What only the owner can do (start these today, everything else waits on them)

1. 📸 Photos: candlesticks swap (1.1), workshop/process shots (2.4), OG picks (1.4)
2. 📏 Measure the 5 products missing dimensions (1.5)
3. 💬 Collect 3–5 testimonials from past customers (2.1)
4. 🇮🇱 Arrange native Hebrew reviewer (2.3)
5. 🏪 Google Business Profile — 15 minutes, biggest free win (3.1)
6. 📱 WhatsApp Business profile (5.4), TikTok handle (4.3), Facebook page (4.4)
7. 🎁 Business Gifts decision: define the offer or hide the category (2.5)
8. 💳 (Parallel track) Payment provider decision — PayPal / Payoneer / Cardcom / PayMe

---

*Living document — update as items complete. Commit rule applies: no push without owner approval.*
