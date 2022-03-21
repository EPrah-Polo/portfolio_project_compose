#from sqlite3 import OperationalError
from flask import Blueprint, jsonify, abort, request
import hashlib
import secrets
import logging

import os
import time
# from sqlalchemy import create_engine
# from decouple import config


db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
#db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_port = 5432

# conn_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user,pw=db_password,url=db_host,db=db_name, echo=True, logging_name='my_engine')

#----------------------------------------------------------------------------#
# Connect to database using psycopg2
#----------------------------------------------------------------------------#
import psycopg2
time.sleep(15)
print("15 seconds has passed. Has the server.json file been imported into pgadmin?...if so - Connect to Database via psycopg2")
conn = psycopg2.connect(
    """
    dbname=%s user=%s host=%s port=%d
    """%(db_name, db_user, db_host, db_port)
)
cur= conn.cursor()
# ------------------------------------------------------------------------------#
# set up a basic, global logger object which will write to the console
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s  %(message)s",
                    datefmt="%Y-%m-%d  %H:%M:%S")
_logger = logging.getLogger(__name__)
#----------------------------------------------------------------------------#
# API endpoints
#----------------------------------------------------------------------------#   
students_bp = Blueprint('students_bp', __name__, url_prefix='/students')

#avoid circular import
#from sing_app import db

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

#----------------------------------------------------------------------------#  
# Blueprint to run GET Request of Students in database
#----------------------------------------------------------------------------#  
@students_bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
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
            print(results)
        # message = results
        # _logger.info(message)
        return jsonify(True, results) # return JSON response
    except Exception as e:
        # something went wrong :(
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

#----------------------------------------------------------------------------#  
# Blueprint to query for a (1) specific student
#----------------------------------------------------------------------------#  
@students_bp.route('/<int:id>/', methods=['GET'])
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
        # message = results
        # _logger.info(message)
        return jsonify(True, results) # return JSON response
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

#----------------------------------------------------------------------------#  
# Blueprint to query all user accounts
#----------------------------------------------------------------------------#  
@students_bp.route('/user_accounts/', methods=['GET']) # decorator takes path and list of HTTP verbs
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
        # message = results
        # _logger.info(message)
        print(results)
        return jsonify(results) # return JSON response
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

#----------------------------------------------------------------------------#  
# Blueprint to Add New Student to database
#----------------------------------------------------------------------------#  
@students_bp.route('/new/', methods=['POST'])
def create():
    try:
        # req body must contain user_id and content
        if 'first_name' not in request.json or 'last_name' not in request.json or 'age' not in request.json:
            return abort(400)
        else:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, age)
                VALUES (%(FIRST_NAME)s, %(LAST_NAME)s, %(AGE)s) RETURNING id, first_name, last_name, age;
                """,
                {"FIRST_NAME": request.json['first_name'], "LAST_NAME": request.json['last_name'], "AGE": request.json['age']}
            )
            results = cur.statusmessage
            #print(results)
            #removed commit below - from psycopg2
            conn.commit()
            #cur.close()
            #conn.close()
            #message = results
            #_logger.info(message)
            print(results)
            return jsonify(True, "Inserted record new student record.<br>Returning status message: " + str(results))
            #return jsonify(True, "Inserted record new student record.<br>Returning status message: " + "testing")
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

# Add a user account for a student
@students_bp.route('/user_account/new/', methods=['POST'])
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
        results = cur.statusmessage
        print(results)
        conn.commit()
        #cur.close()
        #conn.close()
        # message = results
        # _logger.info(message)
        return jsonify(True, "Inserted record new user account record.<br> Returning status message : " + str(results))
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

# Update Student's user account and password
@students_bp.route('/update_account/<int:id>/', methods=['PATCH'])
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
        results = cur.statusmessage
        print(results)
        conn.commit()
        #cur.close()
        #conn.close()
        # message = results
        # _logger.info(message)
        return jsonify(True, "Updated student record. <br/>Returning status message: " + str(results))
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

# Delete Student from students table
@students_bp.route('/<int:id>/', methods=['DELETE'])
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
        results = cur.statusmessage
        print(results)
        conn.commit()
        # message = results
        # _logger.info(message)
        return jsonify(True, " Student succesfully deleted.<br/>Returning status message: ", results)
    except Exception as e:
        # something went wrong :(
        print(e)
        conn.rollback()
        return jsonify(False, " Something went wrong :(")

# Delete Student from students table
@students_bp.route('/exit', methods=['GET'])
def close_connection():
    try:
        cur.close()
        return jsonify(True)
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify(False)

        