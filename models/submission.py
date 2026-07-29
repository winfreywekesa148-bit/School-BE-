from extensions import db

class Submission(db.Model):
    Submission_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.Text)
    course_id = db.Column(db.Integer,
                          db.ForeignKey("course.id"))
    ans = db.Column(db.Text)
    grade = db.Column(db.String)