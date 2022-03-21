from tkinter import W
import pytest_flask
from sing_app import app

@pytest_flask
def test_models():

    with app.app_context():
        from sing_app.templates.models import db
        db.drop_all()
        db.create_all()
        print("Creating all")

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()
        print("Dropping all")