from extensions import ma
from models import User, Mentor, Student, Course, Assignment, Submission, LessonPlan

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = ma.session
        exclude = ('password_hash',)

class MentorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mentor
        load_instance = True
        sqla_session = ma.session

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        sqla_session = ma.session

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        sqla_session = ma.session

class AssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        load_instance = True
        sqla_session = ma.session

class SubmissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Submission
        load_instance = True
        sqla_session = ma.session

class LessonPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LessonPlan
        load_instance = True
        sqla_session = ma.session
