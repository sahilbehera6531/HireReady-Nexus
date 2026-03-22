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
        model="llama-3.1-8b-instant"
    )

    return response.choices[0].message.content