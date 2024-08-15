from flask import Blueprint, request, jsonify

bp = Blueprint('auth', __name__)

@bp.route('/auth/login', methods=['POST'])
def login():
    email = request.json.get('email')
    # In a real application, you would validate the email and perform proper authentication
    if email:
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid email"}), 400