
import pandas as pd

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

PROJECT_ROOT = Path(__file__).resolve().parents[3]
# 1. Load prepared product data
DATA_PATH = PROJECT_ROOT / "python-ai" / "product_clustering_data.csv"

df = pd.read_csv(DATA_PATH)

# 2. Select clustering features
features = [
    "average_units_sold",
    "sales_variation",
    "average_price",
    "average_discount"
]

X = df[features]


# 3. Scale features
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# 4. Test different numbers of clusters
print("===== K-MEANS CLUSTER EVALUATION =====")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)

    inertia = kmeans.inertia_

    silhouette = silhouette_score(
        X_scaled,
        labels
    )

    print(f"\nNumber of clusters: {k}")
    print(f"Inertia: {inertia:.4f}")
    print(f"Silhouette Score: {silhouette:.4f}")


print("\nCluster evaluation completed.")
