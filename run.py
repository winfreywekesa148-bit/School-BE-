from app import create_app
from extensions import db
from models import User, Course, Mentor, Student, Assignment, Submission, LessonPlan

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create seed data if database is empty
        if not User.query.first():
            admin_user = User(
                username='admin_user',
                name='Admin User',
                full_name='Admin Fullname',
                email='admin@example.com',
                role='admin'
            )
            admin_user.set_password('adminpass')
            db.session.add(admin_user)

            student_user = User(
                username='student_user',
                name='Student User',
                full_name='Student Fullname',
                email='student@example.com',
                role='student'
            )
            student_user.set_password('studentpass')
            db.session.add(student_user)

            teacher_user = User(
                username='teacher_user',
                name='Teacher User',
                full_name='Teacher Fullname',
                email='teacher@example.com',
                role='teacher'
            )
            teacher_user.set_password('teacherpass')
            db.session.add(teacher_user)
            db.session.commit()

            mentor = Mentor(
                user_id=teacher_user.user_id,
                first_name='Teacher',
                last_name='User',
                email='teacher@example.com',
                course_id=None
            )
            db.session.add(mentor)
            db.session.commit()

            course = Course(
                title='Mathematics',
                description='Mathematics course',
                credits=4,
                teacher_id=mentor.mentor_id
            )
            db.session.add(course)
            db.session.commit()

            assignment = Assignment(
                course_id=course.course_id,
                title='Math Homework 1',
                due_date=None
            )
            db.session.add(assignment)
            db.session.commit()

            student = Student(
                user_id=student_user.user_id,
                first_name='Student',
                last_name='User',
                grade='A',
                email='student@example.com',
                course_id=course.course_id,
                course_name='Mathematics'
            )
            db.session.add(student)
            db.session.commit()

            submission = Submission(
                course_id=course.course_id,
                assignment_id=assignment.assignment_id,
                student_id=student.student_id,
                grade='B',
                submitted_date=None,
                content='Homework submission',
                course_name='Mathematics',
                mentor_name='Teacher User'
            )
            db.session.add(submission)
            db.session.commit()

            lesson = LessonPlan(
                course_name='Mathematics',
                mentor_id=mentor.mentor_id,
                mentorfirst_name='Teacher',
                mentorlast_name='User',
                topic='Algebra',
                date=None
            )
            db.session.add(lesson)
            db.session.commit()

            print('Database seeded successfully.')
        else:
            print('Database already has data.')

    app.run(debug=True, host='0.0.0.0', port=5000)
