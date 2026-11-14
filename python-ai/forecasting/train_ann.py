
"""Train and evaluate an Artificial Neural Network for retail demand forecasting."""

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from feature_engineering import prepare_forecasting_train_validation_test


# ---------------------------------------------------------
# PATHS AND CONFIGURATION
# ---------------------------------------------------------

FORECASTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = FORECASTING_DIR.parents[1]

RAW_DATA_FILE = (
    REPO_ROOT
    / "dataset"
    / "raw"
    / "retail_store_inventory.csv"
)

ARTIFACT_DIR = FORECASTING_DIR / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = ARTIFACT_DIR / "retail_demand_ann_model.keras"
SCALER_FILE = ARTIFACT_DIR / "retail_demand_ann_scaler.joblib"
METADATA_FILE = ARTIFACT_DIR / "retail_demand_ann_metadata.json"
RESULTS_FILE = FORECASTING_DIR / "ann_forecasting_results.csv"
REPORT_FILE = FORECASTING_DIR / "M11-05-ann-forecasting-evidence.md"

TARGET_COLUMN = "Units Sold"

RANDOM_SEED = 42
EPOCHS = 100
BATCH_SIZE = 256
PATIENCE = 10

tf.keras.utils.set_random_seed(RANDOM_SEED)


# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

def prepare_arrays(train_df, validation_df, test_df):
    """Prepare ANN inputs using training-only feature scaling."""

    feature_columns = [
        column
        for column in train_df.columns
        if column not in ("Date", TARGET_COLUMN)
    ]

    if not feature_columns:
        raise ValueError("No forecasting features were found.")

    X_train = train_df[feature_columns].to_numpy(dtype=np.float32)
    X_validation = validation_df[feature_columns].to_numpy(dtype=np.float32)
    X_test = test_df[feature_columns].to_numpy(dtype=np.float32)

    y_train = train_df[TARGET_COLUMN].to_numpy(dtype=np.float32)
    y_validation = validation_df[TARGET_COLUMN].to_numpy(dtype=np.float32)
    y_test = test_df[TARGET_COLUMN].to_numpy(dtype=np.float32)

    for name, values in {
        "Training features": X_train,
        "Validation features": X_validation,
        "Testing features": X_test,
        "Training target": y_train,
        "Validation target": y_validation,
        "Testing target": y_test,
    }.items():
        if not np.isfinite(values).all():
            raise ValueError(f"{name} contain non-finite values.")

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train).astype(np.float32)
    X_validation_scaled = scaler.transform(X_validation).astype(np.float32)
    X_test_scaled = scaler.transform(X_test).astype(np.float32)

    return (
        X_train_scaled,
        X_validation_scaled,
        X_test_scaled,
        y_train,
        y_validation,
        y_test,
        scaler,
        feature_columns,
    )


# ---------------------------------------------------------
# ANN ARCHITECTURE
# ---------------------------------------------------------

def build_ann(input_features):
    """Build a feed-forward neural network for demand regression."""

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
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"],
    )

    return model


# ---------------------------------------------------------
# MODEL EVALUATION
# ---------------------------------------------------------

def evaluate_model(y_true, predictions):
    """Calculate forecasting evaluation metrics."""

    predictions = np.asarray(predictions).reshape(-1)
    y_true = np.asarray(y_true).reshape(-1)

    return {
        "MAE": float(mean_absolute_error(y_true, predictions)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, predictions))),
        "R2": float(r2_score(y_true, predictions)),
    }


# ---------------------------------------------------------
# MAIN TRAINING PROCESS
# ---------------------------------------------------------

def main():

    print("=" * 65)
    print("RETAIL-X-AI - ANN DEMAND FORECASTING")
    print("=" * 65)

    print("\nTensorFlow version:", tf.__version__)

    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_FILE}"
        )

    print("\nLoading retail dataset...")

    raw_df = pd.read_csv(RAW_DATA_FILE)

    print("Dataset shape:", raw_df.shape)

    print("\nPreparing chronological forecasting splits...")

    train_df, validation_df, test_df, _, split_metadata = (
        prepare_forecasting_train_validation_test(
            raw_df,
            train_fraction=0.70,
            validation_fraction=0.15,
        )
    )

    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError("One or more forecasting splits are empty.")

    if train_df["Date"].max() >= validation_df["Date"].min():
        raise ValueError("Training and validation dates overlap.")

    if validation_df["Date"].max() >= test_df["Date"].min():
        raise ValueError("Validation and testing dates overlap.")

    print("\nDATA SPLIT")
    print("Training records:", len(train_df))
    print("Validation records:", len(validation_df))
    print("Testing records:", len(test_df))

    (
        X_train,
        X_validation,
        X_test,
        y_train,
        y_validation,
        y_test,
        scaler,
        feature_columns,
    ) = prepare_arrays(train_df, validation_df, test_df)

    print("\nNumber of input features:", len(feature_columns))

    # -----------------------------------------------------
    # BUILD MODEL
    # -----------------------------------------------------

    print("\nBuilding Artificial Neural Network...")

    model = build_ann(X_train.shape[1])

    model.summary()

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=PATIENCE,
        restore_best_weights=True,
        verbose=1,
    )

    # -----------------------------------------------------
    # TRAIN MODEL
    # -----------------------------------------------------

    print("\nTraining ANN...")

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_validation, y_validation),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stopping],
        verbose=1,
        shuffle=False,
    )

    best_epoch = int(np.argmin(history.history["val_loss"]) + 1)

    print("\nTraining completed.")
    print("Best epoch:", best_epoch)

    # -----------------------------------------------------
    # VALIDATION EVALUATION
    # -----------------------------------------------------

    validation_predictions = model.predict(
        X_validation,
        verbose=0,
    ).reshape(-1)

    validation_metrics = evaluate_model(
        y_validation,
        validation_predictions,
    )

    # -----------------------------------------------------
    # FINAL TEST EVALUATION
    # -----------------------------------------------------

    print("\nEvaluating on untouched testing data...")

    test_predictions = model.predict(
        X_test,
        verbose=0,
    ).reshape(-1)

    test_metrics = evaluate_model(
        y_test,
        test_predictions,
    )

    print("\nVALIDATION RESULTS")
    for metric, value in validation_metrics.items():
        print(f"{metric}: {value:.4f}")

    print("\nTEST RESULTS")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")

    # -----------------------------------------------------
    # SAVE MODEL AND PREPROCESSING ARTIFACTS
    # -----------------------------------------------------

    model.save(MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)

    # Reload and verify the saved model.
    loaded_model = tf.keras.models.load_model(MODEL_FILE)
    loaded_scaler = joblib.load(SCALER_FILE)

    smoke_rows = min(10, len(X_train))

    original_predictions = model.predict(
        X_train[:smoke_rows],
        verbose=0,
    )

    reloaded_predictions = loaded_model.predict(
        X_train[:smoke_rows],
        verbose=0,
    )

    if not np.allclose(
        original_predictions,
        reloaded_predictions,
        rtol=1e-5,
        atol=1e-5,
    ):
        raise ValueError("Saved ANN predictions do not match the original.")

    if not np.allclose(
        scaler.transform(
            train_df[feature_columns].to_numpy(dtype=np.float32)[:smoke_rows]
        ),
        loaded_scaler.transform(
            train_df[feature_columns].to_numpy(dtype=np.float32)[:smoke_rows]
        ),
    ):
        raise ValueError("Saved scaler verification failed.")

    # -----------------------------------------------------
    # SAVE PREDICTION RESULTS
    # -----------------------------------------------------

    results_df = pd.DataFrame({
        "Date": test_df["Date"].to_numpy(),
        "Actual Units Sold": y_test,
        "Predicted Units Sold": test_predictions,
        "Prediction Error": y_test - test_predictions,
    })

    results_df.to_csv(RESULTS_FILE, index=False)

    # -----------------------------------------------------
    # SAVE METADATA
    # -----------------------------------------------------

    metadata = {
        "model_name": "Artificial Neural Network",
        "framework": "TensorFlow/Keras",
        "tensorflow_version": tf.__version__,
        "target_column": TARGET_COLUMN,
        "source_dataset": RAW_DATA_FILE.relative_to(REPO_ROOT).as_posix(),
        "training_rows": len(train_df),
        "validation_rows": len(validation_df),
        "testing_rows": len(test_df),
        "feature_count": len(feature_columns),
        "feature_columns": feature_columns,
        "training_start": str(train_df["Date"].min()),
        "training_end": str(train_df["Date"].max()),
        "validation_start": str(validation_df["Date"].min()),
        "validation_end": str(validation_df["Date"].max()),
        "testing_start": str(test_df["Date"].min()),
        "testing_end": str(test_df["Date"].max()),
        "architecture": [
            {"layer": "Dense", "units": 128, "activation": "relu"},
            {"layer": "Dropout", "rate": 0.20},
            {"layer": "Dense", "units": 64, "activation": "relu"},
            {"layer": "Dropout", "rate": 0.10},
            {"layer": "Dense", "units": 32, "activation": "relu"},
            {"layer": "Dense", "units": 1, "activation": "linear"},
        ],
        "optimizer": "Adam",
        "learning_rate": 0.001,
        "loss_function": "Mean Squared Error",
        "batch_size": BATCH_SIZE,
        "maximum_epochs": EPOCHS,
        "early_stopping_patience": PATIENCE,
        "best_epoch": best_epoch,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
        "test_data_used_for_training": False,
        "test_data_used_for_validation": False,
        "model_reload_verified": True,
        "scaler_reload_verified": True,
        "smoke_test_rows": smoke_rows,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_file": MODEL_FILE.name,
        "scaler_file": SCALER_FILE.name,
        "results_file": RESULTS_FILE.name,
        "split_metadata": {
            key: str(value) if isinstance(value, (pd.Timestamp, np.datetime64))
            else value
            for key, value in split_metadata.items()
        },
    }

    METADATA_FILE.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # SAVE EVIDENCE REPORT
    # -----------------------------------------------------

    report = f"""# M11-05: Artificial Neural Network Demand Forecasting

## Objective

Develop and evaluate a deep learning model for retail demand forecasting.

## Model

Artificial Neural Network using TensorFlow/Keras.

## Dataset

`dataset/processed/retail_store_inventory_clean.csv`

Target variable: `{TARGET_COLUMN}`

## Data split

| Split | Records |
|---|---:|
| Training | {len(train_df):,} |
| Validation | {len(validation_df):,} |
| Testing | {len(test_df):,} |

The data was split chronologically. The testing period was not used for training or validation.

## Model architecture

- Input layer: {X_train.shape[1]} features.
- Dense layer: 128 neurons, ReLU.
- Dropout: 0.20.
- Dense layer: 64 neurons, ReLU.
- Dropout: 0.10.
- Dense layer: 32 neurons, ReLU.
- Output layer: 1 neuron, linear activation.

Optimizer: Adam.

Loss function: Mean Squared Error.

Early stopping: Validation loss, patience of {PATIENCE} epochs.

Best epoch: {best_epoch}.

## Validation results

| Metric | Result |
|---|---:|
| MAE | {validation_metrics["MAE"]:.4f} |
| RMSE | {validation_metrics["RMSE"]:.4f} |
| R² | {validation_metrics["R2"]:.4f} |

## Final testing results

| Metric | Result |
|---|---:|
| MAE | {test_metrics["MAE"]:.4f} |
| RMSE | {test_metrics["RMSE"]:.4f} |
| R² | {test_metrics["R2"]:.4f} |

## Verification

- ANN model saved successfully.
- Saved ANN model reloaded successfully.
- Reloaded model predictions matched original predictions.
- Feature scaler saved and reloaded successfully.
- Test data was not used for model fitting or validation.
- Test predictions and actual values were saved.

## Generated artifacts

- Model: `python-ai/forecasting/artifacts/retail_demand_ann_model.keras`
- Scaler: `python-ai/forecasting/artifacts/retail_demand_ann_scaler.joblib`
- Metadata: `python-ai/forecasting/artifacts/retail_demand_ann_metadata.json`
- Predictions: `python-ai/forecasting/ann_forecasting_results.csv`

## Limitations

The ANN was evaluated using historical retail observations and engineered demand-history features. Its performance should be compared with other forecasting models using the same test period and metrics.

The results do not establish that the ANN is superior to the existing regression models.
"""

    REPORT_FILE.write_text(report, encoding="utf-8")

    print("\n" + "=" * 65)
    print("ANN FORECASTING COMPLETED")
    print("=" * 65)

    print("Model:", MODEL_FILE)
    print("Scaler:", SCALER_FILE)
    print("Metadata:", METADATA_FILE)
    print("Prediction results:", RESULTS_FILE)
    print("Evidence report:", REPORT_FILE)

    print("\nModel reload verification: PASSED")
    print("Scaler reload verification: PASSED")


if __name__ == "__main__":
    main()
