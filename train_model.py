import os
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

DATASET_PATH = "RAVDESS_dataset"

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        if len(y) < 2048:
            return None

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_scaled = np.mean(mfcc.T, axis=0)

        return mfcc_scaled

    except Exception as e:
        print("Error:", e)
        return None


features = []
labels = []

for actor in os.listdir(DATASET_PATH):
    actor_path = os.path.join(DATASET_PATH, actor)

    for file in os.listdir(actor_path):
        file_path = os.path.join(actor_path, file)

        data = extract_features(file_path)

        if data is not None:
            # extract emotion from filename
            emotion = int(file.split("-")[2])

            # map to confidence
            if emotion in [1, 2, 3]:
                label = 1   # confident
            else:
                label = 0   # not confident

            features.append(data)
            labels.append(label)

print("Total samples extracted:", len(features))
print("Total labels:", len(labels))

import numpy as np

X = np.array(features)
y = np.array(labels)

print("Training model...")

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

print("Model training complete")