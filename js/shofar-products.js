/* Shofar catalogue - the single source of truth for every shofar on the site.
 *
 * Shared by shofars.html (all shofars, shuffled) and the three sub-category
 * pages: shofars-custom.html, shofars-rams.html, shofars-kudu.html. It used to
 * live inline in shofars.html, but with four pages selling the same catalogue an
 * inline copy per page would drift the moment a price or photo changed.
 *
 * Each page picks what it shows with PAGE_PRODUCT_IDS; product order on this
 * array is the canonical order (used by the sub-pages and the JSON-LD).
 *
 * Loaded after js/shofar-options.js, whose size ladders and symbol sets the
 * entries reference directly, and before the page's inline <script>.
 *
 * Display flags:
 *   personalisable - opens the symbol/inscription/comment panel in the modal
 *   plating_note   - ram's horn: silver plating may come in one piece or two
 *   allow_comment  - render the comment box even without personalisation
 */

const PRODUCTS = [
  {
    "id": "custom-shofar",
    "name_en": "Custom Ram's Horn Shofar, Symbol & Text",
    "name_he": "שופר איל מותאם אישית, סמל וטקסט",
    "description_en": "A handmade shofar personalised with your choice of symbol and an optional text inscription (Hebrew/English). Made to order in our studio in Israel.",
    "description_he": "שופר עשוי בעבודת יד, מותאם אישית עם בחירת סמל וכיתוב אישי (עברית/English). מיוצר לפי הזמנה בסטודיו שלנו בישראל.",
    "measurements": "",
    "price_ils": 742,
    "personalisable": true,
    "sizes": RAMS_CUSTOM_SIZES,
    "symbol_set": "rams",
    "photos": ["Cover_silver_Magen_David_with_name_adq1oi"],
    "plating_note": true
  },
  {
    "id": "custom-kudu-shofar",
    "name_en": "Custom Kudu Shofar, Symbol & Text",
    "name_he": "שופר קודו מותאם אישית, סמל וטקסט",
    "description_en": "Kudu-horn shofar decorated in 925 silver and personalised with your choice of symbol and an optional text inscription (Hebrew/English). Made to order in our studio in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925, מותאם אישית עם בחירת סמל וכיתוב אישי (עברית/English). מיוצר לפי הזמנה בסטודיו שלנו בישראל.",
    "measurements": "",
    "price_ils": 1297,
    "personalisable": true,
    "sizes": KUDU_CUSTOM_SIZES,
    "symbol_set": "kudu",
    "photos": ["Name_kudu_shofar_hqdju6"]
  },
  {
    "id": "kudu-hoshen-stones",
    "name_en": "Kudu Shofar – Hoshen Stones",
    "name_he": "שופר קודו אבני חושן",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the twelve stones of the High Priest's breastplate (Hoshen). Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם שנים-עשר אבני החושן של הכהן הגדול. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_Hoshen_stones_endmuo", "Kudu_Hoshen_stones_2_vqf5vu"]
  },
  {
    "id": "kudu-jerusalem-lions",
    "name_en": "Kudu Shofar – Jerusalem Lions",
    "name_he": "שופר קודו אריות ירושלים",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the lions of Jerusalem. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם אריות ירושלים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_Jerusalem_Lions_xelufl", "Jerusalem_Lions_yvs00x"]
  },
  {
    "id": "kudu-jerusalem-lions-menorah",
    "name_en": "Kudu Shofar – Jerusalem Lions with Menorah",
    "name_he": "שופר קודו ירושלים אריות עם מנורה",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the lions of Jerusalem and a seven-branched menorah. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם אריות ירושלים ומנורת שבעת הקנים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_Jerusalem_Lions_with_menorah_rh4cto", "Jerusalem_Lions_with_menorah_eb0mwb"]
  },
  {
    "id": "kudu-holy-ark",
    "name_en": "Kudu Shofar – The Holy Ark",
    "name_he": "שופר קודו ארון הקודש",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the Holy Ark (Aron HaKodesh). Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם ארון הקודש. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_The_holy_ark_fcpqui", "The_holy_ark_pnxpcv"]
  },
  {
    "id": "kudu-spies-meraglim",
    "name_en": "Kudu Shofar – The Spies (Meraglim)",
    "name_he": "שופר קודו המרגלים",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the Spies (Meraglim) carrying the cluster of grapes. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם המרגלים ואשכול הענבים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_The_spies_Meraglim_h6ts6a", "The_spies_Meraglim_iwcj1i"]
  },
  {
    "id": "kudu-messianic-seal-jerusalem",
    "name_en": "Kudu Shofar – Messianic Seal of Jerusalem",
    "name_he": "שופר קודו חותמת ירושלים אוונגליסטי",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the Messianic Seal of Jerusalem - the menorah, fish and Star of David. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם חותמת ירושלים המשיחית - מנורה, דג ומגן דוד. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Messianic_Seal_of_Jerusalem_kudu_jxptwr", "Messianic_Seal_of_Jerusalem_m9274d"]
  },
  {
    "id": "kudu-jerusalem",
    "name_en": "Kudu Shofar – Jerusalem",
    "name_he": "שופר קודו ירושלים",
    "description_en": "Kudu-horn shofar decorated in 925 silver with a view of Jerusalem. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם נוף ירושלים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Jerusalem_kudu_hni3gi", "Jerusalem_uyvuoa"]
  },
  {
    "id": "kudu-star-of-david",
    "name_en": "Kudu Shofar – Star of David",
    "name_he": "שופר קודו מגן דוד",
    "description_en": "Kudu-horn shofar decorated in 925 silver with the Star of David. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם מגן דוד. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Magen_david_kudu_g7rfto", "Magen_David_t2gtml"]
  },
  {
    "id": "kudu-menorah",
    "name_en": "Kudu Shofar – Menorah",
    "name_he": "שופר קודו מנורה",
    "description_en": "Kudu-horn shofar decorated in 925 silver with a seven-branched menorah. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם מנורת שבעת הקנים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Kudu_menorah_joe2bm", "Menorah_miblnm"]
  },
  {
    "id": "kudu-shofar-blowing",
    "name_en": "Kudu Shofar – Shofar Blowing",
    "name_he": "שופר קודו תקיעה בשופר",
    "description_en": "Kudu-horn shofar decorated in 925 silver with a depiction of the shofar blowing. Handmade in Israel.",
    "description_he": "שופר מקרן קודו מעוטר בכסף 925 עם דמות התוקע בשופר. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 1214,
    "sizes": KUDU_SIZES,
    "photos": ["Shofar_blowing_kudu_i490tf", "Shofar_blowing_alriud"]
  },
  {
    "id": "rams-hoshen-stones",
    "name_en": "Ram's Horn Shofar – Hoshen Stones",
    "name_he": "שופר איל אבני חושן",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the twelve stones of the High Priest's breastplate (Hoshen). Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם שנים-עשר אבני החושן של הכהן הגדול. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Hoshen_ram_1_piece_c1mxfo", "Hoshen_stones_ram_shofar_two_pieces_lghmo8"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-jerusalem",
    "name_en": "Ram's Horn Shofar – Jerusalem",
    "name_he": "שופר איל ירושלים",
    "description_en": "Ram's-horn shofar decorated in 925 silver with a view of Jerusalem. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם נוף ירושלים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Jerusalem_ram_2_svqanp", "Jerusalem_ram_shofar_btpd89", "Jerusalem2_pieces_ram_myotlb"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-star-of-david",
    "name_en": "Ram's Horn Shofar – Star of David",
    "name_he": "שופר איל מגן דוד",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the Star of David. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם מגן דוד. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Magen_David_1_ram_pgvhoa", "Magen_David_2_ram_jkcyn3"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-star-of-david-blue-crystals",
    "name_en": "Ram's Horn Shofar – Star of David with Blue Crystals",
    "name_he": "שופר איל מגן דוד וקריסטלים כחולים",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the Star of David set with blue crystals. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם מגן דוד משובץ קריסטלים כחולים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Magen_Daviittke_blue_stones_1_ram_s2dopc", "Magen_David_little_blue_stones_2_ram_vtgefr"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-tka-beshofar-gadol",
    "name_en": "Ram's Horn Shofar – Tka BeShofar Gadol",
    "name_he": "שופר איל בכיתוב תקע בשופר גדול",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the inscription 'Tka BeShofar Gadol' - Sound the great shofar. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם הכיתוב 'תקע בשופר גדול'. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Tka_be_shofar_1_zztbld", "Tka_be_shofar_2_thx7dp", "Tka_be_shofar_3_ce497k"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-jerusalem-lions",
    "name_en": "Ram's Horn Shofar – Jerusalem Lions",
    "name_he": "שופר איל אריות ירושלים",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the lions of Jerusalem. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם אריות ירושלים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Jerusalem_lions_1_goiw6c", "Jerusalem_lions_2_hbl0jk"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-jerusalem-white-crystals",
    "name_en": "Ram's Horn Shofar – Jerusalem with White Crystals",
    "name_he": "שופר איל עם קריסטלים לבנים",
    "description_en": "Ram's-horn shofar decorated in 925 silver with a view of Jerusalem set with white crystals. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם נוף ירושלים משובץ קריסטלים לבנים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Jerusalem_white_stones_1_ram_x44ixt", "Jerusalem_white_stones_2_ram_ltfp1v"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-star-of-david-blue-stone",
    "name_en": "Ram's Horn Shofar – Star of David with Blue Stone",
    "name_he": "שופר איל עם אבן כחולה מרכזית",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the Star of David and a central blue stone. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם מגן דוד ואבן כחולה מרכזית. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Magen_Davidblue_stone_1_ram_mz7hi4", "Magen_David_blue_stone_2_ram_zr7oqo"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-messianic-seal-jerusalem",
    "name_en": "Ram's Horn Shofar – Messianic Seal of Jerusalem",
    "name_he": "שופר איל עם חתם אוונגליסטי של ירושלים",
    "description_en": "Ram's-horn shofar decorated in 925 silver with the Messianic Seal of Jerusalem - the menorah, fish and Star of David. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם חתם ירושלים המשיחי - מנורה, דג ומגן דוד. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["Messianic_Seal_ram_1_ct3nlp", "Messianic_Seal_2_ram_qxybqu"],
    "plating_note": true,
    "allow_comment": true
  },
  {
    "id": "rams-menorah",
    "name_en": "Ram's Horn Shofar – Menorah",
    "name_he": "שופר איל מנורה",
    "description_en": "Ram's-horn shofar decorated in 925 silver with a seven-branched menorah. Handmade in Israel.",
    "description_he": "שופר מקרן איל מעוטר בכסף 925 עם מנורת שבעת הקנים. עבודת יד בישראל.",
    "measurements": "",
    "price_ils": 418,
    "sizes": RAMS_SIZES,
    "photos": ["2510F8BA-2BF5-4BB0-B67F-C9AFB537F6C8_jpx0wa", "Menorah_2_uldtxg"],
    "plating_note": true,
    "allow_comment": true
  }
];

/* ── PAGE GROUPS ──────────────────────────────────────────────────────────
 * What each of the four shofar pages shows. The sub-category pages lead with
 * their own custom shofar and then the designs; the landing page shows the
 * whole catalogue in random order. The design lists are derived from the array
 * above by id prefix, so a new shofar reaches its page on its own.
 */
const PAGE_GROUPS = {
  all:    null,
  custom: ['custom-shofar', 'custom-kudu-shofar'],
  rams:   ['custom-shofar'].concat(PRODUCTS.filter(function (p) { return p.id.indexOf('rams-') === 0; }).map(function (p) { return p.id; })),
  kudu:   ['custom-kudu-shofar'].concat(PRODUCTS.filter(function (p) { return p.id.indexOf('kudu-') === 0; }).map(function (p) { return p.id; })),
};

// PRODUCTS indices to render, in display order. Call once per page load: the
// 'all' shuffle must survive a language or currency toggle, which re-renders.
function buildPageOrder(pageKey) {
  var ids = PAGE_GROUPS[pageKey];
  if (!ids) {
    var order = PRODUCTS.map(function (_, i) { return i; });
    for (var i = order.length - 1; i > 0; i--) {   // Fisher-Yates
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
    }
    return order;
  }
  return ids
    .map(function (id) { return PRODUCTS.findIndex(function (p) { return p.id === id; }); })
    .filter(function (i) { return i >= 0; });
}
