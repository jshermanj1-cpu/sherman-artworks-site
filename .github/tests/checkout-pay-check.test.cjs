// What checkout.html sends the payments backend to check its total against.
//
// The backend reprices the cart and refuses the order with `total_changed` when
// the page's figure disagrees with its own. That only works if the page sends a
// figure the backend can reproduce to the cent. A dollar reader with an Israeli
// address used to get ₪35 of postage converted at the day's rate on both sides,
// rounded to the dollar here and to the cent there, and had their first Pay
// press turned away over three cents. Israel's dollar postage is a fixed $11
// now (SHIPPING.IL.usd here, and in the Worker's src/pricing.js), so a dollar
// reader is quoted, checked and charged in dollars with no rate involved.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');

const NO_SALE = Date.parse('2027-02-01T12:00:00+02:00');
const ADDRESS = {
  fname: 'Dana', lname: 'Levi', email: 'dana@example.com', phone: '0500000000',
  street: '1 Herzl St', city: 'Tel Aviv', country: 'Israel'
};

// The page's own script: the one <script> in checkout.html with no attributes.
function checkoutScript() {
  const html = fs.readFileSync(path.join(root, 'checkout.html'), 'utf8');
  const blocks = html.match(/<script>[\s\S]*?<\/script>/g) || [];
  assert.equal(blocks.length, 1, 'expected exactly one inline script in checkout.html');
  return blocks[0].replace(/^<script>/, '').replace(/<\/script>$/, '');
}

// A checkout page with a cart and a destination, and a backend that answers
// every create-payment with `reply`. Returns the context and the bodies sent.
function checkout({zone, delivery, currency, rates, reply}) {
  const data = new Map();
  const sent = [];
  const context = vm.createContext({
    Date: class extends Date { static now() { return NO_SALE; } },
    window: { addEventListener() {} },
    document: {
      addEventListener() {}, dispatchEvent() {},
      getElementById: () => null, querySelector: () => null, querySelectorAll: () => []
    },
    localStorage: {
      getItem: k => data.get(k) || null, setItem: (k, v) => data.set(k, v), removeItem: k => data.delete(k)
    },
    location: { pathname: '/checkout.html', hostname: 'localhost', search: '' },
    fetch(url, init) {
      if (!/\/create-payment$/.test(url)) return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      sent.push(JSON.parse(init.body));
      return Promise.resolve({ ok: !reply.error, json: () => Promise.resolve(reply) });
    },
    console
  });
  for (const file of ['js/site.js', 'js/cart.js']) {
    vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context);
  }
  vm.runInContext(checkoutScript(), context);

  data.set('sa_cart', JSON.stringify([
    { slug: 'glass-circle-candlesticks', name_en: 'Glass Circle Candlesticks', price_ils: 505, photo: 'x', qty: 2 }
  ]));
  data.set('sa_ship', zone);
  if (delivery) data.set('sa_delivery', delivery);
  data.set('sa_ship_addr', JSON.stringify(ADDRESS));
  context.setCurrencyState(currency);
  // The day's two exchange rates, as the page gets them from the backend.
  vm.runInContext(`usdRate = ${rates.rate}; usdCostRate = ${rates.cost};`, context);
  return { context, sent };
}

const settle = () => new Promise(resolve => setImmediate(resolve));
const STOP = { error: 'stop_here' };           // refuse, so nothing navigates away
const TODAY = { rate: 3.174207, cost: 3.303767 };
// Rates at which ₪35 would convert to $13 and to $9: the figure must not follow.
const WEAK_SHEKEL = { rate: 2.6, cost: 2.7 };
const STRONG_SHEKEL = { rate: 3.8, cost: 3.95 };

test('a dollar reader shipping within Israel pays the dollar list plus a fixed $11', async () => {
  for (const rates of [TODAY, WEAK_SHEKEL, STRONG_SHEKEL]) {
    const { context, sent } = checkout({ zone: 'IL', currency: 'USD', rates, reply: STOP });
    context.payNow();
    await settle();
    assert.equal(sent.length, 1);
    assert.equal(sent[0].zone, 'IL');
    assert.equal(sent[0].currency, 'USD');
    assert.equal(sent[0].expected_currency, 'USD');
    assert.equal(sent[0].expected_total, context.getCartTotalIn('USD') + 11);
    assert.equal(context.getShippingIn('USD'), 11);
    assert.equal(context.getShippingLabel(), '$11');
    // The shekel figure rides along unchanged for a backend that charges shekels.
    assert.equal(sent[0].expected_total_ils, 505 * 2 + 35);
  }
});

test('a shekel reader shipping within Israel still pays ₪35', async () => {
  const { context, sent } = checkout({ zone: 'IL', currency: 'ILS', rates: TODAY, reply: STOP });
  context.payNow();
  await settle();
  assert.equal(sent[0].currency, 'ILS');
  assert.equal(sent[0].expected_currency, 'ILS');
  assert.equal(sent[0].expected_total, 505 * 2 + 35);
  assert.equal(context.getShippingLabel(), '₪35');
});

test('a dollar reader collecting from the gallery pays the dollar list alone', async () => {
  const { context, sent } = checkout({ zone: 'IL', delivery: 'pickup', currency: 'USD', rates: TODAY, reply: STOP });
  context.payNow();
  await settle();
  assert.equal(sent[0].delivery, 'pickup');
  assert.equal(sent[0].expected_currency, 'USD');
  assert.equal(sent[0].expected_total, context.getCartTotalIn('USD'));
});

test('an international order is checked in the currency the page quotes', async () => {
  const usd = checkout({ zone: 'INTL', currency: 'USD', rates: TODAY, reply: STOP });
  usd.context.payNow();
  await settle();
  assert.equal(usd.sent[0].expected_currency, 'USD');
  assert.equal(usd.sent[0].expected_total, usd.context.getCartTotalIn('USD') + 45);
  assert.equal(usd.context.getShippingLabel(), '$45');

  const ils = checkout({ zone: 'INTL', currency: 'ILS', rates: TODAY, reply: STOP });
  ils.context.payNow();
  await settle();
  assert.equal(ils.sent[0].expected_currency, 'ILS');
  assert.equal(ils.sent[0].expected_total, 505 * 2 + Math.round(45 * TODAY.cost));
});

test('after a corrected total, the retry sends back the figure the backend gave', async () => {
  const corrected = {
    error: 'total_changed', currency: 'USD',
    subtotal_ils: 1030, shipping_ils: 35, total_ils: 1065,
    subtotal_usd: 340, shipping_usd: 11, total_usd: 351
  };
  const { context, sent } = checkout({ zone: 'IL', currency: 'USD', rates: TODAY, reply: corrected });
  context.payNow();
  await settle();
  context.payNow();
  await settle();
  assert.equal(sent.length, 2);
  assert.equal(sent[1].expected_currency, 'USD');
  assert.equal(sent[1].expected_total, 351);
});
