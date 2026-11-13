
import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest


# 1. Load dataset
DATA_PATH = "dataset/raw/retail_store_inventory.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# 2. Select anomaly detection features
features = [
    "Units Sold",
    "Price",
    "Discount",
    "Holiday/Promotion"
]

X = df[features]


# 3. Create Isolation Forest model
# Assume approximately 5% of records may be unusual.

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)


# 4. Train model and detect anomalies
print("\nTraining Isolation Forest model...")

predictions = model.fit_predict(X)

print("Training completed successfully.")


# 5. Add anomaly results
df["Anomaly"] = predictions

df["Anomaly Status"] = df["Anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})


# 6. Display anomaly summary
print("\n===== ANOMALY DETECTION RESULTS =====")

print(df["Anomaly Status"].value_counts())


# 7. Calculate anomaly percentage
anomaly_count = (predictions == -1).sum()

anomaly_percentage = (
    anomaly_count / len(df)
) * 100

print("\nTotal records:", len(df))
print("Anomalies detected:", anomaly_count)
print(f"Anomaly percentage: {anomaly_percentage:.2f}%")


# 8. Display sample anomalies
print("\n===== SAMPLE ANOMALOUS RECORDS =====")

anomalies = df[df["Anomaly"] == -1]

print(
    anomalies[
        [
            "Date",
            "Store ID",
            "Product ID",
            "Units Sold",
            "Price",
            "Discount",
            "Holiday/Promotion"
        ]
    ].head(20).to_string(index=False)
)


# 9. Save anomaly results
os.makedirs("python-ai/models", exist_ok=True)

df.to_csv(
    "python-ai/isolation_forest_results.csv",
    index=False
)


# 10. Save trained model
joblib.dump(
    model,
    "python-ai/models/isolation_forest_model.joblib"
)

print("\nModel saved successfully:")
print("python-ai/models/isolation_forest_model.joblib")

print("\nResults saved successfully:")
print("python-ai/isolation_forest_results.csv")
