import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Dummy dataset (replace later with real audio features)
X = np.random.rand(100, 13)   # 100 samples, 13 features (MFCC size)
y = np.random.randint(0, 2, 100)  # 0 = low confidence, 1 = high

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "rf_model.pkl")

print("Model trained and saved as rf_model.pkl")