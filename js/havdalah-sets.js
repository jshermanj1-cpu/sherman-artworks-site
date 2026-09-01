const PRODUCTS = [
  {
    "id": "black-havdalah-set",
    "sku": "SAW-HS-001",
    "family_id": "classic-havdalah-sets",
    "finish": "silver-plated",
    "name_en": "925 Silver-Plated Black Havdalah Set",
    "name_he": "סט הבדלה שחור בציפוי כסף 925",
    "description_en": "Handmade black glass Havdalah set with 925 silver plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה שחור מזכוכית בציפוי כסף 925, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Black",
    "color_he": "שחור",
    "measurements": "",
    "price_ils": 1506,
    "photos": ["Havdala_black_set_wdnnhk"]
  },
  {
    "id": "blue-havdalah-set",
    "sku": "SAW-HS-002",
    "family_id": "classic-havdalah-sets",
    "finish": "silver-plated",
    "name_en": "925 Silver-Plated Blue Havdalah Set",
    "name_he": "סט הבדלה כחול בציפוי כסף 925",
    "description_en": "Handmade blue glass Havdalah set with 925 silver plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה כחול מזכוכית בציפוי כסף 925, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Blue",
    "color_he": "כחול",
    "measurements": "",
    "price_ils": 1506,
    "photos": ["Blue_havdala_set_guzrpu"]
  },
  {
    "id": "white-havdalah-set",
    "sku": "SAW-HS-003",
    "family_id": "classic-havdalah-sets",
    "finish": "silver-plated",
    "name_en": "925 Silver-Plated White Havdalah Set",
    "name_he": "סט הבדלה לבן בציפוי כסף 925",
    "description_en": "Handmade white glass Havdalah set with 925 silver plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה לבן מזכוכית בציפוי כסף 925, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "White",
    "color_he": "לבן",
    "measurements": "",
    "price_ils": 1506,
    "photos": ["Havdala_white_set_wnymec"]
  },
  {
    "id": "orange-havdalah-set",
    "sku": "SAW-HS-004",
    "finish": "silver-plated",
    "name_en": "925 Silver-Plated Orange Havdalah Set",
    "name_he": "סט הבדלה כתום בציפוי כסף 925",
    "description_en": "Handmade orange glass Havdalah set with 925 silver plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה כתום מזכוכית בציפוי כסף 925, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Orange",
    "color_he": "כתום",
    "measurements": "",
    "price_ils": 1334,
    "photos": ["Orange_havdala_set_bh5ut5"]
  },
  {
    "id": "gold-plated-black-havdalah-set",
    "sku": "SAW-HS-005",
    "family_id": "gold-plated-havdalah-sets",
    "finish": "gold-plated",
    "name_en": "Gold-Plated Black Havdalah Set",
    "name_he": "סט הבדלה מזכוכית שחורה בציפוי זהב",
    "description_en": "Handmade black glass Havdalah set with gold plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה מזכוכית שחורה בציפוי זהב, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Black",
    "color_he": "שחור",
    "measurements": "",
    "price_ils": 1657,
    "photos": ["Black_havdalah_set_gold_zblb7f"]
  },
  {
    "id": "gold-plated-blue-havdalah-set",
    "sku": "SAW-HS-006",
    "family_id": "gold-plated-havdalah-sets",
    "finish": "gold-plated",
    "name_en": "Gold-Plated Blue Havdalah Set",
    "name_he": "סט הבדלה מזכוכית כחולה בציפוי זהב",
    "description_en": "Handmade blue glass Havdalah set with gold plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה מזכוכית כחולה בציפוי זהב, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Blue",
    "color_he": "כחול",
    "measurements": "",
    "price_ils": 1657,
    "photos": ["Blue_havdalah_set_gold_kqrs67"]
  },
  {
    "id": "gold-plated-orange-havdalah-set",
    "sku": "SAW-HS-007",
    "family_id": "gold-plated-havdalah-sets",
    "finish": "gold-plated",
    "name_en": "Gold-Plated Orange Havdalah Set",
    "name_he": "סט הבדלה מזכוכית כתומה בציפוי זהב",
    "description_en": "Handmade orange glass Havdalah set with gold plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה מזכוכית כתומה בציפוי זהב, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Orange",
    "color_he": "כתום",
    "measurements": "",
    "price_ils": 1467,
    "photos": ["Orange_havdalah_set_gold_ona5jl"]
  },
  {
    "id": "gold-plated-red-havdalah-set",
    "sku": "SAW-HS-008",
    "family_id": "gold-plated-havdalah-sets",
    "finish": "gold-plated",
    "name_en": "Gold-Plated Red Havdalah Set",
    "name_he": "סט הבדלה מזכוכית אדומה בציפוי זהב",
    "description_en": "Handmade red glass Havdalah set with gold plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה מזכוכית אדומה בציפוי זהב, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Red",
    "color_he": "אדום",
    "measurements": "",
    "price_ils": 1657,
    "photos": ["Red_havdalah_set_gold_xf0lnu"]
  },
  {
    "id": "gold-plated-white-havdalah-set",
    "sku": "SAW-HS-009",
    "family_id": "gold-plated-havdalah-sets",
    "finish": "gold-plated",
    "name_en": "Gold-Plated White Havdalah Set",
    "name_he": "סט הבדלה מזכוכית לבנה בציפוי זהב",
    "description_en": "Handmade white glass Havdalah set with gold plating, crafted in our studio in Israel.",
    "description_he": "סט הבדלה מזכוכית לבנה בציפוי זהב, בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "White",
    "color_he": "לבן",
    "measurements": "",
    "price_ils": 1657,
    "photos": ["White_havdalah_set_gold_nxxpbc"]
  }
];

// Delegates to formatMoney in js/site.js, like every category page does.
function formatProductPrice(ils, exempt) {
  return formatMoney(ils, exempt);
}

function productName(product) {
  return currentLang === "he" ? product.name_he : product.name_en;
}

function productDescription(product) {
  return currentLang === "he" ? product.description_he : product.description_en;
}

function productWhatsApp(product) {
  const name = productName(product);
  const message = currentLang === "he"
    ? 'שלום, אני מתעניין/ת ב"' + name + '". אשמח לפרטים נוספים.'
    : 'Hi, I would like to know more about "' + name + '".';
  return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(message + "\nSKU: " + productSku(product));
}

function buildProductCard(product, index) {
  const name = productName(product);
  const description = productDescription(product);
  return '<article class="product-card" id="' + product.id + '" onclick="openModal(' + index + ')">' +
    '<div class="product-card-img-wrap"><img class="product-card-img" loading="lazy" src="' +
    CDN + "/w_600,c_fit,q_auto,f_auto/" + product.photos[0] + '.jpg" alt="' + escapeAttr(name) + '" /></div>' +
    '<div class="product-card-body"><h2 class="product-card-name">' + escapeHtml(name) + "</h2>" +
    '<p class="product-card-desc">' + escapeHtml(description) + '</p><div class="product-card-meta">' +
    '<span class="product-card-price">' + formatProductPrice(product.price_ils) + "</span></div>" +
    '<p class="product-color-note">' + escapeHtml(T_SITE[currentLang].color_note) + "</p>" +
    '<div class="product-card-actions"><button class="btn-cart" onclick="event.stopPropagation();cartAddFromProduct(' + index + ')">' +
    escapeHtml(T_SITE[currentLang].add_cart) + '</button><div class="product-card-secondary-actions">' +
    '<button class="btn-details" onclick="event.stopPropagation();openModal(' + index + ')">' +
    escapeHtml(T_PAGE[currentLang].view_details) + '</button><a class="btn-order" target="_blank" rel="noopener noreferrer" href="' +
    productWhatsApp(product) + '" onclick="event.stopPropagation()">' + escapeHtml(T_PAGE[currentLang].modal_order) +
    "</a></div></div></div></article>";
}

let productDisplayOrder = null;

function renderProducts() {
  const grid = document.getElementById("grid-products");
  if (!productDisplayOrder) {
    const ids = (typeof SECTIONS !== "undefined" && SECTIONS.products && SECTIONS.products.length)
      ? SECTIONS.products : null;
    const visible = ids ? PRODUCTS.filter(function(p) { return ids.indexOf(p.id) >= 0; }) : PRODUCTS;
    productDisplayOrder = shuffledProductEntries(visible);
  }
  if (grid) {
    grid.innerHTML = productDisplayOrder
      .map(function(entry) { return buildProductCard(entry.p, entry.idx); })
      .join("");
  }
}

let currentModalIdx = null;

function openModal(index) {
  if (!PRODUCTS[index]) return;
  currentModalIdx = index;
  renderModal();
  document.getElementById("productModal").classList.add("open");
  document.body.style.overflow = "hidden";
  history.replaceState(null, "", "#" + PRODUCTS[index].id);
}

function closeModal() {
  document.getElementById("productModal").classList.remove("open");
  document.body.style.overflow = "";
  history.replaceState(null, "", location.pathname + location.search);
  currentModalIdx = null;
}

function renderModalColorPicker(product) {
  const row = document.getElementById("modalColorRow");
  const options = document.getElementById("modalColorOptions");
  const family = product.family_id
    ? PRODUCTS.map((item, index) => ({ item, index })).filter(({ item }) => item.family_id === product.family_id)
    : [];
  if (family.length < 2) {
    row.style.display = "none";
    options.innerHTML = "";
    return;
  }
  options.innerHTML = family.map(({ item, index }) => {
    const color = currentLang === "he" ? item.color_he : item.color_en;
    return '<button type="button" class="variant-color-option" aria-pressed="' +
      (index === currentModalIdx ? "true" : "false") + '" data-product-id="' + item.id +
      '" onclick="selectModalColor(' + index + ')"><img src="' + CDN +
      "/w_120,h_120,c_fill,g_auto,q_auto,f_auto/" + item.photos[0] +
      '.jpg" alt="" loading="lazy" /><span>' + escapeHtml(color) + "</span></button>";
  }).join("");
  row.style.display = "";
}

function selectModalColor(index) {
  if (!PRODUCTS[index]) return;
  currentModalIdx = index;
  renderModal();
  history.replaceState(null, "", "#" + PRODUCTS[index].id);
  requestAnimationFrame(function() {
    const selected = document.querySelector('.variant-color-option[data-product-id="' + PRODUCTS[index].id + '"]');
    if (selected) selected.focus();
  });
}

function renderModal() {
  if (currentModalIdx == null) return;
  const product = PRODUCTS[currentModalIdx];
  const name = productName(product);
  const altName = currentLang === "he" ? product.name_en : product.name_he;
  document.getElementById("modalName").textContent = name;
  document.getElementById("modalNameAlt").textContent = altName;
  document.getElementById("modalDesc").textContent = productDescription(product);
  document.getElementById("modalPrice").innerHTML = formatProductPrice(product.price_ils);
  document.getElementById("modalMainImg").src = CDN + "/q_auto,f_auto/" + product.photos[0] + ".jpg";
  document.getElementById("modalMainImg").alt = name;
  document.getElementById("modalOrderCta").href = productWhatsApp(product);
  renderModalColorPicker(product);
}

document.addEventListener("keydown", function(event) {
  if (event.key === "Escape" && currentModalIdx != null) closeModal();
});

document.addEventListener("DOMContentLoaded", function() {
  renderProducts();
  const slug = location.hash.slice(1);
  const index = PRODUCTS.findIndex(function(product) { return product.id === slug; });
  if (index >= 0) openModal(index);
});
