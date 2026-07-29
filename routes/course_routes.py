from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Course
from extensions import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['GET', 'POST'])
@jwt_required()
def manage_courses():
    if request.method == 'GET':
        courses = Course.query.all()
        result = []
        for course in courses:
            result.append({
                'course_id': course.course_id,
                'title': course.title,
                'description': course.description,
                'credits': course.credits,
                'teacher_id': course.teacher_id
            })
        return jsonify(result), 200
    
    data = request.get_json()
    new_course = Course(
        title=data.get('title'),
        description=data.get('description'),
        credits=data.get('credits', 0),
        teacher_id=data.get('teacher_id')
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course created', 'course_id': new_course.course_id}), 201
