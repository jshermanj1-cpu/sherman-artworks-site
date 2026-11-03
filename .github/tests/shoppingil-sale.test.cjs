const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
function browser(at) {
  const data = new Map();
  const context = vm.createContext({
    Date: class extends Date { static now() { return at.value; } },
    window: { addEventListener() {} },
    document: { addEventListener() {} },
    localStorage: { getItem: k => data.get(k) || null, setItem: (k,v) => data.set(k,v) },
    location: {pathname: '/index.html'}, console
  });
  for(const file of ['js/site.js','js/cart.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),context);
  return context;
}
const start = Date.parse('2026-11-03T00:00:00+02:00');
const end = Date.parse('2026-11-12T00:00:00+02:00');
const products = JSON.parse(fs.readFileSync(path.join(root,'data/products.json'),'utf8'));

test('10% on every product but the menorahs, 3-11 November only', () => {
  const at = {value: start};
  const ctx = browser(at);
  for (const p of products) {
    const rate = p.category === 'hanukkah-menorahs' ? .2 : .1;
    assert.equal(ctx.productDiscount(p.id), rate, p.id);
    const ils = p.price_ils || (p.sizes && p.sizes[0].price_ils);
    assert.equal(ctx.priceParts(ils,0,'ILS',p.id).sale, Math.round(ils*(1-rate)), p.id);
  }
  assert.equal(ctx.productDiscount('quote:abc'), 0);
  assert.equal(ctx.productDiscount(undefined), .1);  // category cards and popups name no product
  at.value = start - 1;
  assert.equal(ctx.productDiscount('glass-circle-candlesticks'), 0);
  at.value = end - 1;
  assert.equal(ctx.productDiscount('glass-circle-candlesticks'), .1);
  at.value = end;
  assert.equal(ctx.productDiscount('glass-circle-candlesticks'), 0);
  assert.equal(ctx.productDiscount(undefined), 0);
});

test('a set discounts the product and keeps the tray at its bundle price', () => {
  const ctx = browser({value: start});
  // Glass Circle Candlesticks with the white tray at its 406 bundle price.
  assert.equal(ctx.priceParts(505 + 406, 406, 'ILS', 'glass-circle-candlesticks').sale, Math.round(505*.9) + 406);
  const reg = ctx.usdFromIls(911), tray = ctx.usdFromIls(406);
  assert.equal(ctx.priceParts(911, 406, 'USD', 'glass-circle-candlesticks').sale, Math.round((reg - tray)*.9) + tray);
});

test('saved carts enter and leave the sale and keep quotes at their price', () => {
  const at = {value: start - 1};
  const ctx = browser(at);
  ctx.localStorage.setItem('sa_cart', JSON.stringify([
    {slug:'glass-circle-candlesticks', price_ils:505, qty:2, meta:{comment:'Keep this'}},
    {slug:'quote:abc', price_ils:1250, price_usd:400, qty:1}
  ]));
  assert.equal(ctx.getCart()[0].price_ils, 505);
  at.value = start;
  let cart = ctx.getCart();
  assert.equal(cart[0].price_ils, 455); assert.equal(cart[0].regular_price_ils, 505);
  assert.equal(cart[1].price_ils, 1250);
  at.value = end;
  cart = ctx.getCart();
  assert.equal(cart[0].price_ils, 505); assert.equal(cart[0].regular_price_ils, undefined);
  assert.equal(cart[0].qty, 2); assert.equal(cart[0].meta.comment, 'Keep this');
});
