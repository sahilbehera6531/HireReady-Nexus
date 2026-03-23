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

        number = re.search(r'\d+', text)

        return int(number.group()) if number else 0

    except:
        return 0
    
def getfeedback(prev_question, answer):

    prompt = f"""
    You are an interviewer.

    Give SHORT and CLEAR feedback on the candidate's answer.

    Rules:
    - Max 3 lines
    - No formatting (**, bullets, markdown)
    - No long paragraphs
    - Be simple and direct

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