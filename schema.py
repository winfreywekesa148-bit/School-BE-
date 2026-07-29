from marshmallow import Schema, fields


class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)


class StudentSchema(Schema):

    student_id = fields.Int(dump_only=True)
    studentfirst_name = fields.Str(required=True)
    studentlast_name = fields.Str(required=True)
    course = fields.Str(required=True)
    email = fields.Email(required=True)


class TeacherSchema(Schema):

    mentor_id = fields.Int(dump_only=True)
    mentorfirst_name = fields.Str(required=True)
    mentorlast_name = fields.Str(required=True)
    course = fields.Str(required=True)
    email = fields.Email(required=True)


class CourseSchema(Schema):

    course_id = fields.Int(dump_only=True)
    course_name = fields.Str(required=True)
    mentor_id = fields.Int(dump_only=True)
    mentorfirst_name = fields.Str(required=True)
    mentorlast_name = fields.Str(required=True)
 


class AssignmentSchema(Schema):

    assignment_id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    due_date = fields.Str(required=True)
    course_id = fields.Int(required=True)


class LessonPlanSchema(Schema):

    lessonplan_id = fields.Int(dump_only=True)
    subject = fields.Str(required=True)
    topic = fields.Str(required=True)
    objectives = fields.Str(required=True)
    activities = fields.Str(required=True)


class SubmissionSchema(Schema):

    submission_id = fields.Int(dump_only=True)
    submission_text = fields.Str(required=True)
    grade = fields.Str()
    assignment_id = fields.Int(required=True)