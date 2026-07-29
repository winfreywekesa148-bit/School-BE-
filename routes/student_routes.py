from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Student
from extensions import db

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['GET', 'POST'])
@jwt_required()
def manage_students():
    if request.method == 'GET':
        students = Student.query.all()
        result = []
        for student in students:
            result.append({
                'student_id': student.student_id,
                'user_id': student.user_id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'grade': student.grade,
                'email': student.email,
                'course_id': student.course_id,
                'course_name': student.course_name
            })
        return jsonify(result), 200
    
    data = request.get_json()
    new_student = Student(
        user_id=data.get('user_id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        grade=data.get('grade'),
        email=data.get('email'),
        course_id=data.get('course_id'),
        course_name=data.get('course_name')
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created', 'student_id': new_student.student_id}), 201
