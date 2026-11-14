
import pandas as pd
from pathlib import Path


# 1. Set project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# 2. Load dataset
DATA_PATH = PROJECT_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully:", df.shape)


# 3. Check store and product consistency
print("\n===== STORE AND PRODUCT CONSISTENCY =====")


# 3.1 Check whether each store has one consistent region
print("\n1. REGIONS PER STORE")

print(
    df.groupby("Store ID")["Region"]
    .nunique()
)

print("\nREGION DETAILS")

print(
    df.groupby(["Store ID", "Region"])
    .size()
    .to_string()
)


# 3.2 Check whether each product has one consistent category
print("\n2. CATEGORIES PER PRODUCT")

print(
    df.groupby("Product ID")["Category"]
    .nunique()
)

print("\nCATEGORY DETAILS")

print(
    df.groupby(["Product ID", "Category"])
    .size()
    .to_string()
)


# 3.3 Check available values in important features
print("\n3. DISCOUNT VALUES")
print(sorted(df["Discount"].dropna().unique()))

print("\n4. HOLIDAY/PROMOTION VALUES")
print(sorted(df["Holiday/Promotion"].dropna().unique()))

print("\n5. WEATHER CONDITIONS")
print(df["Weather Condition"].value_counts())

print("\n6. REGION VALUES")
print(df["Region"].value_counts())


print("\nStore and product consistency inspection completed.")
