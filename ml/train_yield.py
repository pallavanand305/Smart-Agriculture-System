"""
FML Module — Linear Regression Yield Prediction
Predicts crop yield (quintals/hectare) from soil & climate features.
"""
import os, sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

DATA_PATH  = "data/crop_recommendation.csv"
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Simulate yield column: realistic formula + noise
np.random.seed(42)
df["yield"] = (
    0.05 * df["N"] + 0.03 * df["P"] + 0.02 * df["K"] +
    0.4  * df["temperature"] + 0.1 * df["humidity"] +
    1.5  * df["ph"] + 0.01 * df["rainfall"] +
    np.random.normal(0, 1.5, len(df))
).clip(5, 60)

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
X = df[FEATURES].values
y = df["yield"].values

sc = StandardScaler()
X_scaled = sc.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
r2     = r2_score(y_test, y_pred)
print(f"R² Score : {r2:.4f}")
print(f"RMSE     : {rmse:.4f} quintals/ha")

joblib.dump(lr, f"{MODELS_DIR}/yield_lr.pkl")
joblib.dump(sc, f"{MODELS_DIR}/yield_scaler.pkl")
print(f"Yield model saved to {MODELS_DIR}/")
