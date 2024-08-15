from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client['mock_interview_db']

def get_questions():
    return list(db.questions.find({}, {'_id': 0}))

def save_answer(question_id, text, score, feedback):
    db.answers.insert_one({
        'question_id': question_id,
        'text': text,
        'score': score,
        'feedback': feedback
    })

def generate_report():
    answers = list(db.answers.find({}, {'_id': 0}))
    overall_score = sum(answer['score'] for answer in answers) / len(answers) if answers else 0
    return {
        'overall_score': overall_score,
        'answers': answers
    }