from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate_accuracyscore(answer, prev_question):

    prompt = f"""
    You are a strict technical interviewer.

    Evaluate the candidate's answer VERY STRICTLY based on:

    1. Relevance to the question
    2. Correctness of concepts
    3. Completeness of explanation

    Scoring rules:
    - Completely wrong / irrelevant → 0 to 30
    - Partially correct → 30 to 60
    - Mostly correct → 60 to 85
    - Fully correct and clear → 85 to 100

    IMPORTANT RULES:
    - If answer is unrelated → give LOW score (0–30)
    - Do NOT give high score for generic or vague answers
    - Be strict like a real interviewer

    Return ONLY a number between 0 and 100.
    Do NOT explain.

    Question: {prev_question}
    Answer: {answer}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )

        text = response.choices[0].message.content

        try:
            numbers = re.findall(r'\d+', text)
            if numbers:
                score = int(numbers[0])
                return min(max(score, 0), 100)
            return 0
        except:
            return 0

    except:
        return 0
    
def getfeedback(prev_question, answer):

    prompt = f"""
    You are an interviewer.

    Evaluate the candidate's answer and provide concise feedback.

    Rules:
    - Max 2-3 lines
    - DO NOT ask the user to try again or reattempt
    - DO NOT give instructions like "try again" or "answer this"
    - Keep it short, clear and professional

    Question: {prev_question}
    Answer: {answer}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        temperature=0   # ADD THIS
    )

    return response.choices[0].message.content

def getnextquestion(prev_question, answer, Correct, field, difficulty):

    prompt = f"""
    You are an interviewer.

    Ask ONE {difficulty} level technical interview question related to {field}

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