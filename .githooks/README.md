# Git hooks

## One-time setup, per clone

Hooks live here rather than in `.git/hooks` so they are version controlled.
Git does not pick that up on its own, so each clone needs this once:

```bash
git config core.hooksPath .githooks
```

Worktrees share the main repository's config, so setting it once covers every
worktree of the same clone.

To check it took:

```bash
git config core.hooksPath
```

## What runs

`pre-push` runs `_guards.py`, which takes about twenty seconds and checks
fifteen invariants across every page in both languages:

- every Product offer declares `shippingDetails` and `hasMerchantReturnPolicy`
- Hebrew pages name their products in Hebrew
- structured-data names actually appear on the page
- FAQ answers are rendered, not only marked up
- all JSON-LD parses
- the sitemap lists no noindex page, and every URL in it resolves
- every indexable page links the accessibility statement
- card dollar figures match the price checkout charges
- the house copy rules: plain hyphens only, never "sterling", never free shipping
- static cards match `data/products.json`
- the shofar sizing table is current
- SKUs, JSON-LD and the merchant feed agree

A push to `main` is **blocked** when any of these fail, because GitHub Pages
deploys `main` straight to the live site. On any other branch the guards still
run and report, but the push is allowed.

```bash
git push --no-verify     # bypass deliberately
python _guards.py        # run by hand, any time
```

## Why

Every check exists because that thing actually broke and nothing noticed. The
shape is always the same: a product is added, the generator chain is not re-run,
and the page still looks correct in a browser because JavaScript rebuilds it -
while the crawler-visible half, the structured data and the dollar figures
quietly disagree with the catalogue. On 2026-09-01 that had left 198 of 482
offers without shipping and returns, 153 of 153 dollar figures understated, and
the whole gold-plated line invisible to every AI crawler.

If a guard fails, the fix is almost always to re-run the chain and commit what
changes:

```bash
python _static_cards.py && python _subcategory_pages.py && python _shofar_pages.py \
  && python _bake_en.py && python _offer_schema.py && python _he_pages.py \
  && python _merchant_feed.py
```
