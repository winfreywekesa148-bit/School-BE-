from flask import jsonify, Flask
from models import Course
from flask_jwt_extended import jwt_required

app = Flask(__name__)

@app.route("/courses", methods=["GET"])
@jwt_required()
def get_courses():
    courses = Course.query.all()

    course_list = []

    for course in courses:
        course_list.append({
            "course_name": course.course_name,
            "course_id": course.course_id,
            "duration": course.duration,
            "mentorfirst_name": course.mentorfirst_name,
            "mentorlast_name": course.mentorlast_name,
            "department": course.department
            
        })
    return jsonify(course_list),200