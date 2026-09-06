import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 1. Load and Prepare Mock Spaza Shop Data
# Replace this section once the Data Engineer provides the actual CSV dataset
# df = pd.read_csv('spaza_sales_data.csv')

# Generating mock daily sales data for a single product to test the model
np.random.seed(42)
mock_sales = np.random.randint(20, 100, size=365).reshape(-1, 1) 

# Neural networks require scaled data to function correctly
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(mock_sales)

# 2. Convert to Time-Series Sequences (Windowing)
def create_sequences(data, time_steps=7):
    """Uses past sales data to predict future demand."""
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

# Use the past 7 days of sales to predict the 8th day
time_steps = 7 
X, y = create_sequences(scaled_data, time_steps)

# Split into 80% training data and 20% testing data
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# 3. Build the LSTM Model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(time_steps, 1)),
    Dropout(0.2), # Drops 20% of neurons randomly to prevent overfitting
    Dense(1)      # Outputs the single predicted sales value
])

model.compile(optimizer='adam', loss='mse')

# 4. Train the Model
print("Training Retail-X-AI LSTM Model...")
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), verbose=1)

# 5. Evaluate the Model 
predictions = model.predict(X_test)

# Inverse transform to display actual product quantities instead of scaled decimals
actual_sales = scaler.inverse_transform(y_test.reshape(-1, 1))
predicted_sales = scaler.inverse_transform(predictions)

# Calculate error metrics required by Section 10
mae = mean_absolute_error(actual_sales, predicted_sales)
rmse = np.sqrt(mean_squared_error(actual_sales, predicted_sales))

print(f"\nModel Evaluation:")
print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} units")