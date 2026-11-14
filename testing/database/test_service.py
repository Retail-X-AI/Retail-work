
"""Database service tests using an isolated temporary SQLite database."""

import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_PATH = PROJECT_ROOT / "database" / "service.py"

spec = importlib.util.spec_from_file_location("service_module", SERVICE_PATH)
service = importlib.util.module_from_spec(spec)
sys.modules["service_module"] = service
spec.loader.exec_module(service)


class DatabaseServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.original_database_dir = service.DATABASE_DIR
        cls.original_database_path = service.DATABASE_PATH

        test_database_dir = Path(cls.temp_dir.name)
        service.DATABASE_DIR = test_database_dir
        service.DATABASE_PATH = test_database_dir / "test_inventory.db"

        cls.expected_records = len(
            service.pd.read_csv(service.CSV_PATH)
        )

        cls.imported_records = service.initialize_database(
            force_reload=True
        )

    @classmethod
    def tearDownClass(cls):
        service.DATABASE_DIR = cls.original_database_dir
        service.DATABASE_PATH = cls.original_database_path
        cls.temp_dir.cleanup()

    def test_schema_creation(self):
        """Verify that required tables and indexes exist."""
        with service.get_connection() as conn:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }

            indexes = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='index'"
                )
            }

        self.assertTrue({
            "inventory_records",
            "import_metadata",
            "products",
            "spoilage_records",
            "damage_records",
        }.issubset(tables))

        self.assertTrue({
            "idx_inventory_date",
            "idx_inventory_store_product",
            "idx_inventory_product",
        }.issubset(indexes))

    def test_integrity_check(self):
        """Verify SQLite database integrity."""
        with service.get_connection() as conn:
            result = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()

        self.assertEqual(result[0], "ok")

    def test_data_import_count(self):
        """Verify that the imported record count matches the CSV."""
        self.assertEqual(
            self.imported_records,
            self.expected_records,
        )

        summary = service.get_inventory_summary()

        self.assertEqual(
            summary["records"],
            self.expected_records,
        )
        self.assertGreater(summary["stores"], 0)
        self.assertGreater(summary["products"], 0)
        self.assertGreater(summary["categories"], 0)

    def test_data_validation_constraints(self):
        """Verify that SQLite rejects invalid inventory values."""
        columns = [
            "record_date",
            "store_id",
            "product_id",
            "category",
            "region",
            "inventory_level",
            "units_sold",
            "units_ordered",
            "demand_forecast",
            "price",
            "discount",
            "weather_condition",
            "holiday_promotion",
            "competitor_pricing",
            "seasonality",
        ]

        valid_values = [
            "2026-11-01",
            "TEST_STORE",
            "TEST_PRODUCT",
            "Test Category",
            "Test Region",
            10,
            5,
            5,
            8.0,
            10.0,
            0.0,
            "Sunny",
            0,
            10.0,
            "Summer",
        ]

        sql = (
            "INSERT INTO inventory_records "
            f"({', '.join(columns)}) "
            f"VALUES ({', '.join(['?'] * len(columns))})"
        )

        invalid_cases = {
            "inventory_level": -5,
            "units_sold": -1,
            "units_ordered": -1,
            "price": -1.0,
            "discount": 150.0,
            "holiday_promotion": 2,
            "competitor_pricing": -1.0,
        }

        for column, invalid_value in invalid_cases.items():
            with self.subTest(column=column):
                values = valid_values.copy()
                values[columns.index(column)] = invalid_value

                with service.get_connection() as conn:
                    with self.assertRaises(sqlite3.IntegrityError):
                        conn.execute(sql, values)


if __name__ == "__main__":
    unittest.main()
