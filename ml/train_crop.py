"""
FML Module — Random Forest Crop Recommendation
Trains on crop_recommendation.csv, saves model artifacts to models/
"""
import os, sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

DATA_PATH   = "data/crop_recommendation.csv"
MODELS_DIR  = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# ── Load & preprocess ────────────────────────────────────────
df      = pd.read_csv(DATA_PATH)
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
X       = df[FEATURES]
y       = df["label"]

le = LabelEncoder()
sc = StandardScaler()
y_enc    = le.fit_transform(y)
X_scaled = sc.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# ── Train ────────────────────────────────────────────────────
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

acc = accuracy_score(y_test, rf.predict(X_test))
print(f"Accuracy: {acc:.4f}")
print(classification_report(y_test, rf.predict(X_test),
                             target_names=le.classes_))

# ── Save artifacts ───────────────────────────────────────────
joblib.dump(rf, f"{MODELS_DIR}/crop_rf.pkl")
joblib.dump(sc, f"{MODELS_DIR}/crop_scaler.pkl")
joblib.dump(le, f"{MODELS_DIR}/crop_label_encoder.pkl")
print(f"Models saved to {MODELS_DIR}/")
