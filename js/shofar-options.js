/* Shofar size ladders and personalisation symbol sets.
 *
 * Shared by shofars.html and business-gifts.html, which both sell the custom
 * shofars. These used to be duplicated inline in each page, which meant a price
 * or symbol change had to be made twice and silently drifted when it wasn't.
 *
 * Prices are ILS and come from the shofar price table. Sizes always carry both
 * cm and inches, and the size LABEL is horn-specific - a kudu "XS" and a ram's
 * "XS" are different lengths - so never compare labels across horn types.
 *
 * Loaded before the inline <script> that defines PRODUCTS, because the product
 * arrays reference these consts directly.
 */

/* ── SIZE LADDERS ───────────────────────────────────────────────────────── */

// Decorated kudu designs. Sold in S and up only - Mini and XS exist in the
// price table but are not offered for the decorated range, so do not add them.
const KUDU_SIZES = [
  { label: 'S',  range_cm: '70–79',   range_in: '28–31', price_ils: 1214 },
  { label: 'M',  range_cm: '80–89',   range_in: '32–35', price_ils: 1308 },
  { label: 'L',  range_cm: '90–99',   range_in: '35–39', price_ils: 1417 },
  { label: 'XL', range_cm: '100–109', range_in: '39–43', price_ils: 1706 },
  { label: 'J',  range_cm: '110–119', range_in: '43–47', price_ils: 1762 },
  { label: 'XJ', range_cm: '120–129', range_in: '47–51', price_ils: 2423 },
];

// Ram's-horn custom: the full ram's range, Custom column pricing.
const RAMS_CUSTOM_SIZES = [
  { label: 'XS', range_cm: '30–34', range_in: '12–13', price_ils: 742 },
  { label: 'S',  range_cm: '35–39', range_in: '14–15', price_ils: 853 },
  { label: 'M',  range_cm: '40–44', range_in: '16–17', price_ils: 1064 },
  { label: 'L',  range_cm: '45–49', range_in: '18–19', price_ils: 1263 },
  { label: 'XL', range_cm: '50–54', range_in: '20–21', price_ils: 1492 },
  { label: 'J',  range_cm: '55–59', range_in: '22–23', price_ils: 1647 },
  { label: 'XJ', range_cm: '60–65', range_in: '24–26', price_ils: 2718 },
];

// Kudu custom: unlike the decorated kudu designs, this one IS made in Mini and
// XS, so it spans the full kudu range. Custom column pricing.
const KUDU_CUSTOM_SIZES = [
  { label: 'Mini', range_cm: '50–59',   range_in: '20–23', price_ils: 1297 },
  { label: 'XS',   range_cm: '60–69',   range_in: '24–27', price_ils: 1426 },
  { label: 'S',    range_cm: '70–79',   range_in: '28–31', price_ils: 1563 },
  { label: 'M',    range_cm: '80–89',   range_in: '32–35', price_ils: 1657 },
  { label: 'L',    range_cm: '90–99',   range_in: '35–39', price_ils: 1768 },
  { label: 'XL',   range_cm: '100–109', range_in: '39–43', price_ils: 2064 },
  { label: 'J',    range_cm: '110–119', range_in: '43–47', price_ils: 2113 },
  { label: 'XJ',   range_cm: '120–129', range_in: '47–51', price_ils: 2769 },
];

/* ── SYMBOL SETS ────────────────────────────────────────────────────────── */

// Symbol choices depend on the horn: kudu customs carry the full engraved
// design range, ram's-horn customs the smaller classic set. A product picks its
// set with "symbol_set"; anything unset falls back to the ram's list.
// The img values are Cloudinary public IDs for the live preview.
const SYMBOL_SETS = {
  rams: {
    en: ['Menorah', 'Jerusalem', 'Star of David', 'Lion of Judah'],
    he: { 'Menorah': 'מנורה', 'Jerusalem': 'ירושלים', 'Star of David': 'מגן דוד', 'Lion of Judah': 'אריה יהודה' },
    img: {
      'Menorah':       'Menorah_Tavnit_pq1die',
      'Jerusalem':     'Jerusalem_Tavnit_city_ksbaxm',
      'Star of David': 'Magen_David_tavnit_jsgmzi',
      'Lion of Judah': 'Lion_of_Judah_Tavnit_lunjfq',
    },
  },
  kudu: {
    en: ['Lions of Jerusalem', 'Menorah', 'Jerusalem', 'Star of David', 'Hoshen Stones',
         'Jerusalem Lions with Menorah', 'Holy Ark', 'The Spies (Meraglim)', 'Shofar Blowing'],
    he: {
      'Lions of Jerusalem':           'אריות ירושלים',
      'Menorah':                      'מנורה',
      'Jerusalem':                    'ירושלים',
      'Star of David':                'מגן דוד',
      'Hoshen Stones':                'אבני חושן',
      'Jerusalem Lions with Menorah': 'ירושלים אריות עם מנורה',
      'Holy Ark':                     'ארון הקודש',
      'The Spies (Meraglim)':         'המרגלים',
      'Shofar Blowing':               'תקיעה בשופר',
    },
    img: {
      'Lions of Jerusalem':           'Lions_Jerusalem_Tavnit_l2gors',
      'Menorah':                      'Menorah_Tavnit_vgllqe',
      'Jerusalem':                    'Jerusalem_Tavnit_ao9ylq',
      'Star of David':                'Magen_David_Tavnit_rw3npk',
      'Hoshen Stones':                'Hoshen_stones_Tavnit_ywmhiz',
      'Jerusalem Lions with Menorah': 'Lions_menorah_Jerusalem_Tavnit_rskagf',
      'Holy Ark':                     'Holy_ark_Tavnit_odecdg',
      'The Spies (Meraglim)':         'Merglim_Tavnit_emxygo',
      'Shofar Blowing':               'Shofar_blowing_Tavnit_eyjj7d',
    },
  },
};

// Offered on every set: "Other" opens the bespoke contact flow, "No Symbol"
// ships the horn plain. Neither has a preview image, by design.
const SYMBOL_EXTRAS_EN = ['Other', 'No Symbol'];
const SYMBOL_EXTRAS_HE = { 'Other': 'אחר', 'No Symbol': 'ללא סמל' };

function symbolSetFor(p) { return SYMBOL_SETS[(p && p.symbol_set) || 'rams']; }
function symbolOptionsFor(p) { return symbolSetFor(p).en.concat(SYMBOL_EXTRAS_EN); }
function symbolLabelFor(p, sym, l) {
  if (l !== 'he') return sym;
  return symbolSetFor(p).he[sym] || SYMBOL_EXTRAS_HE[sym] || sym;
}
function symbolImageFor(p, sym) { return symbolSetFor(p).img[sym] || null; }
