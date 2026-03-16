"""
FML Module — LSTM Soil Moisture Forecasting
Takes a 24-hour window of sensor readings, predicts next-hour moisture.
"""
import os, numpy as np, pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import joblib

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

WINDOW = 24

# ── Generate synthetic time-series sensor data ───────────────
np.random.seed(42)
n = 2000
hours = np.arange(n)
moisture    = 50 + 20 * np.sin(2 * np.pi * hours / 48) + np.random.normal(0, 3, n)
temperature = 25 +  8 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 1, n)
humidity    = 65 - 10 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 2, n)
hour_feat   = hours % 24

data = np.column_stack([moisture, temperature, humidity, hour_feat])
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# ── Build sequences ──────────────────────────────────────────
X, y = [], []
for i in range(len(data_scaled) - WINDOW):
    X.append(data_scaled[i: i + WINDOW])
    y.append(data_scaled[i + WINDOW, 0])   # predict moisture only
X, y = np.array(X), np.array(y)

split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ── Build & train LSTM ───────────────────────────────────────
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(WINDOW, 4)),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=20, batch_size=32,
              validation_split=0.1, verbose=1)

    y_pred = model.predict(X_test).flatten()
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"LSTM Test RMSE (scaled): {rmse:.4f}")
    model.save(f"{MODELS_DIR}/lstm_moisture.h5")
    print(f"LSTM model saved to {MODELS_DIR}/lstm_moisture.h5")

except ImportError:
    print("TensorFlow not installed — skipping LSTM training.")
    print("Install with: pip install tensorflow")

joblib.dump(scaler, f"{MODELS_DIR}/lstm_scaler.pkl")
np.save(f"{MODELS_DIR}/lstm_last_window.npy", X_test[-1])
print("Scaler and sample window saved.")
