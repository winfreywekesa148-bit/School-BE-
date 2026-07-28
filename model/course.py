from extensions import db

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    duration = db.Column(db.String)
    mentor_name = db.Column(db.String)
    department = db.Column(db.String)
