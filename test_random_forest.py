
# Retail-X-AI
# Random Forest Regressor Test

from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Sample sales data
# Number of products sold per day
X = np.array([
    [1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
    [9],
    [10]
])

# Actual sales quantities
y = np.array([
    10,
    15,
    18,
    25,
    28,
    35,
    38,
    45,
    48,
    55
])

# Create the Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X, y)

# Predict sales for a new input
prediction = model.predict([[11]])

print("Retail-X-AI Random Forest Test")
print("--------------------------------")
print("Model training: Successful")
print("Input value: 11")
print("Predicted sales:", prediction[0])
