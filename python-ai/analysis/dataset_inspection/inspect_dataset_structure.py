
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = PROJECT_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])

print("===== DATASET STRUCTURE REPORT =====")

# 1. Number of different dates
print("\n1. DATE INFORMATION")
print("Unique dates:", df["Date"].nunique())
print("Records per date:")
print(df.groupby("Date").size().describe())

# 2. Check store and product combinations
print("\n2. STORE AND PRODUCT COMBINATIONS")
print("Unique combinations:", df[["Store ID", "Product ID"]].drop_duplicates().shape[0])
print("Expected combinations:", df["Store ID"].nunique() * df["Product ID"].nunique())

# 3. Check whether combinations repeat on the same date
print("\n3. REPEATED STORE AND PRODUCT RECORDS")
print(
    df.duplicated(
        subset=["Date", "Store ID", "Product ID"]
    ).sum()
)

# 4. Check category values
print("\n4. PRODUCT CATEGORIES")
print(df["Category"].value_counts())

# 5. Check seasonality against months
print("\n5. SEASONALITY BY MONTH")
df["Month"] = df["Date"].dt.month
print(pd.crosstab(df["Month"], df["Seasonality"]))

# 6. Check sales and existing forecasts
print("\n6. SALES VS EXISTING FORECAST")
print(df[["Units Sold", "Demand Forecast"]].describe())
