
import os
import joblib
import pandas as pd

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.metrics import silhouette_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Load prepared product data
DATA_PATH = PROJECT_ROOT / "python-ai" / "product_clustering_data.csv"
df = pd.read_csv(DATA_PATH)


# 2. Select features
features = [
    "average_units_sold",
    "sales_variation",
    "average_price",
    "average_discount"
]

X = df[features]


# 3. Create K-Means pipeline
model = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        (
            "kmeans",
            KMeans(
                n_clusters=2,
                random_state=42,
                n_init=10
            )
        )
    ]
)


# 4. Train model
print("Training K-Means model...")

labels = model.fit_predict(X)

print("Training completed successfully.")


# 5. Evaluate clustering
silhouette = silhouette_score(
    model.named_steps["scaler"].transform(X),
    labels
)

print("\n===== CLUSTER PERFORMANCE =====")
print("Number of clusters:", 2)
print(f"Silhouette score: {silhouette:.4f}")


# 6. Add cluster assignments
df["Cluster"] = labels


# 7. Display products in each cluster
print("\n===== PRODUCT CLUSTER ASSIGNMENTS =====")

print(
    df[["Product ID", "Cluster"]]
    .sort_values(["Cluster", "Product ID"])
    .to_string(index=False)
)


# 8. Analyse cluster characteristics
print("\n===== CLUSTER PROFILES =====")

cluster_profiles = df.groupby("Cluster")[features].mean()

print(cluster_profiles.round(2).to_string())


# 9. Show cluster sizes
print("\n===== CLUSTER SIZES =====")

print(df["Cluster"].value_counts().sort_index())


# 10. Save clustering results
MODEL_DIR = PROJECT_ROOT / "python-ai" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = PROJECT_ROOT / "python-ai" / "product_cluster_results.csv"
MODEL_PATH = MODEL_DIR / "kmeans_product_model.joblib"

df.to_csv(RESULTS_PATH, index=False)


# 11. Save trained model
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully:")
print(MODEL_PATH)

print("\nCluster results saved successfully:")
print(RESULTS_PATH)
