from flask import Flask
from config import Config
from extensions import db, jwt, ma, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.login_routes import login_bp
    from routes.register_routes import register_bp
    from routes.course_routes import course_bp
    from routes.assignment_routes import assignment_bp
    from routes.student_routes import student_bp
    from routes.submisson_routes import submission_bp
    from routes.lessonplan_routes import lessonplan_bp
    from routes.delete_lessonplan import delete_lessonplan_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(lessonplan_bp)
    app.register_blueprint(delete_lessonplan_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
