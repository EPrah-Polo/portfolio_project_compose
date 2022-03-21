import pytest_flask
from sing_app import main_blueprint, app

@pytest_flask
def test_main_blueprint():
    app.register_blueprint(main_blueprint.web_main_bp)

    web = app.test_Client()

    rv = web.get('/')
    assert rv.status == '200 OK'
    assert '<h1>Hello</h1>' in rv.data.decode('utf-8')
    assert 'You typed' not in rv.data.decode('utf-8')

    rv = web.get('/run?text=Hello World')
    assert rv.status == '200 OK'
    assert '<h1>Hello</h1>' in rv.data.decode('utf-8')
    assert 'You typed in Hello World' in rv.data.decode('utf-8')

    #print(rv.data)

