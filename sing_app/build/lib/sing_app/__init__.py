from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from sing_app.templates import models

app = Flask(__name__, template_folder= "templates")


#flask_env = os.getenv("FLASK_ENV", None)
#Load config file
if app.config["ENV"] == "production":
    app.config.from_object("sing_app.config_default.ProductionConfig")
else:
    app.config.from_object("sing_app.config_default.DevelopmentConfig")


db  = SQLAlchemy(app)


migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'web_main_bp.login'
#login_manager.login_message = "Please Login"

from sing_app.templates import main_blueprint
app.register_blueprint(main_blueprint.web_main_bp)
#app.register_blueprint(student_blueprint)