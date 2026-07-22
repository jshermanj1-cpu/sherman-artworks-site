# Sherman Art Works — Pricing Program Plan

**Date:** 2026-07-08 | **Status:** Phase 0 tooling + Phase 1 (round 1) + Phase 3 tool built | **Owner of doc:** dev

> **Progress 2026-07-08:** Owner workbook, benchmark data, corridor memo, and the
> `pricing-calculator.html` tool are all built (details in §6). **Waiting on owner cost data**
> to run the Phase-2 audit. Private data lives in the gitignored `_pricing/` folder.
**Goal:** a repeatable, data-backed way to price every piece — existing catalog, new pieces, and custom commissions — so prices protect margin, match what the market will pay, and look right in both ₪ and $.

---

## 1. Why now (current-state observations)

From `data/products.json` (24 products):

| Category | Current pricing | Observation |
|---|---|---|
| Candlesticks (6) | all ₪775 | Flat pricing ignores differences in work/complexity |
| Kiddush cups (6 singles) | all ₪422 | ₪422 ≈ $112 — a clean price point in neither currency |
| Horn goblets (2) | ₪473 | ≈ $126 (7×18 — chai multiple; keep if intentional) |
| Mezuzahs | horn ₪700, glass ₪311 | ₪311 looks like a stale currency conversion |
| Cup + plate bundle | ₪770 vs ₪786 separately | Bundle saves only ₪16 (2%) — no real incentive |
| Shofars | ₪850 / custom ₪1,050 | Personalization premium exists (+₪200) — good instinct, make it systematic |

Core problems the program solves:
1. **No cost floor** — we don't currently know the minimum price at which a piece is worth making.
2. **No market corridor** — prices aren't anchored to what comparable artisan Judaica sells for.
3. **No psychological rounding** — prices land on awkward numbers in both ₪ and $.
4. **No feedback loop** — no record of what sold, what got inquiries but didn't sell, and at what price.

---

## 2. Data needed (the full list)

### 2.1 Internal cost data — OWNER must supply (nobody else can)

Per product (a simple form/spreadsheet; ~15 min per piece):

| Field | Example | Why |
|---|---|---|
| Materials cost (₪) | horn, glass, epoxy, base | Direct cost |
| Silver used (grams × current spot) | repoussé work | Volatile input — priced separately from other materials |
| Hours of work | shaping, plating, finishing | Biggest hidden cost in handmade |
| Your target hourly rate (₪/hr) | one number for the studio | Turns hours into cost. Pick honestly — this is your salary |
| Packaging + local handling (₪) | box, padding, printing | Often forgotten |
| Failure/waste rate (%) | glass pieces that crack | Handmade reality — survivors must pay for losses |
| One-of-a-kind vs repeatable | bowl = one-off; cups = repeatable | One-offs price differently (scarcity premium) |

Studio-level (once, not per product):
- Monthly overhead: studio space, tools, utilities, Cloudinary, domain → allocated per piece.
- **VAT / business status** (osek patur vs murshe; exports typically zero-rated) — determines whether ₪ prices are VAT-inclusive. Owner confirms with accountant.
- Shipping policy: charged separately — International $45 · Israel ₪35.

### 2.2 Demand & sales data — mostly DEV, some owner

| Data | Source | Status |
|---|---|---|
| Product views, `view_details`, `add_to_cart`, `begin_checkout`, `whatsapp_click` per product | GA4 (`G-J55QNV6GF1`) | ✅ Already collected (consent-gated) — dev exports |
| Actual sales: date, item, price paid, channel, buyer country | **Doesn't exist yet** — orders close in WhatsApp | 🔴 Biggest gap. Start a sales log NOW (simple sheet). Backfill from WhatsApp history as best as possible |
| Inquiries that didn't convert (+ reason if known: "too expensive," shipping, timing) | WhatsApp | Owner logs going forward |
| Custom-commission quotes: what was quoted vs accepted/declined | WhatsApp | Owner logs — this is free price-sensitivity data |

### 2.3 Market / competitor data — DEV collects (see §3)

10–15 comparable items per category: seller, product, price, currency, materials, size, handmade-or-mass-produced, personalization offered, shipping included?

### 2.4 Context data

- **ILS↔USD rate history** — site already pulls live rate (`open.er-api.com`). Prices set in ₪ drift in $ terms; the program needs a "recheck trigger" when FX moves >5%.
- **Channel fees** — future payment provider (~1.5–3%), Etsy if we list there (6.5% + payment + listing fees), fair/market stall costs. Price recommendations must be channel-aware.

---

## 3. Should we use other vendors for comparison? — Yes, with rules

**Yes — but as a positioning corridor, not a price to copy.** Two different comp sets, used differently:

**Tier A — artisan/handmade (your true comp set):**
- Etsy handmade Judaica sellers (closest analog: handmade, gift buyers, USD prices)
- Israeli handmade marketplaces (e.g., Marmelada) — ILS comps for glass work
- Named artist studios: Yair Emanuel, Gary Rosenthal (mid/high artisan Judaica); Michael Aram (designer ceiling)
- Barsheshet-Ribak (Tel Aviv) for decorated/silver shofar comps
- Israel Museum shop / gallery shops — artisan glass comps

**Tier B — mass-market Judaica retail (reference only):**
- Judaica.com, World of Judaica, aJudaica, Judaica WebStore

**Rules of use:**
1. Tier A defines the **corridor** (25th–75th percentile of comparable artisan pieces). Our price should normally sit inside or above it — silver-covered horn work justifies "above."
2. Tier B only tells us the *perceived floor* buyers see when googling "mezuzah case." We never match it — a hand-shaped, silver-covered oryx horn is not a ₪90 import — but we should know the gap so product copy justifies it.
3. Record comps in a flat file (`_pricing/benchmarks.csv`, gitignored) so the corridor is recomputable, not vibes.

---

## 4. The pricing model (how a price gets computed)

```
1. COST FLOOR   = (materials + silver + packaging + hours × rate)
                  × (1 + waste%) × (1 + overhead%)
2. MIN PRICE    = floor ÷ (1 − target margin − channel fee%)
                  → below this, decline or redesign the piece
3. CORRIDOR     = 25th–75th percentile of Tier-A comps for the category
4. POSITION     = pick point in/above corridor based on:
                  one-of-a-kind (+), silver work (+), personalization (+15–25%),
                  size/complexity, "hero piece" halo
5. CHARM PRICE  = round to a psychological point in the DOMINANT currency
                  per segment:
                  • Israeli buyers → clean ₪ (₪780, ₪495, ₪1,200)
                  • Diaspora gift buyers → clean $ ($120, $180) or chai
                    multiples ($126, $180, $360 — culturally resonant for gifts)
6. SANITY CHECK = final price ≥ MIN PRICE; bundle prices give ≥8–10% real
                  discount; personalized variant ≥ +15% over base
```

Decision needed from owner (Phase 2): which currency anchors which categories — suggestion: shofars/mezuzahs/goblets anchor in **$** (gift/diaspora market), candlesticks/bowls/cups anchor in **₪** (local market) — to be validated against GA4 geo data.

---

## 5. The tool

An internal, not-linked page in the style of `product-builder.html` — fits the no-backend architecture:

**Workbook ↔ tool:** two front doors to the same data. The **workbook** (`_pricing/pricing-workbook.xlsx`)
is for comfortable offline cost entry in Excel. The **tool** (`pricing-calculator.html`) is for live
calculation, corridor positioning, charm pricing, and export. They share the same formulas so numbers
reconcile; the tool reads/writes a `costs.json` and persists to the browser's localStorage, so the
owner can use either. (If the owner fills the workbook, dev converts it to `costs.json` for the tool.)

**`pricing-calculator.html`** (root, listed in `robots.txt` disallow like product-builder):
- Loads `data/products.json`; cost inputs persist to `localStorage` and export/import as `_pricing/costs.json` (**gitignored** — real costs and margins never go public in the repo).
- Per-product input form for the §2.1 cost fields.
- Outputs: cost floor, min price, corridor position, suggested charm price in ₪ **and** $, channel-adjusted variants (site / Etsy / fair).
- **Audit view:** a table of all 24 products — current price vs floor vs corridor, flagged 🔴 below floor / 🟡 outside corridor / 🟢 OK. This view drives the repricing pass.
- Export: proposed `products.json` price diff for owner approval.

Also created: `_pricing/` folder (gitignored) holding `costs.json`, `benchmarks.csv`, `sales-log.csv`.

---

## 6. Work plan

### Phase 0 — Data collection kickoff (owner, 1–2 weeks, parallel with Phase 1)
- [ ] O-1: Fill cost sheet for all 24 products (dev provides the blank sheet on day 1)
- [ ] O-2: Set studio hourly rate + monthly overhead number
- [ ] O-3: Confirm VAT status with accountant; decide shipping-included vs separate
- [ ] O-4: Start the sales log (dev provides template); backfill past WhatsApp orders
- [ ] O-5: Going forward — log every quote given on customs, and whether it was accepted

### Phase 1 — Competitor benchmark sweep (dev, ~2–3 days)
- [x] D-1: Collect Tier-A comps per category → `_pricing/benchmarks.csv` (round 1; 35 rows, deepen mezuzah/Etsy/IL next)
- [x] D-2: Spot-check Tier-B retail prices per category → in `benchmarks.csv`
- [x] D-3: Compute corridor per category → `_pricing/benchmark-memo.md` (FX drift + candlestick anchor are the headline findings)

### Phase 2 — Pricing model + catalog audit (dev + owner, ~2 days after 0+1 complete)
- [ ] D-4: Apply §4 model to all 24 products; produce audit table (current vs floor vs corridor vs suggested)
- [ ] O-6: Owner reviews; decides currency anchor per category; approves new price list
- [ ] D-5: Fix known oddities in the pass: bundle discount (₪770 → real incentive), ₪311 mezuzah, flat-price categories

### Phase 3 — Build `pricing-calculator.html` (dev, ~2–3 days)
- [x] D-6: Tool built per §5 spec; `_pricing/` gitignored; `robots.txt` disallow added; corridors seeded from Phase 1
- [x] D-7: Formulas verified against the workbook + hand-calc (floor/min/margin/flags reconcile). Live DOM render not yet exercised — parallel session held the preview ports; re-verify in browser before relying on the audit view

### Phase 4 — Rollout + monitoring (ongoing)
- [ ] D-8: Update `products.json` + **manually cross-listed goblet pages** (kiddush-cups.html shows the same goblets — both must change) — ⚠️ per repo rule: preview, summarize, **wait for owner "approve"** before any commit
- [ ] D-9: GA4 before/after per repriced product (views → whatsapp_click rate) at 2, 6 weeks
- [ ] Cadence: **quarterly** price review; **FX trigger** — if ILS/USD moves >5% from last review, recheck $ anchors ahead of schedule; recheck silver-heavy pieces when silver spot moves materially
- [ ] When payment provider lands (M0-3) and/or Etsy channel opens: add channel fees into the model and re-run audit

### Dependencies
- Phase 2 blocks on Phase 0 (costs) + Phase 1 (corridor).
- Nothing here blocks Sprint 20 / launch work; the repricing pass is a natural pre-launch item.

---

## 7. Success criteria

1. Every product has a known cost floor; none priced below it.
2. Every price sits inside/above its category corridor with a written reason if outside.
3. Prices land on clean points in their anchor currency.
4. A new piece can be priced in <10 minutes using the tool.
5. Sales log running — after ~3 months we can see price-vs-conversion per category and iterate from evidence instead of instinct.
