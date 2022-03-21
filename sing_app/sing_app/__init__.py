from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import logging
from logging.handlers import SMTPHandler
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__, template_folder= "templates")


#flask_env = os.getenv("FLASK_ENV", None)
#Load config file
if app.config["ENV"] == "production":
    app.config.from_object("sing_app.config_default.ProductionConfig")
else:
    app.config.from_object("sing_app.config_default.DevelopmentConfig")


mail = Mail(app)

# Apps being initialized
db  = SQLAlchemy(app)


migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'web_main_bp.login'
#login_manager.login_message = "Please Login"

# Register Blueprints
from sing_app.templates import main_blueprint
app.register_blueprint(main_blueprint.web_main_bp)
from sing_app.templates import student_blueprint
app.register_blueprint(student_blueprint.students_bp)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Explore Your Voice Singing Studios Web Page Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)