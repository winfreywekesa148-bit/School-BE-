from extensions import db

class LessonPlan(db.Model):
    __tablename__ = 'lesson_plan'
    
    lesson_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.mentor_id'))
    mentorfirst_name = db.Column(db.String(50))
    mentorlast_name = db.Column(db.String(50))
    topic = db.Column(db.String(200))
    date = db.Column(db.DateTime)
