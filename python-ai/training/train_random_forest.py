
import pandas as pd
import numpy as np
import joblib

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load dataset
DATA_PATH = PROJECT_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"
df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])

# 2. Sort records by store, product and date
df = df.sort_values(
    ["Store ID", "Product ID", "Date"]
).copy()

group_columns = ["Store ID", "Product ID"]

# 3. Create historical sales features
grouped_sales = df.groupby(group_columns)["Units Sold"]

df["sales_lag_1"] = grouped_sales.shift(1)
df["sales_lag_7"] = grouped_sales.shift(7)
df["sales_lag_14"] = grouped_sales.shift(14)
df["sales_lag_28"] = grouped_sales.shift(28)

# 4. Create historical averages
df["rolling_mean_7"] = grouped_sales.transform(
    lambda x: x.shift(1).rolling(7).mean()
)

df["rolling_mean_28"] = grouped_sales.transform(
    lambda x: x.shift(1).rolling(28).mean()
)

# 5. Extract date features
df["day_of_week"] = df["Date"].dt.day_of_week
df["day_of_month"] = df["Date"].dt.day
df["month"] = df["Date"].dt.month
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)

# 6. Remove rows without sufficient sales history
df = df.dropna().copy()

# 7. Define model inputs and target
features = [
    "Store ID",
    "Product ID",
    "sales_lag_1",
    "sales_lag_7",
    "sales_lag_14",
    "sales_lag_28",
    "rolling_mean_7",
    "rolling_mean_28",
    "day_of_week",
    "day_of_month",
    "month",
    "is_weekend"
]

target = "Units Sold"

# 8. Split chronologically (80% training, 20% testing)
dates = np.sort(df["Date"].unique())

split_date = dates[int(len(dates) * 0.8)]

train = df[df["Date"] < split_date]
test = df[df["Date"] >= split_date]

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

print("===== TRAINING INFORMATION =====")
print("Training records:", len(train))
print("Testing records:", len(test))
print("Split date:", split_date)

# 9. Prepare categorical features
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            ["Store ID", "Product ID"]
        )
    ],
    remainder="passthrough"
)

# 10. Create Random Forest model
# 10. Create Random Forest model

random_forest = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features=0.8,
    random_state=42,
    n_jobs=-1
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("random_forest", random_forest)
    ]
)
# 11. Train model
print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Training completed successfully.")
# Training performance diagnostics
train_predictions = model.predict(X_train)

print("\n===== TRAINING PERFORMANCE =====")
print("Training MAE:", round(
    mean_absolute_error(y_train, train_predictions), 2
))

print("Training RMSE:", round(
    np.sqrt(mean_squared_error(y_train, train_predictions)), 2
))

print("Training R2:", round(
    r2_score(y_train, train_predictions), 4
))

print("Actual training standard deviation:", round(y_train.std(), 2))
print("Predicted training standard deviation:", round(
    train_predictions.std(), 2
))

# 12. Make predictions
predictions = model.predict(X_test)
# Prediction distribution diagnostics
diagnostics = pd.DataFrame({
    "Date": test["Date"].values,
    "Actual": y_test.values,
    "Predicted": predictions
})

diagnostics["Absolute Error"] = abs(
    diagnostics["Actual"] - diagnostics["Predicted"]
)

print("\n===== ACTUAL VS PREDICTED DISTRIBUTION =====")
print(diagnostics[["Actual", "Predicted"]].describe().round(2))

print("\n===== MONTHLY PREDICTION PERFORMANCE =====")

monthly_results = diagnostics.groupby(
    diagnostics["Date"].dt.to_period("M")
).agg(
    Actual_Average=("Actual", "mean"),
    Predicted_Average=("Predicted", "mean"),
    MAE=("Absolute Error", "mean")
)

print(monthly_results.round(2).to_string())
# Compare against average training demand
average_predictions = np.full(
    len(y_test),
    y_train.mean()
)

average_mae = mean_absolute_error(
    y_test,
    average_predictions
)

average_rmse = np.sqrt(
    mean_squared_error(y_test, average_predictions)
)

print("\n===== AVERAGE DEMAND BASELINE =====")
print("Average training demand:", round(y_train.mean(), 2))
print("Baseline MAE:", round(average_mae, 2))
print("Baseline RMSE:", round(average_rmse, 2))

# Inspect actual and predicted salespython train_random_forest.py
print("\n===== PREDICTION DIAGNOSTICS =====")
print("Actual average:", round(y_test.mean(), 2))
print("Predicted average:", round(predictions.mean(), 2))
print("Actual standard deviation:", round(y_test.std(), 2))
print("Predicted standard deviation:", round(predictions.std(), 2))

# 13. Evaluate model
mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

# 14. Compare against previous-day sales
baseline_predictions = test["sales_lag_1"]

baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(y_test, baseline_predictions)
)

print("\n===== RANDOM FOREST RESULTS =====")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

print("\n===== PREVIOUS-DAY BASELINE =====")
print("Baseline MAE:", round(baseline_mae, 2))
print("Baseline RMSE:", round(baseline_rmse, 2))

# 15. Save trained model
model_folder = PROJECT_ROOT / "python-ai" / "models"
model_folder.mkdir(parents=True, exist_ok=True)

model_path = model_folder / "random_forest_demand_model.joblib"

joblib.dump(model, model_path)

print("\nModel saved successfully:")
print(model_path)


# 16. Analyse feature importance
print("\n===== FEATURE IMPORTANCE =====")

feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

importance = model.named_steps[
    "random_forest"
].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df.head(15).to_string(index=False))
