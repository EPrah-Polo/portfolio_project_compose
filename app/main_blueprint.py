from flask import render_template, flash, redirect, url_for
from flask import Blueprint
from forms import LoginForm
#----------------------------------------------------------------------------#
# API endpoints
#----------------------------------------------------------------------------#   
web_main_bp = Blueprint('web_main_bp', __name__)
@web_main_bp.route('/')
@web_main_bp.route('/index')
def index():
    user = {'username': 'Edward'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Have a nice day!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@web_main_bp.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('index.html')
    return render_template('login.html', title='Sign In', form=form)