# Below from students.py file
# from flask import Blueprint, jsonify, abort, request
#from flask import Flask
from flask import Flask
from config_default import ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy

#from config_default import ProductionConfig, DevelopmentConfig, TestingConfig

from student_blueprint import students_bp
from main_blueprint import web_main_bp

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
#app = Flask(__name__)
app = Flask(__name__, template_folder= "templates")
#Load config file
if app.config["ENV"] == "production":
    app.config.from_object("config_default.ProductionConfig")
else:
    app.config.from_object("config_default.DevelopmentConfig")
    #app.config.from_object(DevelopmentConfig)

# Must set app.config before db initialization  - https://stackoverflow.com/questions/54141416/airflow-neither-sqlalchemy-database-uri-nor-sqlalchemy-binds-is-set   

#test
#print(f'ENV is set to: {app.config["ENV"]}')
# Register Blueprint    
app.register_blueprint(students_bp)
app.register_blueprint(web_main_bp)

# @app.route('/')
# def index():
#     return "This is a example app."
#     # return jsonify({'name': 'alice',
#     #                 'email': 'alice@outlook.com'})
#print(app.config)
# ADD THE DATABASE CONNECTION TO THE FLASK APP
db  = SQLAlchemy(app)
#----------------------------------------------------------------------------#
# Run instance of server
# app.run(host='0.0.0.0') - note: host='0.0.0.0' allows your local machine to access the container in docker from localhost
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run()
