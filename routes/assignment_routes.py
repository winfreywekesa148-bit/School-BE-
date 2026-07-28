from models import Assignment
from flask import jsonify, Flask
from flask_jwt_extended import jwt_required

app = Flask(__name__)

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
