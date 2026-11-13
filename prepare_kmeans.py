
import pandas as pd

# 1. Load dataset
DATA_PATH = "dataset/raw/retail_store_inventory.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# 2. Group data by product
product_data = df.groupby("Product ID").agg(
    average_units_sold=("Units Sold", "mean"),
    total_units_sold=("Units Sold", "sum"),
    sales_variation=("Units Sold", "std"),
    average_price=("Price", "mean"),
    average_discount=("Discount", "mean")
).reset_index()


# 3. Display product information
print("\n===== PRODUCT ANALYSIS =====")

print(product_data.to_string(index=False))


# 4. Display summary
print("\n===== SUMMARY =====")

print("Number of products:", len(product_data))

print("\nFeature statistics:")
print(product_data.describe().round(2))


# 5. Save prepared data
output_path = "python-ai/product_clustering_data.csv"

product_data.to_csv(output_path, index=False)

print("\nProduct data saved to:", output_path)
