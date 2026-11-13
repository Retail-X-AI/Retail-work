
import joblib
import pandas as pd


# 1. Load results and trained model
df = pd.read_csv("python-ai/isolation_forest_results.csv")

model = joblib.load(
    "python-ai/models/isolation_forest_model.joblib"
)


# 2. Calculate anomaly scores
features = [
    "Units Sold",
    "Price",
    "Discount",
    "Holiday/Promotion"
]

df["Anomaly Score"] = model.decision_function(
    df[features]
)


# 3. Compare normal and anomalous records
print("===== NORMAL VS ANOMALOUS RECORDS =====")

comparison = df.groupby("Anomaly Status")[features].mean()

print(comparison.round(2).to_string())


# 4. Count anomalies by store
print("\n===== ANOMALIES BY STORE =====")

store_anomalies = (
    df[df["Anomaly"] == -1]
    .groupby("Store ID")
    .size()
    .sort_values(ascending=False)
)

print(store_anomalies.to_string())


# 5. Count anomalies by product
print("\n===== ANOMALIES BY PRODUCT =====")

product_anomalies = (
    df[df["Anomaly"] == -1]
    .groupby("Product ID")
    .size()
    .sort_values(ascending=False)
)

print(product_anomalies.to_string())


# 6. Display the 10 most unusual records
# Lower decision scores indicate more unusual records.
print("\n===== 10 MOST UNUSUAL RECORDS =====")

most_unusual = df.nsmallest(10, "Anomaly Score")

print(
    most_unusual[
        [
            "Date",
            "Store ID",
            "Product ID",
            "Units Sold",
            "Price",
            "Discount",
            "Anomaly Score"
        ]
    ].to_string(index=False)
)


print("\nAnomaly analysis completed.")
