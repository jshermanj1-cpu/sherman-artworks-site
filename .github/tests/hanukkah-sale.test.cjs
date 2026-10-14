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
const id = 'silver-tone-blue-half-moon-menorah';
const start = Date.parse('2026-10-12T00:00:00+03:00');
const end = Date.parse('2026-12-05T00:00:00+02:00');
test('every menorah gets the sale, unrelated products remain regular', () => {
  const ctx = browser({value:start});
  const products = JSON.parse(fs.readFileSync(path.join(root,'data/products.json'),'utf8'));
  let eligible=0;
  for(const p of products) {
    const rate=ctx.productDiscount(p.id);
    if(rate) { eligible++; assert.match(p.id, /-menorah$/); }
    const ils=p.price_ils || 500;
    assert.equal(ctx.priceParts(ils,0,'ILS',p.id).sale,rate ? Math.round(ils*.8) : ils);
  }
  // A new menorah colour has to join the sale list in js/site.js too.
  const menorahs = products.filter(p => p.category === 'hanukkah-menorahs').length;
  assert.ok(menorahs >= 48);
  assert.equal(eligible,menorahs);
  assert.equal(ctx.priceParts(1250,0,'USD',id).sale,336);
  assert.equal(ctx.priceParts(1250,0,'USD','kudu-menorah').sale,420);
});
test('saved carts enter and exit sale without losing quantity, metadata or quote prices', () => {
  const at={value:start-1};const ctx=browser(at);
  ctx.localStorage.setItem('sa_cart',JSON.stringify([
    {slug:id,price_ils:1250,qty:2,meta:{comment:'Keep this'}},
    {slug:'quote:abc',price_ils:1250,price_usd:400,qty:1}
  ]));
  assert.equal(ctx.getCart()[0].price_ils,1250);
  at.value=start;
  let cart=ctx.getCart();
  assert.equal(cart[0].price_ils,1000);assert.equal(cart[0].regular_price_ils,1250);
  assert.equal(ctx.cartLineParts(cart[0],'USD').sale,336);
  assert.equal(cart[1].price_ils,1250);
  at.value=end-1;assert.equal(ctx.getCart()[0].price_ils,1000);
  at.value=end;cart=ctx.getCart();
  assert.equal(cart[0].price_ils,1250);assert.equal(cart[0].regular_price_ils,undefined);
  assert.equal(cart[0].qty,2);assert.equal(cart[0].meta.comment,'Keep this');
  assert.equal(ctx.cartLineParts(cart[0],'USD').sale,420);
});
