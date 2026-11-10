import pandas as pd
from pathlib import Path

# ============================================================
# RETAILAI - DATA ANALYSIS & CLEANING
# ============================================================

# Here I define the input file (raw data) and the output file (cleaned summary)
DATA_FILE = "retail_store_inventory.csv"
SUMMARY_FILE = "retailai_product_summary.csv"


# ------------------------------------------------------------
# 1. CHECK FILE
# ------------------------------------------------------------
# Here I am checking if the file is actually there to avoid a crash later.
if not Path(DATA_FILE).exists():
    raise FileNotFoundError(
        f"{DATA_FILE} was not found.\n"
        "Make sure it is in the same folder as analyze_data.py"
    )


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("RETAILAI - DATA ANALYSIS")
print("=" * 70)

print("\nLoading lecturer dataset...")

# Here I am loading the CSV file into a Pandas DataFrame so we can work with it.
df = pd.read_csv(DATA_FILE)

print(f"Records loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ------------------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------
# I am listing the columns that must be in the dataset for the AI to work.
required_columns = [
    "Date", "Store ID", "Product ID", "Category", "Region",
    "Inventory Level", "Units Sold", "Units Ordered", "Demand Forecast",
    "Price", "Discount", "Weather Condition", "Holiday/Promotion",
    "Competitor Pricing", "Seasonality"
]

# Here I check which of those required columns are missing from the CSV.
missing_columns = [col for col in required_columns if col not in df.columns]

# If any are missing, I stop the program and print exactly what is missing.
if missing_columns:
    raise ValueError(
        "\nMissing required columns:\n" + "\n".join(missing_columns)
    )


# ------------------------------------------------------------
# 4. DATA CLEANING
# ------------------------------------------------------------

# Here I convert the "Date" column from plain text into real Date objects.
# If it finds a bad date, it turns it into a blank value so the code doesn't crash.
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# I am listing the columns that are supposed to be numbers.
numeric_columns = [
    "Inventory Level", "Units Sold", "Units Ordered", "Demand Forecast",
    "Price", "Discount", "Holiday/Promotion", "Competitor Pricing"
]

# Here I force these columns to be numbers. If there is text, it becomes a blank value.
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Here I am deleting any row that is missing important information.
# If we don't know the date, product, units sold, or stock level, the row is useless to us.
df = df.dropna(subset=["Date", "Product ID", "Units Sold", "Inventory Level"])


# ------------------------------------------------------------
# 5. BASIC DATA INFORMATION
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)

# I am printing the earliest and latest dates so we know the time period of the data.
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

# I am counting the unique stores, products, categories, and regions to see how big the dataset is.
print(f"Number of stores: {df['Store ID'].nunique()}")
print(f"Number of products: {df['Product ID'].nunique()}")
print(f"Number of categories: {df['Category'].nunique()}")
print(f"Number of regions: {df['Region'].nunique()}")


# ------------------------------------------------------------
# 6. SALES CALCULATIONS
# ------------------------------------------------------------
# Here I am calculating the total units sold, ordered, and the average stock and forecast.
total_units_sold = df["Units Sold"].sum()
total_units_ordered = df["Units Ordered"].sum()
average_inventory = df["Inventory Level"].mean()
average_demand_forecast = df["Demand Forecast"].mean()

# I am creating a new column for Gross Revenue (Units Sold multiplied by Price).
df["Gross Revenue"] = df["Units Sold"] * df["Price"]

# Here I calculate how much money was lost due to discounts.
df["Discount Amount"] = df["Gross Revenue"] * (df["Discount"] / 100)

# I am creating the Net Revenue column by subtracting the discount from the gross revenue.
df["Net Revenue"] = df["Gross Revenue"] - df["Discount Amount"]

# Here I sum up the total revenue.
total_gross_revenue = df["Gross Revenue"].sum()
total_net_revenue = df["Net Revenue"].sum()

# I am printing all of these calculations to the screen to check the numbers.
print("\n" + "=" * 70)
print("SALES SUMMARY")
print("=" * 70)
print(f"Total units sold: {total_units_sold:,.0f}")
print(f"Total units ordered: {total_units_ordered:,.0f}")
print(f"Average inventory level: {average_inventory:,.2f}")
print(f"Average demand forecast: {average_demand_forecast:,.2f}")
print(f"Estimated gross revenue: R {total_gross_revenue:,.2f}")
print(f"Estimated net revenue after discounts: R {total_net_revenue:,.2f}")


# ------------------------------------------------------------
# 7. PRODUCT SUMMARY
# ------------------------------------------------------------
# Here I am grouping the data by Product ID so we can see the totals and averages for each product.
product_summary = (
    df.groupby("Product ID")
    .agg(
        Total_Units_Sold=("Units Sold", "sum"),
        Average_Daily_Units_Sold=("Units Sold", "mean"),
        Average_Inventory_Level=("Inventory Level", "mean"),
        Total_Units_Ordered=("Units Ordered", "sum"),
        Average_Demand_Forecast=("Demand Forecast", "mean"),
        Average_Price=("Price", "mean"),
        Total_Gross_Revenue=("Gross Revenue", "sum"),
        Total_Net_Revenue=("Net Revenue", "sum")
    )
    .reset_index()
)

# Here I am finding the most common category for each product.
product_category = (
    df.groupby("Product ID")["Category"]
    .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
    .reset_index()
)

# I am adding the category column to the product summary table.
product_summary = product_summary.merge(product_category, on="Product ID", how="left")

# Here I am reordering the columns so the table looks neat.
product_summary = product_summary[
    ["Product ID", "Category", "Total_Units_Sold", "Average_Daily_Units_Sold",
     "Average_Inventory_Level", "Total_Units_Ordered", "Average_Demand_Forecast",
     "Average_Price", "Total_Gross_Revenue", "Total_Net_Revenue"]
]


# ------------------------------------------------------------
# 8. TOP SELLING PRODUCTS
# ------------------------------------------------------------
# Here I sort the products by total units sold and keep only the top 10.
top_products = product_summary.sort_values("Total_Units_Sold", ascending=False).head(10)

print("\n" + "=" * 70)
print("TOP 10 SELLING PRODUCTS")
print("=" * 70)
print(top_products[["Product ID", "Category", "Total_Units_Sold"]].to_string(index=False))


# ------------------------------------------------------------
# 9. CATEGORY ANALYSIS
# ------------------------------------------------------------
# Here I am grouping by Category to see which categories sell the most.
category_summary = (
    df.groupby("Category")
    .agg(Total_Units_Sold=("Units Sold", "sum"),
         Average_Inventory=("Inventory Level", "mean"),
         Total_Revenue=("Net Revenue", "sum"))
    .sort_values("Total_Units_Sold", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("CATEGORY PERFORMANCE")
print("=" * 70)
print(category_summary.to_string(index=False))


# ------------------------------------------------------------
# 10. REGION ANALYSIS
# ------------------------------------------------------------
# Here I am grouping by Region to see which areas perform best.
region_summary = (
    df.groupby("Region")
    .agg(Total_Units_Sold=("Units Sold", "sum"),
         Average_Inventory=("Inventory Level", "mean"),
         Total_Revenue=("Net Revenue", "sum"))
    .sort_values("Total_Units_Sold", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("REGIONAL PERFORMANCE")
print("=" * 70)
print(region_summary.to_string(index=False))


# ------------------------------------------------------------
# 11. STORE ANALYSIS
# ------------------------------------------------------------
# Here I am grouping by Store ID to compare how each store is doing.
store_summary = (
    df.groupby("Store ID")
    .agg(Total_Units_Sold=("Units Sold", "sum"),
         Average_Inventory=("Inventory Level", "mean"),
         Total_Revenue=("Net Revenue", "sum"))
    .sort_values("Total_Units_Sold", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("STORE PERFORMANCE")
print("=" * 70)
print(store_summary.to_string(index=False))


# ------------------------------------------------------------
# 12. PROMOTION ANALYSIS
# ------------------------------------------------------------
# Here I am checking if promotions (1) actually increase sales compared to normal days (0).
promotion_summary = (
    df.groupby("Holiday/Promotion")
    .agg(Average_Units_Sold=("Units Sold", "mean"),
         Total_Units_Sold=("Units Sold", "sum"))
    .reset_index()
)

# I am renaming the 0 and 1 to readable text so the output is easier to understand.
promotion_summary["Promotion_Status"] = promotion_summary["Holiday/Promotion"].map({
    0: "No Promotion", 1: "Promotion/Holiday"
})

print("\n" + "=" * 70)
print("PROMOTION ANALYSIS")
print("=" * 70)
print(promotion_summary[["Promotion_Status", "Average_Units_Sold", "Total_Units_Sold"]].to_string(index=False))


# ------------------------------------------------------------
# 13. WEATHER ANALYSIS
# ------------------------------------------------------------
# Here I am checking how weather conditions affect sales.
weather_summary = (
    df.groupby("Weather Condition")
    .agg(Average_Units_Sold=("Units Sold", "mean"),
         Total_Units_Sold=("Units Sold", "sum"))
    .sort_values("Total_Units_Sold", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("WEATHER AND SALES")
print("=" * 70)
print(weather_summary.to_string(index=False))


# ------------------------------------------------------------
# 14. SEASONALITY ANALYSIS
# ------------------------------------------------------------
# Here I am checking which seasons generate the most sales.
season_summary = (
    df.groupby("Seasonality")
    .agg(Average_Units_Sold=("Units Sold", "mean"),
         Total_Units_Sold=("Units Sold", "sum"))
    .sort_values("Total_Units_Sold", ascending=False)
    .reset_index()
)

print("\n" + "=" * 70)
print("SEASONAL SALES")
print("=" * 70)
print(season_summary.to_string(index=False))


# ------------------------------------------------------------
# 15. FORECAST ERROR ANALYSIS
# ------------------------------------------------------------
# Here I am calculating the difference between what the AI predicted and what actually sold.
df["Forecast Error"] = df["Units Sold"] - df["Demand Forecast"]

# I am making all errors positive so they don't cancel each other out.
df["Absolute Forecast Error"] = df["Forecast Error"].abs()

# I am calculating the Mean Absolute Error (MAE) to see how many units the AI is typically off by.
mae = df["Absolute Forecast Error"].mean()

print("\n" + "=" * 70)
print("EXISTING DATASET FORECAST PERFORMANCE")
print("=" * 70)
print(f"Average forecast error (MAE): {mae:.2f} units")


# ------------------------------------------------------------
# 16. POSSIBLE LOW STOCK RECORDS
# ------------------------------------------------------------
# Here I am checking if the current stock is lower than the forecasted demand.
# If it is, this means we are at risk of a stockout.
df["Potential Stock Risk"] = df["Inventory Level"] < df["Demand Forecast"]

# I am counting how many times this risk occurred in the dataset.
stock_risk_count = df["Potential Stock Risk"].sum()

print("\n" + "=" * 70)
print("INVENTORY RISK")
print("=" * 70)
print(f"Records where inventory is below forecast demand: {stock_risk_count:,}")


# ------------------------------------------------------------
# 17. SAVE PRODUCT SUMMARY
# ------------------------------------------------------------
# Here I am saving the final product summary table to a new CSV file.
# The AI and the dashboard will use this file for their calculations.
product_summary.to_csv(SUMMARY_FILE, index=False)

print("\n" + "=" * 70)
print(f"Product summary saved successfully to:\n{SUMMARY_FILE}")
print("=" * 70)