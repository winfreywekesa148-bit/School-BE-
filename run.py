from extensions import db
from models import User, Course, Assignment, Submission
from flask import Flask

app = Flask(__name__)

@app.cli.command('seed')
def seed_db():
    """Seed the database with sample data."""
    from datetime import datetime, timedelta

    # Create admin
    admin = User(username='admin', email='admin@school.edu', full_name='System Admin', role='admin')
    admin.set_password('admin123')

    # Create teacher
    teacher = User(username='teacher1', email='teacher@school.edu', full_name='Jane Smith', role='teacher')
    teacher.set_password('teacher123')

    # Create student
    student = User(username='student1', email='student@school.edu', full_name='John Doe', role='student')
    student.set_password('student123')

    db.session.add_all([admin, teacher, student])
    db.session.commit()

    # Create course
    course = Course(title='Introduction', description='fundamentals', credits=4, teacher_id=teacher.id)
    db.session.add(course)
    db.session.commit()

    # Create assignment
    assignment = Assignment(
        title='Basics Quiz',
        due_date=datetime.utcnow() + timedelta(days=7),
        max_score=100,
        course_id=course.id
    )
    db.session.add(assignment)
    db.session.commit()

    # Add grade
    grade = Submission(score=92.5, student_id=student.id, assignment_id=assignment.id)
    db.session.add(grade)
    db.session.commit()

    print('Database seeded successfully!')


if __name__ == '__main__':
    app.run(debug=True)