from extensions import db

class Assignment(db.Model):
    Assignment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    course_name = db.Column(db.Text)
    course_id = db.Column(db.Integer,
                          db.ForeignKey("course.id"))
    dueDate = db.Column(db.Time)

    #one to many: assignment belongs to one course
    course = db.relationship("Course", back_populates="assignments")

