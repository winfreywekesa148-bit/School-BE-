from extensions import db

class Submission(db.Model):
    __tablename__ = 'submission'
    
    submission_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.assignment_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    grade = db.Column(db.String(10))
    submitted_date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    course_name = db.Column(db.String(100))
    mentor_name = db.Column(db.String(100))
    
    course = db.relationship('Course', back_populates='submissions')
    assignment = db.relationship('Assignment', back_populates='submissions')
