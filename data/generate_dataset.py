"""
Dataset Generator — Smart Agriculture System
Generates a realistic crop_recommendation.csv with 2200 records
matching the Kaggle Crop Recommendation dataset distribution.
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

# Each crop: [N_mean, N_std, P_mean, P_std, K_mean, K_std,
#             temp_mean, temp_std, hum_mean, hum_std,
#             ph_mean, ph_std, rain_mean, rain_std, count]
CROPS = {
    "rice":        [80,10, 45,10, 40,10, 23,2, 82,5, 6.5,0.5, 200,30, 100],
    "maize":       [60,10, 55,10, 44,10, 22,2, 65,5, 6.0,0.5, 60,15,  100],
    "chickpea":    [40,8,  68,8,  80,8,  18,2, 16,5, 7.3,0.3, 80,15,  100],
    "kidneybeans": [20,5,  68,8,  80,8,  20,2, 21,5, 5.7,0.3, 105,15, 100],
    "pigeonpeas":  [20,5,  68,8,  80,8,  27,2, 48,5, 5.8,0.3, 149,20, 100],
    "mothbeans":   [21,5,  48,8,  24,5,  28,2, 53,5, 6.9,0.3, 51,10,  100],
    "mungbean":    [20,5,  48,8,  20,5,  28,2, 85,5, 6.7,0.3, 48,10,  100],
    "blackgram":   [40,8,  68,8,  30,5,  30,2, 65,5, 7.0,0.3, 68,10,  100],
    "lentil":      [18,5,  68,8,  19,5,  24,2, 64,5, 6.9,0.3, 45,10,  100],
    "pomegranate": [18,5,  18,5,  40,8,  21,2, 90,5, 6.0,0.3, 107,20, 100],
    "banana":      [100,10,82,8,  50,8,  27,2, 80,5, 6.0,0.3, 105,20, 100],
    "mango":       [20,5,  27,5,  30,5,  31,2, 50,5, 5.7,0.3, 95,20,  100],
    "grapes":      [23,5,  132,10,200,15,23,2, 81,5, 6.0,0.3, 69,15,  100],
    "watermelon":  [99,10, 17,5,  50,8,  25,2, 85,5, 6.5,0.3, 50,10,  100],
    "muskmelon":   [100,10,17,5,  50,8,  28,2, 92,5, 6.5,0.3, 25,8,   100],
    "apple":       [21,5,  134,10,200,15,22,2, 92,5, 5.9,0.3, 113,20, 100],
    "orange":      [20,5,  16,5,  10,3,  22,2, 92,5, 7.0,0.3, 110,20, 100],
    "papaya":      [49,8,  59,8,  50,8,  33,2, 92,5, 6.7,0.3, 143,20, 100],
    "coconut":     [22,5,  16,5,  30,5,  27,2, 94,5, 5.9,0.3, 175,25, 100],
    "cotton":      [118,10,46,8,  20,5,  23,2, 79,5, 6.9,0.3, 80,15,  100],
    "jute":        [78,10, 46,8,  40,8,  24,2, 79,5, 6.7,0.3, 174,25, 100],
    "coffee":      [101,10,28,5,  29,5,  25,2, 58,5, 6.8,0.3, 158,25, 100],
}

rows = []
for crop, p in CROPS.items():
    n  = int(p[14])
    N  = np.random.normal(p[0],  p[1],  n).clip(0, 140)
    P  = np.random.normal(p[2],  p[3],  n).clip(5, 145)
    K  = np.random.normal(p[4],  p[5],  n).clip(5, 205)
    T  = np.random.normal(p[6],  p[7],  n).clip(8, 44)
    H  = np.random.normal(p[8],  p[9],  n).clip(14, 100)
    ph = np.random.normal(p[10], p[11], n).clip(3.5, 9.5)
    R  = np.random.normal(p[12], p[13], n).clip(20, 300)
    for i in range(n):
        rows.append([round(N[i],2), round(P[i],2), round(K[i],2),
                     round(T[i],2), round(H[i],2), round(ph[i],2),
                     round(R[i],2), crop])

df = pd.DataFrame(rows, columns=["N","P","K","temperature","humidity","ph","rainfall","label"])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/crop_recommendation.csv", index=False)
print(f"Dataset saved: {len(df)} records, {df['label'].nunique()} crops")
print(df.head())
