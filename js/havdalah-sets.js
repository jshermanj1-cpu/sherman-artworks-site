const PRODUCTS = [
  {
    "id": "black-havdalah-set",
    "family_id": "classic-havdalah-sets",
    "name_en": "Black Havdalah Set",
    "name_he": "סט הבדלה שחור",
    "description_en": "Handmade black Havdalah set, crafted in our studio in Israel.",
    "description_he": "סט הבדלה שחור בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Black",
    "color_he": "שחור",
    "measurements": "",
    "price_ils": 1369,
    "photos": ["Havdala_black_set_wdnnhk"]
  },
  {
    "id": "blue-havdalah-set",
    "family_id": "classic-havdalah-sets",
    "name_en": "Blue Havdalah Set",
    "name_he": "סט הבדלה כחול",
    "description_en": "Handmade blue Havdalah set, crafted in our studio in Israel.",
    "description_he": "סט הבדלה כחול בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Blue",
    "color_he": "כחול",
    "measurements": "",
    "price_ils": 1369,
    "photos": ["Blue_havdala_set_guzrpu"]
  },
  {
    "id": "white-havdalah-set",
    "family_id": "classic-havdalah-sets",
    "name_en": "White Havdalah Set",
    "name_he": "סט הבדלה לבן",
    "description_en": "Handmade white Havdalah set, crafted in our studio in Israel.",
    "description_he": "סט הבדלה לבן בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "White",
    "color_he": "לבן",
    "measurements": "",
    "price_ils": 1369,
    "photos": ["Havdala_white_set_wnymec"]
  },
  {
    "id": "orange-havdalah-set",
    "name_en": "Orange Havdalah Set",
    "name_he": "סט הבדלה כתום",
    "description_en": "Handmade orange Havdalah set, crafted in our studio in Israel.",
    "description_he": "סט הבדלה כתום בעבודת יד, מיוצר בסטודיו שלנו בישראל.",
    "color_en": "Orange",
    "color_he": "כתום",
    "measurements": "",
    "price_ils": 1212,
    "photos": ["Orange_havdala_set_bh5ut5"]
  }
];

function formatProductPrice(ils) {
  const main = "₪" + ils.toLocaleString("en-IL");
  if (!usdRate) return main;
  return main + ' <span class="product-card-price-alt">≈ $' + Math.round(ils / usdRate).toLocaleString("en-US") + "</span>";
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
  return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(message);
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

function renderProducts() {
  const grid = document.getElementById("grid-products");
  if (grid) grid.innerHTML = PRODUCTS.map(buildProductCard).join("");
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
