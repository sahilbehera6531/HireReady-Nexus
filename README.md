# 🚀 HireReady-Nexus

AI-powered interview preparation platform with mock interviews, real-time audio evaluation, speech-to-text feedback, and group discussion simulation.

---

## 📌 Features

### 🎯 Mock Interview (Text + Audio)
- AI-generated interview questions
- Dynamic difficulty adjustment (easy → medium → hard)
- Real-time answer evaluation
- Combined scoring:
  - 🧠 Content understanding
  - 🎤 Confidence (audio-based ML model)

---

### 🎤 Audio Evaluation System
- Audio recording via browser (MediaRecorder API)
- Audio processing using **FFmpeg**
- Feature extraction using **MFCC (Librosa)**
- Confidence prediction using **Random Forest model**
- Speech-to-text conversion for feedback consistency

---

### 💬 Feedback System
- AI-generated feedback (concise & professional)
- Same evaluation logic for text and audio
- Strict scoring based on:
  - Relevance
  - Correctness
  - Completeness

---

### 🗣️ Group Discussion Simulation
- Multi-speaker AI responses (Alice, Bob, Charlie)
- Real-time discussion flow
- Dynamic topic evolution after each round
- Turn-based interaction UI

---

## 🧠 Tech Stack

### Backend
- Python (Flask)
- Groq API (LLM-based evaluation)
- SpeechRecognition

### Machine Learning
- Scikit-learn (Random Forest)
- Librosa (audio feature extraction)
- NumPy

### Frontend
- HTML, CSS, JavaScript
- Bootstrap
- MediaRecorder API

### Tools
- FFmpeg (audio conversion)
- Joblib (model serialization)

---

## ⚙️ How It Works

```text
User Input (Text / Audio)
        ↓
Audio → FFmpeg → Feature Extraction → ML Model (Confidence)
        ↓
Speech-to-Text → Transcript
        ↓
Content Evaluation (LLM)
        ↓
Final Score (Content + Confidence)
        ↓
Feedback + Next Question
