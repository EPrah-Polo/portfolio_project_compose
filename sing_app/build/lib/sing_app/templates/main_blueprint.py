from re import template
from flask import render_template, flash, redirect, url_for, request
from flask import Blueprint
from sing_app.templates.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from werkzeug.urls import url_parse
#----------------------------------------------------------------------------#
# API endpoints
#----------------------------------------------------------------------------#   
web_main_bp = Blueprint('web_main_bp', __name__)
@web_main_bp.route('/')
@web_main_bp.route('/index')
#@login_required
def index():
    #user = {'username': 'Edward'}
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
    return render_template('index.html', title='Home', posts=posts)

from sing_app.templates.models import User_Accounts, db

@web_main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web_main_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User_Accounts.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('web_main_bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('web_main_bp.index')
        return redirect(next_page)
        #return redirect(url_for('web_main_bp.index'))
    return render_template('login.html', title='Sign In', form=form)   


@web_main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User_Accounts(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@web_main_bp.route('/user/<username>')
@login_required
def user(username):
    user = User_Accounts.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@web_main_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@web_main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@web_main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))