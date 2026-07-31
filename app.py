from flask import request, jsonify, Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt, ma, migrate

# Import your blueprints
from routes.user_routes import user_bp
from routes.course_routes import course_bp
from routes.assignment_routes import assignment_bp
from routes.student_routes import student_bp
from routes.mentor_routes import mentor_bp
from routes.lessonplan_route import lessonplan_bp


def create_app():

    # Create Flask application
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Allow React to communicate with Flask
    CORS(app, origins=["http://localhost:5173"])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # -----------------------------
    # Register all routes
    # -----------------------------
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(lessonplan_bp)
    # -----------------------------
    # Test Route
    # -----------------------------
    
    @app.route("/")
    def home():
        return {
            "message": "School Management System Backend Running"
        }, 200

    return app

    