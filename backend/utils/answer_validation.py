import groq
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")


groq_client = groq.Groq(api_key=GROQ_API_KEY)
db_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = db_client['mock_interview_db']

def validate_answer(question_id, answer_text):
    # Fetch question and expected keywords from database
    question_data = db.questions.find_one({'id': question_id})
    question = question_data['text']
    keywords = question_data['keywords']

    prompt = f"""
    Question: {question}
    Answer: {answer_text}
    Expected keywords: {', '.join(keywords)}

    Please evaluate the answer based on the following criteria:
    1. Relevance to the question
    2. Clarity and coherence
    3. Use of expected keywords
    4. Flow and structure
    5. Overall quality

    Provide a score out of 10 and brief feedback.
    Give output in this format: "Score: X/10\nFeedback: ..."
    """

    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI assistant that evaluates interview answers."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-70b-versatile"
    )

    # Extract score and feedback from the response
    evaluation = response.choices[0].message.content
    score_line, feedback = evaluation.split('\n', 1)
    score = float(score_line.split(':')[1].strip().split('/')[0])
    
    return score, feedback.strip()