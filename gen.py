from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate_accuracyscore(answer, prev_question):

    prompt = f"""
    You are an interviewer.

    Evaluate the candidate's answer.

    Rules:
    - Return ONLY a number between 0 and 100
    - Do NOT write anything else
    - Do NOT explain
    - Do NOT add words

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
            score = int(re.findall(r'\d+', text)[0])
            if 0 <= score <= 100:
                return score
            else:
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