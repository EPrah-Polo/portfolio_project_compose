import os
# from decouple import config

# db_user = config('DB_USER')
# db_password = config('DB_PASSWORD')
# db_host = config('DB_HOST')
# db_port = config('DB_PORT')
# db_name = config('DB_NAME')
#conn_url = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=db_user,pw=db_password,url=db_host,db=db_name)
#----------TESTING----------------------------#
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

conn_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user,pw=db_password,url=db_host,db=db_name, echo=True, logging_name='my_engine')
#https://pythonise.com/series/learning-flask/flask-configuration-files
class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

#Populate config file with attributes
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev"

    DB_NAME=db_name
    DB_USERNAME=db_user
    DB_PASSWORD=db_password

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME=db_name
    DB_USERNAME=db_user
    DB_PASSWORD=db_password

    SQLALCHEMY_DATABASE_URI=conn_url
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    IMAGE_UPLOADS = "/home/username/projects/my_app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = db_name
    DB_USERNAME = db_user
    DB_PASSWORD = db_password

    SESSION_COOKIE_SECURE = False