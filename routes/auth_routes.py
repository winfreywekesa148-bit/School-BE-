from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from models import User, Mentor, Student, Course, Assignment, Submission, LessonPlan
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/admin/data', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_data():
    users = User.query.all()
    mentors = Mentor.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    assignments = Assignment.query.all()
    submissions = Submission.query.all()
    lessons = LessonPlan.query.all()
    return jsonify({
        'users': len(users),
        'mentors': len(mentors),
        'students': len(students),
        'courses': len(courses),
        'assignments': len(assignments),
        'submissions': len(submissions),
        'lessons': len(lessons)
    }), 200
