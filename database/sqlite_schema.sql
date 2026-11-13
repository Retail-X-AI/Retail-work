PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS inventory_records (
    record_id INTEGER PRIMARY KEY,
    record_date TEXT NOT NULL,
    store_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    inventory_level INTEGER NOT NULL CHECK (inventory_level >= 0),
    units_sold INTEGER NOT NULL CHECK (units_sold >= 0),
    units_ordered INTEGER NOT NULL CHECK (units_ordered >= 0),
    demand_forecast REAL NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    discount REAL NOT NULL CHECK (discount >= 0 AND discount <= 100),
    weather_condition TEXT NOT NULL,
    holiday_promotion INTEGER NOT NULL CHECK (holiday_promotion IN (0, 1)),
    competitor_pricing REAL NOT NULL CHECK (competitor_pricing >= 0),
    seasonality TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inventory_date
    ON inventory_records(record_date);

CREATE INDEX IF NOT EXISTS idx_inventory_store
    ON inventory_records(store_id);

CREATE INDEX IF NOT EXISTS idx_inventory_product
    ON inventory_records(product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_store_product
    ON inventory_records(store_id, product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_category
    ON inventory_records(category);

-- ==========================================
-- PRODUCT SKU MANAGEMENT
-- ==========================================

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    sku_code TEXT NOT NULL UNIQUE
);

-- ==========================================
-- SPOILAGE RECORDS
-- ==========================================

CREATE TABLE IF NOT EXISTS spoilage_records (
    spoilage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_date TEXT NOT NULL,
    store_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    reason TEXT NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- ==========================================
-- DAMAGE RECORDS
-- ==========================================

CREATE TABLE IF NOT EXISTS damage_records (
    damage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_date TEXT NOT NULL,
    store_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    reason TEXT NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- ==========================================
-- STOCK LOSS INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_spoilage_product
    ON spoilage_records(product_id);

CREATE INDEX IF NOT EXISTS idx_damage_product
    ON damage_records(product_id);