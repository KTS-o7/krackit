from flask import Blueprint, request, jsonify
from models.interview import get_questions, save_answer, generate_report
from utils.speech_to_text import transcribe_audio
from utils.answer_validation import validate_answer

bp = Blueprint('interview', __name__)

@bp.route('/questions', methods=['GET'])
def questions():
    return jsonify(get_questions())

@bp.route('/answer', methods=['POST'])
def answer():
    audio_file = request.files['audio']
    question_id = request.form['question_id']
    print("\n\n\n", audio_file, "\n\n\n")
    # Convert speech to text
    with audio_file.stream as audio_stream:
        text = transcribe_audio("../recordings/", audio_file.filename)
    
    # Validate answer
    score, feedback = validate_answer(question_id, text)
    
    # Save answer
    save_answer(question_id, text, score, feedback)
    
    return jsonify({"score": score, "feedback": feedback})

@bp.route('/report', methods=['GET'])
def report():
    return jsonify(generate_report())
