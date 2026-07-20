# SEO / GEO End-to-End Audit — shermanartworks.com
**Date:** 2026-07-20 · **Method:** full repo static analysis + live-site verification (every URL, every image, deployed-file parity, runtime render check). No changes committed — findings + fixes only.

---

## Verdict

The site is in **strong technical SEO shape** — fundamentals that most small sites get wrong all pass here. The real opportunities are: **merchant feed shipping data (required by Google)**, **richer Product schema (shipping/returns)**, and the **Hebrew market, which is currently invisible to search engines**. Everything found is listed below, ranked.

## What passed (verified, not assumed)

| Area | Result |
|---|---|
| Product data sync | All 27 products consistent across inline PRODUCTS arrays ↔ products.json ↔ llms.txt anchors/prices ↔ merchant-feed.xml. Homepage `data-min-ils` from-prices all correct (verified live in-browser too). |
| Structured data | Valid JSON-LD on every page: 31 Product placements (price/currency/availability/brand/images all correct), Store+WebSite graph, FAQPage ×2, BreadcrumbList site-wide, HowTo on custom-orders. Zero parse errors. |
| Meta | Unique title + description on every indexable page; correct self-canonicals everywhere. |
| Indexing control | noindex correct on checkout/404/internal tools; no noindexed page in sitemap; sitemap = exactly the 14 indexable URLs; robots.txt valid + sitemap reference. |
| Live infrastructure | http→https and www→apex redirect in one hop; unknown URLs return real 404; robots/sitemap/llms/feed/products.json live copies byte-identical to repo (CRLF only); llms.txt served `text/plain`. |
| Images | 278/279 Cloudinary URLs return 200 (sole "failure" is the CDN prefix constant inside product-builder.html — not a real image). The June dead-image issue is fully fixed. |
| No-JS content (critical for GEO) | Product names, descriptions, prices, CTAs all present in static HTML — verified by stripping `<script>` (477–930 words/category page). GPTBot/ClaudeBot/PerplexityBot don't execute JS, so this matters more than anything else for AI visibility. |
| AI crawler access | robots.txt allows all bots; llms.txt current and well-structured. |
| Performance | Homepage 13.5 KB gzipped; CSS+JS ~22 KB total; DOMContentLoaded ~56 ms; fonts `display=swap` + preconnect; zero console errors; exchange-rate API responsive. |
| Internal links | No broken internal links; no unintended orphan pages. |

---

## Issues found

### P1 — affects Google product visibility now

**1. Merchant feed: `g:shipping` missing from all 27 items (required field).**
Google Merchant Center requires shipping info per item or account-level shipping settings; without either, items get disapproved or shown without shipping cost (a conversion killer for a ₪30/$45-shipping store with generous free-shipping thresholds worth advertising).
*Fix:* extend `_merchant_feed.py` to emit per item:
```xml
<g:shipping><g:country>IL</g:country><g:price>30.00 ILS</g:price></g:shipping>
```
plus the international tier — or configure shipping once in Merchant Center settings (faster, no feed change). Also add free-shipping thresholds there (₪1,100 / $500).

**2. Merchant feed: `g:google_product_category` missing from all 27 items (recommended, improves matching).**
*Fix:* add in `_merchant_feed.py` by category — e.g. candlesticks → `2784` (Home & Garden > Decor > Candle Holders), cups/goblets → `674` (Kitchen & Dining > Tableware > Drinkware), bowls/trays → `6456` (Decor > Decorative Bowls), mezuzahs/shofars → `5609` (Religious Items). Verify IDs against Google's taxonomy file before shipping.

**3. Product JSON-LD missing `shippingDetails` and `hasMerchantReturnPolicy`.**
Search Console flags these as merchant-listing warnings and Google increasingly renders shipping/returns directly in product results. The data already exists on terms.html — it just isn't in the markup.
*Fix:* add to every offer (site-wide constant, generated in the same place the Product blocks are built):
```json
"shippingDetails": [
  {"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":30,"currency":"ILS"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":"IL"}},
  {"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":45,"currency":"USD"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":["US","GB","CA","AU","FR","DE"]}}
],
"hasMerchantReturnPolicy": {"@type":"MerchantReturnPolicy","applicableCountry":"IL","returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow","merchantReturnDays":14,"returnMethod":"https://schema.org/ReturnByMail","returnFees":"https://schema.org/ReturnFeesCustomerResponsibility"}
```
While in there: add `"sku"` (= product id) and `"itemCondition":"https://schema.org/NewCondition"` — cheap wins that also help feed↔schema matching; consider `priceValidUntil` to clear the GSC warning.

### P2 — strategic gaps

**4. Hebrew is invisible to search engines.**
i18n is runtime-JS only, so crawlers only ever index English. For an Israeli Judaica business, every Hebrew query (פמוטים בעבודת יד, כוס קידוש, שופר מותאם אישית…) is a lost market. Worse, the current hreflang block claims `he` lives at the *same URL* as `en` — contradictory signals (the URL serves English by default), so the annotation does nothing and can mislead.
*Fix, short term:* drop the `he` hreflang line (keep or drop `en`/`x-default`; they're no-ops when there's one language per URL).
*Fix, long term (recommended):* static `/he/` versions of the 7 shop pages + homepage. The translations already exist in each page's `T` object — a build script could bake them into real pages with proper `lang="he" dir="rtl"`, self-canonicals, and genuine bidirectional hreflang. This is the single biggest untapped SEO opportunity on the site.

**5. No reviews/ratings anywhere (schema + trust).**
Competitors' product results show stars; yours can't (`aggregateRating`/`review` absent — legitimately, since no review content exists yet). Also the top E-E-A-T/GEO gap: AI engines lean on third-party corroboration.
*Fix:* Sprint 20's testimonials work should collect real customer quotes (WhatsApp history is likely full of them) → publish with `Review` markup once genuine. Never add rating markup without visible reviews.

**6. GEO content depth: no informational content for AI engines to cite.**
llms.txt + FAQ + clean product data are done. What's missing is the content AI answers actually cite: buying guides ("How to choose Shabbat candlesticks", "Shofar buying guide", "What is a mezuzah case?"). One good guide per category, interlinked from product pages, would target the question-shaped queries that both Google AI Overviews and chat assistants answer.

**7. OG image duplication (known, still open — M13.2.1).**
index, about, contact and custom-orders all share the green-bowl photo; business-gifts and shofars-goblets share the goblets photo. Category pages (candlesticks, kiddush-cups, mezuzahs, custom-shofars, trays-bowls) are properly differentiated. Needs owner photo picks for the 4 generic pages.

### P3 — small fixes and polish

**8. kiddush-cups.html meta description is stale** — "Commission yours today, made to order" dates from its coming-soon era; the page now sells 10 products. Rewrite to mention actual products/prices (e.g., tall & low glass cups, ceramic cup, cup-and-plate sets, from ₪364).

**9. custom-shofars.html title (71 chars) and description (171 chars) exceed display limits** — Google truncates ~60 / ~160. Trim, e.g. title: "Personalised Shofars from Israel - Sherman Art Works".

**10. product-builder.html: robots-Disallowed but no noindex meta.** A Disallowed URL can still be indexed as a bare URL if linked externally ("Indexed, though blocked by robots.txt"). sales-dashboard and pricing-calculator have both; product-builder only has the Disallow.
*Fix:* add `<meta name="robots" content="noindex, nofollow">` to product-builder.html. (Cleanest pattern is actually noindex *without* Disallow — Google must crawl to see the noindex — but adding the meta is the minimal fix.)

**11. store-page.html is indexable.** Meta-refresh stub redirecting to home; canonical→home mitigates, but add `noindex` or delete the file if the external link that needed it is gone.

**12. 404 page renders no text without JS** — h1/body are empty `data-t` shells filled at runtime. Noindex makes this SEO-neutral, but no-JS users and some crawlers see a blank page. Bake the English strings in (same pattern as other pages, where static EN text is present and JS swaps HE).

**13. LCP hints regressed:** context.md documents a homepage hero `preload`; it's gone (0 preloads site-wide, no `fetchpriority`). Site is fast anyway, so low priority — restore `<link rel="preload" as="image" fetchpriority="high">` for the hero, and add `width`/`height` to hero/static imgs not covered by CSS `aspect-ratio` to keep CLS at zero.

**14. llms.txt nits:** file has a UTF-8 BOM (some strict parsers show it as garbage — save without BOM next regeneration); business-gifts bullet is the only one with no price mention (add "from ₪1,050").

**15. Store schema `sameAs` lists only Instagram** — add TikTok (pending owner handle, M0-11) and any other live profiles to strengthen entity resolution.

**16. checkout.html carries both canonical and noindex** — mixed signal, harmless; drop the canonical if touching the file anyway.

### Not issues (checked, fine — don't "fix")

- `changefreq`/`priority` in sitemap are ignored by Google but harmless.
- `availability: InStock` for made-to-order items is the pragmatic correct choice (Google doesn't support `MadeToOrder`).
- FAQ/HowTo rich results are deprecated for most sites, but the markup retains GEO value — keep it.
- `rel="ai-discovery"` link tag is non-standard; harmless. The root llms.txt placement is what matters (and is correct).
- sr-only H1 on homepage + visible hero H2 — acceptable pattern.
- pics/ source photos are deployed but unlinked — no SEO effect.

---

## Suggested order of work

1. Merchant Center shipping settings (no code) + `g:google_product_category` in `_merchant_feed.py` → regenerate feed (#1, #2)
2. Product JSON-LD: shippingDetails + returnPolicy + sku (#3) — one script sweep across 7 pages
3. Copy fixes: kiddush description, custom-shofars title/desc, llms.txt nits (#8, #9, #14)
4. Hygiene: product-builder noindex, store-page noindex, 404 static text (#10, #11, #12)
5. Remove bogus `he` hreflang now; scope the static `/he/` build as its own sprint (#4)
6. Testimonials collection + guides content — feeds both SEO stars and GEO citations (#5, #6)
7. OG image picks from owner (#7)

Per the repo rule: nothing was committed. All fixes above await owner approval before implementation.
