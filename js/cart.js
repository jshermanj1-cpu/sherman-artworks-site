/* ═══════════════════════════════════════════════════════════════
   cart.js - Shopping cart for Sherman Art Works
   Sprint 18 - WhatsApp-first cart, Phase A
   ═══════════════════════════════════════════════════════════════ */

// ── CART STORE ─────────────────────────────────────────────────
const CART_KEY = 'sa_cart';

// Product page per slug - lets cart items link back to their product page
// even for items added before the `page` field existed.
var _PAGE_BY_SLUG = {
  'glass-circle-candlesticks': 'candlesticks.html',
  'gold-colorful-glass-candlesticks': 'candlesticks.html',
  'burgundy-glass-candlesticks': 'candlesticks.html',
  'jerusalem-wine-horn': 'shofars-goblets.html',
  'lion-of-judah-goblet': 'shofars-goblets.html',
  'menorah-goblet': 'shofars-goblets.html',
  'glass-decorative-bowl': 'trays-bowls.html',
  'oryx-mezuzah': 'mezuzahs.html',
  'black-white-stripes-candlesticks': 'candlesticks.html',
  'gold-red-stripes-candlesticks': 'candlesticks.html',
  'green-dots-candlesticks': 'candlesticks.html',
  'black-white-dots-candlesticks': 'candlesticks.html',
  'white-glass-candlesticks': 'candlesticks.html',
  'clear-round-glass-candlesticks': 'candlesticks.html',
  'clear-rectangular-glass-candlesticks': 'candlesticks.html',
  'ram-mezuzah': 'mezuzahs.html',
  'kudu-mezuzah': 'mezuzahs.html',
  'clear-glass-mezuzah': 'mezuzahs.html',
  'tall-blue-glass-cup': 'kiddush-cups.html',
  'tall-colorful-glass-cup': 'kiddush-cups.html',
  'tall-red-glass-cup': 'kiddush-cups.html',
  'low-white-glass-cup': 'kiddush-cups.html',
  'low-colorful-glass-cup': 'kiddush-cups.html',
  'ceramic-kiddush-cup': 'kiddush-cups.html',
  'colorful-glass-cup-and-plate': 'kiddush-cups.html',
  'kiddush-cup-plate': 'kiddush-cups.html',
  'custom-shofar': 'custom-shofars.html'
};

// Hebrew symbol names for personalised items (page SYMBOL_HE maps are function-scoped).
var _SYMBOL_HE = { 'Menorah': 'מנורה', 'Jerusalem': 'ירושלים', 'Star of David': 'מגן דוד', 'Lion of Judah': 'אריה יהודה', 'Other': 'אחר', 'No Symbol': 'ללא סמל' };

function _cartItemUrl(item) {
  var page = item.page || _PAGE_BY_SLUG[item.slug];
  return page ? page + '#' + item.slug : null;
}

// Line-item identity: personalised items carry their meta in the key so two
// shofars with different inscriptions stay separate lines.
function _cartKey(item) {
  return item.key || item.slug;
}

function getCart() {
  try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
  catch (e) { return []; }
}

function _saveCart(items) {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
  document.dispatchEvent(new CustomEvent('sa:cart-change', { detail: { cart: items } }));
}

function addToCart(slug, name_en, name_he, price_ils, photo, meta) {
  var items = getCart();
  var key = meta ? slug + '::' + [meta.symbol || '', meta.text || '', meta.comment || ''].join('|') : slug;
  var page = (location.pathname.split('/').pop() || 'index.html');
  var existing = items.find(function (i) { return _cartKey(i) === key; });
  if (existing) {
    existing.qty += 1;
  } else {
    var entry = { slug: slug, key: key, page: page, name_en: name_en, name_he: name_he || '', price_ils: price_ils, photo: photo, qty: 1 };
    if (meta) entry.meta = meta;
    items.push(entry);
  }
  _saveCart(items);
  if (typeof trackGA4 === 'function') {
    trackGA4('add_to_cart', {
      currency: 'ILS', value: price_ils,
      items: [{ item_id: slug, item_name: name_en, price: price_ils, quantity: 1 }]
    });
  }
  if (typeof a11yAnnounce === 'function') {
    var addedMsg = (typeof T_SITE !== 'undefined' && T_SITE[currentLang] && T_SITE[currentLang].cart_item_added) || 'Item added to cart';
    var itemName = (currentLang === 'he' && name_he) ? name_he : name_en;
    a11yAnnounce(itemName + ': ' + addedMsg);
  }
  openCartDrawer();
}

function removeFromCart(key) {
  if (typeof a11yAnnounce === 'function') {
    var removedMsg = (typeof T_SITE !== 'undefined' && T_SITE[currentLang] && T_SITE[currentLang].cart_item_removed) || 'Item removed from cart';
    a11yAnnounce(removedMsg);
  }
  _saveCart(getCart().filter(function (i) { return _cartKey(i) !== key; }));
}

function updateCartQty(key, qty) {
  if (qty < 1) { removeFromCart(key); return; }
  var items = getCart();
  var item = items.find(function (i) { return _cartKey(i) === key; });
  if (item) { item.qty = qty; _saveCart(items); }
}

// Index-based wrappers for onclick handlers - avoids embedding user text
// (personalisation keys) inside inline JS strings.
function removeFromCartAt(idx) {
  var item = getCart()[idx];
  if (item) removeFromCart(_cartKey(item));
}

function updateCartQtyAt(idx, qty) {
  var item = getCart()[idx];
  if (item) updateCartQty(_cartKey(item), qty);
}

function clearCart() { _saveCart([]); }

function getCartCount() {
  return getCart().reduce(function (s, i) { return s + i.qty; }, 0);
}

function getCartTotal() {
  return getCart().reduce(function (s, i) { return s + i.price_ils * i.qty; }, 0);
}

// ── PAGE-LEVEL HELPERS (use PRODUCTS + currentModalIdx from category pages) ─
function cartAddFromProduct(idx) {
  if (typeof PRODUCTS === 'undefined') return;
  var p = PRODUCTS[idx];
  if (!p) return;
  // Personalised products need their options picked first - open the modal instead.
  if (p.personalisable && typeof openModal === 'function') { openModal(idx); return; }
  addToCart(p.id, p.name_en, p.name_he || '', p.price_ils, p.photos[0]);
}

function cartAddFromModal() {
  if (typeof PRODUCTS === 'undefined' || typeof currentModalIdx === 'undefined' || currentModalIdx == null) return;
  var p = PRODUCTS[currentModalIdx];
  if (!p) return;
  var meta = null;
  if (p.personalisable) {
    var symbolEl = document.getElementById('modalSymbol');
    if (symbolEl) {
      var symbol = symbolEl.value;
      if (!symbol) {
        var hint = document.getElementById('modalCustomHint');
        if (hint) hint.style.display = 'block';
        symbolEl.focus();
        return;
      }
      var textEl = document.getElementById('modalText');
      var commentEl = document.getElementById('modalComment');
      meta = {
        symbol: symbol,
        symbol_he: _SYMBOL_HE[symbol] || symbol,
        text: textEl ? textEl.value.trim() : '',
        comment: commentEl ? commentEl.value.trim() : ''
      };
    }
  }
  addToCart(p.id, p.name_en, p.name_he || '', p.price_ils, p.photos[0], meta);
  if (typeof closeModal === 'function') closeModal();
}

// ── NAV BADGE ──────────────────────────────────────────────────
function updateCartBadge() {
  var n = getCartCount();
  var badge = document.getElementById('cart-count');
  if (!badge) return;
  badge.textContent = n;
  badge.style.display = n > 0 ? 'flex' : 'none';
}

// ── WA CHECKOUT LINK ───────────────────────────────────────────
function buildCheckoutWaLink() {
  var items = getCart();
  var l = (typeof currentLang !== 'undefined') ? currentLang : 'en';
  if (items.length === 0) return 'https://wa.me/' + WA_NUMBER;
  var lines;
  var total = getCartTotal();
  if (l === 'he') {
    lines = ['שלום! אני רוצה להזמין:'];
    items.forEach(function (item) {
      var name = item.name_he || item.name_en;
      lines.push('• ' + name + ' × ' + item.qty + ' (₪' + (item.price_ils * item.qty).toLocaleString('en-IL') + ')');
      if (item.meta) {
        if (item.meta.symbol)  lines.push('   סמל: ' + (item.meta.symbol_he || item.meta.symbol));
        if (item.meta.text)    lines.push('   כיתוב: ' + item.meta.text);
        if (item.meta.comment) lines.push('   הערות: ' + item.meta.comment);
      }
    });
    lines.push('');
    lines.push('סה"כ: ₪' + total.toLocaleString('en-IL'));
    lines.push('');
    lines.push('מה השלב הבא?');
  } else {
    lines = ["Hi! I'd like to order:"];
    items.forEach(function (item) {
      lines.push('• ' + item.name_en + ' × ' + item.qty + ' (₪' + (item.price_ils * item.qty).toLocaleString('en-IL') + ')');
      if (item.meta) {
        if (item.meta.symbol)  lines.push('   Symbol: ' + item.meta.symbol);
        if (item.meta.text)    lines.push('   Inscription: ' + item.meta.text);
        if (item.meta.comment) lines.push('   Comment: ' + item.meta.comment);
      }
    });
    lines.push('');
    lines.push('Total: ₪' + total.toLocaleString('en-IL'));
    lines.push('');
    lines.push("What's the next step?");
  }
  return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
}

// ── CART DRAWER RENDER ─────────────────────────────────────────
// Personalisation lines (symbol / inscription / comment) shown under the item name.
function _cartMetaHtml(item, isHe) {
  if (!item.meta) return '';
  var m = item.meta;
  var rows = [];
  if (m.symbol)  rows.push((isHe ? 'סמל: ' : 'Symbol: ') + escapeHtml(isHe ? (m.symbol_he || m.symbol) : m.symbol));
  if (m.text)    rows.push((isHe ? 'כיתוב: ' : 'Inscription: ') + escapeHtml(m.text));
  if (m.comment) rows.push((isHe ? 'הערות: ' : 'Comment: ') + escapeHtml(m.comment));
  if (!rows.length) return '';
  return '<div class="cart-item-meta">' + rows.join('<br>') + '</div>';
}

function renderCartDrawer() {
  var items = getCart();
  var l = (typeof currentLang !== 'undefined') ? currentLang : 'en';
  var isHe = l === 'he';
  var rate = (typeof usdRate === 'number') ? usdRate : null;
  var showUsd = rate && (typeof currentCurrency === 'undefined' || currentCurrency !== 'ILS');
  var total = getCartTotal();

  var countEl  = document.getElementById('cart-item-count');
  var listEl   = document.getElementById('cart-items-list');
  var footerEl = document.getElementById('cart-drawer-footer');

  if (countEl) countEl.textContent = getCartCount();
  if (!listEl) return;

  if (items.length === 0) {
    listEl.innerHTML = '<p class="cart-empty">' + (isHe ? 'עגלת הקניות ריקה' : 'Your cart is empty') + '</p>';
    if (footerEl) footerEl.style.display = 'none';
    return;
  }
  if (footerEl) footerEl.style.display = '';

  listEl.innerHTML = items.map(function (item, idx) {
    var name  = (isHe && item.name_he) ? item.name_he : item.name_en;
    var thumb = CDN + '/w_80,h_80,c_fill,g_auto,q_auto,f_auto/' + item.photo + '.jpg';
    var lineIls = item.price_ils * item.qty;
    var priceStr = '₪' + lineIls.toLocaleString('en-IL');
    if (showUsd) priceStr += ' <span class="cart-price-alt">≈ $' + Math.round(lineIls / rate) + '</span>';
    var slug = escapeAttr(item.slug);
    var url = _cartItemUrl(item);
    var thumbImg = `<img class="cart-item-thumb" src="${escapeAttr(thumb)}" alt="${escapeAttr(name)}" loading="lazy" />`;
    var nameHtml = escapeHtml(name);
    return `<div class="cart-item" data-slug="${slug}">
  ${url ? `<a class="cart-item-link" href="${escapeAttr(url)}" aria-label="${escapeAttr(name)}">${thumbImg}</a>` : thumbImg}
  <div class="cart-item-info">
    <div class="cart-item-name">${url ? `<a class="cart-item-link" href="${escapeAttr(url)}">${nameHtml}</a>` : nameHtml}</div>
    ${_cartMetaHtml(item, isHe)}
    <div class="cart-item-price">${priceStr}</div>
    <div class="cart-item-controls">
      <button class="cart-qty-btn" onclick="updateCartQtyAt(${idx},${item.qty - 1})" aria-label="Decrease">−</button>
      <span class="cart-qty-val">${item.qty}</span>
      <button class="cart-qty-btn" onclick="updateCartQtyAt(${idx},${item.qty + 1})" aria-label="Increase">+</button>
      <button class="cart-remove-btn" onclick="removeFromCartAt(${idx})" aria-label="Remove">
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
  </div>
</div>`;
  }).join('');

  var totalStr = '₪' + total.toLocaleString('en-IL');
  if (showUsd) totalStr += ' <span class="cart-price-alt">≈ $' + Math.round(total / rate) + '</span>';
  var totalEl = document.getElementById('cart-total-price');
  if (totalEl) totalEl.innerHTML = totalStr;

  var waBtn = document.getElementById('cart-wa-checkout');
  if (waBtn) waBtn.href = buildCheckoutWaLink();
}

// ── OPEN / CLOSE ────────────────────────────────────────────────
function openCartDrawer() {
  renderCartDrawer();
  var drawer  = document.getElementById('cart-drawer');
  var overlay = document.getElementById('cart-overlay');
  if (drawer)  drawer.classList.add('open');
  if (overlay) overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
  if (typeof trackGA4 === 'function') {
    trackGA4('view_cart', {
      currency: 'ILS', value: getCartTotal(),
      items: getCart().map(function (i) {
        return { item_id: i.slug, item_name: i.name_en, price: i.price_ils, quantity: i.qty };
      })
    });
  }
}

function closeCartDrawer() {
  var drawer  = document.getElementById('cart-drawer');
  var overlay = document.getElementById('cart-overlay');
  if (drawer)  drawer.classList.remove('open');
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}

// ── DOM INJECTION ───────────────────────────────────────────────
var _WA_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';
var _CART_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

function _injectCartDrawer() {
  if (document.getElementById('cart-drawer')) return;

  var overlay = document.createElement('div');
  overlay.id = 'cart-overlay';
  overlay.className = 'cart-overlay';
  overlay.addEventListener('click', closeCartDrawer);
  document.body.appendChild(overlay);

  var drawer = document.createElement('div');
  drawer.id = 'cart-drawer';
  drawer.className = 'cart-drawer';
  drawer.setAttribute('role', 'dialog');
  drawer.setAttribute('aria-label', 'Shopping cart');
  drawer.setAttribute('aria-modal', 'true');
  drawer.innerHTML =
    '<div class="cart-drawer-header">' +
      '<h2 class="cart-drawer-title">' + _CART_SVG +
        '<span data-t="cart_title">Cart</span>' +
        '<span id="cart-item-count" class="cart-header-count">0</span>' +
      '</h2>' +
      '<button class="cart-close-btn" onclick="closeCartDrawer()" aria-label="Close cart">×</button>' +
    '</div>' +
    '<div id="cart-items-list" class="cart-items-list" tabindex="0"></div>' +
    '<div id="cart-drawer-footer" class="cart-drawer-footer" style="display:none">' +
      '<div class="cart-total-row">' +
        '<span data-t="cart_total">Total</span>' +
        '<span id="cart-total-price" class="cart-total-price">₪0</span>' +
      '</div>' +
      '<a id="cart-wa-checkout" href="#" target="_blank" rel="noopener noreferrer" class="cart-checkout-btn"' +
         ' onclick="if(typeof trackGA4===\'function\')trackGA4(\'begin_checkout\',{currency:\'ILS\',value:getCartTotal()})">' +
        _WA_SVG + '<span data-t="cart_checkout">Order on WhatsApp</span>' +
      '</a>' +
      '<a href="checkout.html" class="cart-view-full-btn" onclick="closeCartDrawer()" data-t="cart_review">Review order →</a>' +
    '</div>';
  document.body.appendChild(drawer);
}

function _injectCartBtn() {
  if (document.getElementById('cart-icon-btn')) return;
  var nav = document.querySelector('nav');
  if (!nav) return;
  var hamburger = document.getElementById('hamburger');
  var cartBtn = document.createElement('button');
  cartBtn.id = 'cart-icon-btn';
  cartBtn.className = 'cart-icon-btn';
  cartBtn.setAttribute('aria-label', 'Open shopping cart');
  cartBtn.onclick = openCartDrawer;
  cartBtn.innerHTML =
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>' +
    '<span id="cart-count" class="cart-count" aria-live="polite" style="display:none">0</span>';
  if (hamburger) { nav.insertBefore(cartBtn, hamburger); } else { nav.appendChild(cartBtn); }
}

function _injectModalCartBtn() {
  var ctaStack = document.querySelector('.modal-cta-stack');
  if (!ctaStack || document.getElementById('modalAddCartCta')) return;
  var btn = document.createElement('button');
  btn.id = 'modalAddCartCta';
  btn.className = 'modal-cta cart-cta';
  btn.onclick = cartAddFromModal;
  btn.innerHTML =
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>' +
    '<span data-t="add_cart">Add to Cart</span>';
  ctaStack.insertBefore(btn, ctaStack.firstChild);
}

// ── ESCAPE KEY ─────────────────────────────────────────────────
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeCartDrawer();
});

// ── INIT ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  _injectCartDrawer();
  _injectCartBtn();
  _injectModalCartBtn();
  // Re-run setLang to translate freshly injected data-t elements
  if (typeof setLang === 'function' && typeof currentLang !== 'undefined') {
    setLang(currentLang);
  }
  updateCartBadge();
  renderCartDrawer();
});

document.addEventListener('sa:cart-change', function () {
  updateCartBadge();
  renderCartDrawer();
});
