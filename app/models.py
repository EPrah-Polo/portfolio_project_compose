from . import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
#Migrate
#migrate = Migrate(app, db)
# Reference:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships

# Students Class
# uselist=False in db.relationship makes a one-to-one relationship - students and user_accounts is one-to-one relationship
class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), unique=False, nullable=False)
    last_name = db.Column(db.String(128), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_accounts = db.relationship('User_Accounts', backref='students', cascade="all,delete", lazy=True, uselist=False)


    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age
        }

# User Accounts Class - nullable = false = NOT NULL
class User_Accounts(db.Model):
    __tablename__ = 'user_accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username= db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    #students = db.relationship('Students', backref='user_accounts', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'student_id': self.student_id
        }

# Students_Enrolled class
students_enrolled = db.Table('students_enrolled',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

# Courses Class
class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    level = db.Column(db.String(128), unique=False, nullable=True)
    students_enrolled = db.relationship('Students', secondary=students_enrolled, lazy='subquery', cascade="all,delete", backref=db.backref('courses', lazy=True))

# Many to many relationship helper table
students_exercises = db.Table('students_exercises',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
)

courses_exercises = db.Table('courses_exercises',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
)

# Exercises Class
class Exercises(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    # progress_rel defines a one to many relationship between exercises and progress
    progress_rel = db.relationship('Progress', backref='exercises', lazy=True)
    students_exercises = db.relationship('Students', secondary=students_exercises, lazy='subquery', cascade="all,delete", backref=db.backref('exercises', lazy=True))
    courses_exercises = db.relationship('Courses', secondary=courses_exercises, lazy='subquery', cascade="all,delete", backref=db.backref('exercises', lazy=True))

students_progress = db.Table('students_progress',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('progress_id', db.Integer, db.ForeignKey('progress.id'), primary_key=True)
)

# Progress class - one-to-many relationship
class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    timbre = db.Column(db.String(128), unique=False, nullable=True)
    timbre = db.Column(db.String(128), unique=False, nullable=True)
    tone = db.Column(db.String(128), unique=False, nullable=True)
    melodic_phrasing = db.Column(db.String(128), unique=False, nullable=True)
    dynamics = db.Column(db.String(128), unique=False, nullable=True)
    range = db.Column(db.String(128), unique=False, nullable=True)
    feedback = db.Column(db.String(128), unique=False, nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    students_progress = db.relationship('Students', secondary=students_progress, lazy='subquery', cascade="all,delete", backref=db.backref('progress', lazy=True))
