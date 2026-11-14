# M11-05: Artificial Neural Network Demand Forecasting

## Objective

Develop and evaluate a deep learning model for retail demand forecasting.

## Model

Artificial Neural Network using TensorFlow/Keras.

## Dataset

`dataset/processed/retail_store_inventory_clean.csv`

Target variable: `Units Sold`

## Data split

| Split | Records |
|---|---:|
| Training | 51,100 |
| Validation | 11,000 |
| Testing | 11,000 |

The data was split chronologically. The testing period was not used for training or validation.

## Model architecture

- Input layer: 58 features.
- Dense layer: 128 neurons, ReLU.
- Dropout: 0.20.
- Dense layer: 64 neurons, ReLU.
- Dropout: 0.10.
- Dense layer: 32 neurons, ReLU.
- Output layer: 1 neuron, linear activation.

Optimizer: Adam.

Loss function: Mean Squared Error.

Early stopping: Validation loss, patience of 10 epochs.

Best epoch: 8.

## Validation results

| Metric | Result |
|---|---:|
| MAE | 89.4016 |
| RMSE | 110.4432 |
| R² | -0.0130 |

## Final testing results

| Metric | Result |
|---|---:|
| MAE | 87.2793 |
| RMSE | 108.7652 |
| R² | -0.0141 |

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
