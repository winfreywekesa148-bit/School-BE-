from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import LessonPlan
from extensions import db
from utils.decorators import teacher_or_admin_required
from datetime import datetime

lessonplan_bp = Blueprint('lessonplan', __name__)

@lessonplan_bp.route("/lesson-plan", methods=["POST"])
@jwt_required()
@teacher_or_admin_required
def create_lesson_plan():
    data = request.get_json()

    lesson = LessonPlan(
        course_name=data["course_name"],
        mentor_id=data["mentor_id"],
        mentorfirst_name=data["mentorfirst_name"],
        mentorlast_name=data["mentorlast_name"],
        topic=data["topic"],
        date=lesson_date
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({"message": "Lesson created"}), 201

@lessonplan_bp.route("/lesson-plan", methods=["GET"])
@jwt_required()
@teacher_or_admin_required
def get_lesson_plans():

    lessons = LessonPlan.query.all()

    lesson_list = []

    for lesson in lessons:
        lesson_list.append({
            "lesson_id": lesson.lesson_id,
            "course_name": lesson.course_name,
            "mentorfirst_name": lesson.mentorfirst_name,
            "mentorlast_name": lesson.mentorlast_name,
            "topic": lesson.topic,
            "date": lesson.date
        })

    return jsonify(lesson_list), 200
