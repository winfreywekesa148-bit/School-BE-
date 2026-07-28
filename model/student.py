from extensions import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    studentfirst_name = db.Column(db.String)
    studentlast_name = db.Column(db.String)
    course_name = db.Cloumn(db.String)
    course_id = db.Column(db.Integer,
                          db.Foreignkey("course.id"))
