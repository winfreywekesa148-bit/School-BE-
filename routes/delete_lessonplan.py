from models import Lessonplan
from flask import jsonify, Flask
from flask_jwt_extended import jwt_required
from utils.decorators import teacher_or_admin_required
from extensions import db

app = Flask(__name__)

@app.route("/lesson_plan/<int:id>", methods=["DELETE"])
@jwt_required()
@teacher_or_admin_required

def delete_lesson_plan(id):
    lesson = Lessonplan.query.get(id)

    if lesson is None:
        return jsonify({"message": "Lesson plan not found"}), 404

    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson plan deleted"}),200