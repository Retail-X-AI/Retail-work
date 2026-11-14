
import pandas as pd

# Load the original dataset
df = pd.read_csv("dataset/raw/retail_store_inventory.csv")

print("===== DATASET QUALITY REPORT =====")

# 1. Check missing values
print("\n1. MISSING VALUES")
print(df.isnull().sum())

# 2. Check duplicate records
print("\n2. DUPLICATE RECORDS")
print(df.duplicated().sum())

# 3. Check data types
print("\n3. DATA TYPES")
print(df.dtypes)

# 4. Check date range
df["Date"] = pd.to_datetime(df["Date"])

print("\n4. DATE RANGE")
print("First date:", df["Date"].min())
print("Last date:", df["Date"].max())

# 5. Check unique products and stores
print("\n5. PRODUCT AND STORE INFORMATION")
print("Unique products:", df["Product ID"].nunique())
print("Unique stores:", df["Store ID"].nunique())

# 6. Check target variable
print("\n6. UNITS SOLD STATISTICS")
print(df["Units Sold"].describe())

