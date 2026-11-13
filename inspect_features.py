
import pandas as pd

df = pd.read_csv("dataset/raw/retail_store_inventory.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("===== FEATURE INVESTIGATION =====")

# 1. How many seasons are assigned to each month?
print("\n1. NUMBER OF SEASONS PER MONTH")
print(df.groupby(df["Date"].dt.month)["Seasonality"].nunique())

# 2. How many different seasons appear on each date?
print("\n2. SEASONS PER DATE")
print(df.groupby("Date")["Seasonality"].nunique().value_counts())

# 3. Date range covered by each season label
print("\n3. DATE RANGE PER SEASON")
print(
    df.groupby("Seasonality")["Date"]
    .agg(["min", "max", "nunique"])
)

# 4. Check negative values in important columns
print("\n4. NEGATIVE VALUES")
columns = [
    "Units Sold",
    "Inventory Level",
    "Units Ordered",
    "Demand Forecast",
    "Price",
    "Competitor Pricing"
]

for column in columns:
    print(column, ":", (df[column] < 0).sum())

# 5. Display sample records for investigation
print("\n5. SAMPLE RECORDS")
print(
    df[[
        "Date",
        "Store ID",
        "Product ID",
        "Inventory Level",
        "Units Sold",
        "Units Ordered",
        "Demand Forecast"
    ]].head(10).to_string(index=False)
)
