from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client['mock_interview_db']

# Clear existing questions
db.questions.delete_many({})

# Sample questions
questions = [
    {
        "id": "1",
        "text": "Tell me about yourself.",
        "keywords": ["experience", "skills", "background", "achievements"]
    },
    {
        "id": "2",
        "text": "What are your greatest strengths?",
        "keywords": ["skills", "attributes", "examples", "relevance"]
    },
    {
        "id": "3",
        "text": "Where do you see yourself in 5 years?",
        "keywords": ["goals", "ambitions", "career path", "growth"]
    }
]

# Insert questions
db.questions.insert_many(questions)

print("Database initialized with sample questions.")