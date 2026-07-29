from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import LessonPlan
from extensions import db
from utils.decorators import teacher_or_admin_required

delete_lessonplan_bp = Blueprint('delete_lessonplan', __name__)

@delete_lessonplan_bp.route('/lesson_plan/<int:id>', methods=['DELETE'])
@jwt_required()
@teacher_or_admin_required
def delete_lesson_plan(id):
    lesson = LessonPlan.query.get(id)
    if lesson is None:
        return jsonify({'message': 'Lesson plan not found'}), 404
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson plan deleted'}), 200
