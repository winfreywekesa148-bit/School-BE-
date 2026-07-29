from extensions import db

class Student(db.Model):

    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    studentfirst_name = db.Column(db.String)
    studentlast_name = db.Column(db.String)
    course_name = db.Cloumn(db.String)
    course_id = db.Column(db.Integer,
                          db.ForeignKey("course.id"))

    #one to many: a student can have many gardes
    grades = db.relationship("Grade", back_populates="student", lazy="dynamic")

