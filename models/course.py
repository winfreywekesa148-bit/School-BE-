from extensions import db

class Course(db.Model):
    __tablename__ = 'course'
    
    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=0)
    teacher_id = db.Column(db.Integer, db.ForeignKey('mentor.mentor_id'))
    
    assignments = db.relationship('Assignment', back_populates='course')
    submissions = db.relationship('Submission', back_populates='course')
