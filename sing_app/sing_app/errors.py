from flask import render_template
from sing_app.templates.main_blueprint import web_main_bp
from sing_app import db

@web_main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@web_main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500