# Retail-X-AI Forecasting Model Comparison

## Objective

Compare Ridge Regression, Random Forest, XGBoost and Artificial Neural Network models using the same chronological data split and forecasting features.

## Dataset and data split

- Dataset: `dataset/raw/retail_store_inventory.csv`
- Target: `Units Sold`
- Features: 58
- Training records: 51,100
- Validation records: 11,000
- Testing records: 11,000
- Training period: 2022-01-01 00:00:00 to 2023-05-26 00:00:00
- Validation period: 2023-05-27 00:00:00 to 2023-09-13 00:00:00
- Testing period: 2023-09-14 00:00:00 to 2024-01-01 00:00:00

All four models used the same training records and the same engineered features. The test data was not used for training or validation.

## Model configurations

- Ridge Regression: alpha = 10.0
- Random Forest: 60 trees, maximum depth 18, minimum leaf size 3
- XGBoost: 500 estimators, learning rate 0.05, maximum depth 6
- ANN: Dense layers of 128, 64 and 32 neurons, ReLU activation, dropout and Adam optimizer

ANN best epoch: 8

## Validation and test results

| Model | Evaluation | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Ridge Regression | Validation | 89.7752 | 109.7737 | -0.0008 |
| Ridge Regression | Test | 88.4210 | 108.0047 | 0.0001 |
| Random Forest | Validation | 90.1691 | 110.0959 | -0.0067 |
| Random Forest | Test | 88.7448 | 108.3291 | -0.0060 |
| XGBoost | Validation | 90.6310 | 110.7575 | -0.0188 |
| XGBoost | Test | 89.4836 | 109.3094 | -0.0243 |
| ANN | Validation | 89.4016 | 110.4432 | -0.0130 |
| ANN | Test | 87.2793 | 108.7652 | -0.0141 |
| Previous-day Baseline | Test | 119.3419 | 152.7264 | -0.9995 |
| Training Mean Baseline | Test | 88.4597 | 108.0077 | -0.0000 |

## Interpretation

Lower MAE and RMSE indicate smaller forecasting errors. An R² value closer to 1 indicates a stronger fit relative to predicting the target mean.

The final model comparison should consider both MAE and RMSE, validation performance, test performance and prediction behaviour.

The baseline models provide reference points for assessing whether machine learning improves on simple historical demand estimates.

## Limitations

This experiment evaluates historical one-step-ahead demand estimates using engineered historical demand features. It does not establish long-horizon future forecasting performance.

The models use fixed configurations. The results do not represent an exhaustive hyperparameter search.

## Generated evidence

- `forecasting_model_comparison.csv`
- `forecasting_model_comparison.json`
- `forecasting_model_predictions.csv`
