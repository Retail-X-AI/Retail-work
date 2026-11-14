"""M14-04 integration tests for the application restocking service."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from application.backend.recommendations import service  # noqa: E402

class RestockingIntegrationTests(unittest.TestCase):

    def test_service_returns_integrated_historical_recommendations(self):
        result = service.get_restocking_recommendations()

        self.assertTrue(result["success"])
        self.assertEqual(result["data_classification"], "HISTORICAL_DATA")
        self.assertTrue(result["source_date"])
        self.assertGreater(result["record_count"], 0)
        self.assertEqual(
            result["record_count"],
            len(result["recommendations"]),
        )

        for record in result["recommendations"]:
            self.assertIn("reorder_recommendation", record)
            self.assertIn("stockout_status", record)
            self.assertIn(
                "recommendation_status",
                record["reorder_recommendation"],
            )

        self.assertIn("reorder_status_counts", result["summary"])
        self.assertIn("stockout_status_counts", result["summary"])
        self.assertIn("not live stock", result["warning"])

        # API response must be valid strict JSON.
        json.dumps(result, allow_nan=False)

    def test_missing_forecast_file_is_reported(self):
        with patch.object(
            service,
            "FORECAST_PATH",
            REPO_ROOT / "missing_forecast_test_file.csv",
        ):
            with self.assertRaises(FileNotFoundError):
                service.get_restocking_recommendations()


if __name__ == "__main__":
    unittest.main()
