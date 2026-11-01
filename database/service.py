"""SQLite database integration for Retail-X-AI inventory data."""
import hashlib
import sqlite3
from contextlib import contextmanager
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1] 
DATABASE_DIR = PROJECT_ROOT / "database"
SCHEMA_PATH = DATABASE_DIR / "sqlite_schema.sql"
CSV_PATH = PROJECT_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"
DATABASE_PATH = DATABASE_DIR / "retail_inventory.db"

EXPECTED_COLUMNS = [
    "Date", "Store ID", "Product ID", "Category", "Region",
    "Inventory Level", "Units Sold", "Units Ordered", "Demand Forecast",
    "Price", "Discount", "Weather Condition", "Holiday/Promotion",
    "Competitor Pricing", "Seasonality",
]

COLUMN_MAPPING = {
    "Date": "record_date", "Store ID": "store_id", "Product ID": "product_id",
    "Category": "category", "Region": "region", "Inventory Level": "inventory_level",
    "Units Sold": "units_sold", "Units Ordered": "units_ordered",
    "Demand Forecast": "demand_forecast", "Price": "price", "Discount": "discount",
    "Weather Condition": "weather_condition", "Holiday/Promotion": "holiday_promotion",
    "Competitor Pricing": "competitor_pricing", "Seasonality": "seasonality",
}

def _source_hash() -> str:
    """Return a checksum so unchanged CSV data is not imported repeatedly."""
    digest = hashlib.sha256()
    with CSV_PATH.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

@contextmanager
def get_connection():
    """Yield a database connection and always close it after use."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            yield connection
    finally:
        connection.close()

def initialize_database(force_reload: bool = False) -> int:
    """Create the schema and import the CSV when it has changed."""
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Inventory CSV not found: {CSV_PATH}")
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Database schema not found: {SCHEMA_PATH}")

    current_hash = _source_hash()
    with get_connection() as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8-sig")
        connection.executescript(schema)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS import_metadata (
                source_name TEXT PRIMARY KEY,
                source_hash TEXT NOT NULL,
                imported_rows INTEGER NOT NULL
            )
            """
        )
        metadata = connection.execute(
            "SELECT source_hash, imported_rows FROM import_metadata "
            "WHERE source_name = ?",
            (CSV_PATH.name,),
        ).fetchone()

        if (not force_reload and metadata and metadata[0] == current_hash):
            actual_rows = connection.execute(
                "SELECT COUNT(*) FROM inventory_records"
            ).fetchone()[0]
            if actual_rows == metadata[1]:
                return actual_rows

        frame = pd.read_csv(CSV_PATH)
        missing = set(EXPECTED_COLUMNS) - set(frame.columns)
        if missing:
            raise ValueError(
                "Inventory CSV is missing required columns: "
                + ", ".join(sorted(missing))
            )
        frame = frame[EXPECTED_COLUMNS].rename(columns=COLUMN_MAPPING)

        if frame.isnull().any().any():
            raise ValueError(
                "Inventory CSV contains missing values in required fields."
            )

        frame["record_date"] = pd.to_datetime(
            frame["record_date"], errors="raise"
        ).dt.strftime("%Y-%m-%d")
        
        for column in ("inventory_level", "units_sold", "units_ordered"):
            numeric = pd.to_numeric(frame[column], errors="raise")
            if (numeric < 0).any() or (numeric % 1 != 0).any():
                raise ValueError(
                    f"{column} must contain non-negative whole numbers."
                )
            frame[column] = numeric.astype("int64")

        for column in ("demand_forecast", "price", "discount", "competitor_pricing"):
            frame[column] = pd.to_numeric(frame[column], errors="raise")

        if ((frame["price"] < 0).any() or (frame["competitor_pricing"] < 0).any() or (~frame["discount"].between(0, 100)).any()):
            raise ValueError("Price or discount values are outside valid ranges.")
        
        promotion = frame["holiday_promotion"]
        if not promotion.isin([0, 1, True, False]).all():
            raise ValueError(
                "Holiday/Promotion must contain only 0/1 or True/False."
            )
        frame["holiday_promotion"] = promotion.astype("int64")

        connection.execute("BEGIN")
        try:
            connection.execute("DELETE FROM inventory_records")
            columns = ", ".join(f'"{column}"' for column in frame.columns)
            placeholders = ", ".join("?" for _ in frame.columns)
            insert_sql = (
                f"INSERT INTO inventory_records ({columns}) "
                f"VALUES ({placeholders})"
            )
            rows = (
                tuple(value.item() if hasattr(value, "item") else value for value in row)
                for row in frame.itertuples(index=False, name=None)
            )
            connection.executemany(insert_sql, rows)

            imported_rows = connection.execute(
                "SELECT COUNT(*) FROM inventory_records"
            ).fetchone()[0]
            
            if imported_rows != len(frame):
                raise RuntimeError(
                    f"Import mismatch: expected {len(frame)}, found {imported_rows}."
                )
            
            connection.execute(
                """
                INSERT INTO import_metadata
                    (source_name, source_hash, imported_rows)
                VALUES (?, ?, ?)
                ON CONFLICT(source_name) DO UPDATE SET
                    source_hash = excluded.source_hash,
                    imported_rows = excluded.imported_rows
                """,
                (CSV_PATH.name, current_hash, imported_rows),
            )
        except Exception:
            connection.rollback()
            raise
        return imported_rows

def get_inventory_summary() -> dict:
    """Return basic counts from the imported inventory records."""
    with get_connection() as connection:
        row_count, stores, products, categories = connection.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT store_id),
                   COUNT(DISTINCT product_id), COUNT(DISTINCT category)
            FROM inventory_records
            """
        ).fetchone()
    return {
        "records": row_count,
        "stores": stores,
        "products": products,
        "categories": categories,
    }

if __name__ == "__main__":
    count = initialize_database()
    print(f"Database ready: {DATABASE_PATH}")
    print(f"Inventory records available: {count}")
    print(f"Inventory summary: {get_inventory_summary()}")