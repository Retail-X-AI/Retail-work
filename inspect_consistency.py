
import pandas as pd

df = pd.read_csv("dataset/raw/retail_store_inventory.csv")

print("===== STORE AND PRODUCT CONSISTENCY =====")

# 1. Check whether each store has one consistent region
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

# 2. Check whether each product has one consistent category
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

# 3. Check the available values in important features
print("\n3. DISCOUNT VALUES")
print(sorted(df["Discount"].unique()))

print("\n4. HOLIDAY/PROMOTION VALUES")
print(sorted(df["Holiday/Promotion"].unique()))

print("\n5. WEATHER CONDITIONS")
print(df["Weather Condition"].value_counts())

print("\n6. REGION VALUES")
print(df["Region"].value_counts())
