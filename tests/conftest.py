import pytest

from app import create_app


@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    return app


@pytest.yield_fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client
