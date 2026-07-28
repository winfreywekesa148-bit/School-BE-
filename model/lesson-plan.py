from extensions import db

class LessonPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    mentor_id = db.Column(db.Integer,
                          db.Foreignkey("mentor_id"))
    mentorfirst_name = db.Column(db.String)
    mentorlast_name =  db.Column(db.String)
    topic = db.Column(db.String)
    date = db.Column(db.Time)
