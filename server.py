from flask import Flask, render_template, request, jsonify
from gen import calculate_accuracyscore, getfeedback

app = Flask(__name__)
prev_question = "What is Data Science?"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mock_interview')
def mock_interview():
    return "<h1>Mock Interview Page </h1>"

@app.route('/gd')
def group_discussion():
    return "<h1>Group Discussion Page</h1>"

@app.route('/ask', methods=['POST'])
def ask_question():
    global prev_question

    data = request.json
    answer = data.get('answer', '')

    accuracy_score = calculate_accuracyscore(answer, prev_question)

    # NEW: get feedback
    feedback = getfeedback(prev_question, answer)    

    return jsonify({
        "accuracy_score": accuracy_score,
        "feedback": feedback,
        "next_question": prev_question
    })

if __name__ == '__main__':
    
    app.run(debug=True)