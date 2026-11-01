import sqlite3
import pytest
import pandas as pd
from pathlib import Path
import sys
import importlib.util

# 1. Define the exact path to service.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_PATH = PROJECT_ROOT / "database" / "service.py"

# 2. Load the module using its exact path
spec = importlib.util.spec_from_file_location("service_module", SERVICE_PATH)
service = importlib.util.module_from_spec(spec)
sys.modules["service_module"] = service
spec.loader.exec_module(service)

# 3. Assign the functions directly from the loaded module
initialize_database = service.initialize_database
get_connection = service.get_connection
get_inventory_summary = service.get_inventory_summary

@pytest.fixture(scope="module")
def setup_database():
    """Ensure the database is initialized before running tests."""
    initialize_database(force_reload=True)
    yield

@pytest.fixture(scope="module")
def setup_database():
    """Ensure the database is initialized before running tests."""
    initialize_database(force_reload=True)
    yield

def test_schema_creation(setup_database):
    """Test that all tables and indexes are created correctly."""
    with get_connection() as conn:
        # Check if main table exists
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        assert "inventory_records" in table_names
        assert "import_metadata" in table_names

        # Check if indexes exist
        indexes = conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
        index_names = [i[0] for i in indexes]
        assert "idx_inventory_date" in index_names
        assert "idx_inventory_store_product" in index_names

def test_integrity_check(setup_database):
    """Run SQLite's built-in integrity check."""
    with get_connection() as conn:
        result = conn.execute("PRAGMA integrity_check").fetchone()
        assert result[0] == "ok"

def test_data_import_count(setup_database):
    """Test that the correct number of records were imported from the CSV."""
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM inventory_records").fetchone()[0]
        # Based on your README, the dataset contains 73,100 records
        assert count == 73100

def test_data_validation_constraints(setup_database):
    """Test that the database prevents invalid data based on schema constraints."""
    with get_connection() as conn:
        # Try to insert a negative inventory level (should fail due to CHECK constraint)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("""
                INSERT INTO inventory_records 
                (record_date, store_id, product_id, category, region, inventory_level, units_sold, units_ordered, demand_forecast, price, discount, weather_condition, holiday_promotion, competitor_pricing, seasonality)
                VALUES ('2026-11-01', 'S1', 'P1', 'Cat', 'Reg', -5, 10, 10, 15.0, 10.0, 0.0, 'Sunny', 0, 10.0, 'Summer')
            """)
        
        # Try to insert an invalid discount > 100 (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("""
                INSERT INTO inventory_records 
                (record_date, store_id, product_id, category, region, inventory_level, units_sold, units_ordered, demand_forecast, price, discount, weather_condition, holiday_promotion, competitor_pricing, seasonality)
                VALUES ('2026-11-01', 'S1', 'P1', 'Cat', 'Reg', 10, 10, 10, 15.0, 10.0, 150.0, 'Sunny', 0, 10.0, 'Summer')
            """)
            
        # Try to insert invalid holiday_promotion (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("""
                INSERT INTO inventory_records 
                (record_date, store_id, product_id, category, region, inventory_level, units_sold, units_ordered, demand_forecast, price, discount, weather_condition, holiday_promotion, competitor_pricing, seasonality)
                VALUES ('2026-11-01', 'S1', 'P1', 'Cat', 'Reg', 10, 10, 10, 15.0, 10.0, 0.0, 'Sunny', 2, 10.0, 'Summer')
            """)

def test_inventory_summary_function(setup_database):
    """Test the get_inventory_summary function."""
    summary = get_inventory_summary()
    assert summary["records"] == 73100
    assert summary["stores"] > 0
    assert summary["products"] > 0
    assert summary["categories"] > 0