import sys
import unittest
import json
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from _hanukkah_sale import active, sale, START, END

class HanukkahSale(unittest.TestCase):
    def test_boundary_and_rounding(self):
        slug = "gold-tone-terracotta-half-moon-menorah"
        self.assertTrue(active(slug, datetime.fromisoformat(START)))
        self.assertFalse(active(slug, datetime.fromisoformat(END)))
        self.assertEqual(sale(1250, slug, datetime.fromisoformat(START)), 1000)
        self.assertEqual(sale(420, slug, datetime.fromisoformat(START)), 336)
        self.assertEqual(sale(1250, slug, datetime.fromisoformat(END)), 1250)
        self.assertFalse(active("kudu-menorah", datetime.fromisoformat(START)))

    def test_feed_sale_is_limited_and_dated(self):
        ns = "{http://base.google.com/ns/1.0}"
        for filename, regular, discounted in [("merchant-feed.xml", "1250.00 ILS", "1000.00 ILS"), ("merchant-feed-us.xml", "420.00 USD", "336.00 USD")]:
            items = ET.parse(ROOT / filename).getroot().findall("./channel/item")
            on_sale = [i for i in items if i.find(ns + "sale_price") is not None]
            expected_count = 48 if active("silver-tone-blue-half-moon-menorah") else 0
            self.assertEqual(len(on_sale), expected_count)
            for item in on_sale:
                self.assertIn("hanukkah-menorahs", item.findtext(ns + "link"))
                self.assertEqual(item.findtext(ns + "price"), regular)
                self.assertEqual(item.findtext(ns + "sale_price"), discounted)
                self.assertEqual(item.findtext(ns + "sale_price_effective_date"), START + "/" + END)

if __name__ == "__main__":
    unittest.main()
