
import os
import joblib
import numpy as np
import pandas as pd

from xgboost import XGBRegressor

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 1. Load dataset
DATA_PATH = "dataset/raw/retail_store_inventory.csv"

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])

print("Dataset loaded:", df.shape)


# 2. Sort records chronologically
group_columns = ["Store ID", "Product ID"]

df = df.sort_values(
    group_columns + ["Date"]
).reset_index(drop=True)


# 3. Create historical sales features
grouped_sales = df.groupby(group_columns)["Units Sold"]

df["sales_lag_1"] = grouped_sales.shift(1)
df["sales_lag_7"] = grouped_sales.shift(7)
df["sales_lag_14"] = grouped_sales.shift(14)
df["sales_lag_28"] = grouped_sales.shift(28)

df["rolling_mean_7"] = grouped_sales.transform(
    lambda x: x.shift(1).rolling(7).mean()
)

df["rolling_mean_28"] = grouped_sales.transform(
    lambda x: x.shift(1).rolling(28).mean()
)


# 4. Create date features
df["day_of_week"] = df["Date"].dt.day_of_week
df["day_of_month"] = df["Date"].dt.day
df["month"] = df["Date"].dt.month
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)


# 5. Remove records without sufficient history
df = df.dropna().reset_index(drop=True)


# 6. Select features and target
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

X = df[features]
y = df[target]


# 7. Prepare preprocessing
categorical_features = ["Store ID", "Product ID"]

numeric_features = [
    column for column in features
    if column not in categorical_features
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# 8. Split data chronologically (80% training, 20% testing)
dates = np.sort(df["Date"].unique())

split_date = dates[int(len(dates) * 0.8)]

train_mask = df["Date"] < split_date
test_mask = df["Date"] >= split_date

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

print("\n===== DATA SPLIT =====")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Split date:", split_date)


# 9. Create XGBoost model
xgboost_model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_lambda=1,
    random_state=42,
    n_jobs=-1
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("xgboost", xgboost_model)
    ]
)


# 10. Train model
print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

print("Training completed successfully.")


# 11. Generate predictions
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)


# 12. Evaluate model
def evaluate_model(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(actual, predicted)

    return mae, rmse, r2


train_mae, train_rmse, train_r2 = evaluate_model(
    y_train, train_predictions
)

test_mae, test_rmse, test_r2 = evaluate_model(
    y_test, test_predictions
)


# 13. Display performance
print("\n===== XGBOOST TRAINING PERFORMANCE =====")

print(f"Training MAE: {train_mae:.2f}")
print(f"Training RMSE: {train_rmse:.2f}")
print(f"Training R2: {train_r2:.4f}")

print("\n===== XGBOOST TESTING PERFORMANCE =====")

print(f"Testing MAE: {test_mae:.2f}")
print(f"Testing RMSE: {test_rmse:.2f}")
print(f"Testing R2: {test_r2:.4f}")

print("\n===== PREDICTION DISTRIBUTION =====")

print(f"Actual average: {y_test.mean():.2f}")
print(f"Predicted average: {test_predictions.mean():.2f}")

print(f"Actual standard deviation: {y_test.std():.2f}")
print(f"Predicted standard deviation: {np.std(test_predictions):.2f}")


# 14. Compare against simple baselines
previous_day_predictions = X_test["sales_lag_1"]

average_predictions = np.full(
    len(y_test),
    y_train.mean()
)

print("\n===== BASELINE COMPARISON =====")

print(
    "Previous-day MAE:",
    f"{mean_absolute_error(y_test, previous_day_predictions):.2f}"
)

print(
    "Previous-day RMSE:",
    f"{np.sqrt(mean_squared_error(y_test, previous_day_predictions)):.2f}"
)

print(
    "Average-demand MAE:",
    f"{mean_absolute_error(y_test, average_predictions):.2f}"
)

print(
    "Average-demand RMSE:",
    f"{np.sqrt(mean_squared_error(y_test, average_predictions)):.2f}"
)


# 15. Feature importance
feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

importances = model.named_steps[
    "xgboost"
].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\n===== XGBOOST FEATURE IMPORTANCE =====")
print(importance_df.to_string(index=False))


# 16. Save trained model
os.makedirs("python-ai/models", exist_ok=True)

model_path = "python-ai/models/xgboost_demand_model.joblib"

joblib.dump(model, model_path)

print("\nModel saved successfully:", model_path)

print("\nXGBoost training process completed.")
