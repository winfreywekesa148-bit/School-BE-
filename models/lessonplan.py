from extensions import db

class LessonPlan(db.Model):
    __tablename__ = "Lesson_plan"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    mentor_id = db.Column(db.Integer,
                          db.ForeignKey("mentor_id"))
    mentorfirst_name = db.Column(db.String)
    mentorlast_name =  db.Column(db.String)
    topic = db.Column(db.String)
    date = db.Column(db.Time)

    #many to many: many lessonplan has many mentor
    mentor = db.relationship("mentor", back_populates="lessonplan", lazy="dynamic", cascade="all, delete-orphan")
