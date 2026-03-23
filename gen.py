from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate_accuracyscore(answer, prev_question):

    prompt = f"""
    Evaluate this answer.

    Question: {prev_question}
    Answer: {answer}

    Return only a number between 0 and 100.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )

        text = response.choices[0].message.content

        number = re.search(r'\d+', text)

        return int(number.group()) if number else 0

    except:
        return 0
    
def getfeedback(prev_question, answer):

    prompt = f"""
    Question: {prev_question}

    Answer: {answer}

    Provide feedback and improvement suggestions.
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=0   # ADD THIS
    )

    return response.choices[0].message.content

def getnextquestion(prev_question, answer, Correct, field):

    prompt = f"""
    You are an interviewer.

    Ask ONLY ONE short and clear technical interview question.

    Rules:
    - Keep it under 2 lines
    - Do NOT include explanations
    - Do NOT include formatting like ** or markdown
    - Do NOT include examples or constraints
    - Only ask the question

    Previous question: {prev_question}
    Candidate answer: {answer}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant"
    )

    return response.choices[0].message.content