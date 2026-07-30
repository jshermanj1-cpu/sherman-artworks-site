# Sherman Art Works SKU Guide

This file is the source of truth for assigning Sherman Art Works stock keeping units (SKUs).
SKUs identify products for orders, the cart, WhatsApp messages, structured data, and product feeds.
They do not replace product IDs, URL anchors, or Google Merchant Center item IDs.

## Format

Use:

```text
SAW-{CATEGORY}-{PRODUCT NUMBER}-{SIZE}
```

Examples:

- Single-configuration product: `SAW-HG-001`
- Sized candlestick: `SAW-CS-004-S`
- Sized shofar: `SAW-SH-001-XS`
- Mini custom kudu shofar: `SAW-SH-022-MINI`

The size suffix is present only when the customer selects a size. Never add `STD`, `ONE`, or a
similar suffix to a product with one sellable configuration.

## Category codes

| Category | Code | Next unassigned number |
|---|---:|---:|
| Candlesticks | `CS` | `018` |
| Horn Goblets | `HG` | `004` |
| Kiddush Cups | `KC` | `021` |
| Trays & Bowls | `TB` | `009` |
| Mezuzahs | `MZ` | `005` |
| Shofars | `SH` | `023` |
| Havdalah Sets | `HS` | `005` |

The next-number column is a convenience, not the authority. Before assigning a SKU, scan this file
and `data/products.json` for the highest number already used in the category, then add one.

## Rules

1. Start every SKU with `SAW`.
2. Use the category code from the table above.
3. Use a three-digit product number, starting at `001` within each category.
4. Give every design one permanent base SKU.
5. For every product with a `sizes` array, give every sellable size its own SKU by appending the
   uppercase size label. This applies to every category, including candlesticks and shofars.
6. A product without selectable sizes uses its base SKU as its sellable SKU.
7. Reuse the same SKU when a product is cross-listed on more than one page.
8. Never encode a product name, color, price, page, or position into the SKU.
9. Never renumber or reuse an issued SKU, including after a product is discontinued.
10. Keep the existing product `id`, URL anchor, and merchant-feed `<g:id>` unchanged.
11. Before saving, verify that every base and variant SKU is unique across the entire catalog.

## Data model

Store the base SKU on the product:

```json
{
  "id": "lion-of-judah-goblet",
  "sku": "SAW-HG-002"
}
```

For a sized product, also store the explicit sellable SKU on every size:

```json
{
  "id": "white-silver-plated-glass-candlesticks",
  "sku": "SAW-CS-004",
  "sizes": [
    {
      "label": "S",
      "sku": "SAW-CS-004-S"
    },
    {
      "label": "M",
      "sku": "SAW-CS-004-M"
    },
    {
      "label": "L",
      "sku": "SAW-CS-004-L"
    }
  ]
}
```

The top-level SKU groups the design. The size SKU identifies the exact configuration ordered.
Page code that uses shared size ladders may derive the variant SKU from the product's base SKU and
the selected size label, but `data/products.json` must store each variant SKU explicitly.

## Where a SKU must appear

When a product is added or migrated, keep the SKU synchronized in:

1. The product object on its category page or `js/shofar-products.js`
2. `data/products.json`
3. Product JSON-LD (`sku`)
4. Cart line items and checkout
5. WhatsApp order messages
6. `merchant-feed.xml` as `<g:mpn>` while preserving the existing `<g:id>`
7. Any internal order or inventory tracker

The SKU is not required in `llms.txt` or `sitemap.xml`.

## Assignment procedure

1. Determine the product's real catalog category and category code.
2. Search this file and `data/products.json` for `SAW-{CODE}-`.
3. Find the highest base product number already issued in that category.
4. Assign the next number, padded to three digits.
5. Add the base SKU to the product.
6. If the product has sizes, add a variant SKU for every size label, regardless of category.
7. Search the repository for the full proposed SKU and confirm it occurs only where expected.
8. Regenerate derived catalog and merchant-feed files.
9. Verify that all SKUs are present, nonblank, and unique before deployment.
10. Update this guide's assignment table and next-number table in the same change.

## Initial assignments

These assignments are based on the `main` catalog on 2026-07-28: 65 products and 202 sellable
configurations. They are permanent once migrated into the product data.

### Candlesticks (`CS`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-CS-001` | `glass-circle-candlesticks` | Glass Circle Candlesticks | None |
| `SAW-CS-002` | `gold-colorful-glass-candlesticks` | Gold Colorful Glass Candlesticks | None |
| `SAW-CS-003` | `burgundy-glass-candlesticks` | Burgundy Glass Candlesticks | None |
| `SAW-CS-004` | `white-silver-plated-glass-candlesticks` | White 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-005` | `red-silver-plated-glass-candlesticks` | Red 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-006` | `blue-silver-plated-glass-candlesticks` | Blue 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-007` | `green-silver-plated-glass-candlesticks` | Green 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-008` | `black-silver-plated-glass-candlesticks` | Black 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-009` | `blue-green-silver-plated-glass-candlesticks` | Blue-Green 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-010` | `earth-silver-plated-glass-candlesticks` | Earth 925 Silver-Plated Glass Candlesticks | `-S`, `-M`, `-L` |
| `SAW-CS-011` | `black-white-stripes-candlesticks` | Black and White Stripes Candlesticks | None |
| `SAW-CS-012` | `gold-red-stripes-candlesticks` | Gold and Red Stripes Candlesticks | None |
| `SAW-CS-013` | `green-dots-candlesticks` | Green Dots Candlesticks | None |
| `SAW-CS-014` | `black-white-dots-candlesticks` | Black and White Dots Candlesticks | None |
| `SAW-CS-015` | `white-glass-candlesticks` | White Glass Candlesticks | None |
| `SAW-CS-016` | `clear-round-glass-candlesticks` | Clear Round Glass Candlesticks | None |
| `SAW-CS-017` | `clear-rectangular-glass-candlesticks` | Clear Rectangular Glass Candlesticks | None |

### Horn Goblets (`HG`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-HG-001` | `jerusalem-wine-horn` | Jerusalem Wine Horn | None |
| `SAW-HG-002` | `lion-of-judah-goblet` | Lion of Judah Goblet | None |
| `SAW-HG-003` | `menorah-goblet` | Menorah Goblet | None |

### Kiddush Cups (`KC`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-KC-001` | `tall-blue-glass-cup` | Tall Blue Glass Cup | None |
| `SAW-KC-002` | `tall-colorful-glass-cup` | Tall Colorful Glass Cup | None |
| `SAW-KC-003` | `tall-red-glass-cup` | Tall Red Glass Cup | None |
| `SAW-KC-004` | `low-white-glass-cup` | Low White Glass Cup | None |
| `SAW-KC-005` | `low-colorful-glass-cup` | Low Colorful Glass Cup | None |
| `SAW-KC-006` | `ceramic-kiddush-cup` | Ceramic Kiddush Cup | None |
| `SAW-KC-007` | `colorful-glass-cup-and-plate` | Colorful Glass Cup and Plate | None |
| `SAW-KC-008` | `kiddush-cup-plate` | Kiddush Cup Plate | None |
| `SAW-KC-009` | `blue-green-tall-glass-cup` | Blue-Green Tall Glass Cup | None |
| `SAW-KC-010` | `blue-tall-glass-cup` | Blue Tall Glass Cup | None |
| `SAW-KC-011` | `colorful-tall-glass-cup` | Colorful Tall Glass Cup | None |
| `SAW-KC-012` | `red-tall-glass-cup` | Red Tall Glass Cup | None |
| `SAW-KC-013` | `vibrant-red-glass-tall-cup` | Vibrant Red Glass Tall Cup | None |
| `SAW-KC-014` | `orange-glass-cup` | Orange Glass Cup | None |
| `SAW-KC-015` | `white-glass-cup` | White Glass Cup | None |
| `SAW-KC-016` | `blue-bore-pri-hagefen-tall-glass-cup` | Blue Bore Pri Hagefen Tall Glass Cup | None |
| `SAW-KC-017` | `blue-kiddush-cup-plate` | Blue Kiddush Cup Plate | None |
| `SAW-KC-018` | `white-kiddush-cup-plate` | White Kiddush Cup Plate | None |
| `SAW-KC-019` | `blue-green-kiddush-cup-plate` | Blue-Green Kiddush Cup Plate | None |
| `SAW-KC-020` | `red-kiddush-cup-plate` | Red Kiddush Cup Plate | None |

### Trays & Bowls (`TB`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-TB-001` | `glass-decorative-bowl` | Glass Decorative Bowl | None |
| `SAW-TB-002` | `white-silver-plated-glass-tray` | White 925 Silver-Plated Glass Tray | None |
| `SAW-TB-003` | `red-silver-plated-glass-tray` | Red 925 Silver-Plated Glass Tray | None |
| `SAW-TB-004` | `blue-silver-plated-glass-tray` | Blue 925 Silver-Plated Glass Tray | None |
| `SAW-TB-005` | `green-silver-plated-glass-tray` | Green 925 Silver-Plated Glass Tray | None |
| `SAW-TB-006` | `black-silver-plated-glass-tray` | Black 925 Silver-Plated Glass Tray | None |
| `SAW-TB-007` | `blue-green-silver-plated-glass-tray` | Blue-Green 925 Silver-Plated Glass Tray | None |
| `SAW-TB-008` | `test-tray-product` | Test Tray Product | None |

### Mezuzahs (`MZ`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-MZ-001` | `oryx-mezuzah` | Oryx Mezuzah | None |
| `SAW-MZ-002` | `ram-mezuzah` | Ram Mezuzah | None |
| `SAW-MZ-003` | `kudu-mezuzah` | Kudu Mezuzah | None |
| `SAW-MZ-004` | `clear-glass-mezuzah` | Clear Glass Mezuzah | None |

### Shofars (`SH`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-SH-001` | `custom-shofar` | Custom Ram's Horn Shofar, Symbol & Text | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-002` | `kudu-hoshen-stones` | Kudu Shofar - Hoshen Stones | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-003` | `kudu-jerusalem-lions` | Kudu Shofar - Jerusalem Lions | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-004` | `kudu-jerusalem-lions-menorah` | Kudu Shofar - Jerusalem Lions with Menorah | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-005` | `kudu-holy-ark` | Kudu Shofar - The Holy Ark | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-006` | `kudu-spies-meraglim` | Kudu Shofar - The Spies (Meraglim) | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-007` | `kudu-messianic-seal-jerusalem` | Kudu Shofar - Messianic Seal of Jerusalem | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-008` | `kudu-jerusalem` | Kudu Shofar - Jerusalem | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-009` | `kudu-star-of-david` | Kudu Shofar - Star of David | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-010` | `kudu-menorah` | Kudu Shofar - Menorah | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-011` | `kudu-shofar-blowing` | Kudu Shofar - Shofar Blowing | `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-012` | `rams-hoshen-stones` | Ram's Horn Shofar - Hoshen Stones | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-013` | `rams-jerusalem` | Ram's Horn Shofar - Jerusalem | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-014` | `rams-star-of-david` | Ram's Horn Shofar - Star of David | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-015` | `rams-star-of-david-blue-crystals` | Ram's Horn Shofar - Star of David with Blue Crystals | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-016` | `rams-tka-beshofar-gadol` | Ram's Horn Shofar - Tka BeShofar Gadol | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-017` | `rams-jerusalem-lions` | Ram's Horn Shofar - Jerusalem Lions | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-018` | `rams-jerusalem-white-crystals` | Ram's Horn Shofar - Jerusalem with White Crystals | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-019` | `rams-star-of-david-blue-stone` | Ram's Horn Shofar - Star of David with Blue Stone | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-020` | `rams-messianic-seal-jerusalem` | Ram's Horn Shofar - Messianic Seal of Jerusalem | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-021` | `rams-menorah` | Ram's Horn Shofar - Menorah | `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |
| `SAW-SH-022` | `custom-kudu-shofar` | Custom Kudu Shofar, Symbol & Text | `-MINI`, `-XS`, `-S`, `-M`, `-L`, `-XL`, `-J`, `-XJ` |

### Havdalah Sets (`HS`)

| Base SKU | Product ID | Product | Size suffixes |
|---|---|---|---|
| `SAW-HS-001` | `black-havdalah-set` | Black Havdalah Set | None |
| `SAW-HS-002` | `blue-havdalah-set` | Blue Havdalah Set | None |
| `SAW-HS-003` | `white-havdalah-set` | White Havdalah Set | None |
| `SAW-HS-004` | `orange-havdalah-set` | Orange Havdalah Set | None |
