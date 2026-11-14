"""Tests for the current Retail-X-AI chatbot assistant."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
CHATBOT_DIR = REPO_ROOT / "python-ai" / "chatbot"

if str(CHATBOT_DIR) not in sys.path:
    sys.path.insert(0, str(CHATBOT_DIR))

import assistant


class ChatbotAssistantTests(unittest.TestCase):

    def setUp(self):
        assistant.PENDING_STOCK_LOSS = None

    def tearDown(self):
        assistant.PENDING_STOCK_LOSS = None

    def predict_intent(self, intent):
        return patch.object(
            assistant.chatbot_model,
            "predict",
            return_value=[intent]
        )

    def test_empty_message(self):
        with self.predict_intent("GREETING") as predict:
            result = assistant.process_message("   ")

        self.assertEqual(result, "Please enter a question.")
        predict.assert_not_called()

    def test_greeting(self):
        with self.predict_intent("GREETING"):
            result = assistant.process_message("Hello")

        self.assertIn("Hello", result)
        self.assertIn("Retail-X-AI", result)

    def test_help_lists_chatbot_functions(self):
        with self.predict_intent("HELP"):
            result = assistant.process_message("Help")

        self.assertIn("Demand forecasting", result)
        self.assertIn("Inventory levels", result)
        self.assertIn("SKU code lookup", result)

    def test_goodbye(self):
        with self.predict_intent("GOODBYE"):
            result = assistant.process_message("Goodbye")

        self.assertIn("Goodbye", result)

    def test_out_of_scope_message(self):
        with self.predict_intent("OUT_OF_SCOPE"):
            result = assistant.process_message("Tell me a joke")

        self.assertIn("only assist with Retail-X-AI", result)

    def test_inventory_intent_routes_to_handler(self):
        with self.predict_intent("INVENTORY_LEVEL"):
            with patch.object(
                assistant,
                "handle_inventory_level",
                return_value="Inventory result"
            ) as handler:
                result = assistant.process_message(
                    "Show inventory for S001 P0001"
                )

        self.assertEqual(result, "Inventory result")
        handler.assert_called_once()

    def test_reorder_intent_routes_to_handler(self):
        with self.predict_intent("REORDER_RECOMMENDATION"):
            with patch.object(
                assistant,
                "handle_reorder_recommendation",
                return_value="Reorder result"
            ) as handler:
                result = assistant.process_message(
                    "What should S001 reorder for P0001?"
                )

        self.assertEqual(result, "Reorder result")
        handler.assert_called_once()

    def test_stockout_intent_routes_to_handler(self):
        with self.predict_intent("STOCKOUT_STATUS"):
            with patch.object(
                assistant,
                "handle_stockout_status",
                return_value="Stockout result"
            ) as handler:
                result = assistant.process_message(
                    "Check stockout status"
                )

        self.assertEqual(result, "Stockout result")
        handler.assert_called_once()

    def test_forecast_intent_routes_to_handler(self):
        with self.predict_intent("DEMAND_FORECAST"):
            with patch.object(
                assistant,
                "handle_demand_forecast",
                return_value="Forecast result"
            ) as handler:
                result = assistant.process_message(
                    "Show demand forecast"
                )

        self.assertEqual(result, "Forecast result")
        handler.assert_called_once()

    def test_forecast_discloses_historical_evaluation(self):
        summary = {
            "start_date": "2023-09-14",
            "end_date": "2024-01-01",
            "records": 100,
            "stores": 5,
            "products": 20,
            "actual_demand_total": 5000,
            "forecast_demand_total": 4900,
            "mae": 88.45,
            "rmse": 108.00,
        }

        metadata = {"model_name": "Ridge Regression"}

        with patch.object(
            assistant,
            "load_forecasts",
            return_value=object()
        ), patch.object(
            assistant,
            "load_forecast_metadata",
            return_value=metadata
        ), patch.object(
            assistant,
            "validate_forecast_metadata"
        ), patch.object(
            assistant,
            "summarize_forecasts",
            return_value=summary
        ):
            result = assistant.handle_demand_forecast()

        self.assertIn("historical one-step-ahead", result)
        self.assertIn("not predictions for future days", result)

    def test_sales_summary_discloses_historical_data(self):
        summary = {
            "start_date": __import__("datetime").datetime(2023, 9, 14),
            "end_date": __import__("datetime").datetime(2024, 1, 1),
            "total_records": 100,
            "total_units_sold": 500,
            "average_daily_sales": 10.5,
            "highest_sales_day": __import__("datetime").datetime(2023, 9, 15),
            "highest_daily_sales": 30,
            "store_sales": {"S001": 300},
            "category_sales": {"Food": 200},
        }

        with patch.object(
            assistant,
            "generate_sales_summary",
            return_value=summary
        ):
            result = assistant.handle_sales_summary()

        self.assertIn("not live sales", result)
        self.assertIn("historical sales", result)
        self.assertIn("S001", result)

    def test_handler_error_is_returned_as_message(self):
        with self.predict_intent("DEMAND_FORECAST"):
            with patch.object(
                assistant,
                "handle_demand_forecast",
                side_effect=FileNotFoundError("forecast file missing")
            ):
                result = assistant.process_message(
                    "Show demand forecast"
                )

        self.assertIn("Unable to retrieve demand forecast", result)
        self.assertIn("forecast file missing", result)

    def test_spoilage_record_starts_conversation(self):
        with self.predict_intent("SPOILAGE_RECORD"):
            result = assistant.process_message("Record spoiled stock")

        self.assertIn("record date", result.lower())
        self.assertEqual(
            assistant.PENDING_STOCK_LOSS["type"],
            "spoilage"
        )
        self.assertEqual(
            assistant.PENDING_STOCK_LOSS["step"],
            "date"
        )

    def test_damage_record_starts_conversation(self):
        with self.predict_intent("DAMAGE_RECORD"):
            result = assistant.process_message("Record damaged stock")

        self.assertIn("record date", result.lower())
        self.assertEqual(
            assistant.PENDING_STOCK_LOSS["type"],
            "damage"
        )

    def test_invalid_record_date_is_rejected(self):
        with self.predict_intent("SPOILAGE_RECORD"):
            assistant.process_message("Record spoiled stock")

        result = assistant.process_message("14/11/2026")

        self.assertIn("Invalid date", result)
        self.assertEqual(
            assistant.PENDING_STOCK_LOSS["step"],
            "date"
        )

    def test_stock_loss_recording_can_be_cancelled(self):
        with self.predict_intent("DAMAGE_RECORD"):
            assistant.process_message("Record damaged stock")

        result = assistant.process_message("cancel")

        self.assertEqual(
            result,
            "Stock loss recording cancelled."
        )
        self.assertIsNone(assistant.PENDING_STOCK_LOSS)

    def test_stock_loss_recording_validates_product_and_quantity(self):
        with self.predict_intent("SPOILAGE_RECORD"):
            assistant.process_message("Record spoiled stock")

        assistant.process_message("2026-11-14")
        assistant.process_message("S001")

        with patch.object(
            assistant,
            "get_sku_code",
            return_value="SKU-P0001"
        ) as sku_lookup:
            result = assistant.process_message("P0001")

        self.assertIn("Product verified", result)
        sku_lookup.assert_called_once_with("P0001")

        result = assistant.process_message("0")

        self.assertIn("positive whole number", result)
        self.assertEqual(
            assistant.PENDING_STOCK_LOSS["step"],
            "quantity"
        )


if __name__ == "__main__":
    unittest.main()