from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from sqlalchemy.dialects.postgresql.base import TIMESTAMP
# Below from students.py file
from flask import Blueprint, jsonify, abort, request
#from ..models import Students, User_Accounts, Progress, students_progress, db
import hashlib
import secrets
#import random
#from faker import Faker
import psycopg2
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = postgresql://user:pass@localhost:5432/my_sing_course
db = SQLAlchemy(app)

#db.init_app(app)
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

#----------------------------------------------------------------------------#
# API endpoints
#----------------------------------------------------------------------------#    

#s @app.route('/')
# def hello_world():
#     return 'Hello Flask by Edward - Docker in VS Code 2021-01-14!'

# # #test REMOVE AFTER
# # @app.route('/students')
# def hello_world():
#     return 'Hello Flask by Edward - Docker in VS Code 2021-01-14!'

conn = psycopg2.connect(
    """
    dbname=my_sing_course user=postgres host=localhost port=5432
    """
)

cur= conn.cursor()

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('students', __name__, url_prefix='/students')

# Query all students
@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    try:
        cur.execute(
            """
            SELECT *
            FROM students
            """
        )
        #colnames = [desc[0] for desc in cur.description]
        results = []
        
        rows = cur.fetchall()
        for row in rows:
            row_dict = {}
            row_dict['id'] = row[0]
            row_dict['first_name'] = row[1]
            row_dict['last_name'] = row[2]
            row_dict['age'] = row[3]
            #results.append(row_dict.copy())
            results.append(row_dict) 
        #print(results)
        return jsonify(True, results) # return JSON response
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Query for specific student
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    try:
        cur.execute(
            """
            SELECT *
            FROM students s
            WHERE s.id = %(value)s
            """,
            {"value": id}
        )
        results = []
        
        rows = cur.fetchone()
        # Add results of cur.fetchone() to each respective index in row_dict dictionary
        if not rows:
            not_exist = "The student id you entered does not exist."
            results.append(not_exist)
        else:
            row_dict = {}
            row_dict['id'] = rows[0]
            row_dict['first_name'] = rows[1]
            row_dict['last_name'] = rows[2]
            row_dict['age'] = rows[3]
            #results.append(row_dict.copy()) 
            results.append(row_dict) 
            print(results)
        return jsonify(True, results) # return JSON response
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Query all user accounts
@bp.route('/user_accounts', methods=['GET']) # decorator takes path and list of HTTP verbs
def index_accounts():
    try:
        cur.execute(
            """
            SELECT *
            FROM user_accounts
            """
        )
        #accounts = User_Accounts.query.all() # ORM performs SELECT query
        results = []
        
        rows = cur.fetchall()
        for row in rows:
            row_dict = {}
            row_dict['id'] = row[0]
            row_dict['username'] = row[1]
            row_dict['password'] = row[2]
            row_dict['student_id'] = row[3]
            results.append(row_dict) 
        return jsonify(results) # return JSON response
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")


# Add New Student
@bp.route('', methods=['POST'])
def create():
    try:
        # req body must contain user_id and content
        if 'first_name' not in request.json or 'last_name' not in request.json or 'age' not in request.json:
            return abort(400)
        cur.execute(
            """
            INSERT INTO students (first_name, last_name, age)
            VALUES (%(FIRST_NAME)s, %(LAST_NAME)s, %(AGE)s) RETURNING id, first_name, last_name, age;
            """,
            {"FIRST_NAME": request.json['first_name'], "LAST_NAME": request.json['last_name'], "AGE": request.json['age']}
        )
        result = cur.status_message
        print(result)
        conn.commit()
        #cur.close()
        #conn.close()
        return jsonify(True, "Inserted record new student record.<br>Returning status message: " + str(result))
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Add a user account for a student
@bp.route('/user_account/new', methods=['POST'])
def new_account():
    try:
        if 'username' not in request.json or 'password' not in request.json or 'student_id' not in request.json:
            return abort(400)
        cur.execute(
            """
            INSERT INTO user_accounts (username, password, student_id)
            VALUES (%(USERNAME)s, %(PASSWORD)s, %(STUDENT_ID)s) RETURNING id, username, student_id;
            """,
            {"USERNAME": request.json['username'], "PASSWORD": scramble(request.json['password']), "STUDENT_ID": request.json['student_id']}
        )
        result = cur.statusmessage
        print(result)
        conn.commit()
        #cur.close()
        #conn.close()
        return jsonify(True, "Inserted record new user account record.<br> Returning status message : " + str(result))
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Update Student's user account and password
@bp.route('/update_account/<int:id>', methods=['PATCH'])
def update(id: int):
    try:
        if 'id' not in request.json or 'username' not in request.json or 'password' not in request.json or 'student_id' not in request.json:
            return abort(400)
        cur.execute(
            """
        UPDATE user_accounts
        SET username = %(USERNAME)s,
            password = %(PASSWORD)s 
        WHERE id = %(ID)s AND student_id = %(STUDENT_ID)s RETURNING id, username,student_id;
            """,
            {"ID": id, "USERNAME": request.json['username'], "PASSWORD": scramble(request.json['password']), "STUDENT_ID": request.json['student_id']}
        )
        result = cur.statusmessage
        print(result)
        conn.commit()
        #cur.close()
        #conn.close()
        return jsonify(True, "Updated student record. <br/>Returning status message: " + str(result))
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Delete Student from students table
@bp.route('/<int:id>', methods=['DELETE'])
def remove_student(id: int):
    try:
        cur.execute(
            """
            DELETE
            FROM students s
            WHERE s.id = %(value)s RETURNING id, first_name, last_name;
            """,
            {"value": id}
        )
        result = cur.status_message
        print(result)
        conn.commit()
        return jsonify(True, " Student succesfully deleted.<br/>Returning status message: ", result)
    except:
        # something went wrong :(
        return jsonify(False, " Something went wrong :(")

# Delete Student from students table
@bp.route('/exit', methods=['GET'])
def close_connection():
    try:
        cur.close()
        conn.close()
        return jsonify(True)
    except:
        return jsonify(False)


#----------------------------------------------------------------------------#
# Run instance of server
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')