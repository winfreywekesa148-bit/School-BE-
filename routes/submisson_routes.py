from models import Submission
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required
from extensions import db

app = Flask(__name__)

@app.route("/grades/<int:id>", methods=["PUT"])
@jwt_required()

def grade_submission(id):
    submission = Submission.query.get(id)

    if submission is None:
        return jsonify({"message":"No submission found"}), 404

    data = request.get_json()

    submission.grade = data["grade"]

    db.session.commit()

    return jsonify({"message": "Grade updated successfully"}), 200
