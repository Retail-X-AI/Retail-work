
import joblib
import pandas as pd
from pathlib import Path

from sklearn.ensemble import IsolationForest


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Load dataset
DATA_PATH = PROJECT_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"

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
MODEL_DIR = PROJECT_ROOT / "python-ai" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = PROJECT_ROOT / "python-ai" / "isolation_forest_results.csv"
MODEL_PATH = MODEL_DIR / "isolation_forest_model.joblib"

df.to_csv(RESULTS_PATH, index=False)


# 10. Save trained model
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully:")
print(MODEL_PATH)

print("\nResults saved successfully:")
print(RESULTS_PATH)

print("\nIsolation Forest training completed successfully.")