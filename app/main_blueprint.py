from flask import render_template
from flask import Blueprint
#----------------------------------------------------------------------------#
# API endpoints
#----------------------------------------------------------------------------#   
web_main_bp = Blueprint('web_main_bp', __name__)
@web_main_bp.route('/')
@web_main_bp.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)