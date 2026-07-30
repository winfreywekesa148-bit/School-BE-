from flask import Blueprint, request, jsonify

from extensions import db
from models import Mentor, LessonPlan, Assignment

mentor_bp = Blueprint("mentor_bp", __name__)


# ------------------------
# Get all mentors
# ------------------------
@mentor_bp.route("/mentors", methods=["GET"])
def get_mentors():

    mentors = Mentor.query.all()

    data = []

    for mentor in mentors:

        data.append({
            "id": mentor.mentor_id,
            "first_name": mentor.first_name,
            "last_name": mentor.last_name,
            "email": mentor.email
        })

    return jsonify(data), 200


# ------------------------
# Create Lesson Plan
# ------------------------
@mentor_bp.route("/lesson-plans", methods=["POST"])
def create_lesson():

    data = request.get_json()

    lesson = LessonPlan(
        course_name=data["course_name"],
        mentor_id=data["mentor_id"],
        mentorfirst_name=data["mentorfirst_name"],
        mentorlast_name=data["mentorlast_name"],
        topic=data["topic"],
        date=data["date"]
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({
        "message": "Lesson Plan Created"
    }), 201


# ------------------------
# View Lesson Plans
# ------------------------
@mentor_bp.route("/lesson-plans", methods=["GET"])
def get_lessons():

    lessons = LessonPlan.query.all()

    output = []

    for lesson in lessons:

        output.append({
            "id": lesson.lesson_id,
            "course": lesson.course_name,
            "topic": lesson.topic,
            "teacher": lesson.mentorfirst_name
        })

    return jsonify(output), 200


# ------------------------
# Create Assignment
# ------------------------
@mentor_bp.route("/assignments", methods=["POST"])
def create_assignment():

    data = request.get_json()

    assignment = Assignment(
        course_id=data["course_id"],
        title=data["title"],
        due_date=data["due_date"]
    )

    db.session.add(assignment)
    db.session.commit()

    return jsonify({
        "message": "Assignment Created"
    }), 201


# ------------------------
# View Assignments
# ------------------------
@mentor_bp.route("/assignments", methods=["GET"])
def get_assignments():

    assignments = Assignment.query.all()

    output = []

    for assignment in assignments:

        output.append({
            "id": assignment.assignment_id,
            "title": assignment.title,
            "course_id": assignment.course_id,
            "due_date": assignment.due_date
        })

    return jsonify(output), 200


# ------------------------
# Delete Assignment
# ------------------------
@mentor_bp.route("/assignments/<int:id>", methods=["DELETE"])
def delete_assignment(id):

    assignment = Assignment.query.get(id)

    if assignment is None:

        return jsonify({
            "message": "Assignment not found."
        }), 404

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({
        "message": "Assignment deleted."
    }), 200