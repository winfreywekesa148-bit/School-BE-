from models import Student
from flask import jsonify, Flask
from flask_jwt_extended import jwt_required

app = Flask(__name__)

@app.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    students = Student.query.all()

    student_list = []

    for student in students:
        student_list.append({
            "student_id": student.id,
            "studentfirst_name": student.studentfirst_name,
            "studentlast_name": student.studentlast_name,
            "course_name": student.course_name,
            "course_id": student.course_id

        })
    return jsonify(student_list),200
