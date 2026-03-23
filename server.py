from flask import Flask, render_template, request, jsonify
from gen import calculate_accuracyscore, getfeedback, getnextquestion
from model import run_model
import os

app = Flask(__name__)
prev_question = "What is Data Science?"
field = "Data Structures and Algorithm"
Score = 0
mul = 1
difficulty = "easy"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mock_interview')
def mock_interview():
    return render_template('mock_interview.html', prev_question=prev_question)

@app.route('/gd')
def group_discussion():
    return "<h1>Group Discussion Page</h1>"

@app.route('/ask', methods=['POST'])
def ask_question():
    global difficulty
    global prev_question, Score, mul

    data = request.json
    answer = data.get('answer', '')

    accuracy_score = calculate_accuracyscore(answer, prev_question)

    # difficulty logic
    if accuracy_score >= 70:
        if difficulty == "easy":
            difficulty = "medium"
        elif difficulty == "medium":
            difficulty = "hard"

    elif accuracy_score < 40:
        if difficulty == "hard":
            difficulty = "medium"
        elif difficulty == "medium":
            difficulty = "easy"

    #Scoring logic
    if accuracy_score >= 30:
        Score += accuracy_score * mul
        mul += 1
        Correct = True
    else:
        Correct = False
        mul = 1

    next_question = getnextquestion(prev_question, answer, Correct, field, difficulty)

    feedback = getfeedback(prev_question, answer)

    prev_question = next_question

    return jsonify({
        "accuracy_score": accuracy_score,
        "total_score": Score,
        "feedback": feedback,
        "next_question": next_question
    })

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        file = request.files['audio']
        
        filepath = os.path.join("uploads", "recording.wav")
        file.save(filepath)

        confidence = run_model(filepath)
        accuracy_score = int(confidence)

        global Score, mul, prev_question, difficulty

        # difficulty update (same logic as text)
        if accuracy_score >= 70:
            if difficulty == "easy":
                difficulty = "medium"
            elif difficulty == "medium":
                difficulty = "hard"

        elif accuracy_score < 40:
            if difficulty == "hard":
                difficulty = "medium"
            elif difficulty == "medium":
                difficulty = "easy"

        # scoring logic
        if accuracy_score >= 30:
            Score += accuracy_score * mul
            mul += 1
            Correct = True
        else:
            Correct = False
            mul = 1

        # generate next question (SAME as text flow)
        next_question = getnextquestion(prev_question, "Audio response", Correct, field, difficulty)

        feedback = "Audio evaluated successfully"

        prev_question = next_question

        return jsonify({
            "accuracy_score": accuracy_score,
            "total_score": Score,
            "feedback": feedback,
            "next_question": next_question
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    
    app.run(debug=True)