from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import LessonPlan
from extensions import db
from datetime import datetime

lessonplan_bp = Blueprint('lessonplan', __name__)

@lessonplan_bp.route('/lesson-plan', methods=['POST'])
@jwt_required()
def create_lesson_plan():
    data = request.get_json()
    
    date = None
    if data.get('date'):
        try:
            date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use ISO 8601.'}), 400
    
    lesson = LessonPlan(
        course_name=data.get('course_name'),
        mentor_id=data.get('mentor_id'),
        mentorfirst_name=data.get('mentorfirst_name'),
        mentorlast_name=data.get('mentorlast_name'),
        topic=data.get('topic'),
        date=date
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson plan created', 'lesson_id': lesson.lesson_id}), 201
