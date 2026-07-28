from extensions import db

class Mentor(db.Model):
    mentor_id = db.Column(db.Integer, primary_key=True)
    mentorfirst_name = db.Column(db.String)
    mentorlast_name = db.Column(db.String)
    course_name = db.Cloumn(db.String)
    course_id = db.Column(db.Integer,
                          db.Foreignkey("course.id"))
