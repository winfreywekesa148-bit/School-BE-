from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

# ── App Config ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-change-me")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Enable CORS so React (localhost:5173) can talk to Flask (localhost:5000)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

db = SQLAlchemy(app)
jwt = JWTManager(app)


# ── Models ──────────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    course = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "course": self.course,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "teacher_id": self.teacher_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "course_id": self.course_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Submission(db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "assignment_id": self.assignment_id,
            "student_id": self.student_id,
            "content": self.content,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
        }


class LessonPlan(db.Model):
    __tablename__ = "lesson_plans"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "course_id": self.course_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    score = db.Column(db.Float, nullable=True)
    remark = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "assignment_id": self.assignment_id,
            "score": self.score,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── Auth Routes ─────────────────────────────────────────────────────────────

@app.route("/register", methods=["POST"])
def register():
    """
    Expects JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret123",
        "age": 21,
        "course": "Computer Science",
        "role": "student"   // or "teacher"
    }
    """
    data = request.get_json(silent=True) or {}

    # Validation
    required = ["name", "email", "password", "role"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"message": f"Missing fields: {', '.join(missing)}"}), 400

    if data["role"] not in ("student", "teacher"):
        return jsonify({"message": "role must be 'student' or 'teacher'"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User(
        name=data["name"],
        email=data["email"].lower().strip(),
        password_hash=generate_password_hash(data["password"]),
        age=data.get("age"),
        course=data.get("course"),
        role=data["role"],
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Expects JSON:
    {
        "email": "john@example.com",
        "password": "secret123",
        "name": "John Doe"   // optional, kept for frontend compat
    }
    Returns:
    {
        "access_token": "<jwt>",
        "role": "student"
    }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "role": user.role}), 200


@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").lower().strip()
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal whether email exists
        return jsonify({"message": "If that email exists, a reset link was sent"}), 200

    # In production: generate a secure token, email it.
    return jsonify({"message": "If that email exists, a reset link was sent"}), 200


@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").lower().strip()
    new_password = data.get("new_password", "")
    if not email or not new_password:
        return jsonify({"message": "Email and new_password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password reset successfully"}), 200


# ── Student Routes ──────────────────────────────────────────────────────────

@app.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    """Return all users with role='student'."""
    students = User.query.filter_by(role="student").all()
    return jsonify([s.to_dict() for s in students]), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    student = User.query.filter_by(id=student_id, role="student").first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.age = data.get("age", student.age)
    student.course = data.get("course", student.course)
    db.session.commit()
    return jsonify(student.to_dict()), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    student = User.query.filter_by(id=student_id, role="student").first()
    if not student:
        return jsonify({"message": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"}), 200


# ── Course Routes ───────────────────────────────────────────────────────────

@app.route("/courses", methods=["GET"])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses]), 200


@app.route("/courses", methods=["POST"])
@jwt_required()
def create_course():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("teacher_id"):
        return jsonify({"message": "title and teacher_id required"}), 400

    course = Course(
        title=data["title"],
        description=data.get("description"),
        teacher_id=data["teacher_id"],
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


# ── Assignment Routes ───────────────────────────────────────────────────────

@app.route("/assignments", methods=["GET"])
@jwt_required()
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([a.to_dict() for a in assignments]), 200


@app.route("/assignments", methods=["POST"])
@jwt_required()
def create_assignment():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("course_id"):
        return jsonify({"message": "title and course_id required"}), 400

    due = None
    if data.get("due_date"):
        try:
            due = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return jsonify({"message": "Invalid due_date format, use ISO 8601"}), 400

    assignment = Assignment(
        title=data["title"],
        description=data.get("description"),
        course_id=data["course_id"],
        due_date=due,
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify(assignment.to_dict()), 201


# ── Submission Routes ───────────────────────────────────────────────────────

@app.route("/submissions", methods=["GET"])
@jwt_required()
def get_submissions():
    submissions = Submission.query.all()
    return jsonify([s.to_dict() for s in submissions]), 200


@app.route("/submissions", methods=["POST"])
@jwt_required()
def create_submission():
    data = request.get_json(silent=True) or {}
    if not data.get("assignment_id") or not data.get("student_id"):
        return jsonify({"message": "assignment_id and student_id required"}), 400

    sub = Submission(
        assignment_id=data["assignment_id"],
        student_id=data["student_id"],
        content=data.get("content"),
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify(sub.to_dict()), 201


# ── Grade Routes ────────────────────────────────────────────────────────────

@app.route("/grades", methods=["GET"])
@jwt_required()
def get_grades():
    student_id = request.args.get("student_id", type=int)
    query = Grade.query
    if student_id:
        query = query.filter_by(student_id=student_id)
    return jsonify([g.to_dict() for g in query.all()]), 200


@app.route("/grades", methods=["POST"])
@jwt_required()
def create_grade():
    data = request.get_json(silent=True) or {}
    if not data.get("student_id") or not data.get("assignment_id"):
        return jsonify({"message": "student_id and assignment_id required"}), 400

    grade = Grade(
        student_id=data["student_id"],
        assignment_id=data["assignment_id"],
        score=data.get("score"),
        remark=data.get("remark"),
    )
    db.session.add(grade)
    db.session.commit()
    return jsonify(grade.to_dict()), 201


@app.route("/grades/<int:grade_id>", methods=["PUT"])
@jwt_required()
def update_grade(grade_id):
    data = request.get_json(silent=True) or {}
    grade = Grade.query.get(grade_id)
    if not grade:
        return jsonify({"message": "Grade not found"}), 404

    grade.score = data.get("score", grade.score)
    grade.remark = data.get("remark", grade.remark)
    db.session.commit()
    return jsonify(grade.to_dict()), 200


# ── Lesson Plan Routes ──────────────────────────────────────────────────────

@app.route("/lesson-plans", methods=["GET"])
@jwt_required()
def get_lesson_plans():
    plans = LessonPlan.query.all()
    return jsonify([p.to_dict() for p in plans]), 200


@app.route("/lesson-plans", methods=["POST"])
@jwt_required()
def create_lesson_plan():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("course_id"):
        return jsonify({"message": "title and course_id required"}), 400

    plan = LessonPlan(
        title=data["title"],
        content=data.get("content"),
        course_id=data["course_id"],
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify(plan.to_dict()), 201


@app.route("/lesson-plans/<int:plan_id>", methods=["DELETE"])
@jwt_required()
def delete_lesson_plan(plan_id):
    plan = LessonPlan.query.get(plan_id)
    if not plan:
        return jsonify({"message": "Lesson plan not found"}), 404
    db.session.delete(plan)
    db.session.commit()
    return jsonify({"message": "Lesson plan deleted"}), 200


# ── Current User ────────────────────────────────────────────────────────────

@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# ── Health Check ────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "School API is running", "endpoints": [
        "POST /register", "POST /login",
        "GET /students", "PUT /students/<id>", "DELETE /students/<id>",
        "GET /courses", "POST /courses",
        "GET /assignments", "POST /assignments",
        "GET /submissions", "POST /submissions",
        "GET /grades", "POST /grades", "PUT /grades/<id>",
        "GET /lesson-plans", "POST /lesson-plans", "DELETE /lesson-plans/<id>",
        "GET /me"
    ]}), 200


# ── Seed Data (optional, runs once on first start) ──────────────────────────

def seed():
    if User.query.first():
        return  # already seeded

    teacher = User(
        name="Ms. Jane Smith",
        email="teacher@school.com",
        password_hash=generate_password_hash("password123"),
        age=35,
        course="Mathematics",
        role="teacher",
    )
    student = User(
        name="Alice Johnson",
        email="student@school.com",
        password_hash=generate_password_hash("password123"),
        age=20,
        course="Mathematics",
        role="student",
    )
    db.session.add_all([teacher, student])
    db.session.commit()

    course = Course(title="Mathematics 101", description="Intro to math", teacher_id=teacher.id)
    db.session.add(course)
    db.session.commit()

    assignment = Assignment(title="Algebra Quiz", course_id=course.id)
    db.session.add(assignment)
    db.session.commit()

    plan = LessonPlan(title="Week 1: Numbers", content="Learn basic numbers", course_id=course.id)
    db.session.add(plan)
    db.session.commit()

    grade = Grade(student_id=student.id, assignment_id=assignment.id, score=85.0, remark="Good work!")
    db.session.add(grade)
    db.session.commit()

    print("[seed] Created demo teacher, student, course, assignment, lesson plan and grade.")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed()
    print("Starting School backend on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
