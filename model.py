import librosa
import joblib
import numpy as np

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        if len(y) < 2048:
            raise ValueError("Audio too short")

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_scaled = np.mean(mfcc.T, axis=0)

        return mfcc_scaled

    except Exception as e:
        print(f"Error: {e}")
        return None


def run_model(audio_file):
    model = joblib.load("rf_model.pkl")

    features = extract_features(audio_file)

    if features is not None:
        features = features.reshape(1, -1)
        confidence = model.predict_proba(features)[0, 1]
        return confidence * 100
    else:
        return 0