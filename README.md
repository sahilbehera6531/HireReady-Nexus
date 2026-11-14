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

```

## Architecture
```mermaid
flowchart TB
    %% Styling Definitions
    classDef actor fill:#dae8fc,stroke:#6c8ebf,stroke-width:1.5px,color:#000
    classDef mockNode fill:#dae8fc,stroke:#6c8ebf,stroke-width:1.5px,color:#000
    classDef gdNode fill:#d5e8d4,stroke:#82b366,stroke-width:1.5px,color:#000
    classDef audioNode fill:#ffe6cc,stroke:#d79b00,stroke-width:1.5px,color:#000
    classDef modelNode fill:#f8cecc,stroke:#b85450,stroke-width:1.5px,color:#000
    classDef subgraphBox fill:#f5f5f5,stroke:#cccccc,stroke-width:1px,color:#333

    %% External Actors
    Candidate((Candidate)):::actor
    Participant((Discussion Participant)):::actor

    %% Subgraph: Mock Interview
    subgraph MockInterview["Mock Interview"]
        direction TB
        InterviewUI["Interview UI"]:::mockNode
        BrowserClient["Browser Client<br/>[script.js]"]:::mockNode
        InterviewServer["Interview Server<br/>[server.py]"]:::mockNode
        InterviewLogic["Interview Logic<br/>[gen.py]"]:::mockNode
        InterviewState[("Interview State<br/>[server.py]")]:::mockNode

        InterviewUI -.->|loads| BrowserClient
        BrowserClient -->|posts answers| InterviewServer
        InterviewServer -->|returns results| BrowserClient
        InterviewServer -->|evaluates and generates| InterviewLogic
        InterviewServer -->|updates| InterviewState
    end

    %% Subgraph: Group Discussion
    subgraph GroupDiscussion["Group Discussion"]
        direction TB
        DiscussionUI["Discussion UI"]:::gdNode
        DiscussionFlow["Discussion Flow<br/>[server.py]"]:::gdNode

        DiscussionUI -->|sends discussion input| DiscussionFlow
    end

    %% External LLM Service
    GroqLLM["Groq LLM"]:::mockNode

    %% Subgraph: Audio Evaluation
    subgraph AudioEvaluation["Audio Evaluation"]
        direction TB
        AudioCapture["Audio Capture<br/>[script.js]"]:::audioNode
        AudioUpload["Audio Upload<br/>[server.py]"]:::audioNode
        AudioPipeline["Audio Pipeline<br/>[model.py]"]:::audioNode
        FFmpeg["FFmpeg"]:::audioNode
        SpeechRec["Speech Recognition"]:::audioNode

        AudioCapture -->|uploads recording| AudioUpload
        AudioUpload -->|runs analysis| AudioPipeline
        AudioPipeline -->|converts audio| FFmpeg
        AudioPipeline -->|transcribes audio| SpeechRec
    end

    %% Subgraph: Confidence Model
    subgraph ConfidenceModel["Confidence Model"]
        direction TB
        ModelTraining["Model Training<br/>[train_model.py]"]:::modelNode
        RAVDESS[("RAVDESS Audio")]:::modelNode
        RandomForest[("Random Forest<br/>[rf_model.pkl]")]:::modelNode

        ModelTraining -->|extracts training samples| RAVDESS
        ModelTraining -->|saves trained model| RandomForest
    end

    %% Cross-Component Connections
    Candidate -->|uses| InterviewUI
    Participant -->|participates| DiscussionUI

    BrowserClient -->|records audio| AudioCapture
    AudioUpload -->|scores transcript and<br/>generates feedback| InterviewLogic
    AudioUpload -->|updates| InterviewState

    DiscussionFlow -->|generates turns and topic| GroqLLM
    AudioPipeline -->|predicts confidence| RandomForest

    %% Apply Subgraph Styling
    class MockInterview,GroupDiscussion,AudioEvaluation,ConfidenceModel subgraphBox


