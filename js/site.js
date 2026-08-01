/* ═══════════════════════════════════════════════════════════════
   site.js - Shared JavaScript for Sherman Art Works
   Sprint 17 - extracted from all 11 HTML pages
   ═══════════════════════════════════════════════════════════════ */

// ── CONSTANTS ──────────────────────────────────────────────────
const WA_NUMBER = '972523482278';
const CDN = 'https://res.cloudinary.com/doesupaf9/image/upload';

// ── LAUNCH DISCOUNT ────────────────────────────────────────────
// Site-wide launch promotion. Everything except shipping is sold at
// (1 - LAUNCH_DISCOUNT) of its catalogue price. Set to 0 to turn the whole
// promotion off - the banner disappears, struck prices revert, and the cart /
// checkout charge full price again, with no other change needed. The identical
// factor and rounding rule live in the payments Worker (sherman-payments,
// src/pricing.js) so the server reprices card orders to the same total; if you
// change this number, change it there too or card orders will bounce.
const LAUNCH_DISCOUNT = 0.20;

function launchActive() { return LAUNCH_DISCOUNT > 0; }

// Sale price for one item, rounded to the nearest whole shekel. Must match the
// server's rounding (Math.round on the per-line unit) exactly.
function saleIls(ils) {
  return launchActive() ? Math.round(ils * (1 - LAUNCH_DISCOUNT)) : ils;
}

function launchPill() {
  var label = (T_SITE[currentLang] && T_SITE[currentLang].launch_pill) || '20% launch discount';
  return ' <span class="launch-pill">' + label + '</span>';
}

// Wraps any ils->HTML price formatter so it renders the catalogue price struck
// through, followed by the discounted price and a launch pill. When the
// promotion is off it is a passthrough, so wiring it in is always safe.
function launchFormat(ils, fmt, launchExempt) {
  if (!launchActive()) return fmt(ils);
  var exempt = Math.max(0, Number(launchExempt) || 0);
  var eligible = Math.max(0, ils - exempt);
  return '<span class="was-price">' + fmt(ils) + '</span> ' +
         '<span class="now-price">' + fmt(saleIls(eligible) + exempt) + '</span>' + launchPill();
}

// Backend that signs HYP Pay requests and verifies completed transactions.
// With this empty, the result pages report an order as awaiting confirmation
// rather than claiming it succeeded, because a redirect back from a payment
// page proves nothing on its own.
const PAYMENT_API = 'https://sherman-payments.shermanartworks.workers.dev';

// Master switch for card payment in the UI. Set false to take the Pay button
// off the checkout without touching anything else; WhatsApp ordering is
// unaffected either way, so this is the safe lever if payments ever misbehave.
const PAYMENTS_ENABLED = true;

// ── SHARED TRANSLATIONS (T_SITE) ───────────────────────────────
const T_SITE = {
  en: {
    nav_shop:            'Shop',
    nav_custom:          'Custom Orders',
    nav_about:           'About',
    nav_contact:         'Contact',

    badge_soon:          'Coming Soon',

    launch_banner_pre:   'Official launch',
    launch_banner_text:  '20% off everything, site-wide',
    launch_pill:         '20% launch discount',

    cat1_title:          'Candlesticks',
    cat2_title:          'Horn Goblets',
    cat3_title:          'Kiddush Cups',
    cat4_title:          'Trays & Bowls',
    cat5_title:          'Business Gifts',
    cat6_title:          'Mezuzahs',
    cat7_title:          'Shofars',
    cat8_title:          'Havdalah Sets',

    // Shofar sub-categories - used by the nav on every page, not just the
    // shofar pages, so they live here rather than in a page dictionary.
    switch_all:          'All Shofars',
    switch_custom:       'Custom',
    switch_rams:         "Ram's Horn",
    switch_kudu:         'Kudu Horn',
    switch_candles_all:       'All Candlesticks',
    switch_candles_silver:    'Silver-Plated Candlesticks',
    switch_candles_artisanal: 'Artisanal Candlesticks',

    cat_from:            'from',
    cat_cta_browse:      'Browse Collection',
    cat_cta_commission:  'Commission Yours',

    shipping_banner:     '✦  Custom Orders Are Welcome  ✦',

    footer_tagline:      'Handmade glass art & Judaica from Israel',
    footer_col_shop:     'Shop',
    footer_col_studio:   'Studio',
    footer_col_help:     'Help',
    nav_faq:             'FAQ',
    footer_link_candles: 'Candlesticks',
    footer_link_shofars: 'Horn Goblets',
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
    consent_sr:          'Cookie consent',
    consent_text:        'We use anonymous analytics cookies to understand how visitors use the site - no ads, no cross-site tracking.',
    consent_more:        'Privacy Policy',
    consent_accept:      'Accept',
    consent_decline:     'Decline',
    add_cart:            'Add to Cart',
    color_note:          '* Colors and measurements may appear slightly different in person, as each item is handmade.',
    cart_title:          'Cart',
    cart_subtotal:       'Subtotal',
    cart_total:          'Total',
    cart_pay:            'Pay by card',
    cart_checkout:       'Order on WhatsApp',
    cart_review:         'Review order →',

    trust_handcrafted:   'Handcrafted in Israel',
    trust_generations:   'Three generations of artisans',
    trust_shipping:      'Ships worldwide',
    trust_secure:        'Secure ordering',
  },
  he: {
    nav_shop:            'חנות',
    nav_custom:          'הזמנות בהתאמה אישית',
    nav_about:           'אודות',
    nav_contact:         'צור קשר',

    badge_soon:          'בקרוב',

    launch_banner_pre:   'השקה רשמית',
    launch_banner_text:  '20% הנחה על כל האתר',
    launch_pill:         'הנחת השקה 20%',

    cat1_title:          'פמוטים',
    cat2_title:          'גביעי קרן',
    cat3_title:          'כוסות קידוש',
    cat4_title:          'מגשים וקערות',
    cat5_title:          'מתנות לעסקים',
    cat6_title:          'מזוזות',
    cat7_title:          'שופרות',
    cat8_title:          'סטים להבדלה',

    switch_all:          'כל השופרות',
    switch_custom:       'בהתאמה אישית',
    switch_rams:         'שופר איל',
    switch_kudu:         'שופר קודו',
    switch_candles_all:       'כל הפמוטים',
    switch_candles_silver:    'פמוטים בציפוי כסף',
    switch_candles_artisanal: 'פמוטים אומנותיים',

    cat_from:            'מ-',
    cat_cta_browse:      'לקולקציה',
    cat_cta_commission:  'הזמינו אצלנו',

    shipping_banner:     '✦  הזמנות בהתאמה אישית מתקבלות בשמחה  ✦',

    footer_tagline:      'אמנות זכוכית ויודאיקה בעבודת יד מישראל',
    footer_col_shop:     'חנות',
    footer_col_studio:   'הסטודיו',
    footer_col_help:     'עזרה',
    nav_faq:             'שאלות ותשובות',
    footer_link_candles: 'פמוטים',
    footer_link_shofars: 'גביעי קרן',
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
    consent_sr:          'הסכמה לשימוש בעוגיות',
    consent_text:        'אנחנו משתמשים בעוגיות אנליטיקה אנונימיות כדי להבין איך מבקרים משתמשים באתר - ללא פרסומות וללא מעקב בין אתרים.',
    consent_more:        'מדיניות פרטיות',
    consent_accept:      'אישור',
    consent_decline:     'לא תודה',
    add_cart:            'הוסף לסל',
    color_note:          '* הצבעים והמידות עשויים להראות מעט שונים במציאות, מכיוון שכל פריט נעשה בעבודת יד.',
    cart_title:          'עגלה',
    cart_subtotal:       'סכום ביניים',
    cart_total:          'סה"כ',
    cart_pay:            'תשלום בכרטיס אשראי',
    cart_checkout:       'הזמינו ב-WhatsApp',
    cart_review:         'לסיכום הזמנה ←',

    trust_handcrafted:   'עבודת יד מישראל',
    trust_generations:   'שלושה דורות של אומנים',
    trust_shipping:      'משלוחים לכל העולם',
    trust_secure:        'הזמנה מאובטחת',
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
// Taken from the payment backend rather than fetched here, so the figure on the
// page is the one the order is priced with. Two independent fetches of a moving
// rate disagree, and that gap would trip the backend's own total check on
// international orders that were never actually wrong.
//
// The rate leans slightly against the shopper (mid × 0.98), which makes the
// dollar figure a little high. That is the right direction while orders are
// charged in shekels: the customer's bank converts at roughly mid and adds its
// own fee, so a conservative estimate is closer to what their statement will
// say. The previous version divided instead of multiplying and understated it.
const FALLBACK_USD_RATE = 3.06 * 0.98;

async function loadUsdRate() {
  const rn = document.getElementById('rateNote');
  try {
    if (typeof PAYMENT_API !== 'string' || !PAYMENT_API) throw new Error('no backend');
    const c = new AbortController();
    const t = setTimeout(function() { c.abort(); }, 6000);
    const res = await fetch(PAYMENT_API + '/rate', { signal: c.signal });
    clearTimeout(t);
    if (!res.ok) throw new Error('rate endpoint ' + res.status);
    const data = await res.json();
    if (!data || !isFinite(data.rate)) throw new Error('no rate');
    usdRate = data.rate;
    if (rn) rn.textContent = 'Rate updated ' + (data.date || 'today');
  } catch (e) {
    // Same base and direction as the backend's own fallback, so a shopper who
    // loads the page while the backend is unreachable still sees a figure in
    // the same neighbourhood as the one they would be charged.
    usdRate = FALLBACK_USD_RATE;
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
  function fromAmount(ils) {
    if (currentCurrency === 'ILS' || !usdRate) {
      return '₪' + ils.toLocaleString('en-IL');
    }
    return '$' + Math.round(ils / usdRate).toLocaleString('en-US');
  }
  document.querySelectorAll('.cat-card-from[data-min-ils]').forEach(function(el) {
    var ils = parseInt(el.dataset.minIls, 10);
    if (launchActive()) {
      el.innerHTML = fromLabel + ' <span class="was-price">' + fromAmount(ils) + '</span> ' +
                     '<span class="now-price">' + fromAmount(saleIls(ils)) + '</span>';
    } else {
      el.textContent = fromLabel + ' ' + fromAmount(ils);
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
  // Cart surfaces quote prices too, and international shipping is converted from
  // USD - without this the drawer and checkout keep the old currency until the
  // next render for some other reason.
  if (typeof renderShipping === 'function') renderShipping();
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
  if (typeof renderPayment  === 'function') renderPayment();
  if (typeof renderCartDrawer === 'function') renderCartDrawer();
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
    '<p class="sr-only" id="consentBannerTitle" data-t="consent_sr">Cookie consent</p>' +
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
  // Skip-to-content link - targets existing main id or falls back to 'main-content'
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

  // Add accessibility link to the last footer column (Help) if not already present
  if (!document.querySelector('a[href="accessibility.html"]')) {
    var footerStudio = document.querySelector('.footer-links');
    if (footerStudio) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = 'accessibility.html';
      a.dataset.t = 'nav_accessibility';
      a.textContent = (T_SITE[lang] && T_SITE[lang].nav_accessibility) || 'Accessibility Statement';
      li.appendChild(a);
      // append to LAST footer-links column (the Help column)
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
// Re-point the page's global price formatters at the discounted-price wrapper.
// buildCard/renderModal call these by name at render time, so wrapping them here
// - before the first render below - makes every card, modal and size option
// show the launch price with no per-page edits. Passthrough when the promo is
// off, and idempotent so a second call is harmless.
function wrapLaunchFormatters() {
  if (!launchActive()) return;
  ['formatPrice', 'formatPriceModal', 'formatProductPrice'].forEach(function(name) {
    var orig = window[name];
    if (typeof orig !== 'function' || orig.__launchWrapped) return;
    var wrapped = function(ils, launchExempt) { return launchFormat(ils, orig, launchExempt); };
    wrapped.__launchWrapped = true;
    window[name] = wrapped;
  });
}

function initLaunchBanner() {
  if (!launchActive()) return;
  if (document.getElementById('launchBanner')) return;
  var d = T_SITE[currentLang] || T_SITE.en;
  var bar = document.createElement('div');
  bar.className = 'launch-banner';
  bar.id = 'launchBanner';
  bar.setAttribute('role', 'note');
  bar.innerHTML =
    '<span class="launch-banner-flag" data-t="launch_banner_pre">' + d.launch_banner_pre + '</span>' +
    '<span class="launch-banner-text" data-t="launch_banner_text">' + d.launch_banner_text + '</span>';
  document.body.insertBefore(bar, document.body.firstChild);
}

document.addEventListener('DOMContentLoaded', function() {
  wrapLaunchFormatters();
  initConsent();
  initA11y();
  initLaunchBanner();
  // Static /he/ pages set window.__SA_LANG='he' so the URL (not a stale
  // localStorage value) wins - otherwise JS would re-render them in English.
  var lang = window.__SA_LANG || localStorage.getItem('sa_lang') || 'en';
  var cur  = localStorage.getItem('sa_cur')  || 'USD';
  setLang(lang);
  setCurrency(cur);
  loadUsdRate();

  // Hash-based product anchor open (22.5)
  if (typeof PRODUCTS !== 'undefined' && typeof openModal === 'function' && location.hash) {
    var _hId  = location.hash.slice(1);
    var _hIdx = PRODUCTS.findIndex(function(p) { return p.id === _hId; });
    if (_hIdx >= 0) {
      var _hCard = document.getElementById(_hId);
      if (_hCard) _hCard.scrollIntoView({ block: 'center' });
      openModal(_hIdx);
    }
  }

  // Sync WA links to WA_NUMBER
  var waMsg = "Hi, I'm interested in your handmade glass art";
  var waFloating = document.getElementById('floatingWa');
  if (waFloating) waFloating.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hi, I have a question about Sherman Art Works.");
  var waDirect = document.getElementById('waDirectLink');
  if (waDirect) waDirect.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(waMsg);
  var waCorp = document.getElementById('waCorporateLink');
  if (waCorp) waCorp.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent("Hi, I'm interested in a corporate or bulk order.");
});

// Return product/index pairs in a new random order. Category pages cache the
// result for the lifetime of the page so language and currency changes do not
// make products jump around while someone is browsing.
function shuffledProductEntries(products) {
  var entries = products.map(function(product, index) {
    return { p: product, idx: index };
  });
  for (var i = entries.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var current = entries[i];
    entries[i] = entries[j];
    entries[j] = current;
  }
  return entries;
}
