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
gd_topic = "Is AI beneficial for society?"


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mock_interview')
def mock_interview():
    return render_template('mock_interview.html', prev_question=prev_question)

@app.route('/gd')
def group_discussion():
    global gd_topic
    return render_template('gd.html', topic=gd_topic)

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
        global Score, mul, prev_question, difficulty
        file = request.files['audio']
        
        filepath = os.path.join("uploads", "recording.wav")
        file.save(filepath)

        result = run_model(filepath)

        confidence_score = result["score"]
        transcript = result["transcript"]

       # 🎯 HANDLE NO SPEECH
        if transcript.strip() == "":
            accuracy_score = 0
            feedback = "No speech detected. Please speak clearly."
            Correct = False
            mul = 1
        else:
            # 🎯 content score
            content_score = calculate_accuracyscore(transcript, prev_question)

            # 🎯 combine scores
            accuracy_score = int((0.6 * content_score) + (0.4 * confidence_score))
            accuracy_score = min(accuracy_score, 100)
            feedback = getfeedback(prev_question, transcript)

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
        next_question = getnextquestion(prev_question, transcript if transcript.strip() != "" else "No answer", Correct, field, difficulty)

        prev_question = next_question

        return jsonify({
            "accuracy_score": accuracy_score,
            "total_score": Score,
            "feedback": feedback,
            "next_question": next_question
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_group_response', methods=['POST'])
def generate_group_response():
    try:
        data = request.json
        user_input = data.get("user_input")
        global gd_topic
        topic = gd_topic

        prompt = f"""
Topic: {topic}

User said: {user_input}

Continue a group discussion.

Return responses EXACTLY in this format:

Alice: <Alice response>
Bob: <Bob response>
Charlie: <Charlie response>
"""

        from groq import Groq
        import os
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        text = response.choices[0].message.content

        responses = []
        for line in text.split("\n"):
            if ":" in line:
                name, content = line.split(":", 1)
                responses.append({
                    "name": name.strip(),
                    "content": content.strip()
                })
        # 🎯 GENERATE NEW TOPIC (EVOLVING DISCUSSION)
        new_topic_prompt = f"""
        Based on this discussion topic:
        {topic}

        Generate a slightly evolved or follow-up discussion topic.
        Keep it short (1 line).
        """

        topic_response = client.chat.completions.create(
            messages=[{"role": "user", "content": new_topic_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.5
        )

        gd_topic = topic_response.choices[0].message.content.strip()

        return jsonify({
            "responses": responses[:3],
            "topic": gd_topic   # 🔥 ADD THIS
        })

    except Exception:
        return jsonify({
            "responses": [
                {"name": "System", "content": "Error generating discussion response."}
            ]
        })

if __name__ == '__main__':
    
    app.run(debug=True)