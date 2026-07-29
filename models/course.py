from extensions import db

class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    duration = db.Column(db.String)
    mentorfirst_name = db.Column(db.String)
    mentorlast_name = db.Column(db.String)
    department = db.Column(db.String)

    #one to many: a course has many assignments
    assigments = db.relationship("Assignment", back_populates="course", lazy="dynamic")

