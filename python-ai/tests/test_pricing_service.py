"""Unit tests for the Retail-X-AI competitive pricing engine."""
import unittest
from application.backend.pricing.service import recommend_price


class CompetitivePricingTests(unittest.TestCase):
    def test_recommends_profitable_undercut(self):
        result = recommend_price(28, 35, [34, 33.50], 15)
        self.assertEqual(result["recommended_price"], 33.49)
        self.assertEqual(result["status"], "UNDERCUT_RECOMMENDED")
        self.assertGreaterEqual(result["gross_margin_percent"], 15)

    def test_does_not_undercut_below_margin_floor(self):
        result = recommend_price(30, 40, [31], 20)
        self.assertEqual(result["recommended_price"], 40.00)
        self.assertEqual(result["status"], "CANNOT_UNDERCUT_PROFITABLY")

    def test_increases_price_when_current_price_breaks_margin_floor(self):
        result = recommend_price(30, 32, [], 20)
        self.assertEqual(result["recommended_price"], 37.50)
        self.assertEqual(result["status"], "MARGIN_FLOOR_PRICE_INCREASE")

    def test_keeps_price_when_no_competitor_data_and_margin_is_met(self):
        result = recommend_price(20, 30, [], 15)
        self.assertEqual(result["recommended_price"], 30.00)
        self.assertEqual(result["status"], "NO_COMPETITOR_DATA")

    def test_keeps_current_price_when_already_competitive(self):
        result = recommend_price(20, 30, [32, 34], 15)
        self.assertEqual(result["recommended_price"], 30.00)
        self.assertEqual(result["status"], "PRICE_ALREADY_COMPETITIVE")

    def test_accepts_named_competitor_records(self):
        result = recommend_price(
            10, 20,
            [{"name": "Shop A", "price": 18.50}, {"name": "Shop B", "price": 19}],
            15,
        )
        self.assertEqual(result["competitor_count"], 2)
        self.assertEqual(result["lowest_competitor_price"], 18.50)

    def test_rejects_invalid_margin(self):
        with self.assertRaises(ValueError):
            recommend_price(10, 20, [19], 100)

    def test_rejects_negative_competitor_price(self):
        with self.assertRaises(ValueError):
            recommend_price(10, 20, [-1], 15)


if __name__ == "__main__":
    unittest.main()
