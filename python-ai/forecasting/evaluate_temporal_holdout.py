"""M11-05: Evaluate the selected demand forecasting model on temporal holdout."""

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from feature_engineering import prepare_forecasting_train_validation_test
from train_selected_model import prepare_model_inputs


FORECASTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = FORECASTING_DIR.parents[1]

DATA_FILE = (
    REPO_ROOT
    / "dataset"
    / "processed"
    / "retail_store_inventory_clean.csv"
)

ARTIFACT_DIR = FORECASTING_DIR / "artifacts"
MODEL_FILE = ARTIFACT_DIR / "retail_demand_ridge_model.joblib"
METADATA_FILE = ARTIFACT_DIR / "retail_demand_ridge_model_metadata.json"

RESULTS_FILE = ARTIFACT_DIR / "retail_demand_ridge_test_evaluation.json"
REPORT_FILE = FORECASTING_DIR / "M11-05-temporal-holdout-evaluation.md"

TARGET_COLUMN = "Units Sold"
MODEL_NAME = "Ridge Regression"


def main():
    """Evaluate the saved model on the untouched chronological test split."""

    print("=" * 65)
    print("RETAILAI - M11-05 TEMPORAL HOLDOUT EVALUATION")
    print("=" * 65)

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Trained model not found: {MODEL_FILE}")

    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"Model metadata not found: {METADATA_FILE}")

    with METADATA_FILE.open("r", encoding="utf-8") as file:
        model_metadata = json.load(file)

    if model_metadata.get("model_name") != MODEL_NAME:
        raise ValueError(
            "The saved model metadata does not match Ridge Regression."
        )

    if model_metadata.get("test_split_used_for_fitting") is not False:
        raise ValueError(
            "Model metadata does not confirm an untouched test split."
        )

    raw_df = pd.read_csv(DATA_FILE)

    train_df, validation_df, test_df, _, _ = (
        prepare_forecasting_train_validation_test(
            raw_df,
            train_fraction=0.70,
            validation_fraction=0.15,
        )
    )

    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError(
            "Training, validation, and test splits must be non-empty."
        )

    # Confirm the test period starts after the model's fitting period.
    fit_end_date = pd.Timestamp(model_metadata["fit_end_date"])
    test_start_date = pd.Timestamp(test_df["Date"].min())

    if test_start_date <= fit_end_date:
        raise ValueError(
            "The test period overlaps the model's fitting period. "
            "Evaluation stopped to avoid misleading results."
        )

    # Prepare the test features using the existing training logic.
    X_test, y_test, feature_columns = prepare_model_inputs(test_df)

    expected_features = model_metadata["feature_columns"]

    if feature_columns != expected_features:
        raise ValueError(
            "Test features do not match the feature columns recorded "
            "during model training."
        )

    # Load the saved model without retraining it.
    model = joblib.load(MODEL_FILE)

    predictions = np.asarray(model.predict(X_test), dtype=float)

    if len(predictions) != len(y_test):
        raise ValueError(
            "Prediction count does not match the test target count."
        )

    if not np.isfinite(predictions).all():
        raise ValueError("The model produced non-finite test predictions.")

    # Calculate final metrics using the test split.
    mae = float(mean_absolute_error(y_test, predictions))
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))

    test_start = pd.Timestamp(test_df["Date"].min()).strftime("%Y-%m-%d")
    test_end = pd.Timestamp(test_df["Date"].max()).strftime("%Y-%m-%d")

    results = {
        "issue": "M11-05",
        "model_name": MODEL_NAME,
        "source_dataset": DATA_FILE.relative_to(REPO_ROOT).as_posix(),
        "model_artifact": MODEL_FILE.relative_to(REPO_ROOT).as_posix(),
        "target_column": TARGET_COLUMN,
        "evaluation_method": "Chronological temporal holdout",
        "train_fraction": 0.70,
        "validation_fraction": 0.15,
        "test_fraction": 0.15,
        "training_rows": int(len(train_df)),
        "validation_rows": int(len(validation_df)),
        "test_rows": int(len(test_df)),
        "test_unique_dates": int(test_df["Date"].nunique()),
        "fit_end_date": fit_end_date.strftime("%Y-%m-%d"),
        "test_start_date": test_start,
        "test_end_date": test_end,
        "feature_count": len(feature_columns),
        "mae": mae,
        "rmse": rmse,
        "test_data_used_for_training": False,
        "model_retrained_during_evaluation": False,
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    RESULTS_FILE.write_text(
        json.dumps(results, indent=2) + "\n",
        encoding="utf-8",
    )

    # Generate the Markdown report.
    report = f"""# M11-05 — Temporal Holdout Evaluation

## Objective

Evaluate the saved Ridge Regression demand forecasting model on the
chronological test period using Mean Absolute Error (MAE) and Root Mean
Squared Error (RMSE).

## Evaluation results

| Metric | Result |
|---|---:|
| MAE | {mae:.6f} |
| RMSE | {rmse:.6f} |
| Test rows | {len(test_df):,} |
| Unique test dates | {test_df["Date"].nunique():,} |
| Feature count | {len(feature_columns)} |

## Evaluation setup

| Item | Value |
|---|---|
| Model | {MODEL_NAME} |
| Target | `{TARGET_COLUMN}` |
| Training rows | {len(train_df):,} |
| Validation rows | {len(validation_df):,} |
| Test period | {test_start} to {test_end} |
| Model fitting period ends | {fit_end_date.strftime("%Y-%m-%d")} |
| Test data used for training | No |
| Model retrained during evaluation | No |

The saved model was loaded from the existing Joblib artifact. The final
test period occurs after the model's fitting period. The model was not
fitted or modified during this evaluation.

## Metric interpretation

- **MAE:** The average absolute difference between actual demand and
  predicted demand, measured in units sold.
- **RMSE:** The square root of the average squared prediction error,
  measured in units sold. Larger errors have a greater influence on RMSE.

Lower values indicate smaller prediction errors. These metrics evaluate
the model on the test period and should not be confused with the
validation metrics used during model selection.

## Evidence files

- Evaluation script: `python-ai/forecasting/evaluate_temporal_holdout.py`
- Machine-readable results: `python-ai/forecasting/artifacts/retail_demand_ridge_test_evaluation.json`
- Trained model: `python-ai/forecasting/artifacts/retail_demand_ridge_model.joblib`

## Reproducibility

Run from the repository root:

```powershell
python .\\python-ai\\forecasting\\evaluate_temporal_holdout.py