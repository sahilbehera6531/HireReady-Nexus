from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    data = request.json
    answer = data.get('answer', '')

    return jsonify({
        "accuracy_score": 50,
        "next_question": "What is a linked list?"
    })

if __name__ == '__main__':
    
    app.run(debug=True)