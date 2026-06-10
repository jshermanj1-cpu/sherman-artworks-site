/* ═══════════════════════════════════════════════════════════════
   site.js — Shared JavaScript for Sherman Art Works
   Sprint 17 — extracted from all 11 HTML pages
   ═══════════════════════════════════════════════════════════════ */

// ── CONSTANTS ──────────────────────────────────────────────────
const WA_NUMBER = '972523482278';
const CDN = 'https://res.cloudinary.com/doesupaf9/image/upload';

// ── SHARED TRANSLATIONS (T_SITE) ───────────────────────────────
const T_SITE = {
  en: {
    nav_shop:            'Shop',
    nav_custom:          'Custom Orders',
    nav_about:           'About',
    nav_contact:         'Contact',

    badge_soon:          'Coming Soon',

    cat1_title:          'Candlesticks',
    cat2_title:          'Shofars & Goblets',
    cat3_title:          'Kiddush Cups',
    cat4_title:          'Trays & Bowls',
    cat5_title:          'Business Gifts',
    cat6_title:          'Mezuzahs',

    cat_from:            'from',
    cat_cta_browse:      'Browse Collection',
    cat_cta_commission:  'Commission Yours',

    shipping_banner:     '✦  Launch Offer: Free Worldwide Shipping on All Orders  ·  Custom Orders Are Welcome  ✦',

    footer_tagline:      'Handmade glass art & Judaica from Israel',
    footer_col_shop:     'Shop',
    footer_col_studio:   'Studio',
    footer_link_candles: 'Candlesticks',
    footer_link_shofars: 'Shofars & Goblets',
    footer_link_bowls:   'Trays & Bowls',
    footer_all_collections: 'All Collections',
    footer_copy:         '© 2026 Sherman Art Works. All rights reserved.',
    footer_badge:        'Handcrafted in Israel',
    add_cart:            'Add to Cart',
    cart_title:          'Cart',
    cart_total:          'Total',
    cart_checkout:       'Order on WhatsApp',
    cart_review:         'Review order →',
  },
  he: {
    nav_shop:            'חנות',
    nav_custom:          'הזמנות מיוחדות',
    nav_about:           'אודות',
    nav_contact:         'צור קשר',

    badge_soon:          'בקרוב',

    cat1_title:          'פמוטים',
    cat2_title:          'שופרות וגביעים',
    cat3_title:          'כוסות קידוש',
    cat4_title:          'מגשים וקערות',
    cat5_title:          'מתנות עסקיות',
    cat6_title:          'מזוזות',

    cat_from:            'מ-',
    cat_cta_browse:      'לקולקציה',
    cat_cta_commission:  'הזמינו אצלנו',

    shipping_banner:     '✦  מבצע השקה: משלוח חינם לכל העולם  ·  הזמנות מיוחדות מתקבלות בשמחה  ✦',

    footer_tagline:      'אמנות זכוכית ויודאיקה עשויות ביד מישראל',
    footer_col_shop:     'חנות',
    footer_col_studio:   'הסטודיו',
    footer_link_candles: 'פמוטים',
    footer_link_shofars: 'שופרות וגביעים',
    footer_link_bowls:   'מגשים וקערות',
    footer_all_collections: 'כל הקולקציות',
    footer_copy:         '© 2026 שרמן ארט וורקס. כל הזכויות שמורות.',
    footer_badge:        'עשוי ביד בישראל',
    add_cart:            'הוסף לסל',
    cart_title:          'עגלה',
    cart_total:          'סה"כ',
    cart_checkout:       'הזמינו ב-WhatsApp',
    cart_review:         'לסיכום הזמנה ←',
  }
};

// ── ESCAPE HELPERS (used by category-page render functions) ─────
function escapeHtml(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escapeAttr(s) { return (s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;'); }

// ── STATE ───────────────────────────────────────────────────────
let currentLang     = 'en';
let currentCurrency = 'USD';
let usdRate         = null;

// ── EXCHANGE RATE ───────────────────────────────────────────────
// Standardised: USD endpoint, +2% markup, 6s timeout, fallback renders
async function loadUsdRate() {
  try {
    const c = new AbortController();
    const t = setTimeout(function() { c.abort(); }, 6000);
    const res = await fetch('https://open.er-api.com/v6/latest/USD', { signal: c.signal });
    clearTimeout(t);
    if (!res.ok) throw new Error('API error');
    const data = await res.json();
    const raw = data.rates && data.rates.ILS;
    if (!raw) throw new Error('No ILS rate');
    usdRate = raw / 0.98;
    const rn = document.getElementById('rateNote');
    if (rn) rn.textContent = 'Rate live · +2%';
  } catch (e) {
    usdRate = 3.75 / 0.98;
    const rn = document.getElementById('rateNote');
    if (rn) rn.textContent = 'Est. rate';
  }
  // Duck-typed hooks — only run if page defines them
  if (typeof renderProducts === 'function') renderProducts();
  if (typeof renderCheckout === 'function') renderCheckout();
  updatePrices();
}

// ── PRICE HELPERS ───────────────────────────────────────────────
function ilsToUsd(ils) { return usdRate ? ils / usdRate : null; }

function updatePrices() {
  // Updates homepage "from ₪X" / "from $X" spans
  var fromLabel = (T_SITE[currentLang] && T_SITE[currentLang].cat_from)
    || (typeof T_PAGE !== 'undefined' && T_PAGE[currentLang] && T_PAGE[currentLang].cat_from)
    || 'from';
  document.querySelectorAll('.cat-card-from[data-min-ils]').forEach(function(el) {
    var ils = parseInt(el.dataset.minIls, 10);
    if (currentCurrency === 'ILS' || !usdRate) {
      el.textContent = fromLabel + ' ₪' + ils.toLocaleString('en-IL');
    } else {
      el.textContent = fromLabel + ' $' + Math.round(ils / usdRate).toLocaleString('en-US');
    }
  });
}

// ── CURRENCY ────────────────────────────────────────────────────
function setCurrency(cur) {
  currentCurrency = cur;
  var btnILS = document.getElementById('btnILS');
  var btnUSD = document.getElementById('btnUSD');
  if (btnILS) btnILS.classList.toggle('active', cur === 'ILS');
  if (btnUSD) btnUSD.classList.toggle('active', cur === 'USD');
  if (typeof renderProducts === 'function') renderProducts();
  updatePrices();
  localStorage.setItem('sa_cur', cur);
}

// ── LANGUAGE ────────────────────────────────────────────────────
function setLang(l) {
  currentLang = l;
  var sitePart = T_SITE[l] || {};
  var pagePart = (typeof T_PAGE !== 'undefined' && T_PAGE[l]) ? T_PAGE[l] : {};
  var dict = Object.assign({}, sitePart, pagePart);
  document.querySelectorAll('[data-t]').forEach(function(el) {
    var val = dict[el.dataset.t];
    if (val === undefined) return;
    // Use innerHTML only for known rich-text keys; textContent for everything else
    if (el.dataset.t === 'story_body' || el.dataset.t === 'craft_body') {
      el.innerHTML = val;
    } else {
      el.textContent = val;
    }
  });
  document.documentElement.lang = l;
  document.documentElement.dir  = l === 'he' ? 'rtl' : 'ltr';
  var btnEN = document.getElementById('btnEN');
  var btnHE = document.getElementById('btnHE');
  if (btnEN) btnEN.classList.toggle('active', l === 'en');
  if (btnHE) btnHE.classList.toggle('active', l === 'he');
  localStorage.setItem('sa_lang', l);
  if (typeof renderProducts === 'function') renderProducts();
  if (typeof renderCheckout === 'function') renderCheckout();
  if (typeof renderModal === 'function' && typeof currentModalIdx !== 'undefined' && currentModalIdx != null) renderModal();
}

// ── NAV ─────────────────────────────────────────────────────────
function toggleNav() {
  var b = document.getElementById('hamburger');
  var n = document.getElementById('mobileNav');
  var o = b.classList.toggle('open');
  n.classList.toggle('open', o);
  b.setAttribute('aria-expanded', o);
  n.setAttribute('aria-hidden', !o);
}
function closeMobileNav() {
  var b = document.getElementById('hamburger');
  var n = document.getElementById('mobileNav');
  b.classList.remove('open');
  n.classList.remove('open');
  b.setAttribute('aria-expanded', 'false');
  n.setAttribute('aria-hidden', 'true');
}
function toggleShopDropdown(e) {
  if (e) e.stopPropagation();
  var t = document.querySelector('.nav-dropdown-toggle');
  var m = document.querySelector('.nav-dropdown-menu');
  if (!t || !m) return;
  var open = t.getAttribute('aria-expanded') === 'true';
  t.setAttribute('aria-expanded', String(!open));
  m.classList.toggle('open', !open);
}
function toggleMobileShop(e) {
  if (e) e.stopPropagation();
  var t = document.querySelector('.mobile-shop-toggle');
  var m = document.querySelector('.mobile-shop-menu');
  if (!t || !m) return;
  var open = t.getAttribute('aria-expanded') === 'true';
  t.setAttribute('aria-expanded', String(!open));
  m.classList.toggle('open', !open);
}

// Click-outside closes dropdown
document.addEventListener('click', function(e) {
  if (e.target.closest('.nav-dropdown')) return;
  var t = document.querySelector('.nav-dropdown-toggle');
  var m = document.querySelector('.nav-dropdown-menu');
  if (t && m) { t.setAttribute('aria-expanded', 'false'); m.classList.remove('open'); }
});

// Escape closes dropdown + modal
document.addEventListener('keydown', function(e) {
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.nav-dropdown-toggle, .mobile-shop-toggle').forEach(function(t) {
    t.setAttribute('aria-expanded', 'false');
    var s = t.nextElementSibling;
    if (s) s.classList.remove('open');
  });
  if (typeof closeModal === 'function') closeModal();
});

// ── GA4 ─────────────────────────────────────────────────────────
function trackGA4(eventName, params) {
  if (typeof gtag === 'function') gtag('event', eventName, params || {});
}
document.addEventListener('click', function(e) {
  if (e.target.closest('.floating-wa')) {
    trackGA4('whatsapp_click', { location: 'floating_button' });
  }
  if (e.target.closest('.btn-order')) {
    var c = e.target.closest('.product-card');
    var n = c && c.querySelector('.product-card-name');
    trackGA4('whatsapp_click', { location: 'product_card', product_name: n ? n.textContent : '' });
  }
  if (e.target.closest('.btn-details')) {
    var c2 = e.target.closest('.product-card');
    var n2 = c2 && c2.querySelector('.product-card-name');
    trackGA4('view_details', { product_name: n2 ? n2.textContent : '' });
  }
  if (e.target.closest('#modalOrderCta')) {
    var mn = document.getElementById('modalName');
    trackGA4('whatsapp_click', { location: 'product_modal', product_name: mn ? mn.textContent : '' });
  }
  if (e.target.closest('#modalEmailCta')) {
    var mn2 = document.getElementById('modalName');
    trackGA4('email_click', { location: 'product_modal', product_name: mn2 ? mn2.textContent : '' });
  }
  if (e.target.closest('.cta-link.wa') || e.target.closest('.btn-wa')) {
    trackGA4('whatsapp_click', { location: 'page_cta' });
  }
  if (e.target.closest('.cta-link.mail')) {
    trackGA4('email_click', { location: 'page_cta' });
  }
  if (e.target.closest('.cat-card')) {
    var titleEl = e.target.closest('.cat-card').querySelector('.cat-card-title');
    trackGA4('category_browse', { category: titleEl ? titleEl.textContent : '' });
  }
  if (e.target.closest('.form-submit')) {
    trackGA4('whatsapp_click', { location: 'enquiry_form' });
  }
  if (e.target.closest('.btn-gold')) {
    trackGA4('commission_click', { location: 'page_cta' });
  }
  if (e.target.closest('#waCorporateLink')) {
    trackGA4('whatsapp_click', { location: 'corporate_cta' });
  }
});

// ── INIT ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  var lang = localStorage.getItem('sa_lang') || 'en';
  var cur  = localStorage.getItem('sa_cur')  || 'USD';
  setLang(lang);
  setCurrency(cur);
  loadUsdRate();

  // Sync WA links to WA_NUMBER
  var waMsg = "Hi, I'm interested in your handmade glass art";
  var waFloating = document.getElementById('floatingWa');
  if (waFloating) waFloating.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hi, I have a question about Sherman Art Works.");
  var waDirect = document.getElementById('waDirectLink');
  if (waDirect) waDirect.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(waMsg);
  var waCorp = document.getElementById('waCorporateLink');
  if (waCorp) waCorp.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hi, I'm interested in a corporate or bulk order.");
});
