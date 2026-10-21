-- Drop tables if they exist to allow for clean reruns
DROP TABLE IF EXISTS INVENTORY_RECORD;
DROP TABLE IF EXISTS PRODUCT;
DROP TABLE IF EXISTS STORE;
DROP TABLE IF EXISTS DATE_DIM;
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS REGION;

-- 1. Create CATEGORY table
CREATE TABLE CATEGORY (
    Category_ID SERIAL PRIMARY KEY,
    Category_Name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Create REGION table
CREATE TABLE REGION (
    Region_ID SERIAL PRIMARY KEY,
    Region_Name VARCHAR(50) NOT NULL UNIQUE
);

-- 3. Create STORE table
CREATE TABLE STORE (
    Store_ID VARCHAR(10) PRIMARY KEY,
    Region_ID INT NOT NULL,
    Store_Name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_store_region FOREIGN KEY (Region_ID) REFERENCES REGION(Region_ID)
);

-- 4. Create PRODUCT table
CREATE TABLE PRODUCT (
    Product_ID VARCHAR(10) PRIMARY KEY,
    Category_ID INT NOT NULL,
    Product_Name VARCHAR(100) NOT NULL,
    Unit_Price DECIMAL(10, 2) NOT NULL CHECK (Unit_Price >= 0),
    Discount DECIMAL(5, 2) NOT NULL CHECK (Discount >= 0 AND Discount <= 100),
    CONSTRAINT fk_product_category FOREIGN KEY (Category_ID) REFERENCES CATEGORY(Category_ID)
);

-- 5. Create DATE_DIM table (Dimension)
CREATE TABLE DATE_DIM (
    Date_ID SERIAL PRIMARY KEY,
    Full_Date DATE NOT NULL UNIQUE,
    Day INT NOT NULL CHECK (Day BETWEEN 1 AND 31),
    Month INT NOT NULL CHECK (Month BETWEEN 1 AND 12),
    Year INT NOT NULL CHECK (Year >= 2000),
    Season VARCHAR(20) NOT NULL
);

-- 6. Create INVENTORY_RECORD table (Fact Table)
CREATE TABLE INVENTORY_RECORD (
    Record_ID SERIAL PRIMARY KEY,
    Date_ID INT NOT NULL,
    Store_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Inventory_Level INT NOT NULL CHECK (Inventory_Level >= 0),
    Units_Sold INT NOT NULL CHECK (Units_Sold >= 0),
    Units_Ordered INT NOT NULL CHECK (Units_Ordered >= 0),
    Demand_Forecast DECIMAL(10, 2) NOT NULL,
    Competitor_Pricing DECIMAL(10, 2) NOT NULL,
    Weather_Condition VARCHAR(50) NOT NULL,
    Holiday_Promotion BOOLEAN NOT NULL,
    Seasonality VARCHAR(20) NOT NULL,
    CONSTRAINT fk_inventory_date FOREIGN KEY (Date_ID) REFERENCES DATE_DIM(Date_ID),
    CONSTRAINT fk_inventory_store FOREIGN KEY (Store_ID) REFERENCES STORE(Store_ID),
    CONSTRAINT fk_inventory_product FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID)
);

-- ==========================================
-- M07-05 REQUIREMENT: INDEXES
-- ==========================================
CREATE INDEX idx_inventory_date ON INVENTORY_RECORD(Date_ID);
CREATE INDEX idx_inventory_store ON INVENTORY_RECORD(Store_ID);
CREATE INDEX idx_inventory_product ON INVENTORY_RECORD(Product_ID);
CREATE INDEX idx_inventory_store_product ON INVENTORY_RECORD(Store_ID, Product_ID);
CREATE INDEX idx_product_category ON PRODUCT(Category_ID);
