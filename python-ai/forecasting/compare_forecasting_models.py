
"""Fair comparison of four Retail-X-AI demand forecasting models."""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from xgboost import XGBRegressor

from feature_engineering import (
    prepare_forecasting_train_validation_test,
)


# ---------------------------------------------------------
# PATHS AND CONFIGURATION
# ---------------------------------------------------------

FORECASTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = FORECASTING_DIR.parents[1]

DATA_FILE = (
    REPO_ROOT
    / "dataset"
    / "raw"
    / "retail_store_inventory.csv"
)

OUTPUT_DIR = FORECASTING_DIR / "comparison_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METRICS_FILE = OUTPUT_DIR / "forecasting_model_comparison.json"
CSV_FILE = OUTPUT_DIR / "forecasting_model_comparison.csv"
PREDICTIONS_FILE = OUTPUT_DIR / "forecasting_model_predictions.csv"
REPORT_FILE = OUTPUT_DIR / "forecasting_model_comparison.md"

TARGET = "Units Sold"
RANDOM_SEED = 42

EPOCHS = 100
BATCH_SIZE = 256
PATIENCE = 10

tf.keras.utils.set_random_seed(RANDOM_SEED)


# ---------------------------------------------------------
# EVALUATION
# ---------------------------------------------------------

def evaluate_model(actual, predictions):
    """Calculate regression forecasting metrics."""

    actual = np.asarray(actual).reshape(-1)
    predictions = np.asarray(predictions).reshape(-1)

    return {
        "MAE": float(
            mean_absolute_error(actual, predictions)
        ),
        "RMSE": float(
            np.sqrt(mean_squared_error(actual, predictions))
        ),
        "R2": float(
            r2_score(actual, predictions)
        ),
    }


# ---------------------------------------------------------
# ANN ARCHITECTURE
# ---------------------------------------------------------

def build_ann(input_features):
    """Build the same ANN architecture used in train_ann.py."""

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_features,)),

        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.20),

        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.10),

        tf.keras.layers.Dense(32, activation="relu"),

        tf.keras.layers.Dense(1, activation="linear"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="mse",
        metrics=["mae"],
    )

    return model


# ---------------------------------------------------------
# MAIN COMPARISON
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("RETAIL-X-AI: FAIR FORECASTING MODEL COMPARISON")
    print("=" * 70)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    print("\nLoading dataset...")

    raw_df = pd.read_csv(DATA_FILE)

    print("Dataset shape:", raw_df.shape)

    # -----------------------------------------------------
    # PREPARE COMMON CHRONOLOGICAL SPLITS
    # -----------------------------------------------------

    print("\nPreparing common 70/15/15 chronological splits...")

    (
        train_df,
        validation_df,
        test_df,
        _,
        split_metadata,
    ) = prepare_forecasting_train_validation_test(
        raw_df,
        train_fraction=0.70,
        validation_fraction=0.15,
    )

    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError("A forecasting data split is empty.")

    if train_df["Date"].max() >= validation_df["Date"].min():
        raise ValueError("Training and validation dates overlap.")

    if validation_df["Date"].max() >= test_df["Date"].min():
        raise ValueError("Validation and test dates overlap.")

    feature_columns = [
        column
        for column in train_df.columns
        if column not in ("Date", TARGET)
    ]

    if not feature_columns:
        raise ValueError("No forecasting features were generated.")

    if list(validation_df[feature_columns].columns) != feature_columns:
        raise ValueError("Validation features do not match training.")

    if list(test_df[feature_columns].columns) != feature_columns:
        raise ValueError("Test features do not match training.")

    X_train = train_df[feature_columns]
    X_validation = validation_df[feature_columns]
    X_test = test_df[feature_columns]

    y_train = train_df[TARGET].to_numpy(dtype=np.float32)
    y_validation = validation_df[TARGET].to_numpy(dtype=np.float32)
    y_test = test_df[TARGET].to_numpy(dtype=np.float32)

    print("\nDATA SPLIT")
    print("Training records:", len(train_df))
    print("Validation records:", len(validation_df))
    print("Testing records:", len(test_df))
    print("Number of features:", len(feature_columns))

    print(
        "Training period:",
        train_df["Date"].min(),
        "to",
        train_df["Date"].max(),
    )

    print(
        "Validation period:",
        validation_df["Date"].min(),
        "to",
        validation_df["Date"].max(),
    )

    print(
        "Testing period:",
        test_df["Date"].min(),
        "to",
        test_df["Date"].max(),
    )

    # All feature matrices must contain finite numeric values.
    for name, matrix in {
        "Training": X_train,
        "Validation": X_validation,
        "Testing": X_test,
    }.items():

        if not np.isfinite(matrix.to_numpy(dtype=np.float64)).all():
            raise ValueError(
                f"{name} features contain non-finite values."
            )

    # -----------------------------------------------------
    # STORE RESULTS
    # -----------------------------------------------------

    results = {}
    prediction_data = pd.DataFrame({
        "Date": test_df["Date"].to_numpy(),
        "Actual Units Sold": y_test,
    })

    # -----------------------------------------------------
    # 1. RIDGE REGRESSION
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("1. TRAINING RIDGE REGRESSION")
    print("=" * 70)

    ridge_model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=10.0)),
    ])

    ridge_model.fit(X_train, y_train)

    ridge_validation_predictions = ridge_model.predict(
        X_validation
    )

    ridge_test_predictions = ridge_model.predict(X_test)

    results["Ridge Regression"] = {
        "validation": evaluate_model(
            y_validation,
            ridge_validation_predictions,
        ),
        "test": evaluate_model(
            y_test,
            ridge_test_predictions,
        ),
    }

    prediction_data["Ridge Regression"] = ridge_test_predictions

    print("Validation:", results["Ridge Regression"]["validation"])
    print("Test:", results["Ridge Regression"]["test"])

    # -----------------------------------------------------
    # 2. RANDOM FOREST
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("2. TRAINING RANDOM FOREST")
    print("=" * 70)

    random_forest_model = RandomForestRegressor(
        n_estimators=60,
        max_depth=18,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=RANDOM_SEED,
    )

    random_forest_model.fit(X_train, y_train)

    rf_validation_predictions = random_forest_model.predict(
        X_validation
    )

    rf_test_predictions = random_forest_model.predict(X_test)

    results["Random Forest"] = {
        "validation": evaluate_model(
            y_validation,
            rf_validation_predictions,
        ),
        "test": evaluate_model(
            y_test,
            rf_test_predictions,
        ),
    }

    prediction_data["Random Forest"] = rf_test_predictions

    print("Validation:", results["Random Forest"]["validation"])
    print("Test:", results["Random Forest"]["test"])

    # -----------------------------------------------------
    # 3. XGBOOST
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("3. TRAINING XGBOOST")
    print("=" * 70)

    xgboost_model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1,
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )

    xgboost_model.fit(X_train, y_train)

    xgb_validation_predictions = xgboost_model.predict(
        X_validation
    )

    xgb_test_predictions = xgboost_model.predict(X_test)

    results["XGBoost"] = {
        "validation": evaluate_model(
            y_validation,
            xgb_validation_predictions,
        ),
        "test": evaluate_model(
            y_test,
            xgb_test_predictions,
        ),
    }

    prediction_data["XGBoost"] = xgb_test_predictions

    print("Validation:", results["XGBoost"]["validation"])
    print("Test:", results["XGBoost"]["test"])

    # -----------------------------------------------------
    # 4. ARTIFICIAL NEURAL NETWORK
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("4. TRAINING ARTIFICIAL NEURAL NETWORK")
    print("=" * 70)

    tf.keras.backend.clear_session()
    tf.keras.utils.set_random_seed(RANDOM_SEED)

    ann_scaler = StandardScaler()

    X_train_ann = ann_scaler.fit_transform(
        X_train
    ).astype(np.float32)

    X_validation_ann = ann_scaler.transform(
        X_validation
    ).astype(np.float32)

    X_test_ann = ann_scaler.transform(
        X_test
    ).astype(np.float32)

    ann_model = build_ann(X_train_ann.shape[1])

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=PATIENCE,
        restore_best_weights=True,
        verbose=1,
    )

    history = ann_model.fit(
        X_train_ann,
        y_train,
        validation_data=(
            X_validation_ann,
            y_validation,
        ),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stopping],
        verbose=1,
        shuffle=False,
    )

    best_epoch = int(
        np.argmin(history.history["val_loss"]) + 1
    )

    ann_validation_predictions = ann_model.predict(
        X_validation_ann,
        verbose=0,
    ).reshape(-1)

    ann_test_predictions = ann_model.predict(
        X_test_ann,
        verbose=0,
    ).reshape(-1)

    results["ANN"] = {
        "validation": evaluate_model(
            y_validation,
            ann_validation_predictions,
        ),
        "test": evaluate_model(
            y_test,
            ann_test_predictions,
        ),
        "best_epoch": best_epoch,
    }

    prediction_data["ANN"] = ann_test_predictions

    print("Best epoch:", best_epoch)
    print("Validation:", results["ANN"]["validation"])
    print("Test:", results["ANN"]["test"])

    # -----------------------------------------------------
    # BASELINE COMPARISON
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("BASELINE COMPARISON")
    print("=" * 70)

    if "demand_lag_1" in feature_columns:

        previous_day_predictions = X_test[
            "demand_lag_1"
        ].to_numpy()

        results["Previous-day Baseline"] = {
            "test": evaluate_model(
                y_test,
                previous_day_predictions,
            )
        }

        prediction_data["Previous-day Baseline"] = (
            previous_day_predictions
        )

    average_predictions = np.full(
        len(y_test),
        float(np.mean(y_train)),
    )

    results["Training Mean Baseline"] = {
        "test": evaluate_model(
            y_test,
            average_predictions,
        )
    }

    prediction_data["Training Mean Baseline"] = (
        average_predictions
    )

    # -----------------------------------------------------
    # SAVE COMPARISON RESULTS
    # -----------------------------------------------------

    print("\nSaving comparison evidence...")

    comparison_rows = []

    for model_name, model_results in results.items():

        for evaluation_type in ("validation", "test"):

            if evaluation_type not in model_results:
                continue

            metrics = model_results[evaluation_type]

            comparison_rows.append({
                "Model": model_name,
                "Evaluation": evaluation_type.capitalize(),
                "MAE": metrics["MAE"],
                "RMSE": metrics["RMSE"],
                "R2": metrics["R2"],
            })

    comparison_df = pd.DataFrame(comparison_rows)

    comparison_df.to_csv(
        CSV_FILE,
        index=False,
    )

    prediction_data.to_csv(
        PREDICTIONS_FILE,
        index=False,
    )

    metadata = {
        "comparison_name": "Retail-X-AI Forecasting Model Comparison",
        "target": TARGET,
        "dataset": DATA_FILE.relative_to(REPO_ROOT).as_posix(),
        "models": results,
        "feature_count": len(feature_columns),
        "feature_columns": feature_columns,
        "training_rows": len(train_df),
        "validation_rows": len(validation_df),
        "testing_rows": len(test_df),
        "training_start": str(train_df["Date"].min()),
        "training_end": str(train_df["Date"].max()),
        "validation_start": str(validation_df["Date"].min()),
        "validation_end": str(validation_df["Date"].max()),
        "testing_start": str(test_df["Date"].min()),
        "testing_end": str(test_df["Date"].max()),
        "training_data_used_for_all_models": True,
        "validation_data_used_for_model_selection": True,
        "test_data_used_for_training": False,
        "test_data_used_for_validation": False,
        "ann_best_epoch": best_epoch,
        "random_seed": RANDOM_SEED,
        "split_metadata": {
            key: str(value)
            if isinstance(value, (pd.Timestamp, np.datetime64))
            else value
            for key, value in split_metadata.items()
        },
    }

    METRICS_FILE.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # GENERATE MARKDOWN REPORT
    # -----------------------------------------------------

    report = [
        "# Retail-X-AI Forecasting Model Comparison",
        "",
        "## Objective",
        "",
        "Compare Ridge Regression, Random Forest, XGBoost and "
        "Artificial Neural Network models using the same "
        "chronological data split and forecasting features.",
        "",
        "## Dataset and data split",
        "",
        f"- Dataset: `{DATA_FILE.relative_to(REPO_ROOT).as_posix()}`",
        f"- Target: `{TARGET}`",
        f"- Features: {len(feature_columns)}",
        f"- Training records: {len(train_df):,}",
        f"- Validation records: {len(validation_df):,}",
        f"- Testing records: {len(test_df):,}",
        f"- Training period: {train_df['Date'].min()} to "
        f"{train_df['Date'].max()}",
        f"- Validation period: {validation_df['Date'].min()} to "
        f"{validation_df['Date'].max()}",
        f"- Testing period: {test_df['Date'].min()} to "
        f"{test_df['Date'].max()}",
        "",
        "All four models used the same training records and "
        "the same engineered features. The test data was not "
        "used for training or validation.",
        "",
        "## Model configurations",
        "",
        "- Ridge Regression: alpha = 10.0",
        "- Random Forest: 60 trees, maximum depth 18, "
        "minimum leaf size 3",
        "- XGBoost: 500 estimators, learning rate 0.05, "
        "maximum depth 6",
        "- ANN: Dense layers of 128, 64 and 32 neurons, "
        "ReLU activation, dropout and Adam optimizer",
        "",
        f"ANN best epoch: {best_epoch}",
        "",
        "## Validation and test results",
        "",
        "| Model | Evaluation | MAE | RMSE | R² |",
        "|---|---|---:|---:|---:|",
    ]

    for row in comparison_rows:
        report.append(
            f"| {row['Model']} | {row['Evaluation']} | "
            f"{row['MAE']:.4f} | {row['RMSE']:.4f} | "
            f"{row['R2']:.4f} |"
        )

    report.extend([
        "",
        "## Interpretation",
        "",
        "Lower MAE and RMSE indicate smaller forecasting errors. "
        "An R² value closer to 1 indicates a stronger fit relative "
        "to predicting the target mean.",
        "",
        "The final model comparison should consider both MAE and "
        "RMSE, validation performance, test performance and "
        "prediction behaviour.",
        "",
        "The baseline models provide reference points for assessing "
        "whether machine learning improves on simple historical "
        "demand estimates.",
        "",
        "## Limitations",
        "",
        "This experiment evaluates historical one-step-ahead demand "
        "estimates using engineered historical demand features. "
        "It does not establish long-horizon future forecasting "
        "performance.",
        "",
        "The models use fixed configurations. The results do not "
        "represent an exhaustive hyperparameter search.",
        "",
        "## Generated evidence",
        "",
        "- `forecasting_model_comparison.csv`",
        "- `forecasting_model_comparison.json`",
        "- `forecasting_model_predictions.csv`",
        "",
    ])

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # DISPLAY FINAL TEST RANKING
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL TEST PERFORMANCE")
    print("=" * 70)

    test_ranking = comparison_df[
        comparison_df["Evaluation"] == "Test"
    ].sort_values("MAE")

    print(
        test_ranking[
            ["Model", "MAE", "RMSE", "R2"]
        ].to_string(index=False)
    )

    print("\nComparison completed successfully.")

    print("\nGenerated files:")
    print(METRICS_FILE)
    print(CSV_FILE)
    print(PREDICTIONS_FILE)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
