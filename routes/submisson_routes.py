from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Submission, Assignment, Student, Course
from extensions import db
from datetime import datetime
from utils.decorators import teacher_or_admin_required

submission_bp = Blueprint('submission', __name__)

@submission_bp.route('/submissions', methods=['GET', 'POST'])
@jwt_required()
def manage_submissions():
    if request.method == 'GET':
        submissions = Submission.query.all()
        result = []
        for sub in submissions:
            result.append({
                'submission_id': sub.submission_id,
                'course_id': sub.course_id,
                'assignment_id': sub.assignment_id,
                'student_id': sub.student_id,
                'grade': sub.grade,
                'submitted_date': sub.submitted_date.isoformat() if sub.submitted_date else None,
                'content': sub.content,
                'course_name': sub.course_name,
                'mentor_name': sub.mentor_name
            })
        return jsonify(result), 200
    
    data = request.get_json()
    submitted_date = None
    if data.get('submitted_date'):
        try:
            submitted_date = datetime.fromisoformat(data['submitted_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Invalid submitted_date format. Use ISO 8601.'}), 400
    
    new_submission = Submission(
        course_id=data.get('course_id'),
        assignment_id=data.get('assignment_id'),
        student_id=data.get('student_id'),
        grade=data.get('grade'),
        submitted_date=submitted_date,
        content=data.get('content'),
        course_name=data.get('course_name'),
        mentor_name=data.get('mentor_name')
    )
    db.session.add(new_submission)
    db.session.commit()
    return jsonify({'message': 'Submission created', 'submission_id': new_submission.submission_id}), 201

@submission_bp.route('/submissions/<int:submission_id>/grade', methods=['PUT'])
@jwt_required()
@teacher_or_admin_required
def grade_submission(submission_id):
    data = request.get_json()
    print(data)
    
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'message': 'Submission not found'}), 404
    submission.grade = data.get('grade')
    db.session.commit()
    return jsonify({'message': 'Grade updated'}), 200
