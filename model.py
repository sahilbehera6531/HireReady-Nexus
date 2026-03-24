import librosa
import numpy as np
import subprocess
import os
import joblib
import speech_recognition as sr

# Load model ONCE (important)
model = joblib.load("rf_model.pkl")

def extract_features(file_path):
    try:
        # Convert webm → wav using ffmpeg
        converted_path = "temp.wav"

        command = f'ffmpeg -y -i "{file_path}" "{converted_path}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

         # DEBUG
        print("FFMPEG OUTPUT:", result.stdout)
        print("FFMPEG ERROR:", result.stderr)

        if not os.path.exists(converted_path):
            print("Conversion failed — temp.wav not created")
            return None, None
        
        # Now load clean wav
        y, sr = librosa.load(converted_path, sr=22050)

        if len(y) < 2048:
            print("Audio too short")
            return None, None

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_scaled = np.mean(mfcc.T, axis=0)

        return mfcc_scaled, converted_path

    except Exception as e:
        print("Error in feature extraction:", str(e))
        return None, None

model = joblib.load("rf_model.pkl")

def run_model(audio_file):
    try:
        features, wav_path = extract_features(audio_file)
        
        if features is None or wav_path is None:
            return {
                "score": 0,
                "transcript": ""
            }

        # ✅ FIX: reshape BEFORE prediction
        features = features.reshape(1, -1)

        # DEBUG SAFE
        prediction = model.predict_proba(features)
        print("Raw prediction:", prediction)

        confidence = prediction[0][1]

        # amplify
        confidence = min(confidence * 1.5, 1)

        # 🎯 NEW: speech to text
        text = speech_to_text(wav_path)

        if os.path.exists(wav_path):
            os.remove(wav_path)

        return { 
            "score": confidence * 100,
            "transcript": text
        }

    except Exception as e:
        print("Model error:", str(e))
        return {
            "score": 0,
            "transcript": ""
        }
    
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print("Transcribed Text:", text)
            return text
    except Exception as e:
        print("Speech recognition error:", e)
        return ""