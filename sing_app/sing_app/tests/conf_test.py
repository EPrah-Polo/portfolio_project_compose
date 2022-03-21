import pytest

from sing_app import app
@pytest.fixture
def test_app():
    return app