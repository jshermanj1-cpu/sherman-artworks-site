# Copy guidelines

House rules for every piece of English and Hebrew copy on shermanartworks.com:
page text, titles and meta descriptions, alt text, JSON-LD, the inline
`PRODUCTS` arrays, `js/shofar-products.js`, `data/products.json`, `llms.txt`,
the merchant feeds, generator scripts that emit copy (`_*.py`), and the
customer emails (order confirmation, shipped and delivered builders).

Fix copy in its source, not in a generated file - see the generator chain in
`.githooks/README.md`. A regeneration puts the old wording back otherwise.

## American English only

Write all English copy in American English.

- Spelling: color, colorful, favorite, honor, behavior, center, centerpiece,
  centimeters, personalize, personalized, personalization, customize,
  organization, organized, emphasize, canceled, labeled, fulfill, mold,
  gray, inquiry (not enquiry), practice (verb and noun).
- Words: package (not parcel), ZIP / postal code (not postcode), right away
  (not straight away), ship / ships (prefer over dispatch).
- Dates: month first, written out - "October 12, 2026", not "12 October 2026".
  In code, format English dates with `'en-US'`, not `'en-GB'`.
- Change only text a customer, search engine or AI crawler can read. Code
  names keep their current spelling even where it is British - object keys
  (`personalisable`), `T_PAGE` keys (`personalise_btn`), CSS classes
  (`enquiry-form`), anchor ids (`#enquire`), analytics labels
  (`enquiry_form`), database columns and API values (`fulfilment_state`,
  `'cancelled'`). Renaming them breaks the modals, cart, links or data.
- Never rename URLs, slugs, product ids, SKUs or Cloudinary image ids for
  spelling.

Existing pages still carry British spellings; the full list with the file each
fix belongs in is the US English audit of 2026-10-13
(`sherman-artworks-planning/us-english-audit-2026-10-13.md`). New copy follows
this rule from now on.

## Owner's standing rules

- Plain hyphens only - no em dash or en dash anywhere, including ranges
  ("70-79 cm"). The Hebrew maqaf is fine.
- Every silver-plating mention says 925: "925 silver-plated",
  "925 silver plating", "ציפוי כסף 925".
- Never the word "sterling" (or "סטרלינג").
- Shipping is ₪35 in Israel and $45 international. There is no free
  shipping; state the figures plainly without defensive "never free" lines.
- "אבני החושן", never "אבני חושן".

`_guards.py` enforces the dash, "sterling" and free-shipping rules on every
push. The American English rule is not guarded yet, because the existing
British spellings would fail it.
