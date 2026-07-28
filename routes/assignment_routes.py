from models import Assignment, Course
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required
from utils.decorators import teacher_or_admin_required
from datetime import datetime
from extensions import db


app = Flask(__name__)


@app.route("/assignments", methods=["POST"])
@jwt_required()
@teacher_or_admin_required
def create_assignment():

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400
    
    title = data.get("title")
    course_id = data.get("course_id")
    if not title or not course_id:
        return jsonify({"message": "Title and course_id are required"}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    due_date = None
    if data.get("due_date"):
        due_date = datetime.fromisoformat(data["due_date"])

    assignment = Assignment(
        title = title,
        course_name = data.get("course_name"),
        course_id = course_id,
        due_date = due_date

    )

    db.session.add(assignment)
    db.session.comit()
    return jsonify ({"message": "Assignment created successfully."})


@app.route("/assignments", methods=["GET"])
@jwt_required()
def get_assignments():
    assignments = Assignment.query.all()

    assignment_list = []

    for assignment in assignments:
        assignment_list.append({
            "assignment_id": assignment.id,
            "title": assignment.title,
            "course_name": assignment.course_name,
            "course_id": assignment.course_id,
            "dueDate": assignment.studentlast_name      
        })
    return jsonify(assignment_list),200

@app.route("/assignments/<int:assignment_id>", methods=["DELETE"])
@jwt_required()
@teacher_or_admin_required

def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)

    if assignment is None:
        return jsonify({"message": "Assignment not found"}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": "Assignment deleted"}),200      
