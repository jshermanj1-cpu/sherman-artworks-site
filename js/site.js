/* ═══════════════════════════════════════════════════════════════
   site.js - Shared JavaScript for Sherman Art Works
   Sprint 17 - extracted from all 11 HTML pages
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
    cat2_title:          'Shofars & Horn Goblets',
    cat3_title:          'Kiddush Cups',
    cat4_title:          'Trays & Bowls',
    cat5_title:          'Business Gifts',
    cat6_title:          'Mezuzahs',
    cat7_title:          'Custom Shofars',

    cat_from:            'from',
    cat_cta_browse:      'Browse Collection',
    cat_cta_commission:  'Commission Yours',

    shipping_banner:     '✦  Shipping: Israel ₪30 (free over ₪800) · International $45 (free over $500)  ·  Custom Orders Are Welcome  ✦',

    footer_tagline:      'Handmade glass art & Judaica from Israel',
    footer_col_shop:     'Shop',
    footer_col_studio:   'Studio',
    footer_link_candles: 'Candlesticks',
    footer_link_shofars: 'Shofars & Horn Goblets',
    footer_link_bowls:   'Trays & Bowls',
    footer_all_collections: 'All Collections',
    footer_copy:         '© 2026 Sherman Art Works. All rights reserved.',
    footer_badge:        'Handcrafted in Israel',
    nav_privacy:         'Privacy Policy',
    nav_terms:           'Terms of Service',
    nav_accessibility:   'Accessibility Statement',
    skip_to_content:     'Skip to main content',
    cart_item_added:     'Item added to cart',
    cart_item_removed:   'Item removed from cart',
    consent_text:        'We use anonymous analytics cookies to understand how visitors use the site - no ads, no cross-site tracking.',
    consent_more:        'Privacy Policy',
    consent_accept:      'Accept',
    consent_decline:     'Decline',
    add_cart:            'Add to Cart',
    cart_title:          'Cart',
    cart_total:          'Total',
    cart_checkout:       'Order on WhatsApp',
    cart_review:         'Review order →',
  },
  he: {
    nav_shop:            'חנות',
    nav_custom:          'הזמנות בהתאמה אישית',
    nav_about:           'אודות',
    nav_contact:         'צור קשר',

    badge_soon:          'בקרוב',

    cat1_title:          'פמוטים',
    cat2_title:          'שופרות וגביעי קרן',
    cat3_title:          'כוסות קידוש',
    cat4_title:          'מגשים וקערות',
    cat5_title:          'מתנות לעסקים',
    cat6_title:          'מזוזות',
    cat7_title:          'שופרות בהתאמה אישית',

    cat_from:            'מ-',
    cat_cta_browse:      'לקולקציה',
    cat_cta_commission:  'הזמינו אצלנו',

    shipping_banner:     '✦  משלוח בארץ 30 ₪ (חינם מעל 800 ₪) · משלוח בינלאומי $45 (חינם מעל $500)  ·  הזמנות בהתאמה אישית מתקבלות בשמחה  ✦',

    footer_tagline:      'אמנות זכוכית ויודאיקה בעבודת יד מישראל',
    footer_col_shop:     'חנות',
    footer_col_studio:   'הסטודיו',
    footer_link_candles: 'פמוטים',
    footer_link_shofars: 'שופרות וגביעי קרן',
    footer_link_bowls:   'מגשים וקערות',
    footer_all_collections: 'כל הקולקציות',
    footer_copy:         '© 2026 שרמן ארט וורקס. כל הזכויות שמורות.',
    footer_badge:        'עבודת יד מישראל',
    nav_privacy:         'מדיניות פרטיות',
    nav_terms:           'תקנון',
    nav_accessibility:   'הצהרת נגישות',
    skip_to_content:     'דלג לתוכן הראשי',
    cart_item_added:     'פריט נוסף לסל',
    cart_item_removed:   'פריט הוסר מהסל',
    consent_text:        'אנחנו משתמשים בעוגיות אנליטיקה אנונימיות כדי להבין איך מבקרים משתמשים באתר - ללא פרסומות וללא מעקב בין אתרים.',
    consent_more:        'מדיניות פרטיות',
    consent_accept:      'אישור',
    consent_decline:     'לא תודה',
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
  // Duck-typed hooks - only run if page defines them
  if (typeof renderProducts === 'function') renderProducts();
  if (typeof renderCheckout === 'function') renderCheckout();
  if (typeof renderPrivacy  === 'function') renderPrivacy();
  if (typeof renderTerms    === 'function') renderTerms();
  if (typeof renderShipping === 'function') renderShipping();
  if (typeof renderA11y     === 'function') renderA11y();
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
  if (typeof renderPrivacy  === 'function') renderPrivacy();
  if (typeof renderTerms    === 'function') renderTerms();
  if (typeof renderShipping === 'function') renderShipping();
  if (typeof renderA11y     === 'function') renderA11y();
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

// ── GA4 - CONSENT-GATED ─────────────────────────────────────────
// gtag.js loads only after the visitor accepts the cookie banner.
// Choice persists in localStorage('sa_consent') with a cookie fallback:
// in-app browsers (WhatsApp/Instagram) and private mode can drop
// localStorage writes, and cookies also survive www/apex host switches.
var GA4_ID = 'G-J55QNV6GF1';

function _consentCookieDomain() {
  var h = location.hostname;
  if (h === 'localhost' || /^[0-9.:]+$/.test(h)) return '';
  var parts = h.split('.');
  if (parts.length < 2) return '';
  return '; domain=.' + parts.slice(-2).join('.');
}
function _setConsent(v) {
  try { localStorage.setItem('sa_consent', v); } catch (e) {}
  try {
    document.cookie = 'sa_consent=' + v + '; max-age=31536000; path=/; SameSite=Lax' + _consentCookieDomain();
  } catch (e) {}
}
function _getConsent() {
  var v = null;
  try { v = localStorage.getItem('sa_consent'); } catch (e) {}
  if (v === 'granted' || v === 'denied') return v;
  var m = document.cookie.match(/(?:^|;\s*)sa_consent=(granted|denied)/);
  return m ? m[1] : null;
}

function loadGA4() {
  if (window.__ga4Loaded) return;
  window.__ga4Loaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', GA4_ID);
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
  document.head.appendChild(s);
}

function hideConsentBanner() {
  var b = document.getElementById('consentBanner');
  if (b) b.remove();
  var main = document.querySelector('main');
  if (main) main.focus();
}
function acceptConsent() {
  _setConsent('granted');
  hideConsentBanner();
  loadGA4();
}
function declineConsent() {
  _setConsent('denied');
  hideConsentBanner();
}

function initConsent() {
  var c = _getConsent();
  if (c === 'granted') { loadGA4(); return; }
  if (c === 'denied') return;
  if (document.getElementById('consentBanner')) return;
  var div = document.createElement('div');
  div.className = 'consent-banner';
  div.id = 'consentBanner';
  div.setAttribute('role', 'dialog');
  div.setAttribute('aria-modal', 'false');
  div.setAttribute('aria-labelledby', 'consentBannerTitle');
  div.innerHTML =
    '<p class="sr-only" id="consentBannerTitle">Cookie consent</p>' +
    '<p class="consent-text"><span data-t="consent_text">We use anonymous analytics cookies to understand how visitors use the site - no ads, no cross-site tracking.</span> ' +
    '<a href="privacy.html" data-t="consent_more">Privacy Policy</a></p>' +
    '<div class="consent-actions">' +
      '<button type="button" class="consent-btn consent-accept" id="consentAcceptBtn" data-t="consent_accept" onclick="acceptConsent()">Accept</button>' +
      '<button type="button" class="consent-btn consent-decline" data-t="consent_decline" onclick="declineConsent()">Decline</button>' +
    '</div>';
  div.addEventListener('keydown', function(e) { if (e.key === 'Escape') declineConsent(); });
  document.body.appendChild(div);
  setTimeout(function() {
    var btn = document.getElementById('consentAcceptBtn');
    if (btn) btn.focus();
  }, 200);
}

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

// ── ACCESSIBILITY HELPERS ────────────────────────────────────────
function a11yAnnounce(msg) {
  var el = document.getElementById('a11y-announce');
  if (!el) return;
  el.textContent = '';
  setTimeout(function() { el.textContent = msg; }, 50);
}

function initA11y() {
  // Skip-to-content link — targets existing main id or falls back to 'main-content'
  var lang = localStorage.getItem('sa_lang') || 'en';
  var main = document.querySelector('main');
  if (main && !main.id) main.id = 'main-content';
  if (main) main.setAttribute('tabindex', '-1');
  var mainId = (main && main.id) ? main.id : 'main-content';
  var skipText = (T_SITE[lang] && T_SITE[lang].skip_to_content) || 'Skip to main content';
  var skip = document.createElement('a');
  skip.href = '#' + mainId;
  skip.className = 'skip-to-content';
  skip.textContent = skipText;
  document.body.insertBefore(skip, document.body.firstChild);

  // Aria-live region for cart + dynamic announcements
  var live = document.createElement('div');
  live.id = 'a11y-announce';
  live.setAttribute('aria-live', 'polite');
  live.setAttribute('aria-atomic', 'true');
  live.className = 'sr-only';
  document.body.appendChild(live);

  // Add accessibility link to footer Studio column if not already present
  if (!document.querySelector('a[href="accessibility.html"]')) {
    var footerStudio = document.querySelector('.footer-links');
    if (footerStudio) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = 'accessibility.html';
      a.dataset.t = 'nav_accessibility';
      a.textContent = (T_SITE[lang] && T_SITE[lang].nav_accessibility) || 'Accessibility Statement';
      li.appendChild(a);
      // append to LAST footer-links column (Studio column)
      var allFooterLists = document.querySelectorAll('.footer-links');
      var studioList = allFooterLists[allFooterLists.length - 1];
      if (studioList) studioList.appendChild(li);
    }
  }

  // Modal accessibility: focus trap + focus return (works on any page with #productModal)
  var modal = document.getElementById('productModal');
  if (modal) {
    var _lastFocus = null;

    new MutationObserver(function(mutations) {
      mutations.forEach(function(m) {
        if (m.attributeName !== 'class') return;
        if (modal.classList.contains('open')) {
          _lastFocus = document.activeElement;
          var firstBtn = modal.querySelector('button:not([disabled]), a[href]');
          if (firstBtn) firstBtn.focus();
        } else {
          if (_lastFocus) { _lastFocus.focus(); _lastFocus = null; }
        }
      });
    }).observe(modal, { attributes: true, attributeFilter: ['class'] });

    modal.addEventListener('keydown', function(e) {
      if (e.key !== 'Tab') return;
      var focusable = Array.from(modal.querySelectorAll(
        'button:not([disabled]), a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )).filter(function(el) { return el.offsetParent !== null; });
      if (!focusable.length) return;
      var first = focusable[0];
      var last  = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
}

// ── INIT ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  initConsent();
  initA11y();
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
