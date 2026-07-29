from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Assignment, Course
from extensions import db
from datetime import datetime

assignment_bp = Blueprint('assignment', __name__)

@assignment_bp.route('/assignments', methods=['GET', 'POST'])
@jwt_required()
def manage_assignments():
    if request.method == 'GET':
        assignments = Assignment.query.all()
        result = []
        for assignment in assignments:
            result.append({
                'assignment_id': assignment.assignment_id,
                'course_id': assignment.course_id,
                'title': assignment.title,
                'due_date': assignment.due_date.isoformat() if assignment.due_date else None
            })
        return jsonify(result), 200
    
    data = request.get_json()
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Invalid due_date format. Use ISO 8601.'}), 400
    
    new_assignment = Assignment(
        course_id=data.get('course_id'),
        title=data.get('title'),
        due_date=due_date
    )
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment created', 'assignment_id': new_assignment.assignment_id}), 201
