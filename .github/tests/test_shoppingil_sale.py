import sys
import unittest
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from _shoppingil_sale import eligible, sale, upcoming, START, END
from _hanukkah_sale import START as HANUKKAH_START, END as HANUKKAH_END


class ShoppingILSale(unittest.TestCase):
    def test_window_rounding_and_eligibility(self):
        self.assertEqual(datetime.fromisoformat(START).isoformat(), "2026-11-03T00:00:00+02:00")
        self.assertEqual(datetime.fromisoformat(END).isoformat(), "2026-11-12T00:00:00+02:00")
        self.assertTrue(upcoming(datetime.fromisoformat(START)))
        self.assertFalse(upcoming(datetime.fromisoformat(END)))
        self.assertEqual(sale(505), 455)   # 454.5 rounds half up, like Math.round
        self.assertEqual(sale(517), 465)
        self.assertEqual(sale(170), 153)
        self.assertTrue(eligible("glass-circle-candlesticks"))
        self.assertTrue(eligible("kudu-menorah"))  # a shofar, not a Hanukkah menorah
        self.assertFalse(eligible("gold-tone-terracotta-half-moon-menorah"))
        self.assertFalse(eligible("quote:abc"))

    def test_feed_dates_the_sale_on_everything_but_menorahs(self):
        ns = "{http://base.google.com/ns/1.0}"
        window = START + "/" + END
        for filename, currency in [("merchant-feed.xml", "ILS"), ("merchant-feed-us.xml", "USD")]:
            items = ET.parse(ROOT / filename).getroot().findall("./channel/item")
            ours = [i for i in items if i.findtext(ns + "sale_price_effective_date") == window]
            menorahs = [i for i in items if i.findtext(ns + "sale_price_effective_date") == HANUKKAH_START + "/" + HANUKKAH_END]
            if not upcoming():
                self.assertEqual(ours, [])
                continue
            self.assertEqual(len(ours) + len(menorahs), len(items))
            for item in ours:
                regular, cur = item.findtext(ns + "price").split()
                discounted, sale_cur = item.findtext(ns + "sale_price").split()
                self.assertEqual(cur, currency)
                self.assertEqual(sale_cur, currency)
                self.assertEqual(float(discounted), sale(float(regular)))


if __name__ == "__main__":
    unittest.main()
