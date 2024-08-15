from flask import Flask
from flask_cors import CORS
from routes import auth, interview

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth.bp)
app.register_blueprint(interview.bp)

if __name__ == "__main__":
    app.run(debug=True)