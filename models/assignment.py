from extensions import db

class Assignment(db.Model):
    __tablename__ = 'assignment'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime)
    
    course = db.relationship('Course', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment')
