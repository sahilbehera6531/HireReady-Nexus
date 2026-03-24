import os
import librosa
import numpy as np

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

for actor in os.listdir(DATASET_PATH):
    actor_path = os.path.join(DATASET_PATH, actor)

    for file in os.listdir(actor_path):
        file_path = os.path.join(actor_path, file)

        data = extract_features(file_path)

        if data is not None:
            features.append(data)

print("Total samples extracted:", len(features))