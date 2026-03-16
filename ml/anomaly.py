"""
FML Module — k-NN Anomaly Detection
Flags faulty/outlier sensor readings before they reach ML models.
k=5 nearest neighbours; if avg distance > threshold → anomaly.
"""
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib, os

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

class KNNAnomalyDetector:
    def __init__(self, k=5, threshold_percentile=95):
        self.k   = k
        self.pct = threshold_percentile
        self.knn = NearestNeighbors(n_neighbors=k)
        self.threshold = None

    def fit(self, X: np.ndarray):
        self.knn.fit(X)
        dists, _ = self.knn.kneighbors(X)
        avg_dists = dists.mean(axis=1)
        self.threshold = np.percentile(avg_dists, self.pct)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns True where reading is anomalous."""
        dists, _ = self.knn.kneighbors(X)
        return dists.mean(axis=1) > self.threshold

    def save(self, path=f"{MODELS_DIR}/anomaly_knn.pkl"):
        joblib.dump(self, path)

    @staticmethod
    def load(path=f"{MODELS_DIR}/anomaly_knn.pkl"):
        return joblib.load(path)


# ── Quick demo ───────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    normal = np.random.normal(loc=[25, 65, 50], scale=[2, 5, 5], size=(200, 3))
    detector = KNNAnomalyDetector(k=5).fit(normal)

    test = np.array([
        [25.1, 64.8, 49.5],   # normal
        [99.0, 10.0, 5.0],    # anomaly — broken sensor
    ])
    flags = detector.predict(test)
    for i, (row, flag) in enumerate(zip(test, flags)):
        print(f"Reading {i+1}: {row}  →  {'ANOMALY' if flag else 'OK'}")
    detector.save()
    print("Anomaly detector saved.")
