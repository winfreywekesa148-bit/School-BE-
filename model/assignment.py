from extensions import db

class Assignment(db.Model):
    Assignment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    course_name = db.Column(db.Text)
    course_id = db.Column(db.Integer,
                          db.Foreignkey("course.id"))
    dueDate = db.Column(db.Time)
