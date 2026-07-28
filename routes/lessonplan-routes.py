from models import LessonPlan
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required
from extensions import db

app = Flask(__name__)

@app.route("/lesson-plan", methods=["POST"])
@jwt_required()

def get_lesson_plan():
    data = request.get_json()

    lesson = LessonPlan(
        course_name = data["course_name"], 
        mentor_id = data["mentor_id"],
        mentorfirst_name = data["mentorfirst_name"],
        mentorlast_name = data["mentorlast_name"],
        topic = data["topic"],
        date = data["date"]
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({"message": "lesson plan craeted"}), 201
